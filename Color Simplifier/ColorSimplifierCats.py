import numpy as np
from PIL import Image
from math import sqrt


def simplify(listy):
    simplified = []
    for pixels in listy:
        if pixels[0] > 6:
            simplified.append(pixels)
    # sorted_list = bubble_sort(simplified)
    return simplified


def most_pixels(listy, nums, mult=1):
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
    for pixel in listy:
        closest_indx = closest_color(pixel[1])
        if Top[closest_indx] is None:
            Top[closest_indx] = pixel
            n += 1
        if n == nums:
            return Top
    return Top
    

def closest_color(pixel):
    Colors = [(255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (128,128,128), (0,128,0), (0,0,128), (255,165,0), (139,69,19)]
    n = 0
    closest = None
    while n < 13:
        dist = sqrt((pixel[0] - Colors[n][0])**2 + (pixel[1] - Colors[n][1])**2 + (pixel[2] - Colors[n][2])**2)
        if closest is None or closest[0] > dist:
            closest = (dist, n)
        n += 1
    return closest[1]

def closest_pixel(top_n, pixel):
    distances = [None] * len(top_n)
    for index in range(len(top_n)):
        distances[index] = sqrt((top_n[index][0] - pixel[0])**2 + (top_n[index][1]- pixel[1])**2 + (top_n[index][2] - pixel[2]) **2)
    closest_indx = distances.index(min(distances))
    return top_n[closest_indx]

def partition(arr, l, h): 
    i = ( l - 1 ) 
    x = arr[h][0] 
    for j in range(l, h): 
        if   arr[j][0] >= x: 
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i] 
    arr[i + 1], arr[h] = arr[h], arr[i + 1] 
    return (i + 1) 
  
def quickSort(arr, l, h): 
    size = h - l + 1
    stack = [0] * (size) 
    top = -1
    top = top + 1
    stack[top] = l 
    top = top + 1
    stack[top] = h 
    while top >= 0: 
        h = stack[top] 
        top = top - 1
        l = stack[top] 
        top = top - 1
        p = partition(arr, l, h) 
        if p-1 > l: 
            top = top + 1
            stack[top] = l 
            top = top + 1
            stack[top] = p - 1
        if p + 1 < h: 
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h       



def main(image_path = None, num_colors=4):
    im = Image.open(image_path)
    top_pixels = []
    all_pixels = im.load()
    #print( "Running")
    pixels = im.getcolors(im.size[0]*im.size[1])
    #print("Simplifying Colors")
    sim_pixels = simplify(pixels)
    #print("Sorting Colors")
    quickSort(sim_pixels, 0 , len(sim_pixels) - 1)
    #print("Finding Top Colors")
    top_pixels_count = most_pixels(sim_pixels, num_colors)
    for pixel in top_pixels_count:
        if pixel is not None:
            top_pixels.append(pixel[1])
    #print("Converting Colors")
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            all_pixels[i,j] = closest_pixel(top_pixels, all_pixels[i,j])
    #print("Done")
    im.show()
    #im.save(str("Image Grid/Category/Bishops/bishops_" + str(num_colors) + ".png"), format="png")

for n in range(2,8):
    main("Images/HorseTooth.jpeg", num_colors=n)
    print("Done :", n)