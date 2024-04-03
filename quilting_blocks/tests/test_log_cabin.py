import pytest
from quilting_blocks.log_cabin import LogCabin


@pytest.fixture
def default_log_cabin():
    return LogCabin(config={})


@pytest.fixture
def custom_log_cabin():
    return LogCabin(config={"starting_square_completed": 5, "n_rounds": 3})


def test_empty_config_init(default_log_cabin):
    actual = default_log_cabin.get_config()
    expected = {
        "seam_allowance": 0.25,
        "strip_width_completed_1": 1,
        "starting_square_completed": 2,
        "n_rounds": 2,
        "strip_width_completed_2": 1,
    }
    assert actual == expected


def test_partial_config_init(custom_log_cabin):
    actual = custom_log_cabin.get_config()
    expected = {
        "seam_allowance": 0.25,
        "strip_width_completed_1": 1,
        "starting_square_completed": 5,
        "n_rounds": 3,
        "strip_width_completed_2": 1,
    }
    assert actual == expected


@pytest.mark.parametrize(
    "config, expected_size", [
        ("default_log_cabin", 2.5),
        ("custom_log_cabin", 5.5),
    ]
)
def test_initialized_sides_dict(config, expected_size, request):
    config = request.getfixturevalue(config)
    actual = config.sides_dict
    expected = {
        'Top': [expected_size],
        'Right': [expected_size],
        'Bottom': [expected_size],
        'Left': [expected_size],
    }
    assert actual == expected


@pytest.mark.parametrize(
    "config, expected_size", [
        ("default_log_cabin", 2.5),
        ("custom_log_cabin", 5.5),
    ]
)
def test_initialized_pieces_dict(config, expected_size, request):
    config = request.getfixturevalue(config)
    actual = config.pieces_dict
    expected = {
        'Middle': [
            config.piece_info(0, expected_size, expected_size)],
        'Top': [],
        'Right': [],
        'Bottom': [],
        'Left': [],
    }
    assert actual == expected


def test_add_seam_allowance(default_log_cabin):
    actual = default_log_cabin.add_seam_allowance(1)
    expected = 1.5
    assert actual == expected


def test_add_side(default_log_cabin):
    actual = default_log_cabin
    current_sizes = {
        'Top': 2.5,
        'Right': 2.5,
        'Bottom': 2.5,
        'Left': 2.5,
    }
    actual.add_side(current_sizes, 'Top', 1.5)
    expected = {
        'Top': [2.5, 2.5],
        'Right': [2.5, 3.5],
        'Bottom': [2.5, 2.5],
        'Left': [2.5, 3.5],
    }
    assert actual.sides_dict == expected
    current_sizes = {
        'Top': 2.5,
        'Right': 3.5,
        'Bottom': 2.5,
        'Left': 3.5,
    }
    actual.add_side(current_sizes, 'Right', 1.5)
    expected = {
        'Top': [2.5, 2.5, 3.5],
        'Right': [2.5, 3.5, 3.5],
        'Bottom': [2.5, 2.5, 3.5],
        'Left': [2.5, 3.5, 3.5],
    }
    assert actual.sides_dict == expected
    current_sizes = {
        'Top': 3.5,
        'Right': 3.5,
        'Bottom': 3.5,
        'Left': 3.5,
    }
    actual.add_side(current_sizes, 'Bottom', 1.5)
    expected = {
        'Top': [2.5, 2.5, 3.5, 3.5],
        'Right': [2.5, 3.5, 3.5, 4.5],
        'Bottom': [2.5, 2.5, 3.5, 3.5],
        'Left': [2.5, 3.5, 3.5, 4.5],
    }
    assert actual.sides_dict == expected
    current_sizes = {
        'Top': 3.5,
        'Right': 4.5,
        'Bottom': 3.5,
        'Left': 4.5,
    }
    actual.add_side(current_sizes, 'Left', 1.5)
    expected = {
        'Top': [2.5, 2.5, 3.5, 3.5, 4.5],
        'Right': [2.5, 3.5, 3.5, 4.5, 4.5],
        'Bottom': [2.5, 2.5, 3.5, 3.5, 4.5],
        'Left': [2.5, 3.5, 3.5, 4.5, 4.5],
    }
    assert actual.sides_dict == expected


def test_build_round(default_log_cabin):
    actual = default_log_cabin
    actual.build_round(1, 1.5)
    expected_sides_dict = {
        'Top': [2.5, 2.5, 3.5, 3.5, 4.5],
        'Right': [2.5, 3.5, 3.5, 4.5, 4.5],
        'Bottom': [2.5, 2.5, 3.5, 3.5, 4.5],
        'Left': [2.5, 3.5, 3.5, 4.5, 4.5],
    }
    assert actual.sides_dict == expected_sides_dict
    expected_pieces_dict = {
        'Middle': [actual.piece_info(0, 2.5, 2.5),],
        'Top': [actual.piece_info(1, 1.5, 2.5),],
        'Right': [actual.piece_info(1, 1.5, 3.5),],
        'Bottom': [actual.piece_info(1, 1.5, 3.5),],
        'Left': [actual.piece_info(1, 1.5, 4.5),],
    }
    assert actual.pieces_dict == expected_pieces_dict


def test_build_cabin(default_log_cabin):
    actual = default_log_cabin
    actual.build_cabin()
    expected_sides_dict = {
        'Top': [2.5, 2.5, 3.5, 3.5, 4.5, 4.5, 5.5, 5.5, 6.5],
        'Right': [2.5, 3.5, 3.5, 4.5, 4.5, 5.5, 5.5, 6.5, 6.5],
        'Bottom': [2.5, 2.5, 3.5, 3.5, 4.5, 4.5, 5.5, 5.5, 6.5],
        'Left': [2.5, 3.5, 3.5, 4.5, 4.5, 5.5, 5.5, 6.5, 6.5],
    }
    assert actual.sides_dict == expected_sides_dict
    expected_pieces_dict = {
        'Middle': [
            actual.piece_info(0, 2.5, 2.5),
        ],
        'Top': [
            actual.piece_info(1, 1.5, 2.5),
            actual.piece_info(2, 1.5, 4.5),
        ],
        'Right': [
            actual.piece_info(1, 1.5, 3.5),
            actual.piece_info(2, 1.5, 5.5),
        ],
        'Bottom': [
            actual.piece_info(1, 1.5, 3.5),
            actual.piece_info(2, 1.5, 5.5),
        ],
        'Left': [
            actual.piece_info(1, 1.5, 4.5),
            actual.piece_info(2, 1.5, 6.5),
        ],
    }
    assert actual.pieces_dict == expected_pieces_dict


@pytest.fixture
def fabric_pieces():
    fabric_pieces = {
        "Top": [
            LogCabin.piece_info(1, 1.5, 2.5),
            LogCabin.piece_info(2, 1.5, 4.5),
        ],
        "Right": [
            LogCabin.piece_info(1, 1.5, 3.5),
            LogCabin.piece_info(2, 1.5, 5.5)
        ],
    }
    return fabric_pieces


def test_format_fabric_pieces():
    pass


def test_organize_fabric_pieces(default_log_cabin, fabric_pieces):
    default_log_cabin.pieces_dict = fabric_pieces
    default_log_cabin.organize_fabric_pieces()
    expected_fabric_1_pieces = {
        "Top": [LogCabin.piece_info(1, 1.5, 2.5)],
        "Right": [LogCabin.piece_info(1, 1.5, 3.5)],
    }
    expected_fabric_2_pieces = {
        "Top": [LogCabin.piece_info(2, 1.5, 4.5)],
        "Right": [LogCabin.piece_info(2, 1.5, 5.5)],
    }
    assert default_log_cabin.fabric_1_pieces == expected_fabric_1_pieces
    assert default_log_cabin.fabric_2_pieces == expected_fabric_2_pieces


def test_calculate_yardage():
    pass
