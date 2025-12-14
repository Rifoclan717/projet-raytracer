from Light import Light
from Sphere import Sphere
from vec3 import addition_vecteurs, multiplication_scalaire, soustraction_vecteurs, produit_scalaire, taille_vecteur
import math


def ComputeLighting(P, N, scene):
    intensity = 0.0
    for light in scene.lights:
        if light.type == 'ambient':
            intensity += light.intensity
        else:
            if light.type == 'point':
                L = soustraction_vecteurs(light.position, P)
            else:
                L = light.direction
            n_dot_l = produit_scalaire(N, L)
            if n_dot_l > 0:
                intensity += light.intensity * n_dot_l / (taille_vecteur(N) * taille_vecteur(L))
    return intensity


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
    compute_result = multiplication_scalaire(D, closest_t)
    P = addition_vecteurs(O, compute_result)
    N = soustraction_vecteurs(P, closest_sphere.center)
    N = multiplication_scalaire(N, 1 / taille_vecteur(N)) #On normalise ici le vecteur N
    return multiplication_scalaire(closest_sphere.color, ComputeLighting(P, N, scene))

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
                elif parts[0] == 'light':
                    # Format: light type intensity [x y z]
                    type = parts[1]
                    intensity = float(parts[2])
                    if type == 'ambient':
                        light = Light(type, intensity, None)
                    elif type == 'point':
                        x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
                        light = Light(type, intensity, (x, y, z))
                    elif type == 'directional':
                        dx, dy, dz = float(parts[3]), float(parts[4]), float(parts[5])
                        light = Light(type, intensity, (dx, dy, dz))
                    else:
                        print(f"Type de lumière inconnu: {type}")
                        continue
                    scene.add_light(light)
                    print(f"Lumière chargée: {type} avec intensité {intensity}")
    except FileNotFoundError:
        print("Erreur: Le fichier scene.txt est introuvable.")

