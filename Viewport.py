class Viewport:
    def __init__(self, width, height, dist):
        # width, height : size of the viewport (world units)
        # dist : distance from the camera to the viewport (z)
        self.width = width
        self.height = height
        self.dist = dist
        