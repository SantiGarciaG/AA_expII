from pygaze import libtime
from constants import *
import numpy as np
import random
from ui.limitsAA_exp_ui import AvoidanceExpUI
from da.limitsAA_exp_da import AvoidanceExpDA
from et.limitsAA_exp_et import AvoidanceExpET

# AvoidanceExp class provides high-level functions controlling the flow 
# of the experiment. To run the experiment, just create the instance of the class and call run_exp()
class AvoidanceExp:    
    def __init__(self):
        self.user_interface = AvoidanceExpUI()        
        self.data_access = AvoidanceExpDA()
        self.eye_tracker = AvoidanceExpET(user_interface=self.user_interface, 
                                 subj_id=self.data_access.exp_info['subj_id'])
        self.exp_info = self.data_access.exp_info
           
    def run_exp(self, test_mode=False):
        libtime.expstart()
        self.user_interface.show_experiment_start_screen()
        self.user_interface.show_practice_start_screen()
        
        is_threat_left = random.choice([False, True])
        
        if not test_mode:
            for pract_block in range(2):
                self.run_block(pract_block-2, PRACTICE_REWARDS[pract_block], MIN_PRACTICE_TRIALS, 
                               is_threat_left=is_threat_left, is_baseline=True)
                is_threat_left = not is_threat_left
    
            self.user_interface.show_practice_end_screen()
            
            for baseline_block in range(1):
                self.run_block(baseline_block, INITIAL_REWARDS, MIN_N_TRIALS, 
                               is_threat_left=is_threat_left, is_baseline=True)
                is_threat_left = not is_threat_left
        
        lower_bound, upper_bound = 0, 0
        rewards = INITIAL_REWARDS
        threat_preferred = False
        block_no=1
        
        '''
        First, we run the "forward" sequence of blocks: assuming that participants would start from the
        avoid behavior, we try to find the minimum reward for 'approach' which would 
        force them to switch from the avoid behavior.
        '''
        while (not threat_preferred):
#        for i in range(1, N_BLOCKS+1):        
            # REMEMBER: rewards[0] is reward for threat card; rewards[1] is neutral card         
            block_info = self.run_block(block_no, rewards, MIN_N_TRIALS, is_threat_left=is_threat_left, 
                                   is_baseline=False)
            # by just putting > if the response distribution reaches the exact threshold it is 
            # defaulted to decrease the lower pay option -avoid- (otherwise use >= )
            p_threat = block_info[2] 
            if p_threat < P_THRESHOLD:
                # if threat option was chosen in less than 50% of the trials,
                # increase the appeal of the threat option                    
                rewards[0] = rewards[0] + REWARD_DIFFERENCE
            else:
                # if threat was chosen in more than 50% of the trials, we start 
                # a second sequence of blocks with threat reward decreasing.
                # for this, we need to exit the while loop, which will be done as soon as 
                # threat_preferred is True
                upper_bound = rewards[0]
                rewards[0] = rewards[0] - REWARD_DIFFERENCE
                threat_preferred = True
        
            self.data_access.write_block_log(block_info)
            # Here the value is changed in every block / iteration of 'for' loop
            # (from what was before depending on the number of iterations). 
            # So it starts with club_left = True and changed after the next iteration to = False, 
            # and after the second iteration the False is Not more (i.e., True)
            is_threat_left = not is_threat_left 
            block_no+=1            
            
            if block_no > MAX_N_BLOCKS:
                lower_bound = 0
                upper_bound = 0                
                threat_preferred = False
                break
        
        forward_blocks_number = block_no
        '''
        Second, when a participant switches to the approach behavior, we start the "reversed" 
        sequence of blocks. In this sequence, we gradually decrease the reward for approaching the
        threat until the participant switches back to 'avoid'.        
        '''
        while (threat_preferred):
            block_info = self.run_block(block_no, rewards, MIN_N_TRIALS, is_threat_left=is_threat_left, 
                                   is_baseline=False)  
            p_threat = block_info[2] 
            if p_threat > P_THRESHOLD:
                rewards[0] = rewards[0] - REWARD_DIFFERENCE
            else:
                lower_bound = rewards[0]
                threat_preferred = False
            
            self.data_access.write_block_log(block_info)
            
            is_threat_left = not is_threat_left 
            block_no+=1
            
            if block_no-forward_blocks_number > MAX_N_BLOCKS:
                break
        
        self.eye_tracker.close()    
        libtime.pause(500)
                
        self.data_access.write_score_log(baseline=INITIAL_REWARDS[1],
                                         lower_bound=lower_bound, 
                                         upper_bound=upper_bound)

        self.user_interface.show_experiment_end_screen(lower_bound, upper_bound)
        
        # With this function ALL of the screens are ended
        self.user_interface.close()
        
    #------ WE CREATE A FUNCTION THAT WILL RUN THE CONTENTS OF A BLOCK ----------             
    def run_block(self, block_number, rewards, min_n_trials, is_threat_left=True, is_baseline=False):
        self.eye_tracker.calibrate()

        # The threshold is set by taking the max reward and multiplying it by the minimum number 
        # of trials per block (MIN_N_TRIALS)
        threshold = min_n_trials * max(rewards)
        self.user_interface.show_block_start_screen(threshold)
        
        # We create the variable that will contain the points
        accumulated_points = 0
        
        # We create a tuple to append the selections made by participants and be 
        # able to calculate deck-preference
        cards_chosen = []
        
        trial_no = 1
        # This is the loop for proceeding to the next block
        while accumulated_points < threshold:             
            card_chosen, points_earned, response_dynamics_log, consequence_dynamics_log, \
                choice_info = \
                    self.run_trial(accumulated_points, threshold, block_number, trial_no, rewards,
                                   is_threat_left, is_baseline)
                                   
            self.data_access.write_trial_log(response_dynamics_log, consequence_dynamics_log, 
                                             choice_info)  
            
            if card_chosen == 'Threat':
                # so 1 represent the 'threat' deck 
                cards_chosen.append(1)
            else:
                # so 0 represent the 'neutral' deck 
                cards_chosen.append(0)
                
            accumulated_points += points_earned
            # We update the variable adding 1 per trial iteration            
            trial_no += 1
        p_threat = np.array(cards_chosen).mean() 

        scale_rating = self.user_interface.show_rating_screen()

        # We show the interblock message after each block except for the last one
        if block_number < 4:
            self.user_interface.show_block_end_screen()
        
#        while not self.mouse.get_clicked():                
#            self.user_interface.show_block_end_screen()        
        
        block_info = [self.exp_info['subj_id'], block_number, p_threat, scale_rating]
        # The calculated probability of preferring the 'club' deck 
        return block_info
            
    def run_trial(self, accumulated_points, threshold, block_no, trial_no, rewards,
                  is_threat_left=True, is_baseline=False):
        trial_info = {'exp_type': self.exp_info['exp_type'],
                      'subj_id': self.exp_info['subj_id'],                      
                      'block_no': block_no,
                      'trial_no': trial_no,
                      'rewards': rewards,
                      'is_threat_left': is_threat_left,
                      'is_baseline': is_baseline}
        self.user_interface.show_trial_start_screen()

        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_no, trial_no))

#        self.user_interface.show_pre_decks_screen()                                  # *****************

        response_dynamics_log, card_chosen, response_time = self.user_interface.show_decks_screen(                                                                    
                                                                    trial_info=trial_info,
                                                                    tracker=self.eye_tracker)
        self.eye_tracker.stop_recording()

        trial_info['card_chosen'] = card_chosen
        points_earned = 0
        # this if is for the experimental blocks
        if card_chosen == 'Threat':
            points_earned = rewards[0]
        elif card_chosen == 'Neutral':
            points_earned = rewards[1] 
            
        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_no, trial_no))
        consequence_dynamics_log, consequence_time, threat_shown = \
                        self.user_interface.show_consequence_screen(trial_info, self.eye_tracker)
        self.eye_tracker.stop_recording()
        
        self.user_interface.show_trial_end_screen(points_earned, accumulated_points+points_earned,
                                                  threshold)

        choice_info = [self.exp_info['subj_id'], block_no, trial_no, is_threat_left, card_chosen, 
                       points_earned, threat_shown, rewards[0], rewards[1], 
                        response_time, consequence_time]

#        # drift correction after every fifth trial
        if trial_no % 5 == 0:
            self.eye_tracker.correct_drift()        
        
        return card_chosen, points_earned, response_dynamics_log, consequence_dynamics_log, \
                choice_info
        
    def calculate_score(self, rewards, p_club):
        score = rewards[0] - rewards[1] 
        if p_club > 0.5:
            score -= 0.5
        else:
            score += 0.5
        return score


# Comment these two below if exp run from "run_exp..." file
avoid_exp = AvoidanceExp()
avoid_exp.run_exp(test_mode=True) 
#avoid_exp.run_exp() 
