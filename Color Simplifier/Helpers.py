#Create a function to test if the file path is valid
from math import sqrt, atan2, sin, degrees, radians, pi, cos, exp
def valid_path(path):
    try:
        Image.open(path)
        return path
    except FileNotFoundError:
        return "FileNotFoundError"

def getDeltaLowerH(hPrimes, cPrimes):
    if cPrimes[0]*cPrimes[1] == 0:
        return 0
    elif abs(hPrimes[1]-hPrimes[0]) <= 180:
        return hPrimes[1]-hPrimes[0]
    elif (hPrimes[1]-hPrimes[0]) > 180:
        return hPrimes[1]-hPrimes[0]-360
    else:
        return hPrimes[1]-hPrimes[0]+360

def gethBar(hPrimes, cPrimes):
    if cPrimes[0]*cPrimes[1] == 0:
        return hPrimes[0]+hPrimes[1]
    elif abs(hPrimes[0]-hPrimes[1]) <= 180:
        return (hPrimes[0]+hPrimes[1])/2
    elif hPrimes[0]+hPrimes[1] < 360:
        return (hPrimes[0]+hPrimes[1]+360)/2
    else:
        return (hPrimes[0]+hPrimes[1]-360)/2

color1, color2 = (60.2574,-34.0099,36.2677), (60.4626,-34.1751,39.4387)
 
deltaL = color2[0] - color1[0]
cStarAB = (sqrt(color1[1]**2+color1[2]**2)+sqrt(color2[1]**2+color2[2]**2))/2
G = .5*(1 - (cStarAB**7 / (cStarAB**7 + 25**7)))
aPrimes = [((1+G)*color1[1]),((1+G)*color2[1])]
cPrimes = [sqrt(aPrimes[0]**2 + color1[2]**2), sqrt(aPrimes[1]**2 + color2[2]**2)]
deltaC = cPrimes[1] - cPrimes[0]
hPrimes = [degrees(atan2(color1[2], aPrimes[0])+2*pi)%360, degrees(atan2(color2[2], aPrimes[1])+2*pi)%360]
hDelta = getDeltaLowerH(hPrimes, cPrimes)
deltaH = 2*sqrt(cPrimes[0]*cPrimes[1])*sin(radians(hDelta/2))
hBar = gethBar(hPrimes, cPrimes)
T = 1-.17*cos(radians(hBar-30))+.24*cos(radians(2*hBar))+.32*cos(radians(3*hBar+6))-.2*cos(radians(4*hBar-63))
lBar = (color1[0] + color2[0])/2
cBar = (cPrimes[0] + cPrimes[1])/2
SL = 1 + ((.015*(lBar-50)**2)/(sqrt(20+(lBar-50)**2)))
SC = 1 + .045*cBar
SH = 1 + .015*cBar*T
RT = -sin(radians(60*exp(-1*((hBar-275)/25)**2))) * (2*sqrt((cBar**7)/(25**7+cBar**7)))
kL, kC, kH = 1, 1, 1
deltaE = round(sqrt((deltaL/(kL*SL))**2 + (deltaC/(kC*SC))**2 + (deltaH/(kH*SH))**2 + (RT*deltaC*deltaH)/(kC*SC*kH*SH)),4)

print("aPrimes : ", aPrimes)
print("cPrimes : ", cPrimes)
print("hPrimes : ", hPrimes)
print("hBar    : ", hBar)
print("deltaH  : ", deltaH)
print("G       : ", G)
print("T       : ", T)
print("SL      : ", SL)
print("SC      : ", SC)
print("SH      : ", SH)
print("RT      : ", RT)
print("deltaE  : ", deltaE)

