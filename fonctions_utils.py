from Light import Light
from Sphere import Sphere
from parallelogramme import Parallelogram
from vec3 import addition_vecteurs, multiplication_scalaire, soustraction_vecteurs, produit_scalaire, taille_vecteur
import math

# Calculer l'intersection entre un rayon et un parallélogramme (mur)
def IntersectRayParallelogram(O, D, wall):
    
    N = wall.N # Vecteur normal du mur

    denom = produit_scalaire(N, D) # N scalaire D sert à vérifier si le rayon est parallèle au mur

    # Si denom est proche de 0, le rayon est parallèle au mur donc pas d'intersection
    if abs(denom) < 1e-6:
        return float('inf')  # retourne "infini" pour dire pas d'intersection

    # t = distance le long du rayon jusqu'au plan du mur
    # On utilise la formule d'intersection : t = (A - O) . N / (D . N)
    t = produit_scalaire(soustraction_vecteurs(wall.A, O), N) / denom

    # Si t < 0, le mur est derrière le rayon donc pas d'intersection
    if t < 0:
        return float('inf') # retourne "infini" pour dire pas d'intersection

    # P = point exact où le rayon frappe le plan du mur
    P = addition_vecteurs(O, multiplication_scalaire(D, t)) 

    # AP = vecteur du point A du mur au point P
    AP = soustraction_vecteurs(P, wall.A) 

    # On projette AP sur les vecteurs U et V du mur pour savoir si P est à l'intérieur
    alpha = produit_scalaire(AP, wall.U) / produit_scalaire(wall.U, wall.U)
    beta  = produit_scalaire(AP, wall.V) / produit_scalaire(wall.V, wall.V)

    # Si alpha et beta sont entre 0 et 1 donc P est bien dans le parallélogramme
    if 0 <= alpha <= 1 and 0 <= beta <= 1:
        return t  # on retourne la distance jusqu'à l'intersection

    # Sinon retourne "infini" pour dire pas d'intersection
    return float('inf')

# Calculer l'éclairage au point P avec la normale N
def ComputeLighting(P, N, scene, V, s):

    intensity = 0.0 # Intensité lumineuse initiale

    # Parcourir chaque source de lumière dans la scène
    for light in scene.lights:

        # Lumière ambiante
        if light.type == 'ambient':
            # On ajoute simplement l'intensité ambiante
            intensity += light.intensity
            # On continue sans traiter les autres types de lumière
            continue
        
        # Direction de la lumière et distance maximale t_max
        if light.type == 'point':
            # Vecteur de la lumière vers le point P
            L = soustraction_vecteurs(light.position, P)
            # Distance entre la lumière et le point P
            t_max = taille_vecteur(L)
        else:
            # Directionnelle
            L = light.direction
            # On ne vérifie pas les ombres pour les lumières directionnelles
            t_max = float('inf')

        # Vérifier les ombres
        shadow_t, shadow_obj, obj_type = ClosestIntersection(P, L, 0.001, t_max, scene) 
        # Si shadow_obj n'est pas None, il y a une intersection donc on est dans l'ombre
        if shadow_obj != None :
            # On ignore cette lumière car le point est dans l'ombre
            continue

        # Diffuse
        n_dot_l = produit_scalaire(N, L) # On calcule (N . L)
        # Si n_dot_l > 0, la lumière est dans la direction de la normale
        if n_dot_l > 0:
            # On ajoute la composante diffuse à l'intensité
            intensity += light.intensity * n_dot_l / (taille_vecteur(N) * taille_vecteur(L))

        # Spéculaire
        if s > 0: # Si l'objet a une composante spéculaire

            R = ReflectRay(L, N) # Calcul du vecteur réfléchi R
            r_dot_v = produit_scalaire(R, V) # On calcule (R . V)

            # Si r_dot_v > 0, le rayon réfléchi est dans la direction de la caméra
            if r_dot_v > 0:
                # On ajoute la composante spéculaire à l'intensité
                intensity += light.intensity * pow(r_dot_v / (taille_vecteur(R) * taille_vecteur(V)), s) 

    return intensity # On retourne l'intensité totale calculée

# Tracer un rayon depuis l'origine O dans la direction D
def TraceRay(O, D, t_min, t_max, scene, depth):

    # Trouver l'intersection la plus proche du rayon avec les objets de la scène
    t, obj, obj_type = ClosestIntersection(O, D, t_min, t_max, scene)

    # Si pas d'objet intersecté, retourner la couleur de fond (noir)
    if obj is None:
        return (0,0,0)
    
    # Calculer le point d'intersection P
    P = addition_vecteurs(O, multiplication_scalaire(D, t))

    # Si l'objet est une sphère, on calcule sa normale au point P
    if obj_type == "sphere":
        # N = vecteur normal (perpendiculaire) à la surface de la sphère au point P
        N = soustraction_vecteurs(P, obj.center) 
        N = multiplication_scalaire(N, 1/taille_vecteur(N)) 

        # Récupérer les propriétés de la sphère
        color, specular, reflective = obj.color, obj.specular, obj.reflective
    else:
        # Si l'objet est un mur (parallélogramme), la normale est constante
        N, color, specular, reflective = obj.N, obj.color, obj.specular, obj.reflective

    # Calculer l'intensité lumineuse au point P
    intensity = ComputeLighting(P, N, scene, multiplication_scalaire(D, -1), specular)

    # Calculer la couleur locale en fonction de l'intensité
    local_color = multiplication_scalaire(color, intensity)

    # Si on a atteint la profondeur maximale ou si l'objet n'est pas réfléchissant
    if depth <= 0 or reflective <= 0:
        # On retourne la couleur locale
        return local_color  
    
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

    # O = origine du rayon (position de la caméra)
    # D = direction du rayon

    r = sphere.radius # rayon de la sphère
    CO = soustraction_vecteurs(O, sphere.center) # vecteur du centre de la sphère à l'origine du rayon

    a = produit_scalaire(D, D)          # D . D
    b = 2 * produit_scalaire(CO, D)     # 2 * (CO . D)
    c = produit_scalaire(CO, CO) - r*r  # (CO . CO) - r^2

    discriminant = b*b - 4*a*c    # discriminant de l'équation quadratique

    # Si le discriminant est négatif, pas d'intersection
    if discriminant < 0:
        return float('inf'), float('inf')

    # Calculer les deux solutions de l'équation quadratique
    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    # Retourner les deux distances d'intersection
    return t1, t2

# Trouver l'intersection la plus proche entre un rayon et les objets de la scène
def ClosestIntersection(O, D, t_min, t_max, scene):

    # Initialiser les variables pour suivre l'intersection la plus proche
    closest_t = float('inf')
    closest_obj = None
    obj_type = None

    # Sphères
    for sphere in scene.objets: # Parcourir chaque sphère dans la scène

        t1, t2 = IntersectRaySphere(O, D, sphere) # Calculer les intersections avec la sphère
        # Vérifier les deux solutions
        for t in [t1, t2]:
            # Si t est dans l'intervalle valide et plus proche que la précédente
            if t_min < t < t_max and t < closest_t:
                # Mettre à jour les variables d'intersection la plus proche
                closest_t = t
                closest_obj = sphere 
                obj_type = "sphere" # Indiquer que c'est une sphère

    # Murs
    for mur in scene.murs: # Parcourir chaque mur (parallélogramme) dans la scène

        t = IntersectRayParallelogram(O, D, mur) # Calculer l'intersection avec le mur
        # Si t est dans l'intervalle valide et plus proche que la précédente
        if t_min < t < t_max and t < closest_t:
            # Mettre à jour les variables d'intersection la plus proche
            closest_t = t
            closest_obj = mur
            obj_type = "wall" # Indiquer que c'est un mur

    # Retourner les informations de l'intersection la plus proche     
    return closest_t, closest_obj, obj_type

# Calculer le vecteur réfléchi R à partir du vecteur d'incidence R et de la normale N
def ReflectRay(R, N) :
    n_dot_r = produit_scalaire(N, R) # On calcule (N . R)
    # On retourne le rayonnement réfléchi
    return soustraction_vecteurs (multiplication_scalaire(N, 2 * n_dot_r), R)

# Convertir les coordonnées du canevas aux coordonnées du viewport
def CanvasToViewport(viewport,canvas,x,y):
    # On effectue la conversion en utilisant les dimensions du viewport et du canvas
    return (x * viewport.width / canvas.width,y * viewport.height / canvas.height,viewport.dist)


# Charger une scène à partir d'un fichier texte
def load_scene_from_file(scene, filename):
    try:
        with open(filename, 'r') as f: # Ouvrir le fichier en mode lecture
            for line in f: # Lire chaque ligne du fichier
                parts = line.split() # Diviser la ligne en parties
                if not parts: continue # Sauter les lignes vides
                
                # Traiter chaque type d'objet
                
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
                    # Format: parallelogram Ax Ay Az Ux Uy Uz Vx Vy Vz r g b specular reflective
                    Ax, Ay, Az = float(parts[1]), float(parts[2]), float(parts[3])
                    Ux, Uy, Uz = float(parts[4]), float(parts[5]), float(parts[6])
                    Vx, Vy, Vz = float(parts[7]), float(parts[8]), float(parts[9])
                    r, g, b = int(parts[10]), int(parts[11]), int(parts[12])
                    specular = int(parts[13])
                    reflective = int(parts[14])

                    # Création et ajout
                    p = Parallelogram((Ax, Ay, Az), Ux, Uy, Uz, Vx, Vy, Vz, (r,g,b), specular, reflective)
                    scene.add_mur(p) #Parallélogramme ajouté à la scène
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
                        print(f"Type de lumière inconnu: {type}")
                        # Si le type est inconnu, on continue sans ajouter de lumière
                        continue

                    scene.add_light(light) #Light ajoutée à la scène
                    print(f"Lumière chargée: {type} avec intensité {intensity}")

    except FileNotFoundError: # Si le fichier n'est pas trouvé
        print("Erreur: Le fichier scene.txt est introuvable.")

