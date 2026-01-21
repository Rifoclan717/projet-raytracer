from Scene import Scene
from Camera import Camera
from Canvas import Canvas
from Viewport import Viewport
from PIL import Image
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport

if __name__ == '__main__':

    # Initialisation de la scène
    camera = Camera(0, 0, -3)
    viewport = Viewport(1, 1, 1)
    scene = Scene()
    load_scene_from_file(scene, 'scene.txt')
    scene.set_camera(camera)
    scene.set_viewport(viewport)

    Cw = 500
    Ch = 500
    canvas = Canvas(Cw, Ch)

    # Raytracing : calcul de la couleur de chaque pixel
    O = camera.position
    for x in range(-Cw // 2, Cw // 2):
        for y in range(-Ch // 2, Ch // 2):
            D = CanvasToViewport(viewport, canvas, x, y)
            color = TraceRay(O, D, 1, float('inf'), scene, 5)
            canvas.PutPixel(x, y, color)

    # Export de l'image en fichier BMP
    img = Image.new('RGB', (Cw, Ch))
    for y in range(Ch):
        for x in range(Cw):
            pixel = canvas.pixels[y][x]
            img.putpixel((x, y), (int(pixel[0]), int(pixel[1]), int(pixel[2])))
    img.save('output.bmp')

