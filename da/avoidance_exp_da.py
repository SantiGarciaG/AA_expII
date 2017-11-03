from constants import *
import random, csv
import numpy as np
from datetime import datetime
import os

# This class implements data access layer of AvoidanceExp (primarily, logging).
# All data outputs are stored in tab-delimited format in txt files in 'data' folder
class AvoidanceExpDA:                                     
    # stubs for experiment-level variables
    exp_info = {}
    
#    TODO: check if commenting these works?
    response_dynamics_log_file = ''
    consequence_log_file = ''       
    choices_log_file = ''
    scores_log_file = ''
    
    def __init__(self):
        self.exp_info['exp_type'] = EXP_TYPE
        self.exp_info['subj_id'] = self.generate_subj_id()        
        self.exp_info['start_time'] = datetime.strftime(datetime.now(), '%b_%d_%Y_%H_%M_%S')
        self.initialize_log()
    
    def initialize_log(self):
        log_path = 'data/%s'
        log_name = log_path + '/' + self.exp_info['subj_id'] + '_' + \
                self.exp_info['start_time'] + '_%s_%s.txt'

        self.response_dynamics_log_file = log_name % ('dynamics', 'dynamics', 
                                                      self.exp_info['exp_type'])        
        self.consequence_dynamics_log_file = log_name % ('consequence', 'consequence', 
                                                         self.exp_info['exp_type']) 
        self.choices_log_file = log_name % ('choices', 'choices', 
                                            self.exp_info['exp_type'])
        self.scores_log_file = log_path % 'scores.txt'
        
        if not os.path.exists(log_path % 'dynamics'):
            os.makedirs(log_path % 'dynamics')
        if not os.path.exists(log_path % 'consequence'):
            os.makedirs(log_path % 'consequence')
        if not os.path.exists(log_path % 'choices'):
            os.makedirs(log_path % 'choices')
            
        with open(self.response_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'block_no', 'trial_no', 'timestamp', 
                             'mouse_x', 'mouse_y', 'pupil_size', 'eye_x', 'eye_y'])
                             
        with open(self.consequence_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'block_no', 'trial_no', 'timestamp', 
                             'pupil_size', 'eye_x', 'eye_y'])
        
        with open(self.choices_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'block_no', 'trial_no', 'is_red_left', 'card_chosen', 
                             'points_earned', 'threat', 'red_reward', 'blue_reward', 
                             'response_time', 'image_time'])

    def write_trial_log(self, response_dynamics_log, consequence_dynamics_log, choice_info): 
        with open(self.response_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerows(response_dynamics_log)

        with open(self.consequence_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerows(consequence_dynamics_log)
            
        with open(self.choices_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(choice_info)

    def write_score_log(self, baseline, lower_bound, upper_bound):
        with open(self.scores_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow([self.exp_info['subj_id'], self.exp_info['exp_type'], 
                             baseline, lower_bound, upper_bound]) 
            
    # this function generates new random subject id if one is not provided in constants.py
    # (which is only the case for experiments requiring multiple sessions with each subject)
    def generate_subj_id(self):
        file_name = 'existing_subj_ids.txt'
        try:
            f = open(file_name, 'r')
        except IOError:
            with open(file_name, 'w') as f:
                f.write('666\n')
    
        if SUBJ_ID is None:
            existing_subj_ids = np.loadtxt(file_name)
            subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
            while subj_id in existing_subj_ids:
                subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
    
            with open(file_name, 'ab+') as fp:
#                fp.write(str(subj_id)+'\n')
                writer = csv.writer(fp, delimiter = '\t')
                writer.writerow([str(subj_id)])
        else:
            subj_id = SUBJ_ID
        return str(subj_id)