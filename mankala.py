import os
import subprocess as sp

START_ROCKS = 4
NODES = 6
DIRECTIONER = {0:-1, 1:1}


class Mankala:
    def __init__(self):
        self.players_nodes = [[START_ROCKS for _ in range(NODES)], [START_ROCKS for _ in range(NODES)]]
        self.players_scores = [0, 0]
        self.whose_turn = 0
        print('Turn of Player ' + str(self.whose_turn+1))

    def display(self):
        lines = ['' for _ in range(8)]
        lines[0] = 'Player 1'
        lines[1] = '  ' + ' _ '.join(map(str, self.players_nodes[0]))
        lines[2] = str(self.players_scores[0])
        lines[3] = '\t\t\t'+str(self.players_scores[1])
        lines[4] = '  ' + ' _ '.join(map(str, self.players_nodes[1]))
        lines[5] = '\t\t\t Player 2'
        lines[6] = ' [1] [2] [3] [4] [5] [6]'
        lines[7] = 'Turn of Player ' + str(self.whose_turn+1)

        for line in lines:
            print(line)

    def make_turn(self, player, node):
        if player != self.whose_turn:
            raise Exception("It's not yours turn!")
        self.whose_turn = (player + 1) % 2
        steps_left = self.players_nodes[player][node]
        self.players_nodes[player][node] = 0
        self._make_turn_rec(player, player, node+DIRECTIONER[player], steps_left)

    def _make_turn_rec(self, player, player_side, node, steps_left):
        while steps_left > 0:
            if node >= NODES or node < 0:
                if player_side:
                    if player == player_side:
                        steps_left -= 1
                        self.players_scores[player] +=1
                    return self._make_turn_rec(player, 0, NODES-1, steps_left)
                else:
                    if player == player_side:
                        steps_left -= 1
                        self.players_scores[player] +=1
                    return self._make_turn_rec(player, 1, 0, steps_left)

            self.players_nodes[player_side][node] += 1
            steps_left -= 1
            node += DIRECTIONER[player_side]
        self._handle_last_insertion(player, player_side, node)

    def _handle_last_insertion(self, player, player_side, node):
        self._check_turn_repetition(player, player_side, node)
        self._check_capturing(player, player_side, node)

    def _check_turn_repetition(self, player, player_side, node):
        print(player, player_side, node)
        if player == 0 and node == 0 and player_side == 1:
            self.whose_turn = player
        if player == 1 and node == NODES - 1 and player_side == 0:
            self.whose_turn = player

    def _check_capturing(self, player, player_side, node):

        if player == player_side:
            node -= DIRECTIONER[player]
            print("Player", player)
            print("node", node)
            print("Wartosc",self.players_nodes[player][node])
            if self.players_nodes[player][node] == 1:
                self.players_scores[player] += 1
                self.players_nodes[player][node] = 0
                self.players_scores[player] += self.players_nodes[(player+1)%2][node]
                self.players_nodes[(player + 1) % 2][node] = 0



x = Mankala()
while True:
    new = int(input()) -1
    x.make_turn(x.whose_turn, new)
    x.display()

#x.make_turn(0, 5)
#x.display()