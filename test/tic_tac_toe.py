# 컴퓨터가 랜덤으로 움직이기 위해 random 모듈을 가져옵니다.
import random

# 현재 보드 상태를 출력하는 함수
def print_board(board):
    # 각 행을 순회하며 구분자를 사용해 출력
    for row in board:
        print(" | ".join(row))
        print("-" * 5)  # 각 행 아래에 가로선을 출력

# 플레이어가 승리했는지 확인하는 함수
def check_winner(board, player):
    # 모든 행과 열을 확인하여 승리 조건을 만족하는지 확인
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # 행 확인
            return True
        if all([board[j][i] == player for j in range(3)]):  # 열 확인
            return True
    # 두 대각선을 확인하여 승리 조건을 만족하는지 확인
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

# 보드가 꽉 찼는지 확인하는 함수
def is_full(board):
    # 빈 칸이 없으면 True를 반환
    return all(cell != " " for row in board for cell in row)

# 사용자의 입력을 받아오는 함수
def get_human_move(board):
    while True:
        try:
            # 사용자에게 1-9 사이의 숫자를 입력받음
            move = int(input("Enter your move (1-9): ")) - 1
            row, col = divmod(move, 3)  # 입력값을 행과 열 인덱스로 변환
            if board[row][col] == " ":  # 선택한 칸이 비어있는지 확인
                return row, col
            else:
                print("이미 선택된 칸입니다. 다시 시도하세요.")
        except (ValueError, IndexError):
            print("잘못된 입력입니다. 1에서 9 사이의 숫자를 입력하세요.")

# 컴퓨터의 움직임을 결정하는 함수
def get_computer_move(board):
    # 빈 칸을 모두 찾은 후 랜덤으로 하나 선택
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)

# 게임을 실행하는 메인 함수
def main():
    # 빈 3x3 보드를 초기화
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]  # 두 플레이어 정의
    human = random.choice(players)  # 사용자에게 X 또는 O를 랜덤으로 할당
    computer = "O" if human == "X" else "X"  # 컴퓨터에게 나머지 심볼 할당
    print(f"당신은 '{human}'입니다. 컴퓨터는 '{computer}'입니다.")

    current_player = "X"  # X부터 게임 시작
    while True:
        print_board(board)  # 현재 보드 상태 출력
        if current_player == human:
            print("당신의 차례입니다.")
            row, col = get_human_move(board)  # 사용자의 움직임 가져오기
        else:
            print("컴퓨터의 차례입니다.")
            row, col = get_computer_move(board)  # 컴퓨터의 움직임 가져오기

        board[row][col] = current_player  # 현재 플레이어의 움직임으로 보드 업데이트

        if check_winner(board, current_player):  # 현재 플레이어가 승리했는지 확인
            print_board(board)
            if current_player == human:
                print("축하합니다! 당신이 이겼습니다!")
            else:
                print("컴퓨터가 이겼습니다. 다음엔 더 잘해보세요!")
            break

        if is_full(board):  # 보드가 꽉 찼는지 확인 (무승부)
            print_board(board)
            print("무승부입니다!")
            break

        # 다음 플레이어로 전환
        current_player = human if current_player == computer else computer

# 스크립트의 진입점
if __name__ == "__main__":
    main()