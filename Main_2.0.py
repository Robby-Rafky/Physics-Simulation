from math import *
from visualgraph import *
from visual.graph import *
import wx
from ProjectileMaths import *

app = wx.App(False)
screenX, screenY = wx.GetDisplaySize()  # returns tuple with x and y of monitor resolution
screenX = int(screenX) * 0.001  # scales value down to be a multiplier of a 1000*1000 grid
screenY = int(screenY) * 0.001  # scales value down to be a multiplier of a 1000*1000 grid


###INITIAL SCREEN#################################################################
def startUp():  # The startup window, creation of the basic panel with check boxes
    # values and widgets have to global to communicate with other functions
    global windState, restitutionState, windCheckBox, InitialWindow, startProgram, restitutionCheckBox, initialVelocityValue, initialAngleValue, accuracyValue
    InitialWindow = wx.window(width=550, height=190, fullscreen=False, menus=False, title='Projectile Motion',
                           style=wx.CAPTION | wx.CLOSE_BOX | wx.STAY_ON_TOP)  # window creation
    startProgram = wx.Button(InitialWindow.panel, label="Start", pos=(450, 130))  # start button creation
    startProgram.Bind(wx.EVT_BUTTON, startProgramAttempt)  # start button being given a function when pressed
    windCheckBox = wx.CheckBox(InitialWindow.panel, label="Wind", pos=(20, 35),
                               size=(50, 20))  # check box for wind created
    windCheckBox.Bind(wx.EVT_CHECKBOX, windCheck)  # check box given a function when checked
    restitutionCheckBox = wx.CheckBox(InitialWindow.panel, label="Bounce", pos=(20, 60),
                                      size=(70, 20))  # check box for bounce created
    restitutionCheckBox.Bind(wx.EVT_CHECKBOX, restitutionCheck)  # check box given a function when checked
    initialVelocityText = wx.StaticText(InitialWindow.panel, pos=(90, 92), label="Initial velocity :")
    initialVelocityValue = wx.TextCtrl(InitialWindow.panel, pos=(172, 90), size=(50, 20),
                                       style=wx.TE_RIGHT)  # input field for initial velocity
    initialVelocityUnitText = wx.StaticText(InitialWindow.panel, pos=(224, 92), label="m/s")
    initialAngleText = wx.StaticText(InitialWindow.panel, pos=(270, 92), label="Initial Angle :")
    initialAngleValue = wx.TextCtrl(InitialWindow.panel, pos=(341, 90), size=(50, 20),
                                    style=wx.TE_RIGHT)  # input field for initial angle
    initialAngleUnitText = wx.StaticText(InitialWindow.panel, pos=(396, 92), label="degrees")
    angleInfoText = wx.StaticText(InitialWindow.panel, pos=(20, 10),
                                  label="Note : Angles should be measured from the horizontal going anit-clockwise.")
    accuracyText = wx.StaticText(InitialWindow.panel, pos=(10, 122), label="Output precision :")
    accuracyValue = wx.TextCtrl(InitialWindow.panel, pos=(111, 120), size=(50, 20), style=wx.TE_RIGHT,
                                value="4")  # input field for precision
    accuracyUnitText = wx.StaticText(InitialWindow.panel, pos=(170, 122),
                                     label="Decimal Places - (higher values lowers performance)")
    windState = False  # default states to check whether or not wind will be activated
    restitutionState = False  # default states to check whether or not bounce will be activated


def windCheck(evt):  # Event triggers when the wind checkbox is updated (spamming this crashes the program)
    global windState, windForceText, windForceValue, windForceUnitText, windAngleText, windAngleValue, windAngleUnitText, massText, massValue, massUnitText
    windState = windCheckBox.GetValue()  # sets the state to being false if unchecked and true if checked
    if windState:  # if windstate is true, create all the wind related input fields
        windForceText = wx.StaticText(InitialWindow.panel, pos=(90, 37), label="Wind Force :")
        windForceValue = wx.TextCtrl(InitialWindow.panel, pos=(160, 35), size=(50, 20), style=wx.TE_RIGHT)
        windForceUnitText = wx.StaticText(InitialWindow.panel, pos=(212, 37), label="N")
        windAngleText = wx.StaticText(InitialWindow.panel, pos=(355, 37), label="Wind Angle :")
        windAngleValue = wx.TextCtrl(InitialWindow.panel, pos=(425, 35), size=(50, 20), style=wx.TE_RIGHT)
        windAngleUnitText = wx.StaticText(InitialWindow.panel, pos=(477, 37), label="degrees")
        massText = wx.StaticText(InitialWindow.panel, pos=(240, 37), label="Mass :")
        massValue = wx.TextCtrl(InitialWindow.panel, pos=(275, 35), size=(50, 20), style=wx.TE_RIGHT)
        massUnitText = wx.StaticText(InitialWindow.panel, pos=(327, 37), label="kg")
    else:  # otherwise its not true, destroy all the input fields
        windForceText.Destroy()
        windForceValue.Destroy()
        windForceUnitText.Destroy()
        windAngleText.Destroy()
        windAngleValue.Destroy()
        windAngleUnitText.Destroy()
        massText.Destroy()
        massValue.Destroy()
        massUnitText.Destroy()


def restitutionCheck(evt):  # Event triggers when the bounce checkbox is updated (spamming this crashes the program)
    global restitutionState, bounceCountText, bounceCountValue, coefficientText, coefficientValue
    restitutionState = restitutionCheckBox.GetValue()  # sets the state to being false if unchecked and true if checked
    if restitutionState:  # if state is true, create all bounce related input fields
        bounceCountText = wx.StaticText(InitialWindow.panel, pos=(90, 62), label="Num of Bounces :")
        bounceCountValue = wx.TextCtrl(InitialWindow.panel, pos=(190, 60), size=(50, 20), style=wx.TE_RIGHT)
        coefficientText = wx.StaticText(InitialWindow.panel, pos=(260, 62), label="Coefficient of Restitution :")
        coefficientValue = wx.TextCtrl(InitialWindow.panel, pos=(405, 60), size=(50, 20), style=wx.TE_RIGHT)
    else:  # otherwise its not true, destroy all the input fields
        bounceCountText.Destroy()
        bounceCountValue.Destroy()
        coefficientText.Destroy()
        coefficientValue.Destroy()


def startProgramAttempt(evt):  # Event triggers on pressing the start button
    global vel0, theta0Deg, windAngle, windForce, mass, coRest, bounceCount, accuracyOutput
    initialsERR = False  # Initial error flags set to false
    windERR = False  # Initial error flags set to false
    restERR = False  # Initial error flags set to false
    try:  # attempts to convert values to the appropriate type
        vel0 = float(initialVelocityValue.GetValue())
        theta0Deg = float(initialAngleValue.GetValue())
        accuracyOutput = int(accuracyValue.GetValue())
    except:  # fails to convert to appropriate type, so instead of crashing, it sets intials error to true
        initialsERR = True
    if windState:  # only for wind box being checked
        try:  # attempts to convert values to the appropriate type
            windForce = float(windForceValue.GetValue())
            windAngle = float(windAngleValue.GetValue())
            mass = float(massValue.GetValue())
        except:  # fails to convert to appropriate type, so instead of crashing, it sets wind error to true
            windERR = True
    if restitutionState:  # only for the bounce box being checked
        try:  # attempts to convert values to the appropriate type
            coRest = float(coefficientValue.GetValue())
            bounceCount = float(bounceCountValue.GetValue())
        except:  # fails to convert to appropriate type, so instead of crashing, it sets bounce error to true
            restERR = True
    ERRlist = []  # creates list for error message creation
    # based on what errors were raised, it will create custom error to address issues
    if initialsERR:
        ERRlist.append("Initial Velocity, Angle or Precision")
    if windERR:
        ERRlist.append("Wind/Mass Values")
    if restERR:
        ERRlist.append("Restitution/Bounce Values")
    if initialsERR or windERR or restERR:
        ERRmessage = """Error with:
""" + """
""".join(ERRlist)
        ERRwindowInput = wx.MessageDialog(None, ERRmessage, "Error",
                                          style=wx.OK | wx.ICON_ERROR)  # creates the error window
        ERRwindowInput.ShowModal()  # to let it close when you click "ok"
    else:
        startMath(vel0, theta0Deg)  # otherwise if there is no errors, start the math


###MATHEMATICAL PROJECTILE FUNCTIONS##############################################
def startMath(vel0, theta0Deg):
    global projectileBall
    try:  # trying the calculation incase of non real errors
        projectileBall = Proj(accuracy=accuracyOutput)  # creates the projectile object
        projectileBall.setStartValue(vel0=vel0,
                                     theta0Deg=theta0Deg)  # starts with setting the values to be the user input values
        if windState:  # conditional methods to run only when there are values for them
            projectileBall.windForceMod(windAngle=windAngle, windForce=windForce, mass=mass)
        if restitutionState:  # conditional methods to run only when there are values for them
            projectileBall.restitutionInitMod(bounceCount=bounceCount, restitution=coRest)
        calcInitMax()
        runMath()
        InitialWindow.delete()  # removes the initial window when all is calculated and complete
        afterStartScreen()  # sets up the mainwindow screen to be used
        MainWindow.visible = True  # makes the screen visible for user interaction
    except:  # if something went wrong during calculation, window won't dissapear and it throws an error message
        ERRwindowCalc = wx.MessageDialog(None, """Non-Real value obtained: 
Either wind would carry the projectile up forever. - lower the wind force and/or check wind angle value
Projectile rolls along the floor. - lower the amount of bounces and/or raise the coefficient of restitution""", "Error",
                                         style=wx.OK | wx.ICON_ERROR)
        ERRwindowCalc.ShowModal()  # allow user to click "ok" to close window


def calcInitMax():  # starts calculation setup for the main calculations
    projectileBall.calcMaxTime()
    projectileBall.storeFirstMax()
    while projectileBall.flightTime <= projectileBall.timeMax:
        projectileBall.calcVel()
        projectileBall.calcDist()
        projectileBall.setMax()
    projectileBall.resetTime()


def runMath():  # all the calculations and storing of calculations done here
    running = True  # condition for the loop to run
    while running:
        projectileBall.calcVel()
        projectileBall.calcDist()
        projectileBall.normaliseData()
        projectileBall.killTheLag()
        projectileBall.logData()
        if projectileBall.flightTime >= projectileBall.timeMax:  # first condition for ending the loop
            if projectileBall.bounceCount < projectileBall.bounceCountMax:  # if this condition isn't met, then loop ends instantly
                projectileBall.restitutionCalcMod()
                projectileBall.resetTime()
                projectileBall.calcMaxTime()
            else:
                running = False


###VISUAL PROJECTILE FUNCTIONS####################################################
def resetProjPos():  # here to allow me to reset the positions and text of everything when a loop is over
    ball.pos = projectileBall.visualBallPosLog[0]
    velArrow.pos = ball.pos
    velXArrow.pos = ball.pos
    velYArrow.pos = ball.pos
    velArrow.axis = (0, 0, 0)  # axis refers to the direction vector that gives the arrow its direction to point in.
    velXArrow.axis = (0, 0, 0)
    velYArrow.axis = (0, 0, 0)
    ProjScene.center = (ball.pos.x, 0, 0)  # sets the center of the scene to match the ball's current x value
    ProjScene.forward = (0, 0, -15)  # moves the camera to face the center of the scene at a distance
    if largeView:
        timeSlider.SetValue(0)
        velXText.text = "Horizontal Velocity"
        velYText.text = "Vertical Velocity"
        velXText.pos = projectileBall.posTextVelXLog[0]
        velYText.pos = projectileBall.posTextVelYLog[0]
        distXText.text = "Horizontal Distance"
        distYText.text = "Vertical Distance"
        distXText.pos = projectileBall.posTextDistXLog[0]
        distYText.pos = projectileBall.posTextDistYLog[0]


def timeSliderSim(evt):  # when the time slider is updated, this event is called
    value = timeSlider.GetValue()  # grabs the value from the slider
    # lists are read using the obtained value
    ball.pos = projectileBall.visualBallPosLog[value]
    velArrow.pos = ball.pos
    velXArrow.pos = ball.pos
    velYArrow.pos = ball.pos
    velArrow.axis = projectileBall.visualArrowLog[value]
    velXArrow.axis = projectileBall.visualArrowXLog[value]
    velYArrow.axis = projectileBall.visualArrowYLog[value]
    ProjScene.center.x = ball.pos.x
    ProjScene.forward = (0, 0, -15)
    velXText.text = projectileBall.textVelXLog[value]
    velYText.text = projectileBall.textVelYLog[value]
    velYText.pos = projectileBall.posTextVelYLog[value]
    velXText.pos = projectileBall.posTextVelXLog[value]
    distXText.text = projectileBall.textDistXLog[value]
    distYText.text = projectileBall.textDistYLog[value]
    distYText.pos = projectileBall.posTextDistYLog[value]
    distXText.pos = projectileBall.posTextDistXLog[value]


def runSim(evt):
    value = int(0)
    if largeView:  # if statement outside the while loop for more speed during the loop
        while value < (len(projectileBall.normVelXLog)):  # stops when the whole position log for X is over
            rate(projectileBall.calcCount / projectileBall.initTimeMax)
            ball.pos = projectileBall.visualBallPosLog[value]
            velArrow.pos = ball.pos
            velXArrow.pos = ball.pos
            velYArrow.pos = ball.pos
            velArrow.axis = projectileBall.visualArrowLog[value]
            velXArrow.axis = projectileBall.visualArrowXLog[value]
            velYArrow.axis = projectileBall.visualArrowYLog[value]
            ProjScene.center.x = ball.pos.x
            ProjScene.forward = (0, 0, -15)
            velXText.text = projectileBall.textVelXLog[value]
            velYText.text = projectileBall.textVelYLog[value]
            velYText.pos = projectileBall.posTextVelYLog[value]
            velXText.pos = projectileBall.posTextVelXLog[value]
            distXText.text = projectileBall.textDistXLog[value]
            distYText.text = projectileBall.textDistYLog[value]
            distYText.pos = projectileBall.posTextDistYLog[value]
            distXText.pos = projectileBall.posTextDistXLog[value]
            timeSlider.SetValue(value)
            value += 1
    else:  # if statement outside the while loop for more speed during the loop
        while value < (len(projectileBall.normVelXLog)):
            rate(projectileBall.calcCount / projectileBall.initTimeMax)
            ball.pos = projectileBall.visualBallPosLog[value]
            velArrow.pos = ball.pos
            velXArrow.pos = ball.pos
            velYArrow.pos = ball.pos
            velArrow.axis = projectileBall.visualArrowLog[value]
            velXArrow.axis = projectileBall.visualArrowXLog[value]
            velYArrow.axis = projectileBall.visualArrowYLog[value]
            ProjScene.center.x = ball.pos.x
            ProjScene.forward = (0, 0, -15)
            value += 1
    resetProjPos()


def createVisual():  # creates the objects for visual scene to use
    global ball, velArrow, velXArrow, velYArrow
    ball = sphere(radius=0.5, pos=(projectileBall.visualBallPosLog[0]), axis=(1, 0, 0), color=color.black,
                  make_trail=True, trail_type="points", retain=5000, interval=15)
    velArrow = arrow(pos=(ball.pos), axis=(0, 0, 0), shaftwidth=0.3, color=(0.5, 0.5, 0.5))
    velXArrow = arrow(pos=(ball.pos), axis=(0, 0, 0), shaftwidth=0.3, color=color.green)
    velYArrow = arrow(pos=(ball.pos), axis=(0, 0, 0), shaftwidth=0.3, color=color.green)


###WINDOW CONTROLS################################################################
def switchToSmallVis(evt):  # deletes the large scene, creates a smaller scene without slider - for lower end machines.
    global ProjScene, switchLargeButton, largeView
    largeView = False
    timeSlider.Destroy()
    ProjScene.delete()
    ProjScene = display(window=MainWindow, x=10 * screenX, y=10 * screenY, width=600 * screenX, height=500 * screenY,
                        center=(0, 0, 0), background=(0.94, 0.94, 0.94), autoscale=False)
    createVisual()
    switchLargeButton = wx.Button(MainWindow.panel, label="Switch To Large View", pos=(10 * screenX, 940 * screenY))
    switchLargeButton.Bind(wx.EVT_BUTTON, switchToLargeVis)
    switchSmallButton.Destroy()


def switchToLargeVis(evt):  # creates a larger display, deletes the old small one and creates the slider
    global ProjScene, switchSmallButton, timeSlider, largeView, velXText, velYText, distXText, distYText
    largeView = True
    ProjScene.delete()
    ProjScene = display(window=MainWindow, x=10 * screenX, y=0, width=1000 * screenX, height=900 * screenY,
                        center=(0, 0, 0), background=(0.94, 0.94, 0.94), autoscale=False)
    createVisual()
    velXText = label(pos=(projectileBall.posTextVelXLog[0]), text='Horizontal Velocity', color=color.black, opacity=1)
    velYText = label(pos=(projectileBall.posTextVelYLog[0]), text='Vertical Velocity', color=color.black, opacity=1)
    distXText = label(pos=(projectileBall.posTextDistXLog[0]), text='Horizontal Distance', color=color.black, opacity=1)
    distYText = label(pos=(projectileBall.posTextDistYLog[0]), text='Vertical Distance', color=color.black, opacity=1)
    timeSlider = wx.Slider(MainWindow.panel, pos=(10 * screenX, 900 * screenY), size=(980 * screenX, 30 * screenY),
                           minValue=0, maxValue=((len(projectileBall.normVelXLog)) - 1))
    timeSlider.Bind(wx.EVT_SCROLL, timeSliderSim)
    switchSmallButton = wx.Button(MainWindow.panel, label="Switch To Small View", pos=(10 * screenX, 940 * screenY))
    switchSmallButton.Bind(wx.EVT_BUTTON, switchToSmallVis)
    switchLargeButton.Destroy()


def afterStartScreen():  # To lock the user out of crashing the program
    global switchLargeButton, runSimButton, largeView
    createVisual()
    largeView = False  # sets the current state of the program visuals
    runSimButton = wx.Button(MainWindow.panel, label="Run", pos=(110 * screenX, 940 * screenY))
    runSimButton.Bind(wx.EVT_BUTTON, runSim)
    switchLargeButton = wx.Button(MainWindow.panel, label="Switch To Large View", pos=(10 * screenX, 940 * screenY))
    switchLargeButton.Bind(wx.EVT_BUTTON, switchToLargeVis)


###THE REAL DEAL##################################################################
startUp()  # starts up initialisation of initial window for inputs
# Main window cannot be made inside of a function when using integrated Vpython displays, its made out here and hidden from view - No controls given to the user until maths is done
MainWindow = window(width=1000 * screenX, height=1000 * screenY, fullscreen=True, menus=False,
                    title='Projectile Motion', style=wx.CAPTION | wx.CLOSE_BOX)
# ProjScene starts off in small mode, with an option to go large
ProjScene = display(window=MainWindow, x=10 * screenX, y=10 * screenY, width=600 * screenX, height=500 * screenY,
                    center=(0, 0, 0), background=(0.94, 0.94, 0.94), autoscale=False)
MainWindow.visible = False  # hides main window
initialVelocityValue.SetFocus()  # sets intitials text box as the focus of your cursor
