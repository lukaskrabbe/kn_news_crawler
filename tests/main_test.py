# -*- coding: utf-8 -*-
import pytest


def verify_answer(expected, answer):
    assert expected == answer


@pytest.mark.parametrize(
    "input, output", [("Test", "TestTest"), ("abc", "abcabc"), ("abcd", "abcdabcd")]
)
def test_double(input, output):
    assert output == input
