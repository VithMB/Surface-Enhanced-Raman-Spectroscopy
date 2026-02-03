# escolher de modo aos circulos desenhados terem resolucao
 # x,y are default variables of this function ,  0.001 is unit conversion
 # espacamento D e diametro L dos circulos
 # stagio ta em mm nao aceita /1000

############## Settings ##############
setmag 35000   
setpatinfo 0.055, si    # [um]
setparallelmode 0              
                                    
D_um = 0.446 
L_um = 0.347                                 

quantity_circles_x = 5
quantity_circles_y = 5

beam_shifts_x = 3
beam_shifts_y = 3

stage_moves_x = 1
stage_moves_y = 1

######## Auxiliar variables ########
L_correction = L_um/1.24        
pitch_um = L_um + D_um   
circle_radius_um = L_correction/2

############ Draw Pattern ###########
clear
count_circles_x = 0
count_circles_y = 0
DrawingLoop:
    circle_x = -1.25 + (count_circles_x * pitch_um)
    circle_y = +1.05 - (count_circles_y * pitch_um)

    circle circle_x, circle_y, 0, circle_radius_um                

    count_circles_x = count_circles_x + 1

    if (count_circles_x < quantity_circles_x) goto DrawingLoop

    count_circles_x = 0
    count_circles_y = count_circles_y+1

    if (count_circles_y < quantity_circles_y) goto DrawingLoop 
    count_circles_y = 0 
####################################

########## Mill and Move ###########
setbeamshift 0,0 
count_beam_shift_x = 0
count_beam_shift_y = 0
BeamShiftLoop:
    beam_x = 0 - count_beam_shift_x * (pitch_um * quantity_circles_x)   
    beam_y = 0 + count_beam_shift_y * (pitch_um * quantity_circles_y) 
    setbeamshift beam_x, beam_y

    mill

    count_beam_shift_x = count_beam_shift_x + 1

    if (count_beam_shift_x <= number_beam_shifts_x) goto BeamShiftLoop   

    count_beam_shift_x = 0
    count_beam_shift_y = count_beam_shift_y + 1

    if (count_beam_shift_y <= beam_shifts_y) goto BeamShiftLoop

    count_beam_shift_y = 0    

#################################### 

getstagepos                 
stage_x = x + (0.001*5*0.6*4)
stage_y = y

stagemove xy, stage_x, stage_y
setbeamshift 0,0 


count_stage_move_x = 0
count_stage_move_y = 0
StageMoveLoop:
    getstagepos             
    stage_x = x + count_beam_shift_x * (pitch_um * quantity_circles_x * (beam_shifts_x + 1) * 0.001) 
    stage_y = y + count_beam_shift_y * (pitch_um * quantity_circles_y * (beam_shifts_y + 1) * 0.001) 
    stagemove xy, stage_x, stage_y  

    ####################################
    setbeamshift 0,0 
    count_beam_shift_x = 0
    count_beam_shift_y = 0
    BeamShiftLoop:
        beam_x = 0 - count_beam_shift_x * (pitch_um * quantity_circles_x)   
        beam_y = 0 + count_beam_shift_y * (pitch_um * quantity_circles_y) 
        setbeamshift beam_x, beam_y

        mill

        count_beam_shift_x = count_beam_shift_x + 1

        if (count_beam_shift_x <= number_beam_shifts_x) goto BeamShiftLoop   

        count_beam_shift_x = 0
        count_beam_shift_y = count_beam_shift_y + 1

        if (count_beam_shift_y <= beam_shifts_y) goto BeamShiftLoop

        count_beam_shift_y = 0 
    ####################################



########## Finalization ###########
setbeamshift 0,0
setmag 10000
clear
end:
result = 1