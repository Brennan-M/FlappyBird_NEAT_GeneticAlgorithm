import numpy as np
import random
from datetime import datetime

class ann_feeder:

    def __init__(self, player, pipes):
        
        if player is not None and pipes is not None:
            self.player_ymin = player[0]
            self.player_ymax = player[1]

            self.pipes_x_min = pipes[0][0]
            self.pipes_x_max = pipes[0][1]

            self.pipes_y_min = pipes[1][0]
            self.pipes_y_max = pipes[1][1]

            random.seed(datetime.now())


    def update(self):
        pass


    def predict(self):
        random_output = np.random.randint(20)
        if random_output == 0:
            return True
        else:
            return False
        



