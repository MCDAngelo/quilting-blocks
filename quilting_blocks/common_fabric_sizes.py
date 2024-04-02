from collections import namedtuple

fabric_size = namedtuple("fabric_size", ["width", "length", "square_inches"])

FABRIC_CUTS = {
    "fat_quarter": fabric_size(18, 22, 396),
    "fat_eighth": fabric_size(9, 22, 198),
    "yard": fabric_size(36, 44, 1584),
    "fat_half": fabric_size(18, 44, 792),
    "fat_sixteenth": fabric_size(4.5, 22, 99),
    "half_yard": fabric_size(18, 44, 792),
    "quarter_yard": fabric_size(9, 22, 198),
    "eighth_yard": fabric_size(4.5, 22, 99),
}
