from pygaze import libtime
from constants import *
import numpy as np
from ui.avoidance_exp_ui import AvoidanceExpUI
from da.avoidance_exp_da import AvoidanceExpDA
from et.avoidance_exp_et import AvoidanceExpET

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
        
        is_club_left = False
        
        if not test_mode:
            for pract_block in range(2):
                self.run_block(pract_block-2, PRACTICE_REWARDS[pract_block], MAX_PRACTICE_TRIALS, 
                               is_club_left=is_club_left, is_baseline=True)
                is_club_left = not is_club_left
    
            self.user_interface.show_practice_end_screen()
            
            for baseline_block in range(1):
                self.run_block(baseline_block, INITIAL_REWARDS, MAX_N_TRIALS, 
                               is_club_left=is_club_left, is_baseline=True)
                is_club_left = not is_club_left
            
        rewards = INITIAL_REWARDS
        for i in range(1, N_BLOCKS+1):
            # Taking club-deck as reference, 
            # REMEMBER: rewards[0] is reward for club card; rewards[1] is spade card         
            p_club = self.run_block(i, rewards, MAX_N_TRIALS, is_club_left=is_club_left, 
                                   is_baseline=False)  
            
            # We don't adjust the rewards after the last block is finished            
            if i < N_BLOCKS:
                # This is just to have a fall back value if no criteria is specified 
                threshold = 0.5
                if THRESHOLD_TYPE == 'fixed': 
                    threshold = P_THRESHOLD
                elif THRESHOLD_TYPE == 'matching':
                    threshold = rewards[0]/(rewards[0] + rewards[1])
                
                # by just putting > if the response distribution reaches the exact threshold it is 
                # defaulted to decrease the lower pay option -avoid- (otherwise use >= )
                if p_club >= threshold:     
                    # i (taken from the for loop) is used here to index the reward decrease rate 
                    # depending on iterations
                    rewards[0] = rewards[0] - REWARD_DIFFERENCE[i-1] 
                else:
                    # this means that if the first condition is not met, we decrease the reward of 
                    # spade deck 
                    rewards[1] = rewards[1] - REWARD_DIFFERENCE[i-1] 
                    # (if the event of rising the P_THRESHOLD an extra condition 
                    # might be needed for values below the selected threshold)           
                    
            # Here the value is changed in every block / iteration of 'for' loop
            # (from what was before depending on the number of iterations). 
            # So it starts with club_left = True and changed after the next iteration to = False, 
            # and after the second iteration the False is Not more (i.e., True)
            is_club_left = not is_club_left   
        
        self.eye_tracker.close()    
        libtime.pause(500)
        
        score = self.calculate_score(rewards, p_club)
        
        self.data_access.write_score_log(score)

        self.user_interface.show_experiment_end_screen(score)
        
        # With this function ALL of the screens are ended
        self.user_interface.close()
        
    #------ WE CREATE A FUNCTION THAT WILL RUN THE CONTENTS OF A BLOCK ----------             
    def run_block(self, block_number, rewards, max_n_trials, is_club_left=True, is_baseline=False):
        self.eye_tracker.calibrate()

#        scale_rating = self.user_interface.show_rating_screen()                        # mmmmmmmm
        
        # The threshold is set by taking the minimum rewards and multiplying it by the value 
        # in the constant MAX_N_TRIALS
        threshold = max_n_trials * min(rewards)
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
                                   is_club_left, is_baseline)
                                   
            self.data_access.write_trial_log(response_dynamics_log, consequence_dynamics_log, 
                                             choice_info)  
            
            if card_chosen == 'Club':
                # so 1 represent the 'club' deck 
                cards_chosen.append(1)
            else:
                # so 0 represent the 'spade' deck 
                cards_chosen.append(0)
                
            accumulated_points += points_earned
            # We update the variable adding 1 per trial iteration            
            trial_no += 1
        p_club = np.array(cards_chosen).mean() 

         # we collect and save the "scale_rating" after the block ??????                 # mmmmmmmm
#        scale_rating = self.user_interface.show_rating_screen()                         # mmmmmmmm

        # We show the interblock message after each block except for the last one
        if block_number < 4:                
            self.user_interface.show_block_end_screen()
                   
        # The calculated probability of preferring the 'club' deck 
        return p_club
            
    def run_trial(self, accumulated_points, threshold, block_no, trial_no, rewards,
                  is_club_left=True, is_baseline=False):
        trial_info = {'exp_type': self.exp_info['exp_type'],
                      'subj_id': self.exp_info['subj_id'],                      
                      'block_no': block_no,
                      'trial_no': trial_no,
                      'rewards': rewards,
                      'is_club_left': is_club_left,
                      'is_baseline': is_baseline}
        self.user_interface.show_trial_start_screen()

        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_no, trial_no))

        self.user_interface.show_pre_decks_screen()                                  # *****************

        response_dynamics_log, card_chosen, response_time = self.user_interface.show_decks_screen(                                                                    
                                                                    trial_info=trial_info,
                                                                    tracker=self.eye_tracker)
        self.eye_tracker.stop_recording()

        trial_info['card_chosen'] = card_chosen
        points_earned = 0
        # this if is for the experimental blocks
        if card_chosen == 'Club':
            points_earned = rewards[0]
        elif card_chosen == 'Spade':
            points_earned = rewards[1] 
            
        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_no, trial_no))
        consequence_dynamics_log, consequence_time, threat_shown = \
                        self.user_interface.show_consequence_screen(trial_info, self.eye_tracker)
        self.eye_tracker.stop_recording()
        
        self.user_interface.show_trial_end_screen(points_earned, accumulated_points+points_earned,
                                                  threshold)

        choice_info = [self.exp_info['subj_id'], block_no, trial_no, is_club_left, card_chosen, 
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
avoid_exp.run_exp() 
