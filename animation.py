import math
import os
from Scene import Scene         
from Camera import Camera       
from Canvas import Canvas       
from Viewport import Viewport   
from PIL import Image  
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport
from Sphere import Sphere

# Fonction pour rendre une frame et retourner l'image PIL
def render_frame(scene, camera, viewport, Cw, Ch):

    # Configuration de la scène
    canvas = Canvas(Cw, Ch)
    O = camera.position
    
    # Parcours de chaque pixel du canvas
    for x in range(-Cw // 2, Cw // 2): 
        for y in range(-Ch // 2, Ch // 2):
            D = CanvasToViewport(viewport, canvas, x, y) # Direction du rayon a partir du pixel (x, y)
            color = TraceRay(O, D, 1, float('inf'), scene, 3) # Tracer le rayon et obtenir la couleur
            canvas.PutPixel(x, y, color) # Mettre a jour la couleur du pixel dans le canvas
    
    img = Image.new('RGB', (Cw, Ch)) # Creation d'une nouvelle image RGB avec les dimensions du canvas

    # Copier les pixels du canvas vers l'image
    for y in range(Ch):
        for x in range(Cw):
            pixel = canvas.pixels[y][x] # Récupérer la couleur du pixel sous forme de tuple (R, G, B)
            img.putpixel((x, y), (int(pixel[0]), int(pixel[1]), int(pixel[2]))) # Mettre a jour le pixel de l'image
    # Retourner l'image PIL
    return img

if __name__ == '__main__':
    
    viewport = Viewport(1, 1, 1) # Viewport(width, height, distance)

    # Résolution réduite pour aller plus vite
    Cw = 200  
    Ch = 200

    # Créer le dossier pour les frames
    os.makedirs('frames', exist_ok=True)

    # Nombre de frames pour l'animation
    num_frames = 36
    
    # Position de la caméra
    camera = Camera(0, 0.5, -2)

    # Positions initiales des sphères
    # Sphère centrale : x=0, y=-1, z=3 (monte et descend)
    # Sphère gauche : x=-3, y=0.5, z=4 (va vers le centre puis revient)
    # Sphère droite : x=3, y=0.5, z=4 (va vers le centre puis revient)
    
    center_sphere_base_y = -1 # Position de base en y de la sphère centrale
    center_sphere_amplitude = 1.5  # Amplitude du mouvement vertical
    
    left_sphere_base_x = -3 # Position de base en x de la sphère gauche
    right_sphere_base_x = 3 # Position de base en x de la sphère droite
    side_sphere_amplitude = 2  # Amplitude du mouvement horizontal

    print(f"Rendu de {num_frames} frames (résolution {Cw}x{Ch})...")

    images = []  # Liste pour stocker les images des frames

    # Boucle sur chaque frame
    for frame in range(num_frames):
        # Recharger la scène à chaque frame pour réinitialiser les positions
        scene = Scene()
        load_scene_from_file(scene, 'scene.txt')
        scene.set_viewport(viewport)
        scene.set_camera(camera)
        
        # Calculer l'angle pour l'animation (cycle complet)
        t = (frame / num_frames) * 2 * math.pi
        
        # Animation de la sphère centrale (haut/bas)
        center_y_offset = center_sphere_amplitude * math.sin(t)
        new_center_y = center_sphere_base_y + center_y_offset
        
        # Animation des sphères latérales (vers le centre puis s'éloignent)
        side_x_offset = side_sphere_amplitude * math.sin(t)
        new_left_x = left_sphere_base_x + side_x_offset  # -3 + offset (va vers 0)
        new_right_x = right_sphere_base_x - side_x_offset  # 3 - offset (va vers 0)
        
        # Modifier les positions des sphères dans la scène
        # La sphère 0 est la sphère centrale (rouge, position 0, -1, 3)
        # La sphère 1 est la sphère gauche (verte, position -3, 0.5, 4)
        # La sphère 2 est la sphère droite (bleue, position 3, 0.5, 4)
        
        # Mettre à jour les positions des sphères
        for obj in scene.objets:
            if isinstance(obj, Sphere):
                # Sphère centrale (rouge à x=0, z=3)
                if abs(obj.center[0]) < 0.1 and abs(obj.center[2] - 3) < 0.1 and obj.radius == 1:
                    obj.center = (obj.center[0], new_center_y, obj.center[2])
                # Sphère gauche (verte à x=-3)
                elif obj.center[0] < -2 and obj.radius == 1:
                    obj.center = (new_left_x, obj.center[1], obj.center[2])
                # Sphère droite (bleue à x=3)
                elif obj.center[0] > 2 and obj.radius == 1:
                    obj.center = (new_right_x, obj.center[1], obj.center[2])
        
        img = render_frame(scene, camera, viewport, Cw, Ch) # Rendre la frame
        images.append(img) # Ajouter l'image à la liste
        
        filename = f'frames/frame_{frame:03d}.png' # Nom du fichier pour la frame
        img.save(filename) # Sauvegarder l'image de la frame

        print(f"Frame {frame + 1}/{num_frames} sauvegardée: {filename}") # Indication de progression

    # Créer le GIF automatiquement
    print("\nCréation du GIF...")
    images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)
    
    print(f"\nTerminé !")
    print(f"- {num_frames} images dans 'frames/'")
    print(f"- GIF animé: animation.gif")
