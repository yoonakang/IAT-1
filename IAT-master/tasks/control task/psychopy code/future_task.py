
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
#     - situation - statement with 'think of situation' - 12 seconds (10 sec? YK)
#     - rating (importance 1->4) - 4 secs
#     - fixation - 3 secs
# 4 - interspersed throughout have 12 second REST screens - 5 per run (10 sec? YK)




# import psychopy and other modules
from psychopy import visual, core, event, gui, data, sound, logging



import random
import os
import csv
import datetime


# paramaters
use_fullscreen = True
frame_rate = 1
prime_dur = 2*frame_rate
situation_dur = 10*frame_rate
rating_dur = 4*frame_rate
fixation_dur = 3*frame_rate
disdaq_dur = 8 * frame_rate
instruct_dur = 8 * frame_rate
rest_dur = 10 * frame_rate



button_labels = { 'b': 0, 'y': 1, 'g': 2, 'r': 3 }

buttons = button_labels.keys()

values = ('compassion and kindness', 'family and friends', 'spirituality', 
               'power and status', 'wealth', 'fame')

# get subjID and value
subjDlg = gui.Dlg(title="Future Task")
subjDlg.addField('Enter Subject ID:')
subjDlg.addField('Enter Value Number:')
subjDlg.show()







if gui.OK:

    subj_id=subjDlg.data[0]

    subj_value=subjDlg.data[1]

else:

    sys.exit()



# set up window and stimuli

win = visual.Window(size=(800,600), fullscr=use_fullscreen, monitor='testMonitor', units='deg')



# set up stimuli positions, sizes, etc.

fixation = visual.TextStim(win, text='+', height=3)

ready_screen = visual.TextStim(win, text="Ready.....", height=2)

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

    

runs = [[], []]



item_cnt = len(stimuli['REST'])/2



for run in (0,1):

    for group in range(item_cnt):

        condition_order = ['REST', 'value','value','control','control']



        while condition_order[0]=='REST':

            random.shuffle(condition_order)

            #print condition_order



        for trial_type in condition_order:

            runs[run].append(stimuli[trial_type].pop())











# setup logging #

log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")



globalClock = core.Clock()

logging.setDefaultClock(globalClock)





def do_run(run_number, trials):



    timer = core.Clock()



    # 1. add ready screen and wait for trigger

    ready_screen.draw()

    win.flip()

    event.waitKeys(keyList='t')



    # reset globalClock

    globalClock.reset()



    # send START log event

    logging.log(level=logging.DATA, msg='******* START (trigger from scanner) - Run %i *******' % run_number)



    ################ 

    # SHOW INSTRUCTIONS

    ################ 

    

    timer.reset()

    while timer.getTime() < instruct_dur:

    #for frame in range(instruct_dur):

        instruction_image.draw()

        instruction_text.draw()

        win.flip()



        

    #######################

    # MAIN LOOP for trials

    # loop over stimuli

    for trial in trials:

        value = trial['value']

        prime_label = 'Daily Activity' if value == 'control' else value.title()

        situation = trial['message']

        valueStim.setText(prime_label)





        # test for REST trial

        if trial['value']=='REST':

            logging.log(level=logging.DATA, msg='REST fixation')

            timer.reset()

            while timer.getTime() < rest_dur:

                fixation.draw()

                win.flip()

            continue



        # 1. show prime

        logging.log(level=logging.DATA, msg='Prime: %s' % prime_label)
        trials.addData('prime_onset', globalClock.getTime())

        primeStim.setText(prime_label)
        timer.reset()
        while timer.getTime() < prime_dur:
        #for frame in range(prime_dur):
            primeStim.draw()
            win.flip()

        # 2. show situation
        logging.log(level=logging.DATA, msg='Situation: %s' % situation)
        trials.addData('stim_onset', globalClock.getTime())

        situationStim.setText(situation)
        timer.reset()

        while timer.getTime() < situation_dur:
        #for frame in range(situation_dur):
            situationStim.draw()
            thinkStim.draw()
            win.flip()

        event.clearEvents()


        # 3. show rating and get response
        timer.reset()
        logging.log(level=logging.DATA, msg='RESPONSE')
        trials.addData('resp_onset', globalClock.getTime())

        while timer.getTime() < rating_dur:

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
                resp_value = button_labels[resp[0]]
                ratingStim[resp_value].setColor('red')
                trials.addData('rating', resp_value+1)
                trials.addData('rt', timer.getTime())

         # reset rating number color
        for rate in ratingStim:
            rate.setColor('white')


        # 4. fixation
        timer.reset()
        logging.log(level=logging.DATA, msg='FIXATION')
        trials.addData('fixation_onset', globalClock.getTime())

        while timer.getTime() < fixation_dur:
        #for frame in range(fixation_dur):
            fixation.draw()
            win.flip()

    # write logs



    # send END log event

    logging.log(level=logging.DATA, msg='******* END run %i *******' % run_number)



    # save the trial infomation from trial handler

    log_filename2 = "%s_%i.csv" % (log_filename[:-4], run_number )

    trials.saveAsText(log_filename2, delim=',', dataOut=('n', 'all_raw'))
#    log_file.logger.flush()


    event.waitKeys(keyList=('space'))



# =====================

# MAIN 

#

# - set up stimuli and runs



for ridx, run in enumerate(runs):

    #print run

    trials = data.TrialHandler(run, nReps=1, extraInfo=run_data, dataTypes=['stim_onset','rt', 'rating'], method='sequential')

    do_run(ridx+1, trials)

    



