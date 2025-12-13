import math
from vec3 import soustraction_vecteurs, produit_scalaire,taille_vecteur
from Scene import Scene         
from Camera import Camera       
from Canvas import Canvas       
from Viewport import Viewport   
from Sphere import Sphere
from PIL import Image  
from fonctions_utils import load_scene_from_file, TraceRay, CanvasToViewport

if __name__ == '__main__':
    
    camera = Camera(0,0,0)  
    viewport = Viewport(1,1,1)
    scene = Scene()
    # Charger les sphères depuis un fichier texte (format attendu:)
    # lignes de la forme: "sphere cx cy cz radius r g b"
    # Exemple disponible dans scene.txt
    load_scene_from_file(scene, 'scene.txt')
    scene.set_camera(camera)
    scene.set_viewport(viewport)

    Cw = 500
    Ch = 500
    canvas = Canvas(Cw, Ch)
    O = (camera.x, camera.y, camera.z) 
    
    for x in range(-Cw // 2, Cw // 2):
        for y in range(-Ch // 2, Ch // 2):
            D = CanvasToViewport(viewport, canvas, x, y)
            color = TraceRay(O, D, 1, float('inf'), scene)
            canvas.PutPixel(x, y, color)


    #Seulement pour l'affichage de l'image en utilisant PIL...
    img = Image.new('RGB', (Cw, Ch))
    for y in range(Ch):
        for x in range(Cw):
            img.putpixel((x, y), canvas.pixels[y][x])
            
    # Sauvegarde l'image sans ouvrir de viewer (évite blocage en environnement headless)
    img.save('output.bmp')

