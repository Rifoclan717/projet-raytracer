class Canvas:
    # Initialize a canvas with given height and width
    def __init__(self, height, width):
        self.height = height      
        self.width = width
        self.pixels = []  
        for y in range(height):
            ligne = []     
            for x in range(width):
                ligne.append((0, 0, 0))
            self.pixels.append(ligne)

    # Set the color of a pixel at (x, y)
    def PutPixel(self,x,y,color):
        Sx = int((self.width / 2) + x)
        Sy = int((self.height / 2) - y)

        if 0 <= Sx < self.width and 0 <= Sy < self.height:
            self.pixels[Sy][Sx] = color