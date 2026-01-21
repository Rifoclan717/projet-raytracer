import math
import os
from Scene import Scene
from Camera import Camera
from Canvas import Canvas
from Viewport import Viewport
from PIL import Image
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport
from Sphere import Sphere

# Rend une frame et retourne l'image PIL
def render_frame(scene, camera, viewport, Cw, Ch):
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
    # Configuration
    viewport = Viewport(1, 1, 1)
    camera = Camera(0, 0.5, -2)
    Cw, Ch = 200, 200
    num_frames = 36
    os.makedirs('frames', exist_ok=True)

    # Paramètres d'animation
    center_y_base, center_amplitude = -1, 1.5
    left_x_base, right_x_base, side_amplitude = -3, 3, 2

    images = []
    print(f"Rendu de {num_frames} frames...")

    # Génération des frames
    for frame in range(num_frames):
        scene = Scene()
        load_scene_from_file(scene, 'scene.txt')
        scene.set_viewport(viewport)
        scene.set_camera(camera)

        t = (frame / num_frames) * 2 * math.pi

        for obj in scene.objets:
            if isinstance(obj, Sphere) and obj.radius == 1:
                if abs(obj.center[0]) < 0.1:
                    obj.center = (obj.center[0], center_y_base + center_amplitude * math.sin(t), obj.center[2])
                elif obj.center[0] < -2:
                    obj.center = (left_x_base + side_amplitude * math.sin(t), obj.center[1], obj.center[2])
                elif obj.center[0] > 2:
                    obj.center = (right_x_base - side_amplitude * math.sin(t), obj.center[1], obj.center[2])

        img = render_frame(scene, camera, viewport, Cw, Ch)
        images.append(img)
        img.save(f'frames/frame_{frame:03d}.png')
        print(f"Frame {frame + 1}/{num_frames}")

    # Export GIF
    images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)
    print("Terminé ! → animation.gif")
