# The stage actually moves in [mm], the <*0.001> is unit conversion.

#####################################
############## Settings #############
#####################################
StageDelta = 1 * 0.001

##################################### 
##################################### 

getstagepos
CurrentX = x 
 
StageX = CurrentX + StageDelta
stagemove x, StageX 

end:
result = 1