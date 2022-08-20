#-*- coding:utf-8 -*-
import random, json_db

class Leitern:
    def __init__(self, map_x=10, map_y=10, quantity_leadders_up=1, quantity_leadders_down=1):
        try:
            json_db.read("Leitern_DB")
        except:
            json_db.write({}, "Leitern_DB")
        
        self.map = []
        for i,_ in enumerate(range(0, map_y+1)):
            self.map.append([])
            for _ in range(0, map_x+1):
                self.map[i].append("#")
        self.map[-1][0] = "O"

        for up_leadders in range(0, quantity_leadders_up):
            tf = True
            while tf:
                r_start_field_x = random.randint(0, map_x)
                r_start_field_y = random.randint(0, map_y)
                # print(r_start_field_x, r_start_field_y)
                if self.map[r_start_field_y][r_start_field_x] == "#" and r_start_field_y >= 1:
                    leadder_length = random.randint(0,map_y-r_start_field_y-1)
                    
                    print("Leadders Lenght: ", leadder_length)
                    print(map_y-r_start_field_y)
                    r_end_field_x = random.randint(0, map_x)
                    if self.map[r_start_field_y-leadder_length][r_start_field_x] == "#":
                        self.map[r_start_field_y][r_start_field_x] = "S"
                        self.map[r_start_field_y-leadder_length][r_start_field_x] = "s"
                        tf = False
        self.leadders = {"up": quantity_leadders_up, "down": quantity_leadders_down}

        json_data = {"map": self.map, "leadders": self.leadders}
        json_db.write(json_data, "Leitern_DB")

    def init(self, map_x=10, map_y=10, quantity_leadders_up=4, quantity_leadders_down=6):
        self.__init__(map_x, map_y, quantity_leadders_up, quantity_leadders_down)

    def roll_dices(self, dices=2, eyes=[1,6]):
        dices_list = []
        for _ in range(0, dices):
            dices_list.append(random.randint(eyes[0]-1, eyes[1]-1))
        return dices_list

    def movement(self):
        pass
    

l = Leitern()
for i, row in enumerate(l.map):
    print(i, row)
