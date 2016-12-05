


class Innovation(object):


    def __init__(self):
        self.current_innovation_number = 0


    def get_new_innovation_number(self):
    	innovation_number = self.current_innovation_number
    	self.current_innovation_number += 1
    	return innovation_number

