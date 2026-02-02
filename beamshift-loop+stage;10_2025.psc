clear
setmag 35000
setbeamshift 0,0

 
D = 0.250
L = 0.350 
L_prime = L/1.24        
pitch_um = L + D   
circle_radius_um = L_prime/2
number_circles_x = 5
number_circles_y = 5


count_circles_x = 0
count_circles_y = 0
#####################################
DrawingLoop:

    circle_x = -1.25 + (count_circles_x * pitch_um)
    circle_y = +1.05 - (count_circles_y * pitch_um)

    circle circle_x, circle_y, 0, circle_radius_um                

    count_circles_x = count_circles_x + 1

    if (count_circles_x < number_circles_x) goto DrawingLoop

    count_circles_x = 0
    count_circles_y = count_circles_y+1

    if (count_circles_y < number_circles_y) goto DrawingLoop 
    count_circles_y = 0 

#####################################

number_beam_shifts_x = 3
number_beam_shifts_y = 3

count_beam_shift_x = 0
count_beam_shift_y = 0

setpatinfo 0.055, si
setparallelmode 0
#############################################################
BeamShiftLoop:

    beam_x = 0 - ((count_beam_shift_x * (pitch_um * number_circles_x)))   
    beam_y = 0 + ((count_beam_shift_y* (pitch_um * number_circles_y))) 
    setbeamshift beam_x, beam_y

    mill

    count_beam_shift_x = count_beam_shift_x + 1

    if (count_beam_shift_x <= number_beam_shifts_x) goto BeamShiftLoop   

    count_beam_shift_x = 0
    count_beam_shift_y = count_beam_shift_y + 1

    if (count_beam_shift_y <= number_beam_shifts_y) goto BeamShiftLoop

    count_beam_shift_y = 0    

#############################################################
getstagepos
stage_x = x + (0.003*4)
stage_y = y

stagemove xy, stage_x, stage_y
setbeamshift 0,0
#############################################################
BeamShiftLoop2:

    beam_x = 0 - ((count_beam_shift_x * (pitch_um * number_circles_x)))   
    beam_y = 0 + ((count_beam_shift_y* (pitch_um * number_circles_y))) 
    setbeamshift beam_x, beam_y

    mill

    count_beam_shift_x = count_beam_shift_x + 1

    if (count_beam_shift_x <= number_beam_shifts_x) goto BeamShiftLoop2   

    count_beam_shift_x = 0
    count_beam_shift_y = count_beam_shift_y + 1

    if (count_beam_shift_y <= number_beam_shifts_y) goto BeamShiftLoop2

    count_beam_shift_y = 0    

#############################################################
#############################################################
clear
setbeamshift 0,0
setmag 10000
end:
result = 1