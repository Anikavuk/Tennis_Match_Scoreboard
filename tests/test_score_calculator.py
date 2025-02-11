from src.service.service import Score_Calculator


class Test_Score_Calculator:

    def test_score_40_0(self):
        """
            Если игрок 1 выигрывает очко при счете 40-0,
            то он выигрывает гейм
        """
        score_logic = Score_Calculator({
            "player1": {"set": 0, "game": 0, "points": 40},
            "player2": {"set": 0, "game": 0, "points": 0}
        })
        score_logic.score_dict['player1']['points'] = 'AD'
        score_logic.update_games(score_logic.score_dict, 'player1')
        assert score_logic.score_dict['player1']['game'] == 1

    def test_score_40_40(self):
        """
            Если игрок 1 выигрывает очко при счете 40-40,
            то гейм не заканчивается
        """
        score_logic_deuce = Score_Calculator({
            "player1": {"set": 0, "game": 0, "points": 40},
            "player2": {"set": 0, "game": 0, "points": 40}
        })
        score_logic_deuce.is_deuce_condition_met()
        score_logic_deuce.process_deuce_game('player1')
        assert score_logic_deuce.score_dict['player1']['game'] == 0

    def test_tie_break(self, score_tie_break):
        """
            Проверяет счет на тайбрейк
        """
        score_tie_break.is_tiebreaker_condition_met()
        assert score_tie_break.is_tiebreaker_condition_met() == True

    def test_winner_match(self):
        """
            Если игрок 1 выигрывает очко при счете set 2-0,
            то победа в матче
        """
        score_winner_match = Score_Calculator({
            "player1": {"set": 2, "game": 5, "points": 40},
            "player2": {"set": 0, "game": 3, "points": 15}
        })
        score_winner_match.score_dict['player1']['points'] = 'AD'
        score_winner_match.update_games(score_winner_match.score_dict, 'player1')
        score_winner_match.update_set(score_winner_match.score_dict)
        assert score_winner_match.check_the_winner(score_winner_match.score_dict) == 'player1'
