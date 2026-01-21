from vec3 import taille_vecteur

class Parallelogram:
    # Parallelogramme défini par un point A et deux vecteurs U et V
    def __init__(self, A, Ux, Uy, Uz, Vx, Vy, Vz, color, specular, reflective):
        self.A = A
        self.U = (Ux, Uy, Uz) 
        self.V = (Vx, Vy, Vz)
        self.color = color
        self.specular = specular
        self.reflective = reflective

        # Calcul du vecteur normal N = U x V
        N_raw = (
            Uy*Vz - Uz*Vy,
            Uz*Vx - Ux*Vz,
            Ux*Vy - Uy*Vx
        )

        norm = taille_vecteur(N_raw) # Norme de N_raw pour normalisation
        self.N = (N_raw[0]/norm, N_raw[1]/norm, N_raw[2]/norm) # Vecteur normal unitaire
