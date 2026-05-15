# # # General comments

# # The section <Settings> contains all the parameters to be chosen.
# <setmag> chosen the magnification
# First argument of <setpatinfo> is Z depth in [um], second is material. 
# <D> is spacing border-border, and <L> is diameter, <Pitch> is center-center.
# <QuantityCircles> defines the numer of circles to be drawn in each direction on the screen.
# <CircleOffset> is the position of the fist circle on the screen.
# <BeamShifts> is the number of beam shifts +1, for counting the first drawn pattern.
# <BeamOffset> is the position of the first beam shift.
# <StageMoves> is the number of stages movements +1, for counting the first drawn pattern.
# Limit of the Beam Shift is 50um radially from the center. 

# # About numerical operations:
# Parentesis are importante even in multiplication.
# Avoid using division </>, the program struggles with it in some cases.
# Or use </> with <.0> at the end of the number to force float number division.

# # Notes about loops (optional):
# The function <getstagepos> has <x>,<y> as default variables.
# Calling <getstagepos> updates these variables with current stage position.
# The stage actually moves in [mm],the <*0.001> is unit conversion.
# Beamshift is moving left -> right, up -> down.

#####################################
############## Settings #############
#####################################
setmag 5000   
setpatinfo 0.12, si     
setparallelmode 0              
                                    
D = 0.450 
L = 0.350                                 

QuantityCirclesX = 10
QuantityCirclesY = 10

SleeptimeMs = 0
 
BeamShiftsX = 0
BeamShiftsY = 0

BeamOffsetX = 0
BeamOffsetY = 0

StageMovesX = 0
StageMovesY = 0

#####################################
######## Auxiliary Variables ########
#####################################
Pitch = L + D   
CircleDiameter = L

CircleOffsetX = -(Pitch * (QuantityCirclesX - 1))/2.0
CircleOffsetY = +(Pitch * (QuantityCirclesY - 1))/2.0

BeamDeltaX = Pitch * QuantityCirclesX
BeamDeltaY = Pitch * QuantityCirclesY

StageDeltaX = (BeamDeltaX * (BeamShiftsX + 1) * 0.001)/2.0
StageDeltaY = (BeamDeltaY * (BeamShiftsY + 1) * 0.001)/2.0

getstagepos
OriginX = x

#####################################
############ Draw Pattern ###########
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

    CountCirclesY = CountCirclesY+1
    if (CountCirclesY < QuantityCirclesY) goto DrawingLoop 
    CountCirclesY = 0 

sleep SleeptimeMs

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

    CountBeamShiftY = CountBeamShiftY + 1
    if (CountBeamShiftY <= BeamShiftsY) goto BeamShiftLoop
    CountBeamShiftY = 0 

#####################################
############### Stage ###############
#####################################
getstagepos
CurrentX = x 
CurrentY = y

StageX = CurrentX + StageDeltaX  
stagemove x, StageX

CountStageX = CountStageX + 1
if (CountStageX <= StageMovesX) goto BeamShiftLoop
CountStageX = 0

StageY = CurrentY + StageDeltaY  
stagemove xy, OriginX, StageY

CountStageY = CountStageY + 1
if (CountStageY <= StageMovesY) goto BeamShiftLoop
CountStageY = 0

#####################################
########### Finalization ############
#####################################
end:
setbeamshift 0,0
clear
result = 1