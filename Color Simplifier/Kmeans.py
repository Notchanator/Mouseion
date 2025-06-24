from PIL import Image
import numpy as np
import sklearn.cluster
#import matplotlib.pyplot as plt

# 4 Channels means CMYK
# 3 Channels means RGB

def getClusterColors(clusters, pixels):
    clusterColors = []
    num_colors = clusters.max()
    n = 0
    while n <= num_colors:
        cluster = pixels[clusters == n]
        clusterColors.append(tuple(cluster.mean(axis=0).astype(int)))
        n += 1
    return clusterColors

# def elbowGraph(imagePath):
#     im = Image.open(imagePath)
#     pixels = np.asarray(im).reshape(im.size[0]*im.size[1], 3, order="F")
#     SSE = []
#     for num in range(2,14):
#         SSE.append(sklearn.cluster.KMeans(num).fit(pixels).inertia_)
#         print("Done : ", num)
#     k = [i*100 for i in np.diff(SSE,2)].index(min([i*100 for i in np.diff(SSE,2)]))
#     fig, ax = plt.subplots()
#     ax.plot(range(1, len(SSE)+1), SSE)
#     ax.axvline(k, ls='--', color="red", label="k = "+str(k))
#     ax.set(title='David : Elbow Graph', xlabel='Number of clusters', ylabel="SSE")
#     ax.legend()
#     ax.grid(True)
#     plt.show()
    
    

def main(imagePath, numColors = 4, stdout=False):
    im = Image.open(imagePath)
    allPixels = im.load()
    pixels = np.asarray(im).reshape(im.size[0]*im.size[1], 3, order="F")
    if stdout:
        print("Pixels Read In")
    clusters = sklearn.cluster.KMeans(numColors).fit(pixels).labels_
    if stdout:
        print("Clusters Made")
    clusterColors = getClusterColors(clusters, pixels)
    if stdout:
        print("Assigning Clusters")
    for row in range(im.size[0]):
        for col in range(im.size[1]):
            allPixels[row, col] = clusterColors[clusters[row*im.size[1] + col]]
    #im.save(str("Image Grid/Agglomerative/Pirates/pirates_" + str(clusters.max()) + ".png"), format="png")
    im.show()

for n in range(2, 5):
    main("Images/River.jpeg", n)
    print("Done : ", n)

