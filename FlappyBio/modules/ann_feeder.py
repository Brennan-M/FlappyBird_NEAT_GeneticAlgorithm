import numpy as np
import random
from datetime import datetime

class ann_feeder:

    def __init__(self):
        
        
        random.seed(datetime.now())


    def update(self, player, pipes):
        self.player_top = player.top
        self.player_bottom = player.bottom

        self.pipes_top = pipes.top
        self.pipes_bottom = pipes.bottom
        self.pipes_left = pipes.left
        self.pipes_right = pipes.right


    def predict(self):
        random_output = np.random.randint(15)
        if random_output == 0:
            return True
        else:
            return False
        



