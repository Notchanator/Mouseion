import numpy as np
from PIL import Image, ImageCms
from math import sqrt, atan2, sin, degrees, radians, pi, cos, exp
import time


class Pixel:

    def __init__(self, color, rgb, x, y):
        self.color = (int(color[0]), int(color[1]), int(color[2]))
        self.rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        self.coord = (x, y)
        self.cluster = None
        self.visited = False
        self.leftDist = None
        self.upDist = None
        self.rightDist = None
        self.downDist = None

    def __str__(self):
        return f"{self.color} at {self.coord}. Belongs to {self.cluster} and {self.visited}. L{self.leftDist}, R{self.rightDist}, U{self.upDist}, D{self.downDist}"

    def __repr__(self):
        return f"{self.color} at {self.coord}. Belongs to {self.cluster} and {self.visited}. L{self.leftDist}, R{self.rightDist}, U{self.upDist}, D{self.downDist}"

    def setCluster(self, cluster):
        self.cluster = cluster
    
    def visit(self):
        self.visited = True
    
    def setLeftDist(self, other):
        self.leftDist = self.getDeltaEBetween(other)

    def setRightDist(self, other):
        self.rightDist = self.getDeltaEBetween(other)

    def setUpDist(self, other):
        self.upDist = self.getDeltaEBetween(other)

    def setDownDist(self, other):
        self.downDist = self.getDeltaEBetween(other)

    def getDistanceBetween(self, other):
        return round(sqrt((self.color[0] - other.color[0])**2 + (self.color[1] - other.color[1])**2 + (self.color[2] - other.color[2])**2), 4)

    def getDeltaLowerH(self, hPrimes, cPrimes):
        if cPrimes[0]*cPrimes[1] == 0:
            return 0
        elif abs(hPrimes[1]-hPrimes[0]) <= 180:
            return hPrimes[1]-hPrimes[0]
        elif (hPrimes[1]-hPrimes[0]) > 180:
            return hPrimes[1]-hPrimes[0]-360
        else:
            return hPrimes[1]-hPrimes[0]+360

    def gethBar(self, hPrimes, cPrimes):
        if cPrimes[0]*cPrimes[1] == 0:
            return hPrimes[0]+hPrimes[1]
        elif abs(hPrimes[0]-hPrimes[1]) <= 180:
            return (hPrimes[0]+hPrimes[1])/2
        elif hPrimes[0]+hPrimes[1] < 360:
            return (hPrimes[0]+hPrimes[1]+360)/2
        else:
            return (hPrimes[0]+hPrimes[1]-360)/2

    def getDeltaEBetween(self, other):
        deltaL = other.color[0] - self.color[0]
        cStarAB = (sqrt(self.color[1]**2+self.color[2]**2)+sqrt(other.color[1]**2+other.color[2]**2))/2
        G = .5*(1 - (cStarAB**7 / (cStarAB**7 + 25**7)))
        aPrimes = [((1+G)*self.color[1]),((1+G)*other.color[1])]
        cPrimes = [sqrt(aPrimes[0]**2 + self.color[2]**2), sqrt(aPrimes[1]**2 + other.color[2]**2)]
        deltaC = cPrimes[1] - cPrimes[0]
        hPrimes = [degrees(atan2(self.color[2], aPrimes[0])+2*pi)%360, degrees(atan2(other.color[2], aPrimes[1])+2*pi)%360]
        hDelta = self.getDeltaLowerH(hPrimes, cPrimes)
        deltaH = 2*sqrt(cPrimes[0]*cPrimes[1])*sin(radians(hDelta/2))
        hBar = self.gethBar(hPrimes, cPrimes)
        T = 1-.17*cos(radians(hBar-30))+.24*cos(radians(2*hBar))+.32*cos(radians(3*hBar+6))-.2*cos(radians(4*hBar-63))
        lBar = (self.color[0] + other.color[0])/2
        cBar = (cPrimes[0] + cPrimes[1])/2
        SL = 1 + ((.015*(lBar-50)**2)/(sqrt(20+(lBar-50)**2)))
        SC = 1 + .045*cBar
        SH = 1 + .015*cBar*T
        RT = -sin(radians(60*exp(-1*((hBar-275)/25)**2))) * (2*sqrt((cBar**7)/(25**7+cBar**7)))
        kL, kC, kH = 1, 1, 1
        return round(sqrt((deltaL/(kL*SL))**2 + (deltaC/(kC*SC))**2 + (deltaH/(kH*SH))**2 + (RT*deltaC*deltaH)/(kC*SC*kH*SH)),4)

def calculateDistances(pixels):
    # Adds distance between all neighbors
    # Can be done more efficiently through dynamic programming
    # Since there every distance is calculated twice
    for col in range(len(pixels)):
        for row in range(len(pixels[col])):
            if col - 1 >= 0:
                pixels[col][row].setLeftDist(pixels[col-1][row])
            if col + 1 < len(pixels):
                pixels[col][row].setRightDist(pixels[col+1][row])
            if row - 1 >= 0:
                pixels[col][row].setUpDist(pixels[col][row-1])
            if row + 1 < len(pixels[col]):
                pixels[col][row].setDownDist(pixels[col][row+1])
    return pixels

def calculateMeanSDs(pixels):
    listy = []
    for col in range(len(pixels)):
        for row in range(len(pixels[col])):
            if pixels[col][row].rightDist is not None:
                listy.append(pixels[col][row].rightDist)
            if pixels[col][row].downDist is not None:
                listy.append(pixels[col][row].downDist)
    return listy

def createCloud(pixels, col, row, cluster, threshold):
    cloud = []
    queue = [pixels[col][row]]
    while len(queue) > 0:
        pix = queue.pop(0)
        if pix.visited:
            continue
        col = pix.coord[0]
        row = pix.coord[1]
        pix.visit()
        pix.setCluster(cluster)
        cloud.append(pix.rgb)
        # For all edges
        if col > 0 and not pixels[col-1][row].visited and pix.leftDist <= threshold:
            queue.append(pixels[col-1][row])
        if col < len(pixels)-1 and not pixels[col+1][row].visited and pix.rightDist <= threshold:
            queue.append(pixels[col+1][row])
        if row > 0 and not pixels[col][row-1].visited and pix.upDist <= threshold:
            queue.append(pixels[col][row-1])
        if row < len(pixels[col])-1 and not pixels[col][row+1].visited and pix.downDist <= threshold:
            queue.append(pixels[col][row+1])
    return (int(sum(col[0] for col in cloud)/len(cloud)), int(sum(col[1] for col in cloud)/len(cloud)), int(sum(col[2] for col in cloud)/len(cloud)))


def main(path):
    tnull = time.time()
    im = Image.open(path)

    #Covert RGB to CIELAB 
    srgbProfile = ImageCms.createProfile("sRGB")
    labProfile  = ImageCms.createProfile("LAB")
    rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgbProfile, labProfile, "RGB", "LAB")
    lab = ImageCms.applyTransform(im, rgb2lab)

    allPixels = im.load()
    openedImage = np.asarray(im)
    openedImageLAB = np.asarray(lab)
    t0 = time.time()
    print("Opening and Converting Image took ", t0-tnull)

    pixels = [[None for i in range(openedImageLAB.shape[0])] for j in range(openedImageLAB.shape[1])]
    for col in range(len(pixels)):
        for row in range(len(pixels[col])):
            pixels[col][row] = Pixel(openedImageLAB[row][col], openedImage[row][col], col, row)
    t1 = time.time()
    print("Creating Instance Table took ", t1-t0)

    pixels = calculateDistances(pixels)
    t2 = time.time()
    print("Calculating Distances took ", t2-t1)

    listy = calculateMeanSDs(pixels)
    t3 = time.time()

    sd = np.array(listy).std()
    mean = np.array(listy).mean()
    print(f"Mean : {mean} || SD : {sd}")
    print("Calculating metrics took ", t3-t2)

    cloud = []
    cluster = 0
    for row in range(len(pixels[0])):
        for col in range(len(pixels)):
            if not pixels[col][row].visited:
                cloud.append(createCloud(pixels, col, row, cluster, mean))
                cluster += 1
    print("Num of Clusters: ", cluster+1)
    t4 = time.time()
    print("Creating Clusters took ", t4-t3)

    for col in range(len(pixels)):
        for row in range(len(pixels[col])):
            allPixels[col, row] = cloud[pixels[col][row].cluster]

    im.show()

main("Images/Pirates.JPG")

