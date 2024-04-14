import logging
import sys
import math
from functools import reduce
from operator import attrgetter
from quilting_blocks.log_cabin import LogCabin
from quilting_blocks.common_fabric_sizes import FABRIC_CUTS

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("yardage_playground.log")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def check_sq_inches(fabric, required_sq_inches):
    return fabric.square_inches >= required_sq_inches


def max_dimension(pieces):
    max_length = reduce(lambda x, y: x if x > y else y, [
        i.length for v in pieces.values() for i in v])
    max_width = reduce(lambda x, y: x if x > y else y, [
        i.width for v in pieces.values() for i in v])
    return max(max_length, max_width), max_length, max_width


def find_fabric_options(pieces, pieces_sq_inches):
    """
    This function should help determine the best fabric size to use
    """
    _, max_length, max_width = max_dimension(pieces)
    possible_options = []
    for k, v in FABRIC_CUTS.items():
        if (v.length >= max_width and v.width >= max_length
                and check_sq_inches(v, pieces_sq_inches)):
            logger.debug(f"Fabric option {k} may be sufficient")
            possible_options.append(k)
    factor = 10
    sq_inches_val = math.ceil(max_length*factor/36)/factor
    possible_options.append(
        f"custom - {sq_inches_val} yards ({max_length} inches)")
    return possible_options


def check_max_length(fabric, pieces):
    """
    This function should help determine if the fabric size inputed is
    sufficient, if not, should recommend an alternative
    """
    max_val, _, _ = max_dimension(pieces)
    if max_val > max(fabric.length, fabric.width):
        logger.debug(
            f"Fabric piece too small for largest piece: {max_val}")
        logger.debug(
            f"Require at least {max_val} inches for largest piece")
        # Add logic to recommend a larger fabric size and use it
    return max_val <= max(fabric.length, fabric.width)


def _cut_fabric(fabric, piece, subcuts):
    if fabric.width - piece.length > 0:
        subcuts.append(fabric.width - piece.length)
    new_fabric = fabric._replace(length=fabric.length - piece.width)
    return subcuts, new_fabric


def get_sorted_pieces(pieces_dict):
    if len(pieces_dict) == 0:
        return []
    pieces = [i for v in pieces_dict.values() for i in v]
    return sorted(pieces, key=attrgetter('width', 'length'), reverse=True)


def foo(fabric, pieces_dict):
    """
    This function uses a greedy approach to determine how to cut a piece of
    fabric into the required pieces
    """

    pieces = get_sorted_pieces(pieces_dict)
    logger.debug(f"Sorted pieces: {pieces}")
    n_strips = {i.width: 0 for i in pieces}
    leftovers = {i.width: [] for i in pieces}
    accounted_pieces = []
    unaccounted_pieces = []

    logger.debug(f"Fabric size: {fabric}")
    for i, piece in enumerate(pieces):
        logger.debug(f"Piece {i}: {piece}")
        subcuts = leftovers.get(piece.width, [])
        logger.debug(f"Subcuts available: {subcuts}")
        if (
                (fabric.length >= piece.width)
                and ((len(subcuts) == 0)
                     or (piece.length > max(subcuts)))
        ):
            subcuts, fabric = _cut_fabric(
                fabric, piece, subcuts)
            n_strips[piece.width] += 1
            accounted_pieces.append(piece)
            logger.info(
                f"Piece {i} cut from new strip of fabric"
                f" now measuring {fabric.length}x{fabric.width}")
        elif len(subcuts) > 0 and piece.length <= max(subcuts):
            # find largest strip that will accommodate piece
            eligible = list(
                filter(lambda x: x - piece.length >= 0, subcuts))
            closest = (
                eligible[0] if len(eligible) == 1
                else reduce(lambda x, y: x if x < y else y, eligible)
            )
            subcuts.remove(closest)
            closest_fabric = fabric._replace(
                length=piece.width, width=closest, name="subcut")
            subcuts, _ = _cut_fabric(
                closest_fabric, piece, subcuts)
            accounted_pieces.append(piece)
            logger.info(f"Piece {i} cut from subcut")
        elif (
            (piece.length > fabric.width)
            or (piece.width > fabric.length)
        ):
            logger.debug(f"Piece {i} too long for fabric {piece}")
            unaccounted_pieces.append(piece)
            leftovers[piece.width] = subcuts

    logger.debug(f"{len(unaccounted_pieces)} pieces unaccounted for:"
                 f"{unaccounted_pieces}")

    return n_strips, accounted_pieces, leftovers


def main():
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

    fabric_1_options = find_fabric_options(
        lc.fabric_1_pieces, lc.fabric_1_sq_inches)
    fabric_2_options = find_fabric_options(
        lc.fabric_2_pieces, lc.fabric_2_sq_inches)
    logger.info("**********FABRIC 1 PIECES")
    logger.info(lc.fabric_1_pieces)
    logger.info("**********FABRIC 1 TOTAL LENGTH")
    logger.info(lc.fabric_1_total_length)
    logger.debug(f"white square inches: {white.square_inches}")
    logger.debug(f"required square inches: {lc.fabric_1_sq_inches}")
    logger.debug("sufficient sq inches:"
                 f"{check_sq_inches(white, lc.fabric_1_sq_inches)}")
    logger.debug("sufficient length for largest piece:"
                 f"{check_max_length(white, lc.fabric_1_pieces)}")
    logger.debug(f"fabric options: {fabric_1_options}")
    logger.debug(foo(white, lc.fabric_1_pieces))
    logger.info("\n\n**********FABRIC 2 PIECES")
    logger.info(lc.fabric_2_pieces)
    logger.info("**********FABRIC 2 TOTAL LENGTH")
    logger.info(lc.fabric_2_total_length)
    logger.debug(f"colour square inches: {colour.square_inches}")
    logger.debug(f"required square inches: {lc.fabric_2_sq_inches}")
    logger.debug("sufficient sq inches:"
                 f"{check_sq_inches(colour, lc.fabric_2_sq_inches)}")
    logger.debug("sufficient length for largest piece:"
                 f"{check_max_length(colour, lc.fabric_2_pieces)}")
    logger.debug(f"fabric options: {fabric_2_options}")
    logger.debug(foo(colour, lc.fabric_2_pieces))


if __name__ == '__main__':
    main()
