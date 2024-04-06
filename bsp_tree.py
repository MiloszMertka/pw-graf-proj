import numpy as np
from vertex import Vertex
from polygon import Polygon
from bsp_node import BSPNode

class BSPTree:
    def __init__(self, polygons: list[Polygon]) -> None:
        self.root = self.__build(polygons)

    def traverse(self, viewer_position: Vertex) -> list[Polygon]:
        sorted_polygons: list[Polygon] = []
        self.__traverse_node(self.root, viewer_position, sorted_polygons)
        return sorted_polygons

    def __traverse_node(self, node: BSPNode, viewer_position: Vertex, sorted_polygons: list[Polygon]) -> None:
        if node is None:
            return

        plane_point = node.polygon.vertices[0].to_vector3()
        plane_normal = np.cross(node.polygon.vertices[1].to_vector3() - plane_point, node.polygon.vertices[2].to_vector3() - plane_point)
        distance_to_plane = np.dot(plane_point - viewer_position.to_vector3(), plane_normal)

        if distance_to_plane > 0:
            self.__traverse_node(node.front, viewer_position, sorted_polygons)
            sorted_polygons.append(node.polygon)
            self.__traverse_node(node.back, viewer_position, sorted_polygons)
        else:
            self.__traverse_node(node.back, viewer_position, sorted_polygons)
            sorted_polygons.append(node.polygon)
            self.__traverse_node(node.front, viewer_position, sorted_polygons)
        
    def __build(self, polygons: list[Polygon]) -> BSPNode:
        root = BSPNode(polygons[0])
        for polygon in polygons[1:]:
            self.__split_polygon(root, polygon)
        return root
        
    def __split_polygon(self, node: BSPNode, polygon: Polygon) -> None:
        plane_point = node.polygon.vertices[0].to_vector3()
        plane_normal = np.cross(node.polygon.vertices[1].to_vector3() - plane_point, node.polygon.vertices[2].to_vector3() - plane_point)

        if polygon.is_wholly_in_front(plane_point, plane_normal):
            if node.front is None:
                node.front = BSPNode(polygon)
            else:
                self.__split_polygon(node.front, polygon)
        elif polygon.is_wholly_behind(plane_point, plane_normal):
            if node.back is None:
                node.back = BSPNode(polygon)
            else:
                self.__split_polygon(node.back, polygon)
        else:
            front_polygon, back_polygon = polygon.split(plane_point, plane_normal)
            if node.front is None:
                node.front = BSPNode(front_polygon)
            else:
                self.__split_polygon(node.front, front_polygon)
            if node.back is None:
                node.back = BSPNode(back_polygon)
            else:
                self.__split_polygon(node.back, back_polygon)
