import math
import os
from Scene import Scene         
from Camera import Camera       
from Canvas import Canvas       
from Viewport import Viewport   
from PIL import Image  
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport
from Sphere import Sphere

def render_frame(scene, camera, viewport, Cw, Ch):
    """Rend une frame et retourne l'image PIL"""
    canvas = Canvas(Cw, Ch)
    O = camera.position
    
    for x in range(-Cw // 2, Cw // 2):
        for y in range(-Ch // 2, Ch // 2):
            D = CanvasToViewport(viewport, canvas, x, y)
            color = TraceRay(O, D, 1, float('inf'), scene, 3)
            canvas.PutPixel(x, y, color)
    
    img = Image.new('RGB', (Cw, Ch))
    for y in range(Ch):
        for x in range(Cw):
            pixel = canvas.pixels[y][x]
            img.putpixel((x, y), (int(pixel[0]), int(pixel[1]), int(pixel[2])))
    return img

if __name__ == '__main__':
    
    viewport = Viewport(1, 1, 1)

    Cw = 200  # Résolution réduite pour aller plus vite
    Ch = 200

    # Créer le dossier pour les frames
    os.makedirs('frames', exist_ok=True)

    # === ANIMATION : sphères qui bougent ===
    num_frames = 36
    
    # Caméra fixe
    camera = Camera(0, 0.5, -2)

    # Positions initiales des sphères
    # Sphère centrale : x=0, y=-1, z=3 (monte et descend)
    # Sphère gauche : x=-3, y=0.5, z=4 (va vers le centre puis revient)
    # Sphère droite : x=3, y=0.5, z=4 (va vers le centre puis revient)
    
    center_sphere_base_y = -1
    center_sphere_amplitude = 1.5  # Amplitude du mouvement vertical
    
    left_sphere_base_x = -3
    right_sphere_base_x = 3
    side_sphere_amplitude = 2  # Amplitude du mouvement horizontal

    print(f"Rendu de {num_frames} frames (résolution {Cw}x{Ch})...")

    images = []  # Pour créer le GIF

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
        
        img = render_frame(scene, camera, viewport, Cw, Ch)
        images.append(img)
        
        filename = f'frames/frame_{frame:03d}.png'
        img.save(filename)
        print(f"Frame {frame + 1}/{num_frames} sauvegardée: {filename}")

    # Créer le GIF automatiquement
    print("\nCréation du GIF...")
    images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)
    
    print(f"\nTerminé !")
    print(f"- {num_frames} images dans 'frames/'")
    print(f"- GIF animé: animation.gif")
