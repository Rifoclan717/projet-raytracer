from Scene import Scene         
from Camera import Camera       
from Canvas import Canvas       
from Viewport import Viewport   
from PIL import Image  
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport

if __name__ == '__main__':
    
    camera = Camera(0, 0, -3) # Camera(x, y, z)
    viewport = Viewport(1,1,1) # Viewport(width, height, distance)
    scene = Scene() # Creation de la scene vide

    load_scene_from_file(scene, 'scene.txt') # Chargement de la scene a partir d'un fichier texte

    # On definit la camera et le viewport de la scene
    scene.set_camera(camera)
    scene.set_viewport(viewport)
    # On cree le canvas
    Cw = 500
    Ch = 500
    canvas = Canvas(Cw, Ch)

    O = camera.position # Origine des rayons (position de la camera)
    
    # Parcours de chaque pixel du canvas
    for x in range(-Cw // 2, Cw // 2):
        for y in range(-Ch // 2, Ch // 2):
            D = CanvasToViewport(viewport, canvas, x, y) # Direction du rayon a partir du pixel (x, y)
            color = TraceRay(O, D, 1, float('inf'), scene, 5) # Tracer le rayon et obtenir la couleur
            canvas.PutPixel(x, y, color) # Mettre a jour la couleur du pixel dans le canvas


    img = Image.new('RGB', (Cw, Ch)) # Creation d'une nouvelle image RGB avec les dimensions du canvas

    # Copier les pixels du canvas vers l'image
    for y in range(Ch):
        for x in range(Cw):
            integer = (canvas.pixels[y][x])  # Récupérer la couleur du pixel sous forme de tuple (R, G, B)
            r = int(integer[0])
            g = int(integer[1])
            b = int(integer[2])
            integer = (r, g, b)
            img.putpixel((x, y), integer) # Mettre a jour le pixel de l'image

    img.save('output.bmp') # Sauvegarder l'image dans un fichier BMP

