class Camera:
    def __init__(self, x, y, z):
        self.x = x      
        self.y = y
        self.z = z

    @property
    def position(self):
        return (self.x, self.y, self.z)