import math
from vec3 import soustraction_vecteurs, produit_scalaire,taille_vecteur
from Scene import Scene         
from Camera import Camera       
from Canvas import Canvas       
from Viewport import Viewport   
from Sphere import Sphere
from PIL import Image  

def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    CO = soustraction_vecteurs(O, sphere.center)

    a = produit_scalaire(D, D)
    b = 2 * produit_scalaire(CO, D)
    c = produit_scalaire(CO, CO) - r*r

    discriminant = b*b - 4*a*c

    if discriminant < 0:
        return float('inf'), float('inf')

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return t1, t2

def CanvasToViewport(viewport,canvas,x,y):
    return (x * viewport.width / canvas.width,y * viewport.height / canvas.height,viewport.dist)

def TraceRay(O, D, t_min, t_max, scene):
    closest_t = float('inf')
    closest_sphere = None

    for sphere in scene.objets:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
           
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere == None:
        return (255, 255, 255)
    
    return closest_sphere.color

if __name__ == '__main__':
    
    camera = Camera(0,0,0)  
    viewport = Viewport(1,1,1)
    sphere1 = Sphere((0, -1, 3),1,(255, 0, 0))
    sphere2 = Sphere((2, 0, 4),1,(0, 0, 255))   
    sphere3 = Sphere((-2, 0, 4),1,(0, 255, 0))

    scene = Scene()
    scene.add_objet(sphere1)
    scene.add_objet(sphere2)
    scene.add_objet(sphere3)
    scene.set_camera(camera)
    scene.set_viewport(viewport)

    Cw = 500
    Ch = 500
    canvas = Canvas(Cw, Ch)
    O = (camera.x, camera.y, camera.z) 
    
    for x in range(-Cw // 2, Cw // 2):
        for y in range(-Ch // 2, Ch // 2):

            D = canvas_to_viewport = CanvasToViewport(viewport, canvas, x, y)
            color = TraceRay(O, D, 1, float('inf'), scene)
            canvas.PutPixel(x, y, color)
            
    img = Image.new('RGB', (Cw, Ch))
    for y in range(Ch):
        for x in range(Cw):
            img.putpixel((x, y), canvas.pixels[y][x])
            
    img.show()

