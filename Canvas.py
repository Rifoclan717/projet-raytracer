class Canvas:
    def __init__(self, height, width):
        self.height = height      
        self.width = width
        self.pixels = []  
        for y in range(height):
            ligne = []     
            for x in range(width):
                ligne.append((0, 0, 0))
            self.pixels.append(ligne)

    def PutPixel(self,x,y,color):
        # Convert from canvas coordinates (origin at center) to array indices
        Sx = int((self.width / 2) + x)
        Sy = int((self.height / 2) - y)
        # Ensure indices are within bounds and use [row][col] ordering
        if 0 <= Sx < self.width and 0 <= Sy < self.height:
            self.pixels[Sy][Sx] = color