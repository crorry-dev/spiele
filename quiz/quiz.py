#-*- coding:utf-8 -*-
import random

class Busfahren:
    def __init__(self, player_num) -> None:  
        self.used_cards_list = list()
        self.unused_cards_list = list()
        self.player_num = player_num
        self.final_round = 1
        self.final_last_card = None
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
    
    def play_final(self, guess=None, cards=[], init=False, max_cards=5):
        # Params:
        # guess can be "lower", "higher" or "equal"
        # Return:
        # case right guess, game not finished: {card=[[7, "H"], [9, "H"]], sips=0, won=False, opened_card=[11, "D"]}
        # case wrong guess:                    {card=[8, "D"],             sips=2, won=False, opened_card=[12, "D"]}
        # case right guess, game finished:     {card=None,                 sips=0, won=True,  opened_card=[13, "D"]}
        
        

        if init:
            self.make_card_pool()
            self.card_index = 0

        if cards != []:
            if guess == "higher":
                if cards[self.card_index][0] < cards[self.card_index+1][0]:
                    self.card_index += 1
                else:
                    for i in range(1, self.card_index+1):
                        cards[i] = self.get_unused_card()
                    self.card_index = 0
                return self.card_index, cards
            elif guess == "lower":
                if cards[self.card_index][0] > cards[self.card_index+1][0]:
                    self.card_index += 1
                else:
                    for i in range(1, self.card_index+1):
                        cards[i] = self.get_unused_card()
                    self.card_index = 0
                return self.card_index, cards
            elif guess == "equal":
                if cards[self.card_index][0] == cards[self.card_index+1][0]:
                    self.card_index += 1
                else:
                    for i in range(1, self.card_index+1):
                        cards[i] = self.get_unused_card()
                    self.card_index = 0
                return self.card_index, cards

        else:
            cards_for_final = []
            for _ in range(0, max_cards+1):
                cards_for_final.append(self.get_unused_card())
            return cards_for_final

        # Start: get list of cards and card_index; Start card_index = 0
        # InGame: guess = higher, lower, equal
        # if wron_guess -> new Start and sips = card_index
        #
        #if init:
        #    self.make_card_pool()
        #    self.final_last_card = self.get_unused_card()
        #    self.final_round = 1
        #    return({"card": self.final_last_card, "sips": 0, "won": False, "opened_card": None})
        #else:
        #    playing_card = self.get_unused_card()
        #    if self.final_last_card is None:
        #        raise BaseException("Wrong use of function")
        #    if (guess == "lower"  and playing_card[0] < self.final_last_card[0]) or \
        #       (guess == "higher" and playing_card[0] > self.final_last_card[0]) or \
        #       (guess == "equal"  and playing_card[0] == self.final_last_card[0]):
        #            self.final_round += 1
        #            if self.final_round == 5:
        #                return {"card": None, "sips": 0, "won": True, "opened_card": None}
        #            else:
        #                return {"card": playing_card, "sips": 0, "won": False, "opened_card": None}
        #    else:
        #        sips = self.final_round
        #        next_card = self.get_unused_card()
        #
        #        ret_dict = {"card": next_card, "sips": sips, "won": False, "opened_card": playing_card}
        #
        #        self.final_last_card = next_card
        #        self.final_round = 1
#
        #        return ret_dict




# def make_test_game():
#     game = Busfahren()
#     print(game.get_map())
#     print("------")
#     print("Player 1")
#     print(game.get_player_cards())
#     print("Player2")
#     print(game.get_player_cards())

# make_test_game()
# (0,0) [0][0]
# (1,0), (1,1) [1][0] [1][1]
# (2,0), (2,1), (2,2)