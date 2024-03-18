import numpy as np

from utility import iVector2, Vector2, Vector3, Point
from ui import Screen, ProjectionStile

class Projection:
    def move_plane(points: list[Point], shift: Point) -> list[Point]:
        return points + shift

    def project_points(points: list[Vector3], screen: Screen) -> list[Vector2]:
        projected_points = Projection.transform_to_screen_coordinates(points, screen)
        return Projection.move_plane(projected_points, np.array(screen.size)/2)

    def transform_to_screen_coordinates(points: list[Vector3], screen: Screen) -> list[Vector2]:
        screen_center: Vector3 = screen.get_position()
        screen_up_vector: Vector3 = screen.get_up()
        screen_direction: Vector3 = screen.get_forward()
        screen_size: iVector2 = screen.size
        zoom: float = screen.zoom
        orthogonal_projection: bool = screen.projection_stile == ProjectionStile.Orthogonal
        screen_width, screen_height = screen_size

        # Calculate screen coordinate system
        z_axis = -screen_direction / np.linalg.norm(screen_direction)
        x_axis = np.cross(screen_up_vector, z_axis)
        y_axis = np.cross(z_axis, x_axis)
        
        # Create transformation matrix
        transformation_matrix = np.vstack((x_axis, y_axis, z_axis)).T
        
        # Translate points to origin
        translated_points = points - screen_center
        
        # Apply transformation matrix
        screen_coordinates = np.dot(translated_points, transformation_matrix)
        
        # Project points to 2D screen coordinates
        if orthogonal_projection:
            return screen_coordinates[:, :2] * (-1)
        screen_coordinates_2d = screen_coordinates[:, :2] / screen_coordinates[:, 2, None]

        # Scale points to fit screen dimensions
        scale = min(screen_width, screen_height) * zoom
        screen_coordinates_2d[:, 0] *= scale
        screen_coordinates_2d[:, 1] *= scale
        
        return screen_coordinates_2d
    
    def position_from_rotation(rotation_x: float, rotation_y: float, radius: float=1) -> Vector3:
        position_raw = np.array([np.sin(rotation_y), np.sin(rotation_x), np.cos(rotation_y)*np.cos(rotation_x)])
        position_normalized = position_raw / np.linalg.norm(position_raw)
        return position_normalized * radius

    def direction_from_rotation(rotation_x: float, rotation_y: float) -> Vector3:
        return -Projection.position_from_rotation(rotation_x, rotation_y)

    def up_from_rotation(rotation_x: float, rotation_y: float) -> Vector3:
        pos_norm = Projection.position_from_rotation(rotation_x, rotation_y)
        up_raw = np.cross(np.cross(pos_norm,(0,1,0)), pos_norm)
        return up_raw / np.linalg.norm(up_raw)