import logging
import sys
import math
from functools import reduce
from operator import attrgetter
from quilting_blocks.log_cabin import LogCabin
from quilting_blocks.common_fabric_sizes import FABRIC_CUTS

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def main():
    config = {
        "starting_square_completed": 4.5,
        "n_rounds": 7,
        "strip_width_completed": 0.5,
        "strip_width_completed_2": 2.0,
    }
    lc = LogCabin(config=config)
    lc.build_cabin()

    lc.organize_fabric_pieces()
    print("**********FABRIC 1 PIECES")
    print(lc.fabric_1_pieces)
    print("**********FABRIC 1 TOTAL LENGTH")
    print(lc.fabric_1_total_length)

    white = FABRIC_CUTS.get('fat_quarter')

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
                logger.debug(f"Fabric option {k} is sufficient")
                possible_options.append(k)
                # remove ceiling from below
        factor = 10
        yardage_val = math.ceil(max_length*factor/36)/factor
        possible_options.append(
            f"custom - {yardage_val} yards ({max_length} inches)")
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

    def foo(fabric, pieces_dict):
        """
        This function should be used once a fabric size has been selected
        """

        pieces = [i for v in pieces_dict.values() for i in v]
        pieces = sorted(pieces, key=attrgetter('length'), reverse=True)
        logger.debug(f"Sorted pieces: {pieces}")
        n_strips = {i.width: 0 for i in pieces}
        leftovers = {i.width: [] for i in pieces}
        cut_pieces = []
        uncut_pieces = []

        def _create_strip(fabric, piece, leftovers, cut_pieces):
            n_strips[piece.width] += 1
            cut_pieces.append(piece)
            if fabric.width - piece.length > 0:
                leftovers[piece.width].append(fabric.width - piece.length)
            return leftovers, cut_pieces

        for i, piece in enumerate(pieces):
            logger.debug(f"Piece {i}: {piece}")
            subcuts = leftovers.get(piece.width, [])
            logger.debug(f"Subcut: {subcuts}")
            if len(subcuts) > 0:
                if piece.length in subcuts:
                    subcuts.remove(piece.length)
                    cut_pieces.append(piece)
                    logger.info(f"Piece {i} matches subcut - {piece}")
                elif (max(subcuts) >= piece.length):
                    # find closest match:
                    closest = reduce(lambda x, y: x if x < y else y,
                                     filter(lambda x: x - piece.length > 0,
                                            subcuts))
                    subcuts.remove(closest)
                    remaining = closest - piece.length
                    if remaining > 0:
                        subcuts.append(remaining)
                    cut_pieces.append(piece)
                    logger.info(
                        f"Piece {i} cut from subcut with {remaining} "
                        f"remaining - {piece}")
                elif piece.length > fabric.width:
                    logger.debug(f"Piece {i} too long for subcut {piece}")
                    uncut_pieces.append(piece)
                else:
                    leftovers, cut_pieces = _create_strip(
                        fabric, piece, leftovers, cut_pieces)
                    logger.info(
                        f"Piece {i} cut from new strip of fabric - {piece}")
                leftovers[piece.width] = subcuts
            else:
                if piece.length > fabric.width:
                    logger.debug(f"Piece {i} too long for subcut {piece}")
                    uncut_pieces.append(piece)
                else:
                    leftovers, cut_pieces = _create_strip(
                        fabric, piece, leftovers, cut_pieces)
                    logger.info(
                        f"Piece {i} cut from new strip of fabric - {piece}")

        if len(uncut_pieces) > 0:
            logger.debug(f"{len(uncut_pieces)} uncut pieces: {uncut_pieces}")

        return n_strips, cut_pieces, leftovers

    logger.debug(f"white square inches: {white.square_inches}")
    logger.debug(f"required square inches: {lc.fabric_1_yardage}")
    logger.debug(f"sufficient sq inches: {
                 check_sq_inches(white, lc.fabric_1_yardage)}")
    logger.debug(f"sufficient length for largest piece: {
                 check_max_length(white, lc.fabric_1_pieces)}")
    logger.debug(f"fabric options: {
                 find_fabric_options(lc.fabric_1_pieces, lc.fabric_1_yardage)}")
    logger.debug(foo(white, lc.fabric_1_pieces))


if __name__ == '__main__':
    main()
