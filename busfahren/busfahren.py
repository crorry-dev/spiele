#-*- coding:utf-8 -*-
import random
# 7 = 7, A = 14
card_pool = [
    [[7,False],[8,False],[9,False],[10,False],[11,False],[12,False],[13,False],[14,False]], # Herz
    [[7,False],[8,False],[9,False],[10,False],[11,False],[12,False],[13,False],[14,False]], # Karo
    [[7,False],[8,False],[9,False],[10,False],[11,False],[12,False],[13,False],[14,False]], # Schippe
    [[7,False],[8,False],[9,False],[10,False],[11,False],[12,False],[13,False],[14,False]] # Kreuz
]

def make_card_pool():
    # make list of (card_pool)
    pass

def take_random_card_from_pool():
    global card_pool
    tf = True
    while tf:
        card = random.randint(7-7,14-7) # 7-A
        pic = random.randint(0,3) # H, P, S, K 
        if not card_pool[pic][card][1]:
            card_pool[pic][card][1] = True
            tf = False
    return [card, pic]
def random_cards_for_triangle(y_size=5, min_card=7, max_card=13):
    global card_pool
    data = []
    for i in range(1, y_size):
        tmp_data = []
        for ii in range(i):
            tmp_data.append(take_random_card_from_pool())
        data.append(tmp_data)
    return data
def random_cards_for_player(player_id=None, anz_player_cards=3):
    global card_pool
    player_cards = []
    for i in range(anz_player_cards):
        player_cards.append(take_random_card_from_pool())
    return player_cards
def get_playercards(player_id=None, anz_player_cards=3):
    # 7 = 1, A = 8
    return None
#def make_test_game():
#    print(random_cards_for_triangle(5))
#    print("------")
#    print("Player 1")
#    print(random_cards_for_player())
#    print("Player2")
#    print(random_cards_for_player())##
#
#make_test_game()