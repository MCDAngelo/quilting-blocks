import logging
import sys

from collections import namedtuple, Counter

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("log_cabins.log")

formatter = logging.Formatter('[%(asctime)s] - %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

# Add in Block class that other blocks inherit from, that contains
# attributes to get current/final size, stores common final sizes,
# dictionaries to track pieces and amount of fabric needed


class QuiltingBlock:
    block_size = namedtuple("block_size", ["width", "height"])
    default_seam_allowance = 0.25
    pass


class LogCabin(QuiltingBlock):
    # if starting with a square:
    # the top, botton, right, left sides are all equal to the length of the square
    # assume adding strips clockwise starting from top
    # when adding to top or bottom, theres no change to the lengths of top/bottom
    # left and right sides are updated, and vice versa.
    # sides are updated with this formula (X' - self.seam_allowance) + (W - SA)
    # or X' + W - 2SA
    # where self.seam_allowance = seam allowance, X' = starting length,
    # W = width of strip being added
    piece_info = namedtuple("piece_info", ["round", "width", "length"])
    sides = ['Top', 'Right', 'Bottom', 'Left']

    def __init__(self, config):
        self.seam_allowance = config.get(
            "seam_allowance", self.default_seam_allowance)
        self.strip_width_completed_1 = config.get("strip_width_completed", 1)
        self.strip_width_1 = self.add_seam_allowance(
            self.strip_width_completed_1)
        self.starting_square_completed = config.get(
            "starting_square_completed", 2)
        self.starting_square = self.add_seam_allowance(
            self.starting_square_completed)
        self.n_rounds = config.get("n_rounds", 2)
        self.strip_width_completed_2 = config.get(
            "strip_width_completed_2", self.strip_width_completed_1)
        self.strip_width_2 = self.add_seam_allowance(
            self.strip_width_completed_2)
        self.pieces_dict = {
            'Middle': [self.piece_info(
                0, self.starting_square, self.starting_square
            )],
            'Top':  [],
            'Right': [],
            'Bottom': [],
            'Left': [],
        }
        self.sides_dict = {
            'Top': [self.starting_square],
            'Right': [self.starting_square],
            'Bottom': [self.starting_square],
            'Left': [self.starting_square],
        }
        self.round_sizes = {
            0: self.block_size(self.starting_square, self.starting_square),
        }

        logger.info("Initializing log cabin with the following parameters:")
        logger.info(self.get_config())
        logger.debug(f"sides_dict = {self.sides_dict}")
        logger.debug(f"pieces_dict = {self.pieces_dict}")

    def get_config(self):
        return {
            "seam_allowance": self.seam_allowance,
            "strip_width_completed_1": self.strip_width_completed_1,
            "starting_square_completed": self.starting_square_completed,
            "n_rounds": self.n_rounds,
            "strip_width_completed_2": self.strip_width_completed_2,
        }

    def add_seam_allowance(self, x):
        return x + 2*self.seam_allowance

    def add_side(self, current_sizes, side, width):
        added_value = width - 2*self.seam_allowance
        if side in ['Top', 'Bottom']:
            self.sides_dict['Top'].append(current_sizes['Top'])
            self.sides_dict['Bottom'].append(current_sizes['Bottom'])
            self.sides_dict['Right'].append(
                current_sizes['Right'] + added_value)
            self.sides_dict['Left'].append(current_sizes['Left'] + added_value)
        else:
            self.sides_dict['Top'].append(current_sizes['Top'] + added_value)
            self.sides_dict['Bottom'].append(
                current_sizes['Bottom'] + added_value)
            self.sides_dict['Right'].append(current_sizes['Right'])
            self.sides_dict['Left'].append(current_sizes['Left'])
        logger.info(f"{side} side added, current sizes now updated:")
        logger.info(f"{({k: v[-1] for k, v in self.sides_dict.items()})}")

    def build_round(self, round, width):
        for side in self.sides:
            logger.info(f"Adding {width} strip to {side.lower()} side.")
            current_sizes = {k: v[-1] for k, v in self.sides_dict.items()}
            self.pieces_dict[side].append(
                self.piece_info(round, width, current_sizes[side]))
            self.add_side(current_sizes, side, width)
        self.round_sizes[round] = self.block_size(
            self.sides_dict['Top'][-1], self.sides_dict['Right'][-1])

    def build_cabin(self):
        for i in range(1, self.n_rounds + 1):
            logger.info(f"Starting round {i} of {self.n_rounds} rounds.")
            if i % 2 == 0:
                self.build_round(i, width=self.strip_width_2)
            else:
                self.build_round(i, width=self.strip_width_1)

        self.block_size_unfinished = self.block_size(
            self.sides_dict['Top'][-1], self.sides_dict['Right'][-1])
        self.block_size_finished = self.block_size(
            self.block_size_unfinished.width - self.seam_allowance,
            self.block_size_unfinished.height - self.seam_allowance)

        logger.info(f"Final sizes of sides: {self.block_size}")
        logger.info(f"Final pieces: {self.pieces_dict}")

    def organize_fabric_pieces(self):
        self.fabric_1_pieces = {k: [i for i in v if i.round % 2 == 1]
                                for k, v in self.pieces_dict.items()}
        self.fabric_1_rounds = [
            i for i in range(1, self.n_rounds + 1) if i % 2 == 1]
        self.fabric_2_pieces = {k: [i for i in v if i.round % 2 == 0]
                                for k, v in self.pieces_dict.items()}
        self.fabric_2_rounds = [
            i for i in range(0, self.n_rounds + 1) if i % 2 == 0]
        logger.info(f"Pieces required for fabric one: \n\
        {self.fabric_1_pieces}")
        logger.info(f"Pieces required for fabric two: \n\
        {self.fabric_2_pieces}")
        self.fabric_1_pieces_count = Counter(
            [i for v in self.fabric_1_pieces.values() for i in v]
        )
        self.fabric_2_pieces_count = Counter(
            [i for v in self.fabric_2_pieces.values() for i in v]
        )
        self.calculate_sq_inches()

    def format_fabric_pieces(self, fabric_pieces):
        return "\n".join(
            [f"{k}: round {i.round} - {i.width} x {i.length}"
                for k, v in fabric_pieces.items()
                for i in v])

    def save_fabric_pieces(self, file_name):
        # And save in separate lines for ease of use
        # check file info stuff?
        with open(file_name, 'w') as f:
            # clean up to DRY
            f.write("=========Log Cabin Quilt Block=========\n")
            f.write("~Sizes per round: \n")
            f.write("\n".join(
                [f"Round {k}: {v.width} x {v.height}"
                    for k, v in self.round_sizes.items()]))
            f.write("\n")
            f.write("=========Fabric one: =========\n")
            f.write(f"~Total squared inches: {self.fabric_1_sq_inches}\n")
            f.write(f"~Rounds: {self.fabric_1_rounds}\n")
            f.write(self.format_fabric_pieces(self.fabric_1_pieces))
            f.write("\n~Summarized pieces required: \n")
            f.write("\n".join(
                [f"{v} x {k}" for k, v in self.fabric_1_pieces_count.items()])
            )
            f.write("\n")
            f.write("=========Fabric two: =========\n")
            f.write(f"~Total squared inches: {self.fabric_2_sq_inches}\n")
            f.write(f"~Rounds: {self.fabric_2_rounds}\n")
            f.write(self.format_fabric_pieces(self.fabric_2_pieces))
            f.write("\n~Summarized pieces required: \n")
            f.write("\n".join(
                [f"{v} x {k}" for k, v in self.fabric_2_pieces_count.items()])
            )

    def calculate_sq_inches(self):
        def _square_inches_helper(fabric_pieces):
            return sum(
                [i.width * i.length for v in fabric_pieces.values() for i in v]
            )

        def _length_helper(fabric_pieces):
            return sum(
                [i.length for v in fabric_pieces.values()
                 for i in v if i.round > 0]
            )

        self.fabric_1_sq_inches = _square_inches_helper(
            self.fabric_1_pieces
        )
        self.fabric_2_sq_inches = _square_inches_helper(
            self.fabric_2_pieces
        )
        self.fabric_1_total_length = _length_helper(
            self.fabric_1_pieces
        )
        self.fabric_2_total_length = _length_helper(
            self.fabric_2_pieces
        )

        # Add up lengths of pieces for each fabric that have the same width
        # Then, assuming a width of 42 inches for the fabric, start with a
        # naive approach of dividing the total length by 42 to get the number
        # of strips required for that width.
        # To improve the naive approach, sort the pieces of fabric by length
        # and then iterate through the pieces, combining pieces that have
        # lengths that add up to 42 or less. This will give the minimum number
        # of strips required for the fabric.
        # Alternatively, the naive approach can start with one strip for each
        # piece of fabric, and then combine strips that have a total length
        # of 42 or less until no further combinations can be found.
        # This is a greedy approach, but it should work for the purposes of
        # this exercise.
        # An alternative approach would be to use dynamic programming
        # to find the minimum number of strips required for the fabric.
