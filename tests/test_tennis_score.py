import pytest

from src.service.service import Tennis_Score, Tiebreaker


class Test_Tennis_Score:
    @pytest.mark.parametrize(
        "point, res",
        [
            (0, 15),
            (15, 30),
            (30, 40),
            (40, 'AD'),
            ('AD', 0)
        ]
    )
    def test_tennis_score(self, point, res):
        """
        Проверка корректного начисления очков
        """
        tennis_score = Tennis_Score()
        assert tennis_score._counting_of_points(point) == res

    @pytest.mark.parametrize(
        "point, res",
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5,6),
            (6, 7),
            (7, 0)
        ]
    )
    def test_tie_break_logic(self, score_tie_break, point, res):
        if score_tie_break.is_tiebreaker_condition_met():
            tiebreaker_logic = Tiebreaker()
            assert tiebreaker_logic._counting_of_points(point) == res

