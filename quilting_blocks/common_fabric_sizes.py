from collections import namedtuple

fabric_size = namedtuple("fabric_size", ["length", "width", "square_inches"])

FABRIC_CUTS = {
    "fat_quarter": fabric_size(18, 21, 378),
    "fat_eighth": fabric_size(9, 21, 189),
    "yard": fabric_size(36, 42, 1512),
    "fat_half": fabric_size(18, 42, 756),
    "fat_sixteenth": fabric_size(4.5, 21, 94.5),
    "half_yard": fabric_size(18, 42, 756),
    "quarter_yard": fabric_size(9, 21, 189),
    "eighth_yard": fabric_size(4.5, 21, 94.5),
}
