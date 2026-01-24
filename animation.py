import os
from Scene import Scene
from Camera import Camera
from Canvas import Canvas
from Viewport import Viewport
from PIL import Image
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport

# Render a single frame of the scene from the camera's perspective
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
    viewport = Viewport(1, 1, 1)
    camera = Camera(0, 0.5, -2)
    Cw, Ch = 200, 200
    num_frames = 20
    os.makedirs('frames', exist_ok=True)

    images = []
    print(f"Rendu de {num_frames} frames pour l'animation")

    # Generate frames with animated spheres
    for frame in range(num_frames):
        scene = Scene()
        load_scene_from_file(scene, 'scene.txt')
        scene.set_viewport(viewport)
        scene.set_camera(camera)

        sphere0 = scene.objets[0]
        sphere0.center = (sphere0.center[0], sphere0.center[1] + frame * 0.1, sphere0.center[2])

        sphere1 = scene.objets[1]
        sphere1.center = (sphere1.center[0] + frame * 0.1, sphere1.center[1], sphere1.center[2])

        sphere2 = scene.objets[2]
        sphere2.center = (sphere2.center[0] - frame * 0.1, sphere2.center[1], sphere2.center[2])

        img = render_frame(scene, camera, viewport, Cw, Ch)
        images.append(img)
        img.save(f'frames/frame_{frame:03d}.png')
        print(f"Frame {frame + 1}/{num_frames}")

    images = images + images[::-1]

    images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)
    print("fin de la boucle'")
