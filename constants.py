##Experiment-specific variables

EXP_TYPE = 'image'
#EXP_TYPE = 'video'

# Old parameters
MAX_PRACTICE_TRIALS = 4
N_BLOCKS = 4    # Number of "experimental" trial-blocks (not counting practice or baseline)
MAX_N_TRIALS = 10    
INITIAL_REWARDS = [16, 8]
REWARD_DIFFERENCE = [4, 2, 1]
PRACTICE_REWARDS = [[20, 22], [18, 20]]

# New parameters
#MIN_PRACTICE_TRIALS = 4
#N_BLOCKS = 2    # Number of "experimental" trial-blocks (not counting practice or baseline)
#MIN_N_TRIALS = 3
#INITIAL_REWARDS = [12, 10]
#REWARD_DIFFERENCE = 2
#PRACTICE_REWARDS = [[12, 10], [12, 10]]   

##MAX_N_TRIALS = 20 # TAKING AS POINT OF REFERENCE THE LOWER PAY OPTION (IF CHOSEN EXCLUSIVELY) (for "Exp. Group A" condition)

#-------values for testing------------------
#MAX_PRACTICE_TRIALS = 2
#N_BLOCKS = 2    
#MAX_N_TRIALS = 2
#-------------------------

SUBJ_ID = 1111# None # If an id number is given instead, this is used and no id number is automatically generated # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# counterbalancing of the response buttons across blocks: 'alternate' (systematically); 
COUNTERBALANCE = 'alternate' # TODO: 'random' option still to be coded!!!                # ********


FEEDBACK_VIEWING_TIME = 4000 #for img version, 2500 for video version  # This is the time (in miliseconds) participants have to look at the contingent image   
FEEDBACK_VIEWING_THRESHOLD = 25000  # This is the max time (in miliseconds) the feedback is presented

PRACTICE_REWARDS_1 = [22, 20]
PRACTICE_REWARDS_2 = [20, 18]


P_THRESHOLD = 0.5
THRESHOLD_TYPE = "fixed"    # "fixed" for 50/50%, or "matching" for matching-law

CLUB_THREAT_PROB = 1    # where 1 is 100%, 0.5 50% and 0.9 90% etc
SPADE_THREAT_PROB = 0 

ID_RANGE = (1000, 9999)
BEEP_THRESHOLD = 500  # Response time under which the tone is played


TIMESTEP = 10 #mouse coordinate samplin rate in ms

# MAIN
DUMMYMODE = True         # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#DUMMYMODE = False # False for gaze contingent display, True for dummy mode (using mouse or joystick)
LOGFILENAME = 'eyedata' # logfilename, without path
LOGFILE = LOGFILENAME[:] # .txt; adding path before logfilename is optional; logs responses (NOT eye movements, these are stored in an EDF file!)

# DISPLAY
# used in libscreen, for the *_display functions. The values may be adjusted,
# but not the constant's names
SCREENNR = 0 # number of the screen used for displaying experiment
DISPTYPE = 'psychopy' # either 'psychopy' or 'pygame'
DISPSIZE = (1920,1080) # canvas size

#SCREENSIZE = (53., 30.) # physical display size in cm
BGC = (0,0,0,255) # backgroundcolour
FGC = (255,255,255,255) # foregroundcolour

# EYETRACKER
# general
#TRACKERTYPE = 'dummy'      
TRACKERTYPE = 'eyelink' # either 'smi', 'eyelink' or 'dummy' (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
EVENTDETECTION = 'native'
# EyeLink only
# FRL
# Used in libgazecon.FRL. The values may be adjusted, but not the constant names.
FRLSIZE = 200 # pixles, FRL-size
FRLDIST = 125 # distance between fixation point and FRL
FRLTYPE = 'gauss' # 'circle', 'gauss', 'ramp' or 'raisedCosine'
FRLPOS = 'center' # 'center', 'top', 'topright', 'right', 'bottomright', 'bottom', 'bottomleft', 'left', or 'topleft'
# SOUND
# defaults used in libsound. The values may be adjusted, but not the constants'
# names
SOUNDOSCILLATOR = 'sine' # 'sine', 'saw', 'square' or 'whitenoise'
SOUNDFREQUENCY = 440 # Herz
SOUNDLENGTH = 100 # milliseconds (duration)
SOUNDATTACK = 0 # milliseconds (fade-in)
SOUNDDECAY = 5 # milliseconds (fade-out)
SOUNDBUFFERSIZE = 1024 # increase if playback is choppy
SOUNDSAMPLINGFREQUENCY = 48000 # samples per second
SOUNDSAMPLESIZE = -16 # determines bit depth (negative is signed
SOUNDCHANNELS = 2 # 1 = mono, 2 = stereo

# INPUT
# used in libinput. The values may be adjusted, but not the constant names.
MOUSEBUTTONLIST = None # None for all mouse buttons; list of numbers for buttons of choice (e.g. [1,3] for buttons 1 and 3)
MOUSETIMEOUT = None # None for no timeout, or a value in milliseconds
KEYLIST = None # None for all keys; list of keynames for keys of choice (e.g. ['space','9',':'] for space, 9 and ; keys)
KEYTIMEOUT = 1 # None for no timeout, or a value in milliseconds
JOYBUTTONLIST = None # None for all joystick buttons; list of button numbers (start counting at 0) for buttons of choice (e.g. [0,3] for buttons 0 and 3 - may be reffered to as 1 and 4 in other programs)
JOYTIMEOUT = None # None for no timeout, or a value in milliseconds

# CURSOR
# Used in libgazecon.Cursor. The values may be adjusted, but not the constants' names
CURSORTYPE = 'cross' # 'rectangle', 'ellipse', 'plus' (+), 'cross' (X), 'arrow'
CURSORSIZE = 20 # pixels, either an integer value or a tuple for width and height (w,h)
CURSORCOLOUR = 'red' # colour name (e.g. 'red'), a tuple RGB-triplet (e.g. (255, 255, 255) for white or (0,0,0) for black), or a RGBA-value (e.g. (255,0,0,255) for red)
CURSORFILL = True # True for filled cursor, False for non filled cursor
CURSORPENWIDTH = 3 # cursor edge width in pixels (only if cursor is not filled)