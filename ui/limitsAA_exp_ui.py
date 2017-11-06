from __future__ import division
from psychopy import visual
from pygaze import libscreen, libtime, libinput, libsound
import pygaze
from constants import *
import numpy as np
import random
import os

# This class implements user interface of AvoidanceExp based on psychopy API (and partly pygaze)
class AvoidanceExpUI:
    standard_text_heigth = 28

    # (width, height)
    start_button_size = (50, 30)
    # (x offset, y offset)
    start_button_offset = (0, 30)
    start_button_pos = (0, -DISPSIZE[1]/2 + (start_button_size[1]/2 + start_button_offset[1]))


    # (width, height)
    deadzone_size = (DISPSIZE[0], 90)                                               # *****************
    deadzone_pos = start_button_pos

    # (width, height) # TO BE REPLACED BY DEADZONE (SINZE THE TONE ALERT WILL NO LONGER BE WORKING)
    start_area_size = (90, 60) 
    
    # (width, height)
    card_size = (180, 240)
    # (x offset, y offset)
    card_offset = (160, 91)

    # (x offset, y offset)
    reward_offset = (48, 5)

      
    left_card_pos = (-DISPSIZE[0]/2 + (card_size[0]/2 + card_offset[0]), 
                     DISPSIZE[1]/2 - (card_size[1]/2 + card_offset[1]))
    right_card_pos = (DISPSIZE[0]/2 - (card_size[0]/2 + card_offset[0]), 
                     DISPSIZE[1]/2 - (card_size[1]/2 + card_offset[1]))\

    left_reward_pos = (-DISPSIZE[0]/2 + (card_size[0]/2 + card_offset[0]), 
                     DISPSIZE[1]/2 - (card_size[1]/2 + (card_offset[1] + reward_offset[0])))
    right_reward_pos = (DISPSIZE[0]/2 - (card_size[0]/2 + card_offset[0]), 
                     DISPSIZE[1]/2 - (card_size[1]/2 + (card_offset[1] + reward_offset[0])))    
    
    # the actual size of the img is 960x720 but here is reduced to ensure the subject sees content
    consequence_area_size = (730, 460)    

#    # (width, height)
#    rating_button_size = (90, 60)                                                        # mmmmmmmm
#    rating_button_pos = (0, -200) # (x, y) of "base button" for offsets 
#
#    button_x_offsets = [-DISPSIZE[1]/2, -DISPSIZE[1]/2.6, -DISPSIZE[1]/3.6, -DISPSIZE[1]/5.8, -DISPSIZE[1]/16, 
#                        DISPSIZE[1]/16, DISPSIZE[1]/5.8, DISPSIZE[1]/3.6, DISPSIZE[1]/2.6, DISPSIZE[1]/2] 
#    button_y_offsets = [0,0,0,0,0,0,0,0,0,0] # For each button (0...10)  

#    scale_rating_labels = ['1','2','3','4','5','6','7','8','9','10']                 # mmmmmmmm


    def __init__(self):
        self.disp = libscreen.Display()
        self.win = pygaze.expdisplay
        self.mouse = libinput.Mouse(visible=True)
        
        # TODO: change this to PsychoPy's sound.Sound
        # TODO: move the sound to resources
        self.rt_alert_sound = libsound.Sound(soundfile = 'img/rt_beep.wav')
        
        instructions_file = 'resources/%s_instructions.txt'
        
        self.experiment_start_screen = self.intialize_message_screen(
                                instructions_file % ('experiment_start'), wrapWidth=1000)
        self.experiment_end_screen, self.final_score_stim = self.initialize_experiment_end_screen(
                                instructions_file % ('experiment_end'))

        self.practice_start_screen = self.intialize_message_screen(
                                instructions_file % ('practice_start'))
        self.practice_end_screen = self.intialize_message_screen(
                                instructions_file % ('practice_end'), color= '#FFAA00')

        self.block_start_screen, self.block_threshold_stim = self.initialize_block_start_screen(
                                instructions_file % ('block_start'))
        self.block_end_screen = self.intialize_message_screen(
                                instructions_file % ('block_end'))
        
        self.trial_start_screen, self.start_button_rect = self.initialize_trial_start_screen()
#        self.pre_decks_screen, self.start_area_rect = self.initialize_pre_decks_screen()        # *****************
        self.decks_screen = self.initialize_decks_screen()
        self.consequence_screen = self.initialize_consequence_screen(EXP_TYPE)
        self.trial_end_screen = self.initialize_trial_end_screen()


    def intialize_message_screen(self, message_file, **kwargs):
        message_screen = libscreen.Screen()
        with open(message_file) as f:
            instructions = f.read()
        instructions_stim = visual.TextStim(self.win, text=instructions, units='pix', 
                                                    height=self.standard_text_heigth, **kwargs)
        message_screen.screen.append(instructions_stim)        
        return message_screen    
    
    def show_message_screen(self, screen):
        self.mouse.set_visible(True)
        self.disp.fill(screen)
        self.disp.show()
        self.mouse.get_clicked()
        self.mouse.set_visible(False)
        libtime.pause(500)

   
    def show_experiment_start_screen(self):
        self.show_message_screen(self.experiment_start_screen)

    
    def initialize_experiment_end_screen(self, message_file):
        experiment_end_screen = self.intialize_message_screen(message_file)
        
        final_score_stim = visual.TextStim(self.win, pos=(0,-250), color= '#F5F500',
                                                    height=50, units='pix')
        experiment_end_screen.screen.append(final_score_stim)
    
        return experiment_end_screen, final_score_stim    
    
    def show_experiment_end_screen(self, upper_bound, lower_bound):
        self.final_score_stim.setText('Upper bound: %i \n Lower bound: %i' 
                                      % (lower_bound, upper_bound))
        self.show_message_screen(self.experiment_end_screen)

                
    def show_practice_start_screen(self):
        self.show_message_screen(self.practice_start_screen)

        
    def show_practice_end_screen(self):
        self.show_message_screen(self.practice_end_screen)


    def initialize_block_start_screen(self, message_file):
        block_start_screen = self.intialize_message_screen(message_file)
        
        block_threshold_stim = visual.TextStim(self.win, pos=(0,-150), color= '#F5F500',
                                                    height=60, units='pix')
        block_start_screen.screen.append(block_threshold_stim)
    
        return block_start_screen, block_threshold_stim

    def show_block_start_screen(self, threshold):
        self.block_threshold_stim.setText(str(threshold))
        self.show_message_screen(self.block_start_screen)

    
    def show_block_end_screen(self):
        self.show_message_screen(self.block_end_screen)

    def initialize_trial_start_screen(self):
        trial_start_screen = libscreen.Screen()
        
        start_button_rect = visual.Rect(win=self.win, pos=self.start_button_pos,
                                          width=self.start_button_size[0], 
                                            height=self.start_button_size[1],
                                            lineColor=(200,200,200), lineColorSpace='rgb255',
                                            fillColor=None, lineWidth=3)  
                                                   
        start_button_text = visual.TextStim(self.win, text='Start', pos=self.start_button_pos) 
        
        trial_start_screen.screen.append(start_button_rect)
        trial_start_screen.screen.append(start_button_text)

        return trial_start_screen, start_button_rect
        
    def show_trial_start_screen(self):
        self.mouse.set_visible(True)
        self.disp.fill(self.trial_start_screen)
        self.disp.show()
        
        while not self.mouse.mouse.isPressedIn(self.start_button_rect):
            continue
        self.mouse.set_visible(False)


    def initialize_pre_decks_screen(self):                                         # *****************
        pre_decks_screen = libscreen.Screen()
        start_area_rect = visual.Rect(win=self.win, pos=self.start_button_pos,
                                            width=self.start_area_size[0], 
                                            height=self.start_area_size[1],
                                            lineColor=None, fillColor=None)
        pre_decks_screen.screen.append(start_area_rect)
        return pre_decks_screen, start_area_rect
    
    def show_pre_decks_screen(self):                                                # *****************
        self.mouse.set_visible(visible=True)
        self.disp.fill(self.pre_decks_screen)        
        self.disp.show()
        while self.start_area_rect.contains(self.mouse.mouse):
            self.disp.show()
            continue


    def initialize_decks_screen(self):
        decks_screen = libscreen.Screen()
        
        
#        self.deadzone_rect = visual.Rect(win=self.win, pos=self.deadzone_pos,       # *****************
#                                            width=self.deadzone_size[0], 
#                                            height=self.deadzone_size[1],
#                                            lineColor=None, fillColor=None)                
       
        # We're using psychopy object ImageStim  
        self.left_card_img = visual.ImageStim(self.win, pos=self.left_card_pos) 
        self.right_card_img = visual.ImageStim(self.win, pos=self.right_card_pos)

        self.left_card_rect = visual.Rect(win=self.win, pos=self.left_card_pos,
                                          width=self.card_size[0], height=self.card_size[1],
                                            lineColor=None, fillColor=None)
        self.right_card_rect = visual.Rect(win=self.win, pos=self.right_card_pos,
                                          width=self.card_size[0], height=self.card_size[1],
                                            lineColor=None, fillColor=None)  
                                            
       
        self.reward_left = visual.TextStim(self.win, pos=self.left_reward_pos, 
                                           color= 'black', height= 90)        
        self.reward_right = visual.TextStim(self.win, pos=self.right_reward_pos, 
                                            color= 'black', height= 90)
                
        
        # Here we specify the screeen onto which the decks are to be displayed
#        decks_screen.screen.append(self.deadzone_rect)                             # *****************
        decks_screen.screen.append(self.left_card_img)
        decks_screen.screen.append(self.right_card_img)
        decks_screen.screen.append(self.left_card_rect)
        decks_screen.screen.append(self.right_card_rect)
        decks_screen.screen.append(self.reward_left) 
        decks_screen.screen.append(self.reward_right) 
        
        return decks_screen

    def show_decks_screen(self, trial_info, tracker):
        self.mouse.set_visible(visible=True)
        # This (re)sets the deck images every trial, so it doesn't show the flipped images 
        # after reading code below
        # Note that what changes is the image drawn (not the variable)
        if trial_info['is_threat_left']:         
            self.left_card_img.setImage('resources/club_suitCard.png')        
            self.right_card_img.setImage('resources/spade_suitCard.png')                
            self.reward_left.setText(text= str(trial_info['rewards'][0])) 
            self.reward_right.setText(text= str(trial_info['rewards'][1])) 
        else:
            self.left_card_img.setImage('resources/spade_suitCard.png')        
            self.right_card_img.setImage('resources/club_suitCard.png')
            # We change the [] number to change the reward depending on the deck location
            self.reward_left.setText(text= str(trial_info['rewards'][1])) 
            self.reward_right.setText(text= str(trial_info['rewards'][0])) 

#        while self.deadzone_rect.contains(self.mouse.mouse):                     # *****************
#            self.disp.fill(self.decks_screen)
#            self.disp.show()

                    
        self.disp.fill(self.decks_screen)
        self.disp.show()
        
        card_chosen = None
        response_dynamics_log = []

        rt_alert_played = False 
        trial_start_time = libtime.get_time()
        
        while card_chosen is None:
            mouse_position = self.mouse.get_pos()
            t = libtime.get_time() - trial_start_time


            if ((self.start_button_rect.contains(self.mouse.mouse)) and \
                    (t > BEEP_THRESHOLD) and \
                    (not rt_alert_played)):
                self.rt_alert_sound.play()
                rt_alert_played = True
                
            eye_position = tracker.sample()
            pupil_size = tracker.pupil_size()
 
            response_dynamics_log.append([trial_info['subj_id'], trial_info['block_no'], 
                                          trial_info['trial_no'], str(t), 
                                            mouse_position[0], mouse_position[1], 
                                            pupil_size, eye_position[0], eye_position[1]])
            
            if self.mouse.mouse.isPressedIn(self.left_card_rect):
                if trial_info['is_threat_left']:
                    card_chosen = 'Threat'
                    self.left_card_img.setImage('resources/flippedClubs.png')
                else:
                    card_chosen = 'Neutral'
                    self.left_card_img.setImage('resources/flippedSpades.png')
            elif self.mouse.mouse.isPressedIn(self.right_card_rect):
                if trial_info['is_threat_left']:
                    card_chosen = 'Neutral'
                    self.right_card_img.setImage('resources/flippedSpades.png')
                else:
                    card_chosen = 'Threat'
                    self.right_card_img.setImage('resources/flippedClubs.png')
            
            libtime.pause(TIMESTEP)        
        response_time = libtime.get_time()-trial_start_time
        
        self.disp.fill(self.decks_screen)
        self.disp.show()
        libtime.pause(300)
        
        return response_dynamics_log, card_chosen, response_time    

    def initialize_consequence_screen(self, exp_type):
        consequence_screen = libscreen.Screen()
        
        if exp_type == 'image':
            # By not including any position values (e.g.,pos = (0, 0) ), as ImageStim argument, 
            # the image is place at the centre by default (or so it seems)
            self.consequence_image = visual.ImageStim(pygaze.expdisplay)    
            consequence_screen.screen.append(self.consequence_image)
            
            consequence_instructions = visual.TextStim(pygaze.expdisplay, pos=(0, -450), 
                                                       color= '#FF0000', 
                                                text='Look at the image for 4 seconds to continue', 
                                                wrapWidth=800, height= 28)

            consequence_screen.screen.append(consequence_instructions)
        elif exp_type == 'video':
            pass
        
        return consequence_screen
    
    def show_consequence_screen(self, trial_info, tracker):        
        if DUMMYMODE:
            self.mouse.set_visible(visible=True)
        else:
            self.mouse.set_visible(visible=False)
            
        threat_shown = False
        if (trial_info['exp_type']=='image'):
            self.consequence_image.setImage('img/neutral/' + \
                                            random.choice(os.listdir('img/neutral')))
            rnd = random.uniform(0,1)
            if ((not trial_info['is_baseline']) and \
                ((trial_info['card_chosen'] == 'Threat' and rnd < THREAT_THREAT_PROB) or \
                (trial_info['card_chosen'] == 'Neutral' and rnd < NEUTRAL_THREAT_PROB))):
                self.consequence_image.setImage('img/spiders/' + \
                                                    random.choice(os.listdir('img/spiders')))
                threat_shown = True
                
            consequence_dynamics_log = []
            image_start_time = libtime.get_time()
            previous_frame_finished_time = libtime.get_time()
            gaze_time = 0
            while True:
                self.disp.fill(self.consequence_screen)
                self.disp.show()
                eye_position = tracker.sample()
                pupil_size = 0 if DUMMYMODE else tracker.pupil_size()
    
                t = libtime.get_time() - image_start_time
                consequence_dynamics_log.append([trial_info['subj_id'], trial_info['block_no'], 
                                                 trial_info['trial_no'], str(t), pupil_size, 
                                                    eye_position[0], eye_position[1]])     
                if ((abs(eye_position[0] - (DISPSIZE[0]/2)) < self.consequence_area_size[0]/2) and 
                    (abs(eye_position[1] - (DISPSIZE[1]/2)) < self.consequence_area_size[1]/2)):
                        gaze_time += libtime.get_time() - previous_frame_finished_time
                previous_frame_finished_time = libtime.get_time()
                
                if (gaze_time >= FEEDBACK_VIEWING_TIME) or \
                    ((libtime.get_time() - image_start_time) >= FEEDBACK_VIEWING_THRESHOLD):
                    break
            consequence_time = libtime.get_time()-image_start_time
            
            return consequence_dynamics_log, consequence_time, threat_shown
        elif (trial_info['exp_type']=='video'):
            pass
        
    def initialize_trial_end_screen(self):
        trial_end_screen = libscreen.Screen()
        
        self.points_earned = visual.TextStim(pygaze.expdisplay, pos=(0,480), color='#F5F500', 
                                             height=30)  #fontsize=height
        trial_end_screen.screen.append(self.points_earned)
        
        trial_end_instructions = visual.TextStim(pygaze.expdisplay, pos=(0,-450), color='#80FF40', 
                                          text='CLICK TO CONTINUE', height=28)
        trial_end_screen.screen.append(trial_end_instructions)
        
        self.accumulated_points = visual.TextStim(pygaze.expdisplay, pos=(0,440), color='#F5F500', 
                                           height=28)
        trial_end_screen.screen.append(self.accumulated_points)
        
        return trial_end_screen
                
    def show_trial_end_screen(self, points_earned, accumulated_points, threshold):
        self.mouse.set_visible(True)
        
        self.points_earned.setText(text='You have earned %i points' % (points_earned))
        self.accumulated_points.setText(text='Accumulated points: %i out of %i' % \
                                            (accumulated_points, threshold))
        
        self.disp.fill(self.trial_end_screen)
        self.disp.show()
        
        self.mouse.get_clicked()

        libtime.pause(500)


#    def initialize_rating_screen(self):
#        rating_screen = libscreen.Screen()
#
#        instruction_text_file = 'resources/%s_question.txt'
#        with open(instruction_text_file) as f:
#                instructions = f.read()
#
#        labels = []
#        label_size = 18        
#        
#        instructions_stim = visual.TextStim(self.win, text=instructions, units='pix', 
#                                            wrapWidth=1200,#pos=(0,DISPSIZE[1]/2-300), 
#                                            color='white', height=30)
#        rating_screen.screen.append(instructions_stim)
#
#        self.rating_buttons = []        
#        
#        for i, label in enumerate(labels):
#            button = visual.Rect(win=pygaze.expdisplay, 
#                    pos=(self.rating_button_pos[0]+self.button_x_offsets[i], 
#                         self.rating_button_pos[1]+self.button_y_offsets[i]),
#                    width=self.rating_button_size[0], height=self.rating_button_size[1],
#                    lineColor=(200,200,200), lineWidth=3, 
#                    lineColorSpace='rgb255', fillColor=None)
#            button_text = visual.TextStim(win=pygaze.expdisplay, text=labels[i], height=18,
#                      pos=(self.rating_button_pos[0]+self.button_x_offsets[i], 
#                           self.rating_button_pos[1]+self.button_y_offsets[i]))
#            self.rating_buttons.append(button)
#            
#            rating_screen.screen.append(button)
#            rating_screen.screen.append(button_text)
#
#        happyFace_img = visual.ImageStim(pygaze.expdisplay, 
#                                         image='resources/happyFace.png', 
#                                         pos=self.rating_emoticon_positions[0])
#        rating_screen.screen.append(happyFace_img)                                          
#        
#        neutralFace_img = visual.ImageStim(pygaze.expdisplay, 
#                                           image='resources/neutralFace.png', 
#                                           pos=self.rating_emoticon_positions[1])
#        rating_screen.screen.append(neutralFace_img)  
#
#        scaredFace_img = visual.ImageStim(pygaze.expdisplay, 
#                                          image='resources/scaredFace.png', 
#                                          pos=self.rating_emoticon_positions[2])
#        rating_screen.screen.append(scaredFace_img)   
#
#        return rating_screen
#
#    def show_rating_screen(self):
#        self.mouse.set_visible(True)
#        
#        self.disp.fill(self.rating_screen)
#        self.disp.show()        
#        
#        while(True):
#            for i, button in enumerate(self.rating_buttons):
#                if self.mouse.mouse.isPressedIn(button):
#                    return i
#            self.disp.fill(self.rating_screen)
#            self.disp.show()
    
    def close(self):
        self.disp.close()
           