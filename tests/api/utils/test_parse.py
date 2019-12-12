from mariner.utils import parse


def test_number():
    """Returns an integer out of number string."""
    assert parse.number("1,000,000") == 1000000
    assert parse.number("1 000 000") == 1000000
    assert parse.number("-") == 0
