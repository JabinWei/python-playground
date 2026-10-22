import pytest
from unittest.mock import patch
from tic_tac_toe import (
    create_board,
    print_board,
    check_winner,
    get_move,
    play_one_round
)

@pytest.mark.task(taskno = 1)
class TestGetMove:
    """
    任务1: 测试 get_move 函数
    """

    """
    测试案例1: 正常输入成功返回
    """
    @patch("builtins.input", side_effect=['ab', '1,2', '45', '2 3'])
    def test_player_move(self, mock_input):
        board = create_board()
        result_row, result_col = get_move(board, 'player')
        assert result_row == 1, result_col == 2

    """
    测试案例2: 在相同地方重复落子，返回失败
    """
    @patch("builtins.input", side_effect=['2 3', '2 3', '1 2'])
    @patch("builtins.print")
    def test_player_move_same(self, mock_print, mock_input):
        board = create_board()
        for i in range(2):
            row, col = get_move(board, 'X')
            board[row][col] = 'X'
        assert mock_print.call_count == 1
        assert any("该位置已有棋子" in str(call) for call in mock_print.call_args_list)

    """
    测试案例3: 再超出棋盘的位置落子，是否能够正确提示
    """
    @patch("builtins.input", side_effect=['7 8', '2 2'])
    @patch("builtins.print")
    def test_player_move_out_of_range(self, mock_print, mock_input):
        board = create_board()
        row, col = get_move(board, 'O')
        assert any("坐标范围错误！行和列都必须在 1~3 之间。" in str(call) for call in mock_print.call_args_list)

@pytest.mark.task(taskno = 2)
class TestCheckWinner:
    """
    任务2: 测试 check_winner 函数
    """

    """
    测试案例: 检查所有赢的可能性，这里两方玩家获胜条件相同，故对所有胜利场景进行玩家交叉测试。
    """
    @pytest.mark.parametrize("board, expected_game_over, expected_winner", [
        # X 横向赢（第一行）
        ([['X', 'X', 'X'],
          [' ', ' ', ' '],
          [' ', ' ', ' ']], True, 'X'),
        # O 横向赢（第二行）
        ([[' ', ' ', ' '],
          ['O', 'O', 'O'],
          [' ', ' ', ' ']], True, 'O'),
        # X 横向赢（第三行）
        ([[' ', ' ', ' '],
          [' ', ' ', ' '],
          ['X', 'X', 'X']], True, 'X'),
        # O 竖向赢（第一列）
        ([['O', ' ', ' '],
          ['O', ' ', ' '],
          ['O', ' ', ' ']], True, 'O'),
        # X 竖向赢（第二列）
        ([[' ', 'X', ' '],
          [' ', 'X', ' '],
          [' ', 'X', ' ']], True, 'X'),
        # O 竖向赢（第三列）
        ([[' ', ' ', 'O'],
          [' ', ' ', 'O'],
          [' ', ' ', 'O']], True, 'O'),
        # X 斜向赢（右斜）
        ([['X', ' ', ' '],
          [' ', 'X', ' '],
          [' ', ' ', 'X']], True, 'X'),
        # O 斜向赢（左斜）
        ([[' ', ' ', 'O'],
          [' ', 'O', ' '],
          ['O', ' ', ' ']], True, 'O'),
        # 谁都没赢（棋盘已满平局）
        ([['O', 'X', 'O'],
          ['X', 'X', 'O'],
          ['O', 'O', 'X']], True, None),
        # 谁都没赢（棋盘未满平局）
        ([[' ', 'X', 'O'],
          ['X', ' ', 'O'],
          ['O', 'O', 'X']], False, None)
    ])
    def test_check_winner(self, board, expected_game_over, expected_winner):
        actl_game_over, actl_winner = check_winner(board)
        assert actl_game_over == expected_game_over
        assert actl_winner == expected_winner

@pytest.mark.task(taskno = 3)
class TestPlayOneRound:

    """
    测试案例1: 测试游戏一轮
    """
    def test_play_one_round(self, monkeypatch):
        calls = []
        def mock_input(_):
            calls.append(1)
            if len(calls) == 1:
                  return "1 1"
            if len(calls) == 2:
                  return "1 2"
            if len(calls) == 3:
                  return "2 2"
            if len(calls) == 4:
                  return "1 3"
            if len(calls) == 5:
                  return "3 3"
        monkeypatch.setattr("builtins.input", mock_input)
        play_one_round()