

# control task for compassion and prejudice project



#Values:
#   1. Compassion and Kindness (becoming compassionate and kind to others)
#   2. Family and Friends (having good relationships with family and friends)
#   3. Spirituality (developing spiritual connection to the world)
#   4. Power and Status (gaining power and social status)
#   5. Wealth (making money and possessing wealth)
#   6. Fame (becoming famous and popular)


# DESIGN
#
# 1. ready screen - wait for 'T' trigger
# 2. instruction reminder - button box
# 3. main loop - trial presentation
#     - value prime (e.g. FAME) - 2 seconds
#     - situation - statement with 'think of situation' - 12 seconds
#     - rating (importance 1->4) - 4 secs
#     - fixation - 3 secs
# 4 - interspersed throughout have 12 second REST screens - 5 per run



# import psychopy and other modules

from psychopy import visual, core, event, gui, data, sound, logging

import random
import os
import csv
import datetime


# paramaters
use_fullscreen = False
frame_rate = 30
prime_dur = 2*frame_rate
situation_dur = 12*frame_rate
rating_dur = 4*frame_rate
fixation_dur = 3*frame_rate
disdaq_dur = 8 * frame_rate
instruct_dur = 8 * frame_rate
rest_dur = 9 * frame_rate

button_labels = { 'b': 0, 'y': 1, 'g': 2, 'r': 3 }
button_labels = { '1': 0, '2': 1, '3': 2, '4': 3 , 'space': 0}
buttons = button_labels.keys()


values = ('compassion and kindness', 'family and friends', 'spirituality', 
               'power and status', 'wealth', 'fame')


# get subjID and value
subjDlg = gui.Dlg(title="Future Task")
subjDlg.addField('Enter Value Number:')
subjDlg.show()

if gui.OK:
    subj_value=subjDlg.data[0]
else:
    sys.exit()


subj_id='DEMO'
subj_value = int(subj_value)

# set up window and stimuli
win = visual.Window(size=(800,600), fullscr=use_fullscreen, monitor='testMonitor', units='deg')

# set up stimuli positions, sizes, etc.
fixation = visual.TextStim(win, text='+', height=3)
ready_screen = visual.TextStim(win, text="Press space to continue", height=1.2)
primeStim = visual.TextStim(win, text='', height=1.4, wrapWidth=25)
valueStim = visual.TextStim(win, text='', pos=(0,6))
situationStim = visual.TextStim(win, text='', height=1.4, pos=(0,2), alignHoriz='center',  wrapWidth=15)
thinkStim = visual.TextStim(win, text='Think of a situation', pos=(0,-2))
restStim = visual.TextStim(win,text='REST',height=2.5)


# instrcution screen
instruction_image = visual.SimpleImageStim(win,image="buttonpad.png",pos=(-1,-3.5))
instruction_text = visual.TextStim(win, height=1.3,color="#FFFFFF", 
        text="Use the buttons to indicate how important each statement is to you", 
        pos=(0,+5))


anchor1 = visual.TextStim(win, text='Not very\nimportant', pos=(-8,-6))
anchor4 = visual.TextStim(win, text='Very\nimportant', pos=(8,-6))


ratingStim=[]

xpos = [-8, -3, 3, 8]

for rating in (1,2,3,4):
    ratingStim.append(visual.TextStim(win, text='%i' % rating, pos=(xpos[rating-1],-4)))

    

# change this to determine which value to display
subj_value=int(subj_value)
selected_value=values[subj_value-1]


log_filename = 'logs/%s.csv' % subj_id



run_data = {
    'Participant ID': subj_id,
    'Value': selected_value,
    'Date': str(datetime.datetime.now()),
    'Description': 'Physical Activity 2 Project CNLab - Future Task'
}
# change this to determine which value to display

subj_value=int(subj_value-1)
selected_value=values[subj_value]


# load stimuli from stimuli csv file
stimuli={}
stimuli['value'] = [stim for stim in csv.DictReader(open('stimuli.csv','rU')) if stim['value'] == selected_value]
stimuli['control'] = [stim for stim in csv.DictReader(open('stimuli.csv','rU')) if stim['value'] == 'control']
stimuli['REST'] = [{'value': 'REST', 'message': 'REST'}]*10

# set up the pseudo-randomized order of the trials for runs 1 and 2

for stim_type in stimuli:
    random.shuffle(stimuli[stim_type])
    
runs = [ [ stimuli['value'].pop(), stimuli['value'].pop(), stimuli['control'].pop(), stimuli['control'].pop()] ]


# setup logging #
log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")

globalClock = core.Clock()
logging.setDefaultClock(globalClock)


def do_run(run_number, trials):

    # 1. add ready screen and wait for trigger
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList='space')

    # reset globalClock
    globalClock.reset()

    # send START log event
    logging.log(level=logging.DATA, msg='******* START (trigger from scanner) - Run %i *******' % run_number)

    ################ 
    # SHOW INSTRUCTIONS
    ################ 
    #for frame in range(instruct_dur):
    instruction_image.draw()
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=('space'))

        
    #######################
    # MAIN LOOP for trials
    # loop over stimuli
    for tidx, trial in enumerate(trials):
        value = trial['value']
        prime_label = 'Daily Activity' if value == 'control' else value.title()
        situation = trial['message']
        valueStim.setText(prime_label)


        # test for REST trial
        if trial['value']=='REST':

            for frame in range(rest_dur):
                fixation.draw()
                win.flip()

            # fixation
            for frame in range(fixation_dur):
                fixation.draw()
                win.flip()
            continue

        # 1. show prime
        primeStim.setText(prime_label)
        
        if tidx%2==0:
            primeStim.draw()
            win.flip()
            event.waitKeys(keyList=('space'))
        else:
            for frame in range(prime_dur):
                primeStim.draw()
                win.flip()

        # 2. show situation
        situationStim.setText(situation)
        if tidx%2==0:
            situationStim.draw()
            thinkStim.draw()
            win.flip()
            event.waitKeys(keyList=('space'))
        else:
            for frame in range(situation_dur):
                situationStim.draw()
                thinkStim.draw()
                win.flip()

        event.clearEvents()

        # 3. show rating and get response
        timer = core.Clock()
        timer.reset()
        space_pressed = False
        while (tidx % 2 != 0 and timer.getTime()<rating_dur/frame_rate) or (tidx % 2 == 0 and space_pressed==False):
        #for frame in range(rating_dur):
            situationStim.draw()
            valueStim.draw()
            anchor1.draw()
            anchor4.draw()

            # draw rating
            for resp in ratingStim:
                resp.draw()
            win.flip()


            # get key response
            resp = event.getKeys(keyList = buttons)
            
            if len(resp) > 0 : 
                if resp[0]=='space':
                    space_pressed=True
                    continue
                resp_value = button_labels[resp[0]]
                ratingStim[resp_value].setColor('red')
                trials.addData('resp', resp_value+1)

         # reset rating number color
        for rate in ratingStim:
            rate.setColor('white')


        # 4. fixation
        for frame in range(fixation_dur):
            fixation.draw()
            win.flip()

        ready_screen.draw()
        win.flip()
        event.waitKeys(keyList=['space'])



    # write logs

    # send END log event
    logging.log(level=logging.DATA, msg='******* END run %i *******' % run_number)

    # save the trial infomation from trial handler
    log_filename2 = "%s_%i.csv" % (log_filename[:-4], run_number )
    trials.saveAsText(log_filename2, delim=',', dataOut=('n', 'all_raw'))



# =====================
# MAIN 
#
# - set up stimuli and runs

for ridx, run in enumerate(runs):
    #print run
    trials = data.TrialHandler(run, nReps=1, extraInfo=run_data, dataTypes=['stim_onset','rt', 'rating'], method='sequential')
    do_run(ridx+1, trials)
    

