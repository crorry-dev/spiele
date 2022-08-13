#-*- coding:utf-8 -*-
import random

class Busfahren:
    def __init__(self, player_num) -> None:  
        self.used_cards_list = list()
        self.unused_cards_list = list()
        self.player_num = player_num
        self.make_card_pool()

    def make_card_pool(self):
        # initialize used and unused cards 
        for symbol in ["H", "D", "S", "C"]:                 # heart, diamond, spades, club
            for i in [7, 8, 9, 10, 11, 12, 13, 14]:         # 7 = 7, A = 14
                self.unused_cards_list.append([i, symbol])  # initialize unused cards
        self.used_cards_list = list()                       # initialize used cards

    def get_unused_card(self):
        # get unused card
        if not len(self.unused_cards_list) > 0:                       # raise exception if there is no unnused card
            raise BaseException("There is no unused card")
        card_pos = random.randint(0, len(self.unused_cards_list) - 1) # choose random unused card
        self.used_cards_list.append(self.unused_cards_list[card_pos]) # append to used cards
        self.unused_cards_list.pop(card_pos)                          # remove card from unused cards
        return self.used_cards_list[-1]                               # return choosen card (last one in the list)

    def get_map(self, row_nums=4):
        # get map that is played
        # first implemented map is a pyramide
        map = list()
        for i in range(row_nums):
            map.append(list())
            for _ in range(i + 1):
                map[-1].append(self.get_unused_card())
        return map

    def get_player_cards(self, player_cards_num=3):
        # get cards for player
        player_cards_list = list()
        for _ in range(player_cards_num):
            player_cards_list.append(self.get_unused_card())
        return player_cards_list

# def make_test_game():
#     game = Busfahren()
#     print(game.get_map())
#     print("------")
#     print("Player 1")
#     print(game.get_player_cards())
#     print("Player2")
#     print(game.get_player_cards())

# make_test_game()