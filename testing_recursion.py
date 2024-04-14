from quilting_blocks.common_fabric_sizes import FABRIC_CUTS
from quilting_blocks.log_cabin import LogCabin
import yardage_playground as yp
import itertools
from functools import reduce


white = FABRIC_CUTS.get('fat_quarter')
colour = FABRIC_CUTS.get('fat_quarter')
config = {
    "starting_square_completed": 4.5,
    "n_rounds": 7,
    "strip_width_completed": 0.5,
    "strip_width_completed_2": 1.75,
}
lc = LogCabin(config=config)
lc.build_cabin()

lc.organize_fabric_pieces()

yp.find_fabric_options(lc.fabric_1_pieces, lc.fabric_1_sq_inches)

max_val = 40  # white.width
pieces = yp.get_sorted_pieces(lc.fabric_1_pieces)
pieces = pieces*4
print(pieces)
unique_sets = {}


def check_for_nonoverlapping_sets(c):
    n_items = reduce(lambda a, b: a + b, map(lambda y: len(y), c))
    n_unique_items = len(set.union(*map(set, c)))
    return n_items == n_unique_items


for i in range(1, len(pieces)):
    unique_sets[i] = {}
    combos = itertools.combinations(pieces, i)
    n_combos = len(list(itertools.combinations(pieces, i)))
    print(f"{n_combos} combinations of size {i}")
    complete_combos = filter(lambda x:
                             reduce(lambda a, b: a + b,
                                    map(lambda y: y.length, x)) == max_val,
                             combos)
    complete_combos = list(complete_combos)
    print(f"{len(complete_combos)} complete combos of size {i}")
    # need to get the piece_id for each item in the complete_combos
    # determine if there are any non-overlapping sets of pieces
    # to create mulitple subcuts
    if len(complete_combos) > 0:
        piece_ids = [tuple(map(lambda x: x.piece_id, combo))
                     for combo in complete_combos]
        if len(piece_ids) > 1:
            print(f"piece_ids: {piece_ids}")
            # check for overlapping pieces
            for c in range(2, len(piece_ids) + 1):
                unique_sets[i][c] = []
                print(f"checking for {c} overlapping pieces")
                for combo in itertools.combinations(piece_ids, c):
                    if check_for_nonoverlapping_sets(combo):
                        unique_sets[i][c].append(combo)
                        print(f"combo: {combo}")
                        # remove from pieces/piece_ids
        pass
