from xythrion.utils import remove_whitespace, convert_3d_tuples


def test_remove_some_whitespace():
    assert remove_whitespace("t est ") == "test"


def test_remove_no_whitespace():
    assert remove_whitespace("test") == "test"


def test_convert_single_digits_in_tuple():
    assert convert_3d_tuples("(2, 2, 2)") == (2, 2, 2)


def test_convert_multiple_digits_in_tuple():
    assert convert_3d_tuples("(12, 23, 24)") == (12, 23, 24)


def test_convert_different_digits_in_tuple():
    assert convert_3d_tuples("(1, 22, 333)") == (1, 22, 333)
