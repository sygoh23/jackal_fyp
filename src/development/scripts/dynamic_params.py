"""
Contains dynamic parameters to be accessed and modified throughout the algorithm

--> Import this file as 'import dynamic_params', then access/modify any parameters as 'dynamic_params.parameter'
--> Do not assign local variables with the same name as these parameters
--> Modifying a parameter will modify it for all files which access it
"""

########## Algorithm ##########
dist_last = []          # Last reported distance
reached_target = 0      # Flag for whether robot has reached the target doorway