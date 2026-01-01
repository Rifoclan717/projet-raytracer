from Light import Light
from Sphere import Sphere
from parallelogramme import Parallelogram
from vec3 import addition_vecteurs, multiplication_scalaire, soustraction_vecteurs, produit_scalaire, taille_vecteur
import math

def IntersectRayParallelogram(O, D, wall):
    # N = normale du mur
    N = wall.N

    # denom = D ⋅ N (produit scalaire) 
    # Si D est parallèle au mur (denom proche de 0), il n'y a pas d'intersection
    denom = produit_scalaire(N, D)
    if abs(denom) < 1e-6:
        return float('inf')  # retourne "infini" pour dire pas d'intersection

    # t = distance le long du rayon où il frappe le plan du mur
    # formule : t = ((A - O) ⋅ N) / (D ⋅ N)
    t = produit_scalaire(
        soustraction_vecteurs(wall.A, O),
        N
    ) / denom

    # Si t < 0, le mur est derrière le rayon donc pas d'intersection
    if t < 0:
        return float('inf')

    # P = point exact où le rayon frappe le plan du mur
    P = addition_vecteurs(O, multiplication_scalaire(D, t))

    # AP = vecteur depuis un coin du mur (A) jusqu'au point d'intersection
    AP = soustraction_vecteurs(P, wall.A)

    # On projette AP sur les vecteurs U et V du mur pour savoir si P est à l'intérieur
    alpha = produit_scalaire(AP, wall.U) / produit_scalaire(wall.U, wall.U)
    beta  = produit_scalaire(AP, wall.V) / produit_scalaire(wall.V, wall.V)

    # Si alpha et beta sont entre 0 et 1 donc P est bien dans le parallélogramme
    if 0 <= alpha <= 1 and 0 <= beta <= 1:
        return t  # on retourne la distance jusqu'à l'intersection

    # Sinon intersection en dehors du mur
    return float('inf')

# Calculer l'éclairage en un point donné
def ComputeLighting(P, N, scene, V, s):
    intensity = 0.0

    for light in scene.lights:
        if light.type == 'ambient':
            intensity += light.intensity
            continue

        if light.type == 'point':
            L = soustraction_vecteurs(light.position, P)
            t_max = taille_vecteur(L)
        else:
            L = light.direction
            t_max = float('inf')

        # Shadow ray
        shadow_t, shadow_obj, obj_type = ClosestIntersection(P, L, 0.001, t_max, scene)
        if shadow_obj != None :
            continue

        # Diffuse
        n_dot_l = produit_scalaire(N, L)
        if n_dot_l > 0:
            intensity += light.intensity * n_dot_l / (taille_vecteur(N) * taille_vecteur(L))

        # Specular
        if s > 0:
            R = ReflectRay(L, N)
            r_dot_v = produit_scalaire(R, V)
            if r_dot_v > 0:
                intensity += light.intensity * pow(
                    r_dot_v / (taille_vecteur(R) * taille_vecteur(V)), s
                )

    return intensity

def TraceRay(O, D, t_min, t_max, scene, depth):
    # On cherche l'intersection la plus proche entre le rayon (O,D) et les objets de la scène
    t, obj, obj_type = ClosestIntersection(O, D, t_min, t_max, scene)

    # Si on touche rien, on retourne le noir (pas de lumière)
    if obj is None:
        return (0,0,0)
    
    # P = point d'intersection réel sur l'objet
    P = addition_vecteurs(O, multiplication_scalaire(D, t))

    # Si l'objet est une sphère, on calcule sa normale
    if obj_type == "sphere":
        # N = vecteur normal (perpendiculaire) à la surface de la sphère
        N = soustraction_vecteurs(P, obj.center)
        N = multiplication_scalaire(N, 1/taille_vecteur(N))  # normalisation
        # On récupère la couleur, le specular (brillance), et la réflexion
        color, specular, reflective = obj.color, obj.specular, obj.reflective
    else:
        # Sinon, pour un mur ou un parallélogramme, on prend directement la normale stockée
        N, color, specular, reflective = obj.N, obj.color, obj.specular, obj.reflective

    # Calcul de la lumière sur ce point : diffuse + spéculaire
    # On envoie la normale N et le vecteur vers la caméra (-D)
    intensity = ComputeLighting(P, N, scene, multiplication_scalaire(D, -1), specular)

    # Couleur locale = couleur de l'objet * intensité lumineuse
    local_color = multiplication_scalaire(color, intensity)

    # Si on a atteint la profondeur maximale ou si l'objet n'est pas réfléchissant
    if depth <= 0 or reflective <= 0:
        return local_color  # pas de rayon réfléchi, juste la couleur locale
    
    # Sinon, on calcule le rayon réfléchi
    R = ReflectRay(multiplication_scalaire(D, -1), N)
    
    # On renvoie le résultat du rayon réfléchi (récursif) avec profondeur réduite
    reflected = TraceRay(P, R, 0.001, float('inf'), scene, depth-1)

    # La couleur finale = mélange entre couleur locale et couleur réfléchie
    return addition_vecteurs(
        multiplication_scalaire(local_color, 1-reflective),   # part locale
        multiplication_scalaire(reflected, reflective)       # part réfléchie
    )



# Calculer l'intersection entre un rayon et une sphère
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

def ClosestIntersection(O, D, t_min, t_max, scene):
    closest_t = float('inf')
    closest_obj = None
    obj_type = None
    # Sphères
    for sphere in scene.objets:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        for t in [t1, t2]:
            if t_min < t < t_max and t < closest_t:
                closest_t = t
                closest_obj = sphere
                obj_type = "sphere"
    # Murs
    for mur in scene.murs:
        t = IntersectRayParallelogram(O, D, mur)
        if t_min < t < t_max and t < closest_t:
            closest_t = t
            closest_obj = mur
            obj_type = "wall"
    return closest_t, closest_obj, obj_type

# Calculer le rayon réfléchi
def ReflectRay(R, N) :
    n_dot_r = produit_scalaire(N, R) # On calcule (N . R)
    return soustraction_vecteurs (multiplication_scalaire(N, 2 * n_dot_r), R) # On calcule 2 * N * (N . R) - R

# Convertir les coordonnées du canevas aux coordonnées du viewport
def CanvasToViewport(viewport,canvas,x,y):
    return (x * viewport.width / canvas.width,y * viewport.height / canvas.height,viewport.dist)


#Charger une scène à partir d'un fichier texte
def load_scene_from_file(scene, filename):
    try:
        with open(filename, 'r') as f: # Ouvrir le fichier en mode lecture
            for line in f: # Lire chaque ligne du fichier
                parts = line.split() # Diviser la ligne en parties
                if not parts: continue # Sauter les lignes vides
                
                if parts[0] == 'sphere':
                    # Format: sphere x y z radius r g b specular reflective
                    # On convertit les textes en float/int
                    cx, cy, cz = float(parts[1]), float(parts[2]), float(parts[3])
                    radius = float(parts[4])
                    r, g, b = int(parts[5]), int(parts[6]), int(parts[7])
                    specular = int(parts[8])
                    reflective = float(parts[9])
   
                    # Création et ajout
                    sphere = Sphere((cx, cy, cz), radius, (r, g, b), specular, reflective)
                    scene.add_objet(sphere) #Sphere ajoutée à la scène
                    print(f"Sphère chargée: {sphere.center}")
                
                elif parts[0] == 'parallelogram':
                    # Format: parallelogram Ax Ay Az Ux Uy Uz Vx Vy Vz r g b specular reflectivee
                    Ax, Ay, Az = float(parts[1]), float(parts[2]), float(parts[3])
                    Ux, Uy, Uz = float(parts[4]), float(parts[5]), float(parts[6])
                    Vx, Vy, Vz = float(parts[7]), float(parts[8]), float(parts[9])
                    r, g, b = int(parts[10]), int(parts[11]), int(parts[12])
                    specular = int(parts[13])
                    reflective = int(parts[14])
                    p = Parallelogram((Ax, Ay, Az), Ux, Uy, Uz, Vx, Vy, Vz, (r,g,b), specular, reflective)
                    scene.add_mur(p)
                    print("Parallelogramme chargé")

                elif parts[0] == 'light':
                    # Format: light type intensity [x y z]
                    type = parts[1]
                    intensity = float(parts[2])

                    if type == 'ambient': # Lumière ambiante
                        light = Light(type, intensity, None)

                    elif type == 'point': # Lumière ponctuelle
                        x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
                        light = Light(type, intensity, (x, y, z))

                    elif type == 'directional': # Lumière directionnelle
                        dx, dy, dz = float(parts[3]), float(parts[4]), float(parts[5])
                        light = Light(type, intensity, (dx, dy, dz))

                    else:
                        print(f"Type de lumière inconnu: {type}") #Si le type est inconnu, on continue
                        continue

                    scene.add_light(light) #Light ajoutée à la scène
                    print(f"Lumière chargée: {type} avec intensité {intensity}")

    except FileNotFoundError: # Si le fichier n'est pas trouvé
        print("Erreur: Le fichier scene.txt est introuvable.")

