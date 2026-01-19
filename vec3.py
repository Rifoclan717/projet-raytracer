import math

def soustraction_vecteurs(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

def addition_vecteurs(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

def produit_scalaire(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def taille_vecteur(v):
    return math.sqrt(produit_scalaire(v, v))

def multiplication_scalaire(v, scalar):
    return (v[0] * scalar, v[1] * scalar, v[2] * scalar)