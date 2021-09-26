import random, sys, json, os


class MineSweeper:
    def __init__(self, board_size, mines_amount):
        global seed
        self.board_size = board_size
        self.board = '0' * board_size * board_size
        self.vis_board = [0 for i in range(board_size ** 2)]  # 0 - не видно, 1 - видно, 2 - флаг
        self.mines_am = 0
        self.dug = []
        self.dug_am = 0
        self.flagged = []
        self.flagged_am = 0

        while self.mines_am < mines_amount:
            random.seed(seed)
            bombX = random.randint(0, board_size - 1)
            random.seed(seed)
            seed = random.randint(-(10 ** 9), 10 ** 9)

            random.seed(seed)
            bombY = random.randint(0, board_size - 1)
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

        for x in range(board_size):
            for y in range(board_size):
                if self.board[x + y * board_size] != '*':
                    bAm = self.get_num_near_bombs(x, y)
                    if bAm:
                        bl = list()
                        bl.extend(self.board)
                        bl[x + y * board_size] = str(bAm)
                        self.board = ''.join(bl)

    def get_num_near_bombs(self, x, y):
        bomb_am = 0

        for r in range(max(0, x - 1), min(x + 1 + 1, self.board_size)):
            for c in range(max(0, y - 1), min(y + 1 + 1, self.board_size)):
                if r == x and c == y:
                    continue

                if self.board[r + c * self.board_size] == '*':
                    bomb_am += 1

        return bomb_am

    def dig(self, x, y):
        if (x, y) not in self.dug and self.vis_board[x + y * self.board_size] != 2:
            self.dug.append((x, y))
            self.dug_am += 1

            self.vis_board[x + y * self.board_size] = 1

            if self.board[x + y * self.board_size] == '*':
                return False
            if self.board[x + y * self.board_size] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return True

            for r in range(max(0, x - 1), min(x + 1 + 1, self.board_size)):
                for c in range(max(0, y - 1), min(y + 1 + 1, self.board_size)):
                    if (r, c) in self.dug:
                        continue
                    self.dig(r, c)
        return True

    def flag(self, x, y):
        if self.are_coords_valid(x, y):
            if not (x, y) in self.flagged:
                if self.vis_board[x + y * self.board_size] == 0:
                    self.flagged_am += 1
                    self.vis_board[x + y * self.board_size] = 2
                    self.flagged.append((x, y))
        else:
            print('Invalid coordinates')

    def are_coords_valid(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def print(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                temp_str = self.board[x + y * self.board_size]
                temp_vis = self.vis_board[x + y * self.board_size]
                if temp_vis == 0:
                    print(' #', end='')
                elif temp_vis == 1:
                    if temp_str == '0':
                        print(' .', end='')
                    else:
                        print(' ' + temp_str, end='')
                else:
                    print(' F', end='')
            print()


def save_game_state(valid=False):
    if valid:
        data = {
            'validness': True,
            'creation': {
                'source_seed': original_seed,
                'board_size': board.board_size,
                'bomb_am': board.mines_am
            },
            'player_related': {
                'dug': board.dug,
                'flagged': board.flagged
            }
        }
    else:
        data = {
            'validness': False
        }

    with open('mineSweeper.json', 'w') as msj:
        msj.write(json.dumps(data))


if __name__ == '__main__':
    new_game = False

    while True:
        ans = input('Do you wish to continue from a saved game? Y/N > ')
        if ans == 'Yes':
            if not os.path.isfile('mineSweeper.json'):
                print('The save file is unavailable')
                continue
            msfile = open('mineSweeper.json')
            saved_data = json.load(msfile)
            if not saved_data['validness']:
                print('The save file is unavailable')
                continue
            break
        elif ans == 'No':
            original_seed = random.randint(-(10 ** 9), 10 ** 9)
            seed = original_seed
            new_game = True
            break
        else:
            print('Please answer with either "Yes" or "No" \n')

    if new_game:
        while True:
            try:
                nInf = list(map(lambda el: int(el),
                                input('Please enter the size of the board and the amount of mines > ').split()))
                break
            except ValueError:
                print('Wrong syntax, please try again \n')
                continue
        bSize, mAm = nInf
        board = MineSweeper(bSize, mAm)
        print('\nNow you can start playing the game.')
        print('Write the row and the column of where you wish to perform an Action and this Action')
        print('The action must be one of the following: Dig, Flag, Unflag.')
        print('Or you can write Exit without entering the coordinates to exit the game\n')
    else:
        creation_data = saved_data['creation']
        player_data = saved_data['player_related']
        seed = creation_data['source_seed']
        board = MineSweeper(creation_data['board_size'], creation_data['bomb_am'])

        for d in player_data['dug']:
            board.dig(d[0], d[1])
        for f in player_data['flagged']:
            board.flag(f[0], f[1])

    while board.dug_am != board.board_size ** 2 - board.mines_am or board.flagged_am != board.mines_am:
        board.print()
        print()

        msg = input('Command > ')
        print()

        if msg == 'Exit':
            temp_msg = input('Do you want to save the game? Y/N > ')
            if temp_msg == 'Yes':
                save_game_state(True)
            else:
                save_game_state(False)
            sys.exit()
        elif msg[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print('Inaccessible command, please try again')
            continue

        y, x = int(msg.split()[0]) - 1, int(msg.split()[1]) - 1
        com = msg.split()[2]

        if x < 0 or x >= board.board_size:
            print('Inaccessible coordinates, please try again')
            continue
        if y < 0 or y >= board.board_size:
            print('Inaccessible coordinates, please try again')
            continue

        safe = False

        if com == 'Open':
            safe = board.dig(x, y)
            if not safe:
                board.print()
                print()
                break

        if com == 'Flag':
            board.flag(x, y)
            safe = True

    if not safe:
        print('You lost')
        save_game_state()
    else:
        print('You won')
        save_game_state()
