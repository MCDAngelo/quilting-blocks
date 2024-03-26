import logging
import sys

from collections import namedtuple

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("log_cabins.log")

formatter = logging.Formatter('[%(asctime)s] - %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

## Add in Block class that other blocks inherit from, that contains
## attributes to get current/final size, stores common final sizes, 
## dictionaries to track pieces and amount of fabric needed
DEFAULT_SEAM_ALLOWANCE = 0.25

class QuiltingBlock:
    finished_size = namedtuple("finished_size", ["width", "height"])
    pass


class LogCabin:

    def __init__(self, config):
        self.strip_width_1 = config.get("strip_width_completed", 1)
        self.starting_square = config.get("starting_square_completed", 2)
        self.x = self.starting_square
        self.y = self.starting_square
        self.n_rounds = config.get("n_rounds", 2)
        self.strip_width_2 = config.get("strip_width_2", self.strip_width_1)
        self.seam_allowance = config.get("seam_allowance", DEFAULT_SEAM_ALLOWANCE)
        self.sides = ['Top', 'Right', 'Bottom', 'Left']
        self.sides_dict = {
                'Top':  [],
                'Right': [],
                'Bottom': [],
                'Left':  [],
         }
        self.pieces_dict = {}

        logger.info(f"Initializing log cabin with the following parameters:\n  {config}")

    def add_side(self, current_sizes, side, width):
        added_value = width - 2*self.seam_allowance
        if side in ['Top', 'Bottom']:
            self.sides_dict['Top'].append(current_sizes['Top'])
            self.sides_dict['Bottom'].append(current_sizes['Bottom'])
            self.sides_dict['Right'].append(current_sizes['Right'] + added_value)
            self.sides_dict['Left'].append(current_sizes['Left'] + added_value)
        else:
            self.sides_dict['Top'].append(current_sizes['Top'] + added_value)
            self.sides_dict['Bottom'].append(current_sizes['Bottom'] + added_value)
            self.sides_dict['Right'].append(current_sizes['Right'])
            self.sides_dict['Left'].append(current_sizes['Left'])
        for side in self.sides:



    def build_round(self, round, width):
        for side in self.sides:
            current_sizes = {k: v[-1] for k, v in self.sides_dict.items()}
            self.pieces_dict[side].append((round, width, current_sizes[side]))
            T,R,B,L = add_side(current_sizes, side, width, self.seam_allowance)
            sides_dict = update_function(sides_dict, T,R,B,L) to append new sizes

    def build_cabin():
        # have two width values for even vs. odd rounds
        for i in rounds:
            if i % 2 == 0:
                add_round(i, w = w_even)
            else:
                add_round(i, w = w_odd)

# need to add seam_allowance
# if starting with a square:
# the top, botton, right, left sides are all equal to the length of the square
# assume adding strips clockwise starting from top
# when adding to top or bottom, theres no change to the lengths of top or bottom
# left and right sides are updatedi, and vice versa. 
# sides are updated with this formula (X' - self.seam_allowance) + (W - SA) or X' + W - 2SA
# where self.seam_allowance = seam allowance, X' = starting length, W = width of strip being added

# Ideas:
# have a dictionary to keep track of the sides each round:
# {'top': [(1, x), (2, x2), ...]} - so a list of named tuples (round, length)
# and a separate dictionary to keep track of the pieces that are needed:
# {'top' : [(1, w, x), (3, w, x2), ...]} - list of named tuples (round, width, piece length)



if __name__ == '__main__': 
    config = {
            "starting_square_completed": 5,
            "n_rounds": 2,
            "seam_allowance": 0.25,
            "strip_width_completed": 1,
        }

    lc = LogCabin(config = config)
    print(lc.x)
    print(lc.y)
    print(lc.strip_width_1)
    print(lc.strip_width_2)


    qb = QuiltingBlock()



