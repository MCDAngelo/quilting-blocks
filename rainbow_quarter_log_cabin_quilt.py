import math

from quilting_blocks.log_cabin import LogCabin
from quilting_blocks.common_fabric_sizes import FABRIC_CUTS


config = {
    "starting_square_completed": 4.5,
    "n_rounds": 7,
    "strip_width_completed": 1.0,
    "strip_width_completed_2": 2.0,
}

lc = LogCabin(config=config)
lc.build_cabin()
lc.organize_fabric_pieces()
lc.save_fabric_pieces("rainbow_log_cabin.txt")
pieces = lc.pieces_dict

block_size_finished = lc.block_size_finished

print(f"finished blocks will be: {block_size_finished}")

block_height_on_point = math.sqrt(block_size_finished.width**2 +
                                  block_size_finished.height ** 2)

# Quarter log cabin information:
print("4 quarter log cabins from one log cabin block")
quarter_block_height_on_point = block_height_on_point / 2
print(f"Quarter block height/width on point: \
{round(quarter_block_height_on_point, 1)}")

print(f"For a 45\" square quilt, the quilt will be \
{round(45/quarter_block_height_on_point, 1)} blocks high and wide")

print(f"A quilt that is 3 quarter blocks high and wide will be \
{round(quarter_block_height_on_point*3, 1)} inches tall/wide")

width_of_quilt = 3*quarter_block_height_on_point
quilt_area = width_of_quilt**2
print(f"A 3x3 quarter log cabin (on point) quilt will be \
{round(quilt_area, 1)} square inches")

block_area = (block_size_finished.height * block_size_finished.width) / 4

number_of_quarter_blocks = quilt_area / block_area
print(f"A 3x3 quarter log cabin (on point) quilt will require \
{round(number_of_quarter_blocks, 1)} log cabin blocks")


white_fabric = FABRIC_CUTS.get('fat_quarter')

quarter_lc_per_white_fq = white_fabric.square_inches / (
    lc.fabric_1_yardage / 4)
print(f"Each fat quarter of white can make \
{quarter_lc_per_white_fq} quarter log cabin blocks")
