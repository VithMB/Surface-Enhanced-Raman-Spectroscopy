# # # General comments

# # The section <Settings> contains all the parameters to be chosen.
# <setmag> chosen the magnification
# First argument of <setpatinfo> is Z depth in [um], second is material. 
# <D> is spacing border-border, and <L> is diameter, <Pitch> is center-center.
# <QuantityCircles> defines the numer of circles to be drawn in each direction on the screen.
# <CircleOffset> is the position of the fist circle on the screen.
# <StageMoves> is the number of stage movements, not counting the first drawn pattern.
# Limit of the Beam Shift is 50um radially from the center. 

# # About numerical operations:
# Parentesis are importante even in multiplication.
# Avoid using division </>, the program struggles with it in some cases.
# Or use </> with <.0> at the end of the number to force float number division.

# # Notes about loops (optional):
# The function <getstagepos> has <x>,<y> as default variables.
# Calling <getstagepos> updates these variables with current stage position.
# The stage actually moves in [mm], the <*0.001> is unit conversion.

#####################################
############## Settings #############
#####################################
setmag 5000   
setpatinfo 0.09, si     
setparallelmode 0              
                                    
D = 0.450 
L = 0.350                                 

QuantityCirclesX = 10
QuantityCirclesY = 4

SleeptimeMs = 0

StageMovesX = 3
StageMovesY = 2

#####################################
######## Auxiliary Variables ########
#####################################
Pitch = L + D   
CircleDiameter = L

CircleOffsetX = -(Pitch * (QuantityCirclesX - 1))/2.0
CircleOffsetY = +(Pitch * (QuantityCirclesY - 1))/2.0

StageDeltaX = Pitch * QuantityCirclesX * 0.001
StageDeltaY = Pitch * QuantityCirclesY * 0.001
StageDeltaY = StageDeltaY * 1.05
getstagepos
OriginX = x
OriginY = y

getstagepos
OriginX = x

#####################################
########### Draw Pattern ############
#####################################
clear
CountCirclesX = 0
CountCirclesY = 0

DrawingLoop:
    CircleX = CircleOffsetX + (Pitch * CountCirclesX)
    CircleY = CircleOffsetY - (Pitch * CountCirclesY)

    circle CircleX, CircleY, 0, CircleDiameter                

    CountCirclesX = CountCirclesX + 1
    if (CountCirclesX < QuantityCirclesX) goto DrawingLoop
    CountCirclesX = 0

    CountCirclesY = CountCirclesY + 1
    if (CountCirclesY < QuantityCirclesY) goto DrawingLoop

sleep SleeptimeMs

<<<<<<< HEAD:AutoScript FIB/2026-05-15_Vitor_script_circulo.psc
#####################################
############ Stage Loop Y ###########
#####################################
CountStageY = 0

StageLoopY:

    #####################################
    ############ Stage Loop X ###########
    #####################################
    CountStageX = 0

    StageLoopX:
=======
################################# 
########## Beam & Mill ##########
#################################
setbeamshift BeamOffsetX,BeamOffsetY

CountBeamShiftX = 0
CountBeamShiftY = 0
CountStageX = 0
CountStageY = 0

BeamShiftLoop: 
    mill

    getbeamshift 
    CurrentBeamX = xbeam 
    CurrentBeamY = ybeam

    BeamX = CurrentBeamX - BeamDeltaX
    setbeamshift BeamX, CurrentBeamY

    CountBeamShiftX = CountBeamShiftX + 1
    if (CountBeamShiftX <= BeamShiftsX) goto BeamShiftLoop   
    CountBeamShiftX = 0
    
    BeamY = CurrentBeamY + BeamDeltaY
    setbeamshift BeamOffsetX, BeamY
>>>>>>> 235dc7a453975a8cf541f92eb5da4a55d16a6fb2:AutoScript FIB/2026-04-29_Vitor_script_circulo.psc


<<<<<<< HEAD:AutoScript FIB/2026-05-15_Vitor_script_circulo.psc
=======
#####################################
############### Stage ###############
#####################################
getstagepos
CurrentX = x 
CurrentY = y

StageX = CurrentX + StageDeltaX  
stagemove x, StageX
>>>>>>> 235dc7a453975a8cf541f92eb5da4a55d16a6fb2:AutoScript FIB/2026-04-29_Vitor_script_circulo.psc

        #####################################
        ############### Mill ################
        #####################################
        mill

<<<<<<< HEAD:AutoScript FIB/2026-05-15_Vitor_script_circulo.psc
        #####################################
        ########## Advance Stage X ##########
        #####################################
        CountStageX = CountStageX + 1
        if (CountStageX > StageMovesX) goto EndStageLoopX
=======
StageY = CurrentY + StageDeltaY  
stagemove xy, OriginX, StageY
>>>>>>> 235dc7a453975a8cf541f92eb5da4a55d16a6fb2:AutoScript FIB/2026-04-29_Vitor_script_circulo.psc

        getstagepos
        CurrentX = x
        StageX = CurrentX + StageDeltaX
        stagemove x, StageX
        goto StageLoopX

    EndStageLoopX:

    #####################################
    ########## Advance Stage Y ##########
    #####################################
    CountStageY = CountStageY + 1
    if (CountStageY > StageMovesY) goto EndStageLoopY

    getstagepos
    CurrentY = y
    StageY = CurrentY - StageDeltaY
    stagemove xy, OriginX, StageY  

    goto StageLoopY 

EndStageLoopY:

#####################################
########### Finalization ############
#####################################
end:
clear
result = 1
