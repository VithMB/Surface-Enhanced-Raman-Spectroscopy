### General comments
# The section <Settings> contains all the parameters to be chosen.

# <setmag> is such that the drawn circles fit well.
# First argument of <setpatinfo> is Z depth in [um]. 
# <D> is spacing border-border, <L> is diameter, <pitch> is center-center.
# Milled <L> is purposely done x0.81 smaller.

# Limit of the Beam Shift is 50um from the center.
# Set at 35um to keep at center
# 	
 
# Avoid using division /, the program struggles with it in some cases.
# Or use / with .0 at the end of the number to force float number division.

# The function <getstagepos> has <x>,<y> as default variables.
# Calling <getstagepos> updates these variables with current stage position.
# The stage actually moves in [mm],the <*0.001> is unit conversion.

#####################################
############## Settings #############
setmag 35000   
setpatinfo 0.06, si     
setparallelmode 0              
                                    
D = 0.446 
L = 0.347                                 

quantity_circles_x = 4
quantity_circles_y = 4

circle_offset_x = 1.25
circle_offset_y = 1.05
 
beam_shifts_x = 15
beam_shifts_y = 15

beam_offset_x = 35
beam_offset_y = 35

stage_moves_x = 0
stage_moves_y = 0

#####################################
######## Auxiliary Variables ########
L_correction = L * 0.81       
pitch = L + D   
circle_radius = L_correction * 0.5

beam_delta_x = pitch * quantity_circles_x
beam_delta_y = pitch * quantity_circles_y

stage_delta_x = beam_delta_x * (beam_shifts_x + 1) * 0.001
stage_delta_y = beam_delta_y * (beam_shifts_y + 1) * 0.001

#####################################
############ Draw Pattern ###########
clear
count_circles_x = 0
count_circles_y = 0
DrawingLoop:
    circle_x = -circle_offset_x + (pitch * count_circles_x)
    circle_y = +circle_offset_y - (pitch * count_circles_y)

    circle circle_x, circle_y, 0, circle_radius                

    count_circles_x = count_circles_x + 1
    if (count_circles_x < quantity_circles_x) goto DrawingLoop
    count_circles_x = 0

    count_circles_y = count_circles_y+1
    if (count_circles_y < quantity_circles_y) goto DrawingLoop 
    count_circles_y = 0 

#####################################
############### Stage ###############
getstagepos
origin_x = x
origin_y = y

count_stage_move_x = 0
count_stage_move_y = 0
StageMoveLoop:             
    stage_x = origin_x + (stage_delta_x * count_stage_move_x)
    stage_y = origin_y - (stage_delta_y * count_stage_move_y) 
    stagemove xy, stage_x, stage_y  

    ################################# 
    ########## Beam & Mill ##########
    setbeamshift beam_offset_x ,beam_offset_y 

    count_beam_shift_x = 0
    count_beam_shift_y = 0
    BeamShiftLoop: 
        beam_x = beam_offset_x - (beam_delta_x * count_beam_shift_x)
        beam_y = -beam_offset_y + (beam_delta_y * count_beam_shift_y)
        setbeamshift beam_x, beam_y

        mill

        count_beam_shift_x = count_beam_shift_x + 1
        if (count_beam_shift_x <= beam_shifts_x) goto BeamShiftLoop   
        count_beam_shift_x = 0

        count_beam_shift_y = count_beam_shift_y + 1
        if (count_beam_shift_y <= beam_shifts_y) goto BeamShiftLoop
        count_beam_shift_y = 0 

    #################################
    count_stage_move_x = count_stage_move_x + 1
    if (count_stage_move_x <= stage_moves_x) goto StageMoveLoop
    count_stage_move_x = 0

    count_stage_move_y = count_stage_move_y + 1
    if (count_stage_move_y <= stage_moves_y) goto StageMoveLoop
    count_stage_move_y = 0

#####################################
########### Finalization ############
setbeamshift 0,0
setmag 10000
clear
end:
result = 1