from vertex import Vertex
from line import Line

VERTEX_PREFIX = 'v '
LINE_PREFIX = 'l '

class FileReader:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> list[Line]:
        lines: list[Line] = []
        vertices: list[Vertex] = []
        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith(VERTEX_PREFIX):
                    coordinates = line.split()
                    x = float(coordinates[1])
                    y = float(coordinates[2])
                    z = float(coordinates[3])
                    vertex = Vertex(x, y, z)
                    vertices.append(vertex)
                elif line.startswith(LINE_PREFIX):
                    indices = line.split()
                    i = int(indices[1]) - 1
                    j = int(indices[2]) - 1
                    lines.append(Line(vertices[i], vertices[j]))
        return lines
        