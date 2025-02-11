import pytest

from src.service.service import Score_Calculator

@pytest.fixture
def score_tie_break():
    score_tie_break = Score_Calculator(score_dict={
        "player1": {"set": 0, "game": 6, "points": 0},
        "player2": {"set": 0, "game": 6, "points": 0}
    })
    return score_tie_break