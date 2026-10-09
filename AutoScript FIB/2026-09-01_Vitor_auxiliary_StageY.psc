# The stage actually moves in [mm], the <*0.001> is unit conversion.

#####################################
############## Settings #############
#####################################
StageDelta = 1 * 0.001

##################################### 
##################################### 

getstagepos 
CurrentY = y
 
StageY = CurrentY - StageDelta
stagemove y, StageY  

end:
result = 1