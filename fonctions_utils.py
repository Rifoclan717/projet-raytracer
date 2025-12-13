from Sphere import Sphere
from vec3 import soustraction_vecteurs, produit_scalaire
import math

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


#Fait avec chatgpt car je savais pas comment faire
def load_scene_from_file(scene, filename):
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if not parts: continue # Sauter les lignes vides
                
                if parts[0] == 'sphere':
                    # Format: sphere x y z radius r g b
                    # On convertit les textes en float/int
                    cx, cy, cz = float(parts[1]), float(parts[2]), float(parts[3])
                    radius = float(parts[4])
                    r, g, b = int(parts[5]), int(parts[6]), int(parts[7])
                    
                    # Création et ajout
                    s = Sphere((cx, cy, cz), radius, (r, g, b))
                    scene.add_objet(s)
                    print(f"Sphère chargée: {s.center}")
    except FileNotFoundError:
        print("Erreur: Le fichier scene.txt est introuvable.")

