import random


class MineSweeper:
    def __init__(self, board_size, mines_amount):
        global seed

        self.board_size = board_size
        self.board = '.' * board_size * board_size
        self.vis_board = [0] * board_size * board_size      # 0 - не видно, 1 - видно, 2 - флаг
        self.mines_am = 0
        while self.mines_am < mines_amount:
            random.seed(seed)
            bombX = random.randint(0, board_size-1)

            random.seed(seed)
            bombY = random.randint(0, board_size-1)
            random.seed(seed)
            seed = random.randint(-(10 ** 9), 10 ** 9)

            if self.board[bombX + bombY * board_size] == '*':
                continue
            else:
                bl = list()
                bl.extend(self.board)
                bl[bombX + bombY * board_size] = '*'
                self.board = ''.join(bl)
                self.mines_am += 1

    def print(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                temp_str = self.board[x + y * self.board_size]
                temp_vis = self.vis_board[x + y * self.board_size]
                if temp_vis == 0:
                    print(' #', end='')
                elif temp_vis == 1:
                    print(' ' + temp_str, end='')
                else:
                    print(' F', end='')
            print()


if __name__ == '__main__':
    new_game = False

    while True:
        ans = input('Do you wish to continue from a saved game? Y/N > ')
        if ans == 'Yes':
            print(0)
            break
        elif ans == 'No':
            seed = random.randint(-(10 ** 9), 10 ** 9)
            new_game = True
            break
        else:
            print('Please answer with either "Yes" or "No" \n')

    if new_game:
        while True:
            try:
                nInf = list(map(lambda el: int(el), input('Please enter the size of the board and the amount of mines > ').split()))
                break
            except ValueError:
                print('Wrong syntax, please try again \n')
                continue
        bSize, mAm = nInf
        board = MineSweeper(bSize, mAm)
        while True:
            board.print()
            print()

            input('Debug > ')
            print()
    else:
        print('Here goes a saved game')