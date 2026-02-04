## General commentaries:
# The section <Settings> contains all the parameters to be chosen.
# Choose a <setmag>> such that the 5x5 drawn circles fit well.
# First argument of <setpatinfo> is Z depth in [um]. 
# <D> is spacing border-border, <L> is diameter.
# Milled <L> must be 0.81 smaller.
# Avoid using division /, the program struggles with it in some cases.
# The function <getstagepos> has <x>,<y> as default variables.
# Calling <getstagepos> updates these variables with current stage position.
# The same applies to <getbeamshift> with <xbeam>,<ybeam>.
# The stage actually moves in [mm],the <*0.001> is unit conversion.

#####################################
############## Settings #############
setmag 35000   
setpatinfo 0.055, si     
setparallelmode 0              
                                    
D_um = 0.446 
L_um = 0.347                                 

quantity_circles_x = 5
quantity_circles_y = 5
 
beam_shifts_x = 1
beam_shifts_y = 1

stage_moves_x = 1
stage_moves_y = 1

#####################################
######## Auxiliary Variables ########
L_correction = L_um * 0.81       
pitch_um = L_um + D_um   
circle_radius_um = L_correction * 0.5

beam_delta_x = pitch_um * quantity_circles_x
beam_delta_y = pitch_um * quantity_circles_y

stage_delta_x = beam_delta_x * (beam_shifts_x + 1) * 0.001
stage_delta_y = beam_delta_y * (beam_shifts_y + 1) * 0.001

#####################################
############ Draw Pattern ###########
clear
count_circles_x = 0
count_circles_y = 0
DrawingLoop:
    circle_x = -1.25 + pitch_um * count_circles_x
    circle_y = +1.05 - pitch_um * count_circles_y

    circle circle_x, circle_y, 0, circle_radius_um                

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
    stage_x = origin_x + stage_delta_x * count_stage_move_x
    stage_y = origin_y - stage_delta_y * count_stage_move_y 
    stagemove xy, stage_x, stage_y  

    ################################# 
    ########## Beam & Mill ##########
    setbeamshift 0,0 

    count_beam_shift_x = 0
    count_beam_shift_y = 0
    BeamShiftLoop: 
        beam_x = 0 + beam_delta_x * count_beam_shift_x
        beam_y = 0 - beam_delta_y * count_beam_shift_y
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