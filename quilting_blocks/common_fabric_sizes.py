from collections import namedtuple

fabric_size = namedtuple(
    "fabric_size", ["name", "length", "width", "square_inches"])

FABRIC_CUTS = {
    "fat_quarter": fabric_size("fat_quarter", 18, 21, 378),
    "fat_eighth": fabric_size("fat_eight", 9, 21, 189),
    "yard": fabric_size("yard", 36, 42, 1512),
    "fat_half": fabric_size("fat_half", 18, 42, 756),
    "fat_sixteenth": fabric_size("fat_sixteenth", 4.5, 21, 94.5),
    "half_yard": fabric_size("half_yard", 18, 42, 756),
    "quarter_yard": fabric_size("quarter_yard", 9, 21, 189),
    "eighth_yard": fabric_size("eighth_yard", 4.5, 21, 94.5),
}
