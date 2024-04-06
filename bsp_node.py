from polygon import Polygon

class BSPNode:
    def __init__(self, polygon: Polygon) -> None:
        self.polygon = polygon
        self.front = None
        self.back = None
