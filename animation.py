import math
import os
from vec3 import multiplier_matrice_vecteur, creer_rotation
from Scene import Scene         
from Camera import Camera       
from Canvas import Canvas       
from Viewport import Viewport   
from PIL import Image  
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport

def render_frame(scene, camera, viewport, Cw, Ch):
    """Rend une frame et retourne l'image PIL"""
    canvas = Canvas(Cw, Ch)
    O = camera.position
    
    for x in range(-Cw // 2, Cw // 2):
        for y in range(-Ch // 2, Ch // 2):
            D = CanvasToViewport(viewport, canvas, x, y)
            D = multiplier_matrice_vecteur(camera.rotation, D)
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
    scene = Scene()
    load_scene_from_file(scene, 'scene.txt')
    scene.set_viewport(viewport)

    Cw = 200  # Résolution réduite pour aller plus vite
    Ch = 200

    # Créer le dossier pour les frames
    os.makedirs('frames', exist_ok=True)

    # === ANIMATION : rotation de la caméra autour de la scène ===
    num_frames = 36  # Nombre de frames (360° / 36 = 10° par frame)
    radius = 6       # Distance de la caméra au centre
    center_y = 0.5   # Hauteur de la caméra

    print(f"Rendu de {num_frames} frames (résolution {Cw}x{Ch})...")

    images = []  # Pour créer le GIF

    for frame in range(num_frames):
        angle = (frame / num_frames) * 360  # Angle en degrés (0 à 360)
        
        # Position de la caméra sur un cercle autour du centre (0, 0, 3)
        cam_x = radius * math.sin(math.radians(angle))
        cam_z = 3 + radius * math.cos(math.radians(angle))
        
        # La caméra pointe vers le centre de la scène
        rot_y = -angle
        
        camera = Camera(cam_x, center_y, cam_z, 0, rot_y, 0)
        scene.set_camera(camera)
        
        img = render_frame(scene, camera, viewport, Cw, Ch)
        images.append(img)
        
        filename = f'frames/frame_{frame:03d}.png'
        img.save(filename)
        print(f"Frame {frame + 1}/{num_frames} sauvegardée: {filename}")

    # Créer le GIF automatiquement
    print("\nCréation du GIF...")
    images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=180, loop=0)
    
    print(f"\nTerminé !")
    print(f"- {num_frames} images dans 'frames/'")
    print(f"- GIF animé: animation.gif")
