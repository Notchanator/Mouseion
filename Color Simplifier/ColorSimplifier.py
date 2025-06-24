from PIL import Image
from math import sqrt
from sys import argv

def simplify(listy):
    simplified = []
    for pixels in listy:
        if pixels[0] > 6:
            simplified.append(pixels)
    return simplified

def most_pixels(listy, nums):
    top_n = [None] * nums
    sort_indx = 0
    top_indx = 0
    while top_n[nums - 1] is None:
        if top_n[top_indx] is None:
            top_n[top_indx] = listy[sort_indx]
            sort_indx += 1
            top_indx = 0
        else:
            if similar_colors(top_n[top_indx], listy[sort_indx]) == True:
                sort_indx += 1
            else:
                top_indx += 1
    return top_n


def similar_colors(pixel1, pixel2):
    dist = sqrt((pixel1[1][0] - pixel2[1][0]) ** 2 + (pixel1[1][1] - pixel2[1][1]) ** 2 + (pixel1[1][2] - pixel2[1][2]) ** 2)
    if dist <= 100:
        return True
    return False

def closest_pixel(top_n, pixel):
    distances = [None] * len(top_n)
    for indx in range(len(top_n)):
        distances[indx] = sqrt((top_n[indx][0] - pixel[0])**2 + (top_n[indx][1]- pixel[1])**2 + (top_n[indx][2] - pixel[2]) **2)
    closest_indx = distances.index(min(distances))
    return(top_n[closest_indx])

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
        p = partition( arr, l, h ) 
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

def main(image_path, num_colors = 4):
    im = Image.open(image_path)
    top_pixels = []
    all_pixels = im.load()
    pixels = im.getcolors(im.size[0]*im.size[1])
    sim_pixels = simplify(pixels)
    quickSort(sim_pixels, 0 , len(sim_pixels) - 1)
    top_pixels_count = most_pixels(sim_pixels, num_colors)
    for pixel in top_pixels_count:
        top_pixels.append(pixel[1])
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            all_pixels[i,j] = closest_pixel(top_pixels, all_pixels[i,j])
    im.show()
    #im.save(str("Image Grid/Oldest/Pirates Fam/fam_" + str(num_colors) + ".png"), format="png")
    print("Done : ", n)
    return im

#for n in range(2, 16):
main("Images/Dope_Building.jpg", 4)
    