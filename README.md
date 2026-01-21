# Raytracer Python

Un raytracer simple écrit en Python, capable de rendre des scènes 3D avec des sphères, des murs, des ombres, des réflexions et différents types d'éclairage.

## Fonctionnalités

- Rendu de sphères et parallélogrammes (murs)
- Éclairage : ambiant, ponctuel, directionnel
- Ombres portées
- Réflexions récursives
- Export en image BMP
- Animation GIF

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Rendu statique

```bash
python3 main.py
```

Génère `output.bmp` à partir de la scène définie dans `scene.txt`.

### Animation

```bash
python3 animation.py
```

Génère un GIF animé `animation.gif` et les frames dans le dossier `frames/`.

## Format de scène (scene.txt)

```
sphere x y z radius r g b specular reflective
parallelogram Ax Ay Az Ux Uy Uz Vx Vy Vz r g b specular reflective
light ambient intensity
light point intensity x y z
light directional intensity dx dy dz
```

### Exemple

```
sphere 0 -1 3 1 255 0 0 500 0.2
light ambient 0.2
light point 0.6 2 1 0
```

## Structure du projet

```
├── main.py              # Point d'entrée principal
├── animation.py         # Génération d'animations GIF
├── Canvas.py            # Gestion du canvas 2D
├── Camera.py            # Position de la caméra
├── Viewport.py          # Configuration du viewport
├── Scene.py             # Conteneur de la scène
├── Sphere.py            # Objet sphère
├── parallelogramme.py   # Objet mur/parallélogramme
├── Light.py             # Sources de lumière
├── vec3.py              # Opérations vectorielles
├── fonctions_utils.py   # Raytracing et utilitaires
└── scene.txt            # Définition de la scène
```

## Auteur

Mohamed et Kadir
