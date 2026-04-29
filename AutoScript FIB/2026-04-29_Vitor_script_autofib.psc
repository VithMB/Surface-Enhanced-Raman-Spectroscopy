# # # General comments

# # The section <Settings> contains all the parameters to be chosen.
# <setmag> chosen the magnification
# First argument of <setpatinfo> is Z depth in [um], second is material. 
# <D> is spacing border-border, and <L> is diameter, <Pitch> is center-center.
# <QuantityCircles> defines the numer of circles to be drawn in each direction on the screen.
# <CircleOffset> is the position of the fist circle on the screen.
# <BeamShifts> is the number of beam shifts +1, for counting the first drawn pattern.
# <BeamOffset> is the position of the first beam shift.
# <StageMovesX> is the number of stages movements +1, for counting the first drawn pattern.
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
setpatinfo 0.06, si     
setparallelmode 0              
                                    
D = 0.446 
L = 0.347                                 

QuantityCirclesX = 20
QuantityCirclesY = 20

SleeptimeMs = 40000
 
BeamShiftsX = 1
BeamShiftsY = 1

BeamOffsetX = 0
BeamOffsetY = 0

StageMovesX = 1

#####################################
######## Auxiliary Variables ########
#####################################
Pitch = L + D   
CircleDiameter = L

CircleOffsetX = -(Pitch * (QuantityCirclesX - 1))*0.5
CircleOffsetY = +(Pitch * (QuantityCirclesY - 1))*0.5

BeamDeltaX = Pitch * QuantityCirclesX
BeamDeltaY = Pitch * QuantityCirclesY

StageDeltaX = BeamDeltaX * (BeamShiftsX + 1) * 0.001
StageDeltaY = BeamDeltaY * (BeamShiftsY + 1) * 0.001

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

BeamShiftLoop: 
    BeamX = BeamOffsetX - (BeamDeltaX * CountBeamShiftX)
    BeamY = BeamOffsetY + (BeamDeltaY * CountBeamShiftY)
    setbeamshift BeamX, BeamY

    mill

    CountBeamShiftX = CountBeamShiftX + 1
    if (CountBeamShiftX < BeamShiftsX) goto BeamShiftLoop   
    CountBeamShiftX = 0

    CountBeamShiftY = CountBeamShiftY + 1
    if (CountBeamShiftY < BeamShiftsY) goto BeamShiftLoop
    CountBeamShiftY = 0 

#####################################
############### Stage ###############
#####################################
getstagepos
OriginX = x 
StageX = OriginX + StageDeltaX  
stagemove x, StageX

CountStageX = CountStageX + 1
if (CountStageX < StageMovesX) goto BeamShiftLoop

#####################################
########### Finalization ############
#####################################
end:
setbeamshift 0,0
clear
result = 1