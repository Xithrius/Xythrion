from bot.utils import convert_3d_tuples, remove_whitespace


def test_remove_some_whitespace() -> None:
    assert remove_whitespace("t est ") == "test"


def test_remove_no_whitespace() -> None:
    assert remove_whitespace("test") == "test"


def test_convert_single_digits_in_tuple() -> None:
    assert convert_3d_tuples("(2,2,2)") == (2, 2, 2)


def test_convert_multiple_digits_in_tuple() -> None:
    assert convert_3d_tuples("(12,23,24)") == (12, 23, 24)


def test_convert_different_digits_in_tuple() -> None:
    assert convert_3d_tuples("(1,22,333)") == (1, 22, 333)
