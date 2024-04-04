from vertex import Vertex
from polygon import Polygon

VERTEX_PREFIX = 'v '
POLYGON_PREFIX = 'p '

class FileReader:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> list[Polygon]:
        vertices: list[Vertex] = []
        polygons: list[Polygon] = []
        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith(VERTEX_PREFIX):
                    coordinates = line.split()
                    x = float(coordinates[1])
                    y = float(coordinates[2])
                    z = float(coordinates[3])
                    vertex = Vertex(x, y, z)
                    vertices.append(vertex)
                elif line.startswith(POLYGON_PREFIX):
                    indices = line.split()
                    polygon_vertices: list[Vertex] = []
                    for index in indices[1:]:
                        i = int(index) - 1
                        polygon_vertices.append(vertices[i])
                    polygons.append(Polygon(polygon_vertices))
        return polygons
        