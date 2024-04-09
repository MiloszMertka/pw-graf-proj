class Material:
    def __init__(self, color: tuple[int, int, int], ambient: float, diffuse: float, specular: float, shininess: int) -> None:
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
