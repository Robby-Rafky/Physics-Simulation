from visual import vector
from math import *
#Simple Projectile Motion
#ProjMotion w/ Wind Force
#ProjMotion w/ bounce
#math banter
def rndPlease(num, accuracy):
    return str(round(float(num), accuracy))

 #The more you know
    #velXCurrent = Current horizontal velocity
    #velYCurrent = Current vertical velocity
    #flightTime = Current flight time
    #distX = Current total horizontal displacement
    #distY = Current total vertical displacement
    #velNet = Current resultant velocity
    #theta = Current angle
    #vel0 = Initial velocity
    #distXMax = Maximum distance
    #distYMax = Maximum height
    #timeMax = Total flight time
    #theta0Deg = initial angle (degrees)
    #theta0 = initial angle (degrees)
    #velX0 = initial horizontal
    #velY0 = initial vertical
    #restitution = Coefficient of restitution
    #norm = prefix on a variable that states visual modified
    #bounceCount = number of bounces
    #accuracy = number of decimal places that the program outputs to user
    #calcCount = number of calculations done for the first bounce, scaled by number of bounces.
    #totalAccY = total acceleration vertically
    #totalAccX = total acceleration horizontally
    #windAccX = total horizontal acceleration due to wind
    #windAccY = total vertical acceleration due to wind
    #initTimeMax = Max time for first bounce

class Proj:
    g = 9.81

###INITIALISATION#################################################################

    def __init__(self, accuracy):#creating a bunch of lists to be written to later
        self.calcCount = float("700.0")
        self.accuracy = int(accuracy)
        self.velXLog = []
        self.velYLog = []
        self.distXLog = []
        self.distYLog = []
        self.flightTimeLog = []
        self.normVelXLog = []
        self.normVelYLog = []
        self.normDistXLog = []
        self.normDistYLog = []
        self.bounceCountLog = []
        self.visualBallPosLog = []
        self.visualArrowLog = []
        self.visualArrowXLog = []
        self.visualArrowYLog = []
        self.textVelXLog = []
        self.textVelYLog = []
        self.posTextVelYLog = []
        self.posTextVelXLog = []
        self.posTextDistYLog = []
        self.posTextDistXLog = []
        self.textDistYLog = []
        self.textDistXLog = []
        
    def setStartValue(self, vel0, theta0Deg):#sets initial values for calculating to begin
        self.theta0 = radians(float(theta0Deg))#the maths module does its trig calculations in radians so entered value is converted initially
        self.vel0 = float(vel0)
        self.vel = float(vel0)
        self.velX0 = self.vel0*cos(self.theta0)#calculating the horizontal component of velocity
        self.velY0 = self.vel0*sin(self.theta0)#calculating the vertical component of velocity
        self.velX = self.velX0#setting this a new variable so that we have a unchanged copy of the initial
        self.velY = self.velY0#setting this a new variable so that we have a unchanged copy of the initial
        self.windAccX = float(0)
        self.windAccY = float(0)
        self.flightTime = float(0)
        self.distXMax = float(0)
        self.distYMax = float(0)
        self.bounceCount = int(0)
        self.bounceCountMax = int(0)
        self.sumDistX = float(0)
        self.sumFlightTime = float(0)
        self.theta = self.theta0#setting this a new variable so that we have a unchanged copy of the initial
        
    def resetTime(self):#in its own method so its clear to me when time is reset
        self.flightTime = float(0)

###WIND DLC####################################################################### 

    def windForceMod(self, windAngle, windForce, mass):#wind angle from horizontal, going clockwise (in degrees),mass in kg, windForce =FORCE EXERTED on proj
        self.windAngle = radians(float(windAngle))#convert to radians for maths module
        self.mass = float(mass)
        self.windAcc = (float(windForce))/(float(self.mass))#acceleration = force / mass 
        self.windAccX = self.windAcc*cos(self.windAngle)#componenets of acceleration
        self.windAccY = self.windAcc*sin(self.windAngle)#componenets of acceleration

###RESTITUTION DLC################################################################

    def restitutionInitMod(self, bounceCount, restitution):#sets initial values for bounces
        self.bounceCountMax = int(bounceCount)
        self.restitution = float(restitution)

    def restitutionCalcMod(self):
        self.velX = self.velXCurrent#sets new launch value as the current
        self.beforeSpeed = self.velYCurrent#sets before value as the current
        self.afterSpeed = (abs(self.beforeSpeed))*self.restitution#speed of approach*coefficient of resitution
        self.bounceAngle = atan(self.afterSpeed/(abs(self.velX)))#using trig to find the new launch angle
        self.velY = self.afterSpeed#sets new launch value as the calculated value
        self.theta = self.bounceAngle#setting initial angle for new launch
        self.bounceCount += 1#now that is has completed one bounce, increment counter
        self.vel = (self.velX**2 + self.velY**2)**(0.5)#pythagoras to find resultant velocity from components
        self.sumDistX += self.distX#adds current distance traveled to the total distance traveled
        self.sumFlightTime += self.flightTime#adds current time to total time traveled
        
###GLOBAL DISTANCE, VELOCITY AND ACCELERATIONS####################################

    def calcMaxTime(self):
        self.totalAccX = self.windAccX#only wind effects the horizontal acceleration
        self.totalAccY = self.windAccY - self.g#gravity and wind accelerations
        self.timeMax = ((-2)*(self.vel)*(sin(self.theta)))/(self.totalAccY)#formula to obtain the total time to be taken for the current bounce

    def storeFirstMax(self):
        self.initTimeMax = self.timeMax

    def calcVel(self):#calculates the current velocities for a given time
        self.velYCurrent = self.velY + self.totalAccY*self.flightTime#vertical
        self.velXCurrent = self.velX + self.totalAccX*self.flightTime#horizontal

    def calcDist(self):#calculates distance for the given time
        self.distY = self.velY*self.flightTime + 0.5*(self.totalAccY)*(self.flightTime**2)#vertical
        self.distX = self.velX*self.flightTime + 0.5*(self.totalAccX)*(self.flightTime**2)#horizontal
        self.flightTime += self.initTimeMax/self.calcCount#increments time by a portion of the max time for that bounce

    def setMax(self):#sets maximums for normalisation later
        if self.distY > self.distYMax:
            self.distYMax = self.distY
        if self.distX > self.distXMax:
            self.distXMax = self.distX
            
###LOGGING AND NORMALISATIONS#####################################################

    def logData(self):#logs all the data for reading later
        self.velXLog.append(rndPlease(num = self.velXCurrent, accuracy = self.accuracy))#horizontal, and rounds to precision that user specifies
        self.velYLog.append(rndPlease(num = self.velYCurrent, accuracy = self.accuracy))#vertical, and rounds to precision that user specifies
        self.distXLog.append(rndPlease(num = (self.distX+self.sumDistX), accuracy = self.accuracy))#horizontal total saved distance plus the current distance
        self.distYLog.append(rndPlease(num = self.distY , accuracy = self.accuracy))#current height
        self.flightTimeLog.append(rndPlease(num = (self.flightTime+self.sumFlightTime), accuracy = self.accuracy))#total flight time and time of current bounce
        self.normDistXLog.append(self.normDistX)
        self.normDistYLog.append(self.normDistY)
        self.normVelXLog.append(self.normVelX)
        self.normVelYLog.append(self.normVelY)
        self.bounceCountLog.append(self.bounceCount)
        self.visualBallPosLog.append(self.visualBallPos)
        self.visualArrowLog.append(self.visualArrow)
        self.visualArrowXLog.append(self.visualArrowX)
        self.visualArrowYLog.append(self.visualArrowY)
        self.textVelXLog.append(self.textVelX)
        self.textVelYLog.append(self.textVelY)
        self.posTextVelYLog.append(self.posTextVelY)
        self.posTextVelXLog.append(self.posTextVelX)
        self.posTextDistYLog.append(self.posTextDistY)
        self.posTextDistXLog.append(self.posTextDistX)
        self.textDistYLog.append(self.textDistY)
        self.textDistXLog.append(self.textDistX)
        
    def normaliseData(self):#Normalisation used to fix the vertical height and extend the horizontal to fit screen better
        self.normDistX = ((self.distX+self.sumDistX)/self.distYMax)*10
        self.normDistY = (self.distY/self.distYMax)*10
        self.normVelX = (self.velXCurrent/self.velY0)*3
        self.normVelY = (self.velYCurrent/self.velY0)*3

    def killTheLag(self): #my way of fighting the lag, a bunch of inefficient processes - however alot of performance issues are dealt with here
        self.visualBallPos = vector((self.normDistX-5), (self.normDistY-2), 0)
        self.visualArrow = vector((self.normVelX+0.5), (self.normVelY+0.5), 0)
        self.visualArrowX = vector((self.normVelX+0.5), 0, 0)
        self.visualArrowY = vector(0, (self.normVelY+0.5), 0)
        self.textVelX = "Horizontal Velocity: "+str(rndPlease(num = self.velXCurrent, accuracy = self.accuracy))+" m/s" #this is over the top - i need speed
        self.textVelY = "Vertical Velocity: "+str(rndPlease(num = self.velYCurrent, accuracy = self.accuracy))+" m/s"
        self.posTextVelX = vector((self.normDistX-8), -4.5, 0)
        self.posTextVelY = vector((self.normDistX-2), -4.5, 0)
        self.textDistY = "Vertical Distance: "+str(rndPlease(num = self.distY, accuracy = self.accuracy))+" m"
        self.textDistX = "Horizontal Distance: "+str(rndPlease(num = (self.distX+self.sumDistX), accuracy = self.accuracy))+" m"
        self.posTextDistX = vector((self.normDistX-8), -6, 0)
        self.posTextDistY = vector((self.normDistX-2), -6, 0)


