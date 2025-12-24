from vec3 import creer_rotation

class Camera:
    def __init__(self, x, y, z, rot_x=0, rot_y=0, rot_z=0):
        """Caméra avec position (x,y,z) et rotation (rot_x, rot_y, rot_z) en degrés"""
        self.x = x      
        self.y = y
        self.z = z
        self.rotation = creer_rotation(rot_x, rot_y, rot_z)
    
    @property
    def position(self):
        return (self.x, self.y, self.z)