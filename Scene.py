class Scene:
    def __init__(self):
        self.camera = None
        self.viewport = None
        self.objets = []
        self.lights = []

    def set_camera(self, camera):
        self.camera = camera

    def set_viewport(self, viewport):
        self.viewport = viewport

    def add_objet(self, objet):
        self.objets.append(objet)
    
    def add_light(self, light):
        self.lights.append(light)