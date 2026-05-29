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
                                    
Height = 0.100
Base = 0.300    
Depth = 0.10                      
                           
QuantityCirclesX = 5
QuantityCirclesY = 5

SleeptimeMs = 0

StageMovesX = 0
StageMovesY = 0

setpatinfo Depth, si     
setparallelmode 0 

#####################################
######## Auxiliary Variables ########
##################################### 
PitchX = Base + 0.150 
PitchY = Height + 0.150   

CircleOffsetX = -(PitchX * (QuantityCirclesX - 1))/2.0
CircleOffsetY = +(PitchY * (QuantityCirclesY - 1))/2.0

StageDeltaX = PitchX * QuantityCirclesX * 0.001
StageDeltaY = PitchY * QuantityCirclesY * 0.001

getstagepos
OriginX = x
OriginY = y

#####################################
############ Draw Pattern ###########
#####################################
clear
CountCirclesX = 0
CountCirclesY = 0
DrawingLoop:
    CircleX = CircleOffsetX + (PitchX * CountCirclesX)
    CircleY = CircleOffsetY - (PitchY * CountCirclesY)

    SquareStartX = CircleX - (Base/2.0)
    SquareStartY = CircleY + (Height/2.0)
    SquareEndX = CircleX + (Base/2.0)
    SquareEndY = CircleY - (Height/2.0)

    box SquareStartX, SquareStartY, SquareEndX, SquareEndY              

    CountCirclesX = CountCirclesX + 1
    if (CountCirclesX < QuantityCirclesX) goto DrawingLoop
    CountCirclesX = 0

    CountCirclesY = CountCirclesY+1
    if (CountCirclesY < QuantityCirclesY) goto DrawingLoop 
    CountCirclesY = 0 

sleep SleeptimeMs

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



        #####################################
        ############### Mill ################
        #####################################
        mill

        #####################################
        ########## Advance Stage X ##########
        #####################################
        CountStageX = CountStageX + 1
        if (CountStageX > StageMovesX) goto EndStageLoopX

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
