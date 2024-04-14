from collections import namedtuple

fabric_size = namedtuple(
    "fabric_size", ["name", "length", "width", "square_inches"])

FABRIC_CUTS = {
    "fat_sixteenth": fabric_size("fat_sixteenth", 4.5, 21, 94.5),
    "sixteenth_yard": fabric_size("sixteenth_yard", 2.25, 42, 94.5),
    "fat_eighth": fabric_size("fat_eight", 9, 21, 189),
    "eighth_yard": fabric_size("eighth_yard", 4.5, 42, 189),
    "fat_quarter": fabric_size("fat_quarter", 18, 21, 378),
    "quarter_yard": fabric_size("quarter_yard", 9, 42, 378),
    "fat_half": fabric_size("fat_half", 21, 36, 756),
    "half_yard": fabric_size("half_yard", 18, 42, 756),
    "yard": fabric_size("yard", 36, 42, 1512),
}
