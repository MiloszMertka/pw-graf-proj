from polygon import Polygon

class BSPNode:
    def __init__(self, polygon: Polygon) -> None:
        self.polygon = polygon
        self.front: BSPNode = None
        self.back: BSPNode = None
