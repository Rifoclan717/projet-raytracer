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

# === MATRICES DE ROTATION ===

def rotation_x(angle_deg):
    """Matrice de rotation autour de l'axe X"""
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return [[1, 0, 0], [0, c, -s], [0, s, c]]

def rotation_y(angle_deg):
    """Matrice de rotation autour de l'axe Y"""
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]

def rotation_z(angle_deg):
    """Matrice de rotation autour de l'axe Z"""
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]

def multiplier_matrice_vecteur(m, v):
    """Multiplie une matrice 3x3 par un vecteur 3D"""
    return (
        m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]*v[2],
        m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]*v[2],
        m[2][0]*v[0] + m[2][1]*v[1] + m[2][2]*v[2]
    )

def multiplier_matrices(m1, m2):
    """Multiplie deux matrices 3x3"""
    r = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r[i][j] += m1[i][k] * m2[k][j]
    return r

def creer_rotation(rx, ry, rz):
    """Crée une matrice de rotation combinée (angles en degrés)"""
    return multiplier_matrices(rotation_x(rx), multiplier_matrices(rotation_y(ry), rotation_z(rz)))