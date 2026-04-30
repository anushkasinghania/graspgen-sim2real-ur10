import os
import sys
import tqdm
import json
import scipy
import trimesh
import argparse
import numpy as np
from qpsolvers import solve_qp

from trimesh import transformations as tra

# Add meshcat imports for visualization
from grasp_gen.utils.meshcat_utils import (
    create_visualizer,
    visualize_pointcloud,
    visualize_mesh,
    visualize_grasp,
    get_color_from_score,
)


def make_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--object", default="meshes/metal_sheet.obj", help="Object mesh."
    )
    parser.add_argument(
        "--root-dir",
        default="",
        help="Root directory for object mesh path. This will not be stored in the output.json.",
    )
    parser.add_argument(
        "--gripper",
        required=False,
        help="JSON or Yaml file describing the vacuum gripper.",
    )
    parser.add_argument(
        "--grasps",
        default=None,
        help="If specified, will evaluate grasps only (no sampling).",
    )
    parser.add_argument(
        "--num", default=1000, type=int, help="Number of suction grasps."
    )
    parser.add_argument(
        "--scale", type=float, default=1.0, required=False, help="Scale of object mesh."
    )
    parser.add_argument(
        "--num-disturbances",
        default=10,
        type=int,
        help="Number of random disturbance samples.",
    )
    parser.add_argument(
        "--qp-solver",
        default="clarabel",
        choices=("clarabel", "cvxopt", "daqp", "ecos", "osqp", "scs"),
        help="Name of the QP solver to use.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Name of the JSON file to write results to. Compatible with acronym-pipeline format.",
    )
    parser.add_argument("--no-viz", action="store_true", help="No visualization.")
    parser.add_argument(
        "--random-seed",
        type=int,
        default=None,
        help="Random seed. Defaults to None.",
    )
    parser.add_argument(
        "--random-seed-eval",
        type=int,
        default=None,
        help="Random seed for evaluation. Defaults to None.",
    )
    return parser


def colorized_points(points, quality):
    return trimesh.PointCloud(vertices=points, colors=colorize(quality))


def colorize(quality):
    colors = np.zeros(shape=(len(quality), 4), dtype=np.uint8)
    colors[:, 3] = 255
    # colors[:, 1] = np.array(quality) * 255
    # colors[:, 0] = 255 - np.array(quality) * 255

    for i, qual in enumerate(quality):
        colors[i, :3] = color_interpolation(qual)
    return colors


def color_interpolation(input):
    red = np.array([255, 0, 0])
    yellow = np.array([255, 255, 0])
    green = np.array([0, 255, 0])

    if input < 0.5:
        return (1.0 - 2.0 * input) * red + 2.0 * input * yellow
    else:
        return (2.0 - 2.0 * input) * yellow + (2.0 * input - 1.0) * green


def colorize_for_meshcat(quality):
    """Convert quality scores to colors for meshcat visualization."""
    colors = np.zeros(shape=(len(quality), 3), dtype=np.uint8)

    for i, qual in enumerate(quality):
        colors[i, :3] = color_interpolation(qual)
    return colors


def skew(x):
    """Create skew-symmetric matrix from vector for cross-product via matrix multiplication."""
    return np.array([[0, -x[2], x[1]], [x[2], 0, -x[0]], [-x[1], x[0], 0]])


def adjoint_transform(frame_a, frame_b):
    """Used to transform wrenches or twists between different reference frames.
    E.g.: adj_ab = adjoint_transform(a, b) can be used to transform
    this wrench: f_a = np.dot(adj_ab.T, f_b)
    see e.g. p. 62 of MLS: 'A Mathematical Introduction to Robotic Manipulation'
    """

    transform_ab = np.matmul(frame_a, trimesh.transformations.inverse_matrix(frame_b))
    rot_ab = transform_ab[:3, :3]
    tra_ab = transform_ab[:3, 3]

    adjoint = np.zeros((6, 6))

    adjoint[:3, :3] = rot_ab
    adjoint[3:, 3:] = rot_ab

    adjoint[:3, 3:] = np.matmul(skew(tra_ab), rot_ab)

    return adjoint


def sunflower_radius(k, n, b):
    if k > n - b:
        return 1.0
    else:
        return np.sqrt(k - 0.5) / np.sqrt(n - (b + 1) / 2)


def sunflower(n, radius, alpha=2.0, geodesic=False):
    golden_ratio = (1 + np.sqrt(5)) / 2
    points = []
    angle_stride = 360 * golden_ratio if geodesic else 2 * np.pi / golden_ratio**2
    b = round(alpha * np.sqrt(n))  # number of boundary points

    for k in range(1, n + 1):
        r = sunflower_radius(k, n, b) * radius
        theta = k * angle_stride
        points.append((r * np.cos(theta), r * np.sin(theta), 0.0))

    return np.array(points)


class SuctionCupArray(object):
    def __init__(
        self,
        poses,
        num_sides,
        radius,
        height,
        spring_max_length_change=0.1,
        suction_force=250.0,
        material_kappa=0.005,
        friction_mu=0.5,
        interpolated_perimeter_vertices=0,
        standoff_distance=0.001,
        num_suction_points_for_hole_check=50,
        collision_mesh_fname=None,
    ):
        # pose of apex (?) (height w.r.t. base)
        # number of base vertices
        # that form an n-gon with circumradius r and
        # location of base vertices (opening angle of right pyramid)
        self.poses = np.array(poses)
        self.num_suction_cups = len(poses)
        self.num_sides = num_sides
        self.radius = radius
        self.height = height

        self.standoff_distance = standoff_distance  # take scale into account !

        self.V = suction_force  # newton suction force
        self.kappa = (
            material_kappa  # elastic limit / yield strength of the suction cup material
        )
        self.mu = friction_mu

        self._create_pyramid(
            self.num_sides,
            self.radius,
            self.height,
            interpolated_perimeter_vertices=interpolated_perimeter_vertices,
        )

        self.num_suction_points_for_hole_check = num_suction_points_for_hole_check
        self.suction_points = sunflower(
            n=num_suction_points_for_hole_check,
            radius=self.radius,
            alpha=2.0,
            geodesic=False,
        )

        # 10% according to: "Deformation constraints in a mass-spring model to describe rigid cloth behaviour" by X. Provot et al.
        # assumption is that all springs are equal - and they are currently in their steady state
        self.spring_max_length_change = spring_max_length_change
        perimeter_spring_lengths, flexion_spring_lengths, cone_spring_lengths = (
            self.get_spring_lengths(obj_mesh=None, suction_ring_transform=None)
        )
        spring_length = perimeter_spring_lengths[0]
        self.perimeter_spring_length_max = spring_length * (
            1.0 + spring_max_length_change
        )
        self.perimeter_spring_length_min = spring_length * (
            1.0 - spring_max_length_change
        )

        spring_length = cone_spring_lengths[0]
        self.cone_spring_length_max = spring_length * (1.0 + spring_max_length_change)
        self.cone_spring_length_min = spring_length * (1.0 - spring_max_length_change)

        spring_length = flexion_spring_lengths[0]
        self.flexion_spring_length_max = spring_length * (
            1.0 + spring_max_length_change
        )
        self.flexion_spring_length_min = spring_length * (
            1.0 - spring_max_length_change
        )

        self.collision_mesh = None
        if collision_mesh_fname is not None:
            self.collision_mesh = trimesh.load(collision_mesh_fname, force="mesh")
        self.collision_mesh_fname = collision_mesh_fname

    def _create_pyramid(
        self, sides, radius, height, rotation=0.0, interpolated_perimeter_vertices=0
    ):
        # generate base polygon
        one_segment = np.pi * 2 / sides

        vertices = []
        total_number_of_vertices = sides + sides * interpolated_perimeter_vertices + 1
        mesh_vertex_indices = []
        faces = []

        perimeter_spring_paths = []  # edges we need to use to calculate path lengths
        perimeter_springs = []
        cone_springs = []
        flexion_springs = []

        apex_index = total_number_of_vertices - 1
        for i in range(sides):
            point = (
                np.sin(one_segment * i + rotation) * radius,
                np.cos(one_segment * i + rotation) * radius,
                0.0,
            )
            vertices.append(point)
            mesh_vertex_indices.append(len(vertices) - 1)

            # append interpolated points along segment
            if interpolated_perimeter_vertices > 0:
                point2 = (
                    np.sin(one_segment * (i + 1) + rotation) * radius,
                    np.cos(one_segment * (i + 1) + rotation) * radius,
                    0.0,
                )
                pts_x = np.linspace(
                    point[0],
                    point2[0],
                    interpolated_perimeter_vertices + 1,
                    endpoint=False,
                )
                pts_y = np.linspace(
                    point[1],
                    point2[1],
                    interpolated_perimeter_vertices + 1,
                    endpoint=False,
                )
                pts_z = np.linspace(
                    point[2],
                    point2[2],
                    interpolated_perimeter_vertices + 1,
                    endpoint=False,
                )

                tmp = []
                for j in range(interpolated_perimeter_vertices):
                    tmp.append([len(vertices) - 1, len(vertices)])
                    vertices.append((pts_x[j + 1], pts_y[j + 1], pts_z[j + 1]))
                tmp.append(
                    [len(vertices) - 1, len(vertices) % (total_number_of_vertices - 1)]
                )
                perimeter_spring_paths.append(tmp)

            first_vertex = i * (1 + interpolated_perimeter_vertices)
            second_vertex = apex_index
            third_vertex = (first_vertex + 1 + interpolated_perimeter_vertices) % (
                total_number_of_vertices - 1
            )

            faces.append([i, sides, (i + 1) % sides])

            perimeter_springs.append([first_vertex, third_vertex])
            cone_springs.append([first_vertex, second_vertex])
            flexion_springs.append(
                [
                    first_vertex,
                    (third_vertex + 1 + interpolated_perimeter_vertices)
                    % (total_number_of_vertices - 1),
                ]
            )

        # add apex
        vertices.append((0, 0, height))
        vertices = np.array(vertices)
        mesh_vertex_indices.append(len(vertices) - 1)

        self.vertices = vertices

        self.perimeter_spring_paths = np.array(perimeter_spring_paths)
        self.perimeter_springs = np.array(perimeter_springs)
        self.interpolated_perimeter_vertices = interpolated_perimeter_vertices

        self.cone_springs = np.array(cone_springs)
        self.flexion_springs = np.array(flexion_springs)

        self.mesh_vertex_indices = np.array(mesh_vertex_indices)
        self.faces = np.array(faces)
        # self.mesh = trimesh.Trimesh(vertices=vertices[mesh_vertex_indices], faces=faces)

    def sample_grasps(self, obj_mesh, num_grasps):
        # First sample which suction cup from the array to chose
        suction_cup_indices = np.random.randint(
            low=0, high=self.num_suction_cups, size=num_grasps
        )
        suction_cup_poses = self.poses[suction_cup_indices]

        # Sample where to attach the suction cup on the object mesh
        point_on_surface, face_index = trimesh.sample.sample_surface(
            obj_mesh, num_grasps
        )
        approach_vector = obj_mesh.face_normals[face_index]

        # get transformation from point and approach vector
        grasp_transforms = []
        for p, v, T in zip(point_on_surface, approach_vector, suction_cup_poses):
            contact_transform = trimesh.geometry.plane_transform(p, v)
            grasp_transform = (
                T
                @ tra.rotation_matrix(
                    angle=np.random.uniform(-np.pi, np.pi), direction=[0, 0, 1]
                )
                @ trimesh.transformations.translation_matrix(
                    [0, 0, -self.standoff_distance]
                )
                @ contact_transform
            )

            # TODO: maybe this can be avoided
            grasp_transform = trimesh.transformations.inverse_matrix(grasp_transform)

            grasp_transforms.append(grasp_transform)

        new_points_on_surface = np.array([ct[:3, 3] for ct in grasp_transforms])

        return new_points_on_surface, approach_vector, np.array(grasp_transforms)

    def get_spring_lengths(self, obj_mesh, suction_ring_transform):
        # intersect all rays emerging from points on suction cup ring
        # (shifted towards apex) in approach_vector direction
        #
        # - Project n-gon vertices onto object surface (along approach vector)
        # - Calculate apex distance to base such that average distance == height

        if obj_mesh is None:
            transformed_vertices = self.vertices
        else:
            if trimesh.ray.has_embree:
                intersector = trimesh.ray.ray_pyembree.RayMeshIntersector(
                    obj_mesh, scale_to_box=True
                )
            else:
                intersector = trimesh.ray.ray_triangle.RayMeshIntersector(obj_mesh)

            transformed_vertices = trimesh.transform_points(
                self.vertices, suction_ring_transform, translate=True
            )
            ray_origins = transformed_vertices[:-1]
            # transformed_apex = transformed_vertices[-1]

            suction_ring, index_ray, _ = intersector.intersects_location(
                ray_origins,
                np.tile(-suction_ring_transform[:3, 2], (len(ray_origins), 1)),
                multiple_hits=False,
            )
            if len(suction_ring) != len(ray_origins):
                raise RuntimeError("no suction")

            inv_index_ray = np.empty(index_ray.size, dtype=np.int32)
            for i in np.arange(index_ray.size):
                inv_index_ray[index_ray[i]] = i

            # suction_ring = np.copy(suction_ring[inv_index_ray])
            suction_ring = suction_ring[inv_index_ray]

            # calculate apex
            apex_param = min(
                0,
                np.sum(
                    (suction_ring - suction_ring_transform[:3, 3]).dot(
                        suction_ring_transform[:3, 2]
                    )
                )
                / self.num_sides
                - self.height,
            )
            apex = (
                suction_ring_transform[:3, 3]
                - apex_param * suction_ring_transform[:3, 2]
            )

            transformed_vertices = np.vstack([suction_ring, apex])

        if self.interpolated_perimeter_vertices > 0:
            perimeter_spring_lengths = np.sum(
                [
                    [
                        np.linalg.norm(
                            transformed_vertices[v[0]] - transformed_vertices[v[1]]
                        )
                        for v in p
                    ]
                    for p in self.perimeter_spring_paths
                ],
                axis=1,
            )
        else:
            perimeter_spring_lengths = np.linalg.norm(
                transformed_vertices[self.perimeter_springs[:, 0]]
                - transformed_vertices[self.perimeter_springs[:, 1]],
                axis=1,
            )

        flexion_spring_lengths = np.linalg.norm(
            transformed_vertices[self.flexion_springs[:, 0]]
            - transformed_vertices[self.flexion_springs[:, 1]],
            axis=1,
        )

        cone_spring_lengths = np.linalg.norm(
            transformed_vertices[self.cone_springs[:, 0]]
            - transformed_vertices[self.cone_springs[:, 1]],
            axis=1,
        )

        return perimeter_spring_lengths, flexion_spring_lengths, cone_spring_lengths

    def is_sealed(self, obj_mesh, grasp_transform):
        # From: https://arxiv.org/pdf/1709.06670.pdf
        #
        # Calculate energy of suction cup using a spring-mass model
        #
        #
        # (a) The cone faces of the suction cup do not collide with the object
        #     during approach or in the contact configuration.
        sealed = [True] * self.num_suction_cups

        suction_cup_collision = False
        if suction_cup_collision:
            return [False] * self.num_suction_cups

        #
        # Check for object holes.
        #
        # (b) The object surface has no holes within the contact ring traced
        #     out by C's perimeter springs.
        holes_present = False

        if trimesh.ray.has_embree:
            intersector = trimesh.ray.ray_pyembree.RayMeshIntersector(
                obj_mesh, scale_to_box=True
            )
        else:
            intersector = trimesh.ray.ray_triangle.RayMeshIntersector(obj_mesh)

        # Check all three suction cup seals for holes
        for i, suction_cup_T in enumerate(self.poses):
            # sample points in suction cup bottom
            suction_ring_transform = grasp_transform @ suction_cup_T
            suction_points_transformed = trimesh.transform_points(
                self.suction_points, suction_ring_transform, translate=True
            )

            collisions, _, _ = intersector.intersects_location(
                suction_points_transformed,
                np.tile(-suction_ring_transform[:3, 2], (len(self.suction_points), 1)),
                multiple_hits=False,
            )
            # trimesh.Scene((trimesh.points.PointCloud(suction_points), obj_mesh)).show()
            holes_present = len(suction_points_transformed) != len(collisions)

            if holes_present:
                # s = trimesh.Scene([obj_mesh])
                # s.add_geometry(transform=self._last_suction_transform, geometry=dbg_mesh)
                # s.show()
                sealed[i] = False

        if not any(sealed):
            return sealed

        #
        # Calculate Spring Energy
        #
        # (c) The energy required in each spring to maintain the contact
        #     configuration is below a real-valued threshold modeling the
        #     maximum deformation of the suction cup material against the
        #     object surface.
        for i, suction_cup_T in enumerate(self.poses):
            if sealed[i]:
                try:
                    (
                        perimeter_spring_lengths,
                        flexion_spring_lengths,
                        cone_spring_lengths,
                    ) = self.get_spring_lengths(
                        obj_mesh=obj_mesh,
                        suction_ring_transform=grasp_transform @ suction_cup_T,
                    )

                    if any(
                        perimeter_spring_lengths > self.perimeter_spring_length_max
                    ) or any(
                        perimeter_spring_lengths < self.perimeter_spring_length_min
                    ):
                        # logging.warn("Perimenter spring length violation")
                        sealed[i] = False

                    if any(cone_spring_lengths > self.cone_spring_length_max) or any(
                        cone_spring_lengths < self.cone_spring_length_min
                    ):
                        # logging.warn("Cone spring length violation")
                        sealed[i] = False

                    if any(
                        flexion_spring_lengths > self.flexion_spring_length_max
                    ) or any(flexion_spring_lengths < self.flexion_spring_length_min):
                        # logging.warn("Flexion spring length violation")
                        sealed[i] = False
                except RuntimeError:
                    sealed[i] = False

        return sealed

    def is_wrench_resistant(self, contact_frames, w, qp_solver="clarabel"):
        """Given a contact_frame and disturbance wrench, return whether this grasp can resist the disurbance."""
        object_frame = np.eye(4)

        contact_wrench_basis = np.eye(6)
        grasp_map = []
        num_fingers = len(contact_frames)
        for contact_frame in contact_frames:
            adjoint = adjoint_transform(object_frame, contact_frame)
            # the grasp map maps each finger's contact forces/torques
            # into the common object's coordinate frame
            # It is of dimensioniality 6 x (num_fingers * 6)
            grasp_map.append(np.matmul(adjoint.T, contact_wrench_basis))

        grasp_map = np.hstack(grasp_map)

        # generate quadratic program of form:
        #
        # minimize
        #     (1/2) * x.T * P * x + q.T * x
        #
        # subject to
        #     G * x <= h
        #     A * x == b
        #
        # Our objective:
        #   ||grasp_map x - w||_2^2 = x^T grasp_map^T grasp_map x - 2 w^T grasp_map x + w^T w
        # That means:
        #   P = 2 * grasp_map^T grasp_map
        #   q = -2 * w^T grasp_map
        P = 2.0 * np.matmul(grasp_map.T, grasp_map)
        q = -2.0 * np.dot(w.T, grasp_map)

        # Note: f_N = f_z + V
        # Our constraints:
        #  (friction)
        #   sqrt(3) | f_x | <= mu f_N
        #   sqrt(3) | f_y | <= mu f_N
        #   sqrt(3) | t_z | <= r mu f_N
        #  (material)
        #   sqrt(2) | t_x | <= pi radius kappa
        #   sqrt(2) | t_y | <= pi radius kappa
        #  (suction)
        #   f_z >= -V
        sqrt3 = np.sqrt(3.0)
        sqrt2 = np.sqrt(2.0)
        G = np.array(
            [
                [sqrt3, 0, -self.mu, 0, 0, 0],
                [-sqrt3, 0, -self.mu, 0, 0, 0],
                [0, sqrt3, -self.mu, 0, 0, 0],
                [0, -sqrt3, -self.mu, 0, 0, 0],
                [0, 0, -self.mu * self.radius, 0, 0, sqrt3],
                [0, 0, -self.mu * self.radius, 0, 0, -sqrt3],
                [0, 0, 0, sqrt2, 0, 0],
                [0, 0, 0, -sqrt2, 0, 0],
                [0, 0, 0, 0, sqrt2, 0],
                [0, 0, 0, 0, -sqrt2, 0],
                [0, 0, -1.0, 0, 0, 0],
            ]
        )
        G = scipy.linalg.block_diag(*([G] * num_fingers))

        h = np.array(
            [
                self.mu * self.V,
                self.mu * self.V,
                self.mu * self.V,
                self.mu * self.V,
                self.radius * self.mu * self.V,
                self.radius * self.mu * self.V,
                np.pi * self.radius * self.kappa,
                np.pi * self.radius * self.kappa,
                np.pi * self.radius * self.kappa,
                np.pi * self.radius * self.kappa,
                self.V,
            ]
        )
        h = np.tile(h, num_fingers)

        x = solve_qp(
            P=scipy.sparse.csc_matrix(P),
            q=q,
            G=scipy.sparse.csc_matrix(G),
            h=h,
            solver=qp_solver,
        )
        # other options: ['cvxopt', 'daqp', 'ecos', 'osqp', 'scs']
        #  ['clarabel', 'daqp', 'ecos', 'osqp', 'scs']
        #
        # Seem to work: osqp, scs, clarabel
        #
        # Run-time for 2000 grasps:
        # clarabel: 31s (without np.ndarray)
        # clarabel: 30s (with scipy.sparse.csc_matrix) <---
        # osqp: 34s
        # scs: 67s

        if x is None:
            return False, None

        res = np.linalg.norm(grasp_map.dot(x) - w) ** 2

        # print("QP solution: res = {}".format(res))
        return np.isclose(res, 0.0, atol=1e-3), x

    def evaluate_grasps(
        self,
        obj_mesh,
        points_on_surface,
        approach_vectors,
        grasp_transforms,
        num_disturbances=10,
        qp_solver="clarabel",
        tqdm_disable=True,
    ):
        """Check seal formation and wrench resistance of suction grasps."""

        # check sealing
        sealed = []
        for tf in tqdm.tqdm(grasp_transforms, disable=tqdm_disable):
            seal = self.is_sealed(obj_mesh, grasp_transform=tf)
            sealed.append(seal)

        sealed = np.array(sealed)
        # sealing operation; here: if a single cup is sealed it's fine
        # sealed = sealed.sum(axis=1).clip(0, 1)
        # here: all suction cups need to be sealed
        sealed = sealed.all(axis=1)

        # print(f"Number of sealed grasps: {sum(sealed)} out of {len(sealed)}")

        # Maybe move this into is_sealed(), see (a)
        # check collisions
        collision_mesh_gripper = self.collision_mesh
        collision_mgr_gripper, collision_mgr_gripper_node_names = (
            trimesh.collision.scene_to_collision(collision_mesh_gripper.scene())
        )
        collision_mgr_gripper_node_names = list(collision_mgr_gripper_node_names.keys())
        assert len(collision_mgr_gripper_node_names) <= 1

        collision_mgr, _ = trimesh.collision.scene_to_collision(obj_mesh.scene())
        grasp_in_collision = []

        # create random disturbances
        disturbances = np.random.normal(size=(num_disturbances, 3))
        disturbances = disturbances / np.linalg.norm(disturbances, axis=1).reshape(
            -1, 1
        )

        grasp_success = []
        for tf, is_sealed in tqdm.tqdm(
            zip(grasp_transforms, sealed),
            total=len(grasp_transforms),
            disable=tqdm_disable,
        ):
            # contact_frame = trimesh.geometry.plane_transform(point_on_surf, approach_v)
            # contact_frame = trimesh.transformations.inverse_matrix(contact_frame)
            # contact_frame = np.matmul(
            #     contact_frame, trimesh.transformations.euler_matrix(np.pi, 0, 0)
            # )

            if not is_sealed:
                grasp_success.append(0.0)
                grasp_in_collision.append(False)
            else:
                # check collisions
                collision_mgr_gripper.set_transform(
                    name=collision_mgr_gripper_node_names[0], transform=tf
                )
                in_collision = collision_mgr.in_collision_other(collision_mgr_gripper)
                grasp_in_collision.append(in_collision)

                suction_contacts = [p @ tf for p in self.poses]
                succ = []
                for dist in disturbances:
                    disturbance = np.hstack([dist, [0, 0, 0]])
                    # TODO transform to suction ring transform
                    suc, _ = self.is_wrench_resistant(
                        suction_contacts, disturbance, qp_solver=qp_solver
                    )
                    succ.append(suc)
                grasp_success.append(sum(succ) / len(succ))

        return (
            points_on_surface,
            approach_vectors,
            grasp_transforms,
            sealed,
            np.array(grasp_success),
            np.array(grasp_in_collision),
        )

    def as_dict(self):
        return {
            "poses": self.poses.tolist(),
            "num_sides": self.num_sides,
            "radius": self.radius,
            "height": self.height,
            "suction_force": self.V,
            "material_kappa": self.kappa,
            "friction_mu": self.mu,
            "interpolated_perimeter_vertices": self.interpolated_perimeter_vertices,
            "spring_max_length_change": self.spring_max_length_change,
            "standoff_distance": self.standoff_distance,
            "num_suction_points_for_hole_check": self.num_suction_points_for_hole_check,
            "collision_mesh_fname": self.collision_mesh_fname,
        }

    @classmethod
    def from_file(cls, fname, key=None):
        if fname.endswith(".json"):
            import json

            data = json.load(open(fname, "r"))
        elif fname.endswith(".yaml"):
            import yaml

            data = yaml.safe_load(open(fname, "r"))

        if key is not None:
            data = data[key]

        return cls(
            poses=data["poses"],
            num_sides=data["num_sides"],
            radius=data["radius"],
            height=data["height"],
            suction_force=data["suction_force"],
            material_kappa=data["material_kappa"],
            friction_mu=data["friction_mu"],
            interpolated_perimeter_vertices=data["interpolated_perimeter_vertices"],
            spring_max_length_change=data["spring_max_length_change"],
            standoff_distance=data["standoff_distance"],
            num_suction_points_for_hole_check=data["num_suction_points_for_hole_check"],
            collision_mesh_fname=data["collision_mesh_fname"],
        )


# make function so I can call from fastapi service
def main_func(args):

    if args.output is not None:
        if os.path.isfile(args.output) and os.access(args.output, os.R_OK):
            print(f"File {args.output} already exists. Skipping.")
            sys.exit(0)

    if args.random_seed:
        np.random.seed(args.random_seed)

    if args.gripper:
        suction_gripper = SuctionCupArray.from_file(fname=args.gripper)
    else:
        suction_gripper = SuctionCupArray(
            poses=np.array([np.eye(4)]),
            num_sides=15,
            radius=0.025,
            height=0.06,
            friction_mu=0.5,
            material_kappa=0.005,
            collision_mesh_fname=os.path.join(args.root_dir, args.object),
        )

    if not args.grasps:
        # load mesh
        fname_object_mesh = os.path.join(args.root_dir, args.object)
        obj_mesh = trimesh.load(fname_object_mesh)
        if args.scale != 1.0:
            obj_mesh.apply_scale(args.scale)

        # fix object's CoM
        obj_center_mass = obj_mesh.center_mass
        obj_mesh.apply_translation(-obj_center_mass)

        print(
            f"Dimensions of {fname_object_mesh}: {obj_mesh.extents}, CoM: {obj_center_mass}"
        )

        # sample grasps
        import time

        t0 = time.time()
        points_on_surface, approach_vectors, grasp_transforms = (
            suction_gripper.sample_grasps(obj_mesh=obj_mesh, num_grasps=args.num)
        )
        print(f"Sampling {args.num} grasps took {time.time() - t0}s")
    else:
        # Use grasps from input file -- for now assume JSON
        grasps = json.load(open(args.grasps, "r"))

        args.object = grasps["object"]["file"]
        args.scale = grasps["object"]["scale"]

        fname_object_mesh = os.path.join(args.root_dir, grasps["object"]["file"])
        obj_mesh = trimesh.load(fname_object_mesh)
        if grasps["object"].get("scale", 1.0) != 1.0:
            obj_mesh.apply_scale(grasps["object"]["scale"])

        # fix object's CoM
        obj_center_mass = obj_mesh.center_mass
        obj_mesh.apply_translation(-obj_center_mass)

        grasp_transforms = np.array(grasps["grasps"]["transforms"])
        grasp_transforms[:, :3, 3] -= obj_center_mass
        approach_vectors = np.array([None] * len(grasp_transforms))
        points_on_surface = np.copy(grasp_transforms[:, :3, 3])

    # evaluate
    if args.random_seed_eval:
        np.random.seed(args.random_seed_eval)

    import time

    t0 = time.time()
    points, approach_vectors, contact_transforms, sealed, success, in_collision = (
        suction_gripper.evaluate_grasps(
            obj_mesh=obj_mesh,
            points_on_surface=points_on_surface,
            approach_vectors=approach_vectors,
            grasp_transforms=grasp_transforms,
            num_disturbances=args.num_disturbances,
            qp_solver=args.qp_solver,
        )
    )
    print(f"Evaluating {args.num} grasps took {time.time() - t0}s")
    if args.output is not None:
        if False:
            # Filter only successful ones -- not used
            # won't work with in_collision None
            success_idx = sealed.nonzero()
            success_idx = np.intersect1d(success_idx, (~in_collision).nonzero())
            object_in_gripper = [True] * len(success_idx)
        else:
            success_idx = np.arange(len(contact_transforms))
            object_in_gripper = np.logical_and(sealed, ~(in_collision.astype(bool)))

        # Transform data according to mesh.center_mass
        suction_points = points
        if points[0] is not None:
            suction_points += obj_center_mass
        output_transforms = np.copy(contact_transforms)
        output_transforms[:, :3, 3] += obj_center_mass

        # ACRONYM dataset file format
        output_dict = {
            "object": {
                "file": args.object,  # this will be without root_dir
                "scale": args.scale,
            },
            "gripper": suction_gripper.as_dict(),
            "grasps": {
                "transforms": output_transforms[success_idx].tolist(),
                "suction_points": suction_points[success_idx].tolist(),
                "approach_vectors": approach_vectors[success_idx].tolist(),
                "object_in_gripper": object_in_gripper[success_idx].tolist(),
                "is_sealed": sealed[success_idx].tolist(),
                "score": success[success_idx].tolist(),
            },
        }

        print(
            f"Writing result to ({sum(object_in_gripper)}/{len(success_idx)} successes): {args.output}"
        )
        with open(args.output, "w") as f:
            json.dump(output_dict, f)

    if not args.no_viz:
        # Create meshcat visualizer
        vis = create_visualizer()
        gripper_name = "single_suction_cup_30mm"

        # Visualize object mesh
        visualize_mesh(vis, "object_mesh", obj_mesh, color=[169, 169, 169])

        # Visualize sealed configurations
        print(f"Visualizing sealed configurations ({sum(sealed)}/{len(sealed)})")
        sealed_colors = colorize_for_meshcat(sealed.astype(float))
        visualize_pointcloud(vis, "sealed_points", points, sealed_colors, size=0.005)

        # Visualize configurations not in collision
        print(
            f"Visualizing configurations not in collision ({sum(~in_collision)}/{len(in_collision)})"
        )
        collision_colors = colorize_for_meshcat((~in_collision).astype(float))
        visualize_pointcloud(
            vis, "collision_free_points", points, collision_colors, size=0.005
        )

        # Visualize quality of configurations
        print(
            f"Visualizing quality of configurations (configs greater zero: {sum(success > 0)}/{len(success)}). Max: {np.max(success)}"
        )
        quality_colors = colorize_for_meshcat(success)
        visualize_pointcloud(vis, "quality_points", points, quality_colors, size=0.005)

        # Visualize best configurations (top 10)
        print("Visualizing 'best' configurations (top 10).")
        combined_criteria = sealed * success

        # Get indices of top 10 grasps
        top_indices = np.argsort(combined_criteria)[-10:][
            ::-1
        ]  # Sort descending and take top 10

        # Visualize the top 10 grasps
        for i, idx in enumerate(top_indices):
            grasp_transform = contact_transforms[idx]
            grasp_score = combined_criteria[idx]

            # Use different colors for different ranks (red for best, orange for others)
            if i == 0:
                color = [255, 0, 0]  # Red for best
            else:
                color = [255, 165, 0]  # Orange for others

            # Visualize the grasp
            visualize_grasp(
                vis,
                f"best_grasps/grasp_{i:02d}",
                grasp_transform,
                color=color,
                gripper_name=gripper_name,
                linewidth=0.6,
            )

            # # Visualize gripper mesh at this position
            # if suction_gripper.collision_mesh is not None:
            #     visualize_mesh(
            #         vis,
            #         f"best_grippers/gripper_{i:02d}",
            #         suction_gripper.collision_mesh,
            #         color=color,
            #         transform=grasp_transform
            #     )

            print(f"  Grasp {i+1}: Score = {grasp_score:.3f}")

        print(
            f"Visualized {len([idx for idx in top_indices if combined_criteria[idx] > 0])} grasps with positive scores."
        )

        print("Visualization complete. Check meshcat browser window.")
        input("Press Enter to continue...")


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    main_func(args)
