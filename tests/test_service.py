from src.service.service import Tennis_Score, ScoreCalculator
import pytest

class TestTennis_Score:
    @pytest.mark.parametrize(
        "point, res",
        [
        (0, 15),
        (15,30),
        (30,40),
        (40, 'AD'),
        ('AD', 0)
        ]
    )
    def test_tennis_score(self, point, res):
        tennis_score = Tennis_Score()
        assert tennis_score._counting_of_points(point) == res


    # def test_logic():
    #     assert 2 + 2 == 4
