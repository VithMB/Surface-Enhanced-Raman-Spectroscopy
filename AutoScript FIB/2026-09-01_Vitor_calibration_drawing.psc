# # # General comments

# # The section <Settings> contains all the parameters to be chosen.
# <setmag> chosen the magnification
# First argument of <setpatinfo> is Z depth in [um], second is material.  
# <QuantityCircles> defines the numer of circles to be drawn in each direction on the screen.
# <CircleOffset> is the position of the fist circle on the screen. 
 
 
#####################################
############## Settings #############
#####################################
setmag 5000                

L = 0.050 
Depth = 0.10                             

QuantityCirclesX = 1
QuantityCirclesY = 3
          
Pitch = 1000 

setpatinfo Depth, si     
setparallelmode 0 

#####################################
######## Auxiliary Variables ########
#####################################  
CircleDiameter = L

CircleOffsetX = -(Pitch * (QuantityCirclesX - 1))/2.0
CircleOffsetY = +(Pitch * (QuantityCirclesY - 1))/2.0 

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

#####################################
########### Finalization ############
#####################################
end:
result = 1
