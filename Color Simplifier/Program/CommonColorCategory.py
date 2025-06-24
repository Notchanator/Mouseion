import numpy as np
from PIL import Image

class CommonColorCategory:

    def __init__(self, file_url: str):
        self.image = Image.open(file_url)
        self.image_pixels = self.image.load()
        self.pixels = self.image.getcolors(self.image.size[0] * self.image.size[1])

    def pixelsDistance(self, pixel1, pixel2):
        return np.sqrt((pixel1[0] - pixel2[0])**2 + (pixel1[1] - pixel2[1])**2 + (pixel1[2] - pixel2[2])**2)
    
    def simplify(self):
        simplified = []
        for pixels in self.pixels:
            if pixels[0] > 6:
                simplified.append(pixels)
        # sorted_list = bubble_sort(simplified)
        return simplified


    def mostPixels(self, pixels, nums):
        """
        "White":(255,255,255),
        "Black":(0,0,0),
        "Red":(255,0,0),
        "Lime":(0,255,0),
        "Blue":(0,0,255),
        "Yellow":(255,255,0),
        "Cyan":(0,255,255),
        "Magenta":(255,0,255),
        "Gray":(128,128,128),
        "Green":(0,128,0),
        "Navy":(0,0,128),
        "Orange":(255,165,0),
        "Brown":(139,69,19)
        """
        Top = [None] * 13
        n = 0
        for pixel in pixels:
            closest_indx = self.closestColor(pixel[1])
            if Top[closest_indx] is None:
                Top[closest_indx] = pixel[1]
                n += 1
            if n == nums:
                return Top
        return Top
        

    def closestColor(self, pixel):
        Colors = [(255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (128,128,128), (0,128,0), (0,0,128), (255,165,0), (139,69,19)]
        n = 0
        closest = None
        while n < 13:
            dist = self.pixelsDistance(pixel, Colors[n])
            if closest is None or closest[0] > dist:
                closest = (dist, n)
            n += 1
        return closest[1]

    def closestPixel(self, top_colors, pixel):
        distances = [None] * len(top_colors)
        for index in range(len(top_colors)):
            distances[index] = self.pixelsDistance(top_colors[index], pixel)
        closest_indx = distances.index(min(distances))
        return top_colors[closest_indx]
    
    def assignColors(self, top_pixels: list):
        # Remove NaNs.
        top_pixels = [pixel for pixel in top_pixels if pixel]
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                self.image_pixels[i,j] = self.closestPixel(top_pixels, self.image_pixels[i,j])
    
    def simplifyImage(self, num_colors: int):
        simplified_pixels = self.simplify()
        QuickSort(simplified_pixels)
        top_pixels = self.mostPixels(simplified_pixels, num_colors)
        self.assignColors(top_pixels)
        return self.image

class QuickSort:

    def __init__(self, array: list):
        self.low = 0
        self.high = len(array) - 1
        self.sort(array)

    def partition(self, arr): 
        i = (self.low - 1 ) 
        x = arr[self.high][0] 
        for j in range(self.low, self.high): 
            if   arr[j][0] >= x: 
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i] 
        arr[i + 1], arr[self.high] = arr[self.high], arr[i + 1] 
        return (i + 1) 

    def sort(self, array): 
        size = self.high - self.low + 1
        stack = [0] * (size) 
        top = -1
        top = top + 1
        stack[top] = self.low 
        top = top + 1
        stack[top] = self.high 
        while top >= 0: 
            self.high = stack[top] 
            top = top - 1
            self.low = stack[top] 
            top = top - 1
            p = self.partition(array) 
            if p - 1 > self.low: 
                top = top + 1
                stack[top] = self.low 
                top = top + 1
                stack[top] = p - 1
            if p + 1 < self.high: 
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = self.high

image = CommonColorCategory("Images/Dope_Building.jpg").simplifyImage(4)
image.show()