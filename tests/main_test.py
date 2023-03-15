import pytest
from src.string_functions import *


def verify_answer(expected, answer):
    assert expected == answer


@pytest.mark.parametrize(
    "input, output", [("Test", "TestTest"), ("abc", "abcabc"), ("abcd", "abcdabcd")]
)
def test_double(input, output):
    answer = double_string(input)
    assert output == answer
