import numpy as np
from PIL import Image

class CommonColorSimplifier:

    def __init__(self, file_url: str):
        self.image = Image.open(file_url)
        self.image_pixels = self.image.load()
        self.pixels = self.image.getcolors(self.image.size[0] * self.image.size[1])

    def simplify(self):
        simplified = []
        for pixels in self.pixels:
            if pixels[0] > 6:
                simplified.append(pixels)
        return simplified

    def mostPixels(self, pixels, nums):
        top_n = [None] * nums
        sort_indx = 0
        top_indx = 0
        while top_n[nums - 1] is None:
            if top_n[top_indx] is None:
                top_n[top_indx] = pixels[sort_indx][1]
                sort_indx += 1
                top_indx = 0
            else:
                if self.similarColors(top_n[top_indx], pixels[sort_indx][1]) == True:
                    sort_indx += 1
                else:
                    top_indx += 1
        return top_n


    def similarColors(self, pixel1, pixel2):
        dist = np.sqrt((pixel1[0] - pixel2[0]) ** 2 + (pixel1[1] - pixel2[1]) ** 2 + (pixel1[2] - pixel2[2]) ** 2)
        if dist <= 100:
            return True
        return False

    def closestPixel(self,top_n, pixel):
        distances = [None] * len(top_n)
        for indx in range(len(top_n)):
            distances[indx] = np.sqrt((top_n[indx][0] - pixel[0])**2 + (top_n[indx][1]- pixel[1])**2 + (top_n[indx][2] - pixel[2]) **2)
        closest_indx = distances.index(min(distances))
        return(top_n[closest_indx])
    
    def assignColors(self, top_pixels: list):
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


image = CommonColorSimplifier("Images/Dope_Building.jpg").simplifyImage(4)
image.show()
    