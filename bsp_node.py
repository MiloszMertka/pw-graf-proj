import numpy as np
from polygon import Polygon
from vertex import Vertex

class BSPNode:
    def __init__(self, polygon: Polygon):
        self.polygon = polygon
        self.front = None
        self.back = None

def build_bsp_tree(polygons: list[Polygon]) -> BSPNode:
    if not polygons:
        return None

    root = BSPNode(polygons[0])
    for polygon in polygons[1:]:
        split_polygon(root, polygon)
    return root

def split_polygon(node: BSPNode, polygon: Polygon) -> None:
    plane_point = node.polygon.vertices[0].to_vector3()  # Use first vertex of the polygon as a point on the plane
    plane_normal = np.cross(node.polygon.vertices[1].to_vector3() - plane_point, node.polygon.vertices[2].to_vector3() - plane_point)

    if polygon.is_wholly_in_front(plane_point, plane_normal):
        if node.front is None:
            node.front = BSPNode(polygon)
        else:
            split_polygon(node.front, polygon)
    elif polygon.is_wholly_behind(plane_point, plane_normal):
        if node.back is None:
            node.back = BSPNode(polygon)
        else:
            split_polygon(node.back, polygon)
    else:
        front_polygon, back_polygon = polygon.split(plane_point, plane_normal)
        if node.front is None:
            node.front = BSPNode(front_polygon)
        else:
            split_polygon(node.front, front_polygon)
        if node.back is None:
            node.back = BSPNode(back_polygon)
        else:
            split_polygon(node.back, back_polygon)

def traverse_bsp_tree(node: BSPNode, viewer_position: Vertex, sorted_polygons: list[Polygon]) -> None:
    if node is None:
        return

    # Calculate the distance from the viewer to the plane of the current node's polygon
    plane_point = node.polygon.vertices[0].to_vector3()  # Use first vertex of the polygon as a point on the plane
    plane_normal = np.cross(node.polygon.vertices[1].to_vector3() - plane_point, node.polygon.vertices[2].to_vector3() - plane_point)
    distance_to_plane = np.dot(plane_point - viewer_position.to_vector3(), plane_normal)

    # Traverse the front and back subtrees based on the viewer's position relative to the plane
    if distance_to_plane > 0:
        traverse_bsp_tree(node.front, viewer_position, sorted_polygons)
        sorted_polygons.append(node.polygon)
        traverse_bsp_tree(node.back, viewer_position, sorted_polygons)
    else:
        traverse_bsp_tree(node.back, viewer_position, sorted_polygons)
        sorted_polygons.append(node.polygon)
        traverse_bsp_tree(node.front, viewer_position, sorted_polygons)
