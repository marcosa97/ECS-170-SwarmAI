import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import *
from sc2.unit import *

'''
Commented out line 38 of sc2.game_info.py to make the map "testing" work.
'''
#Screen attributes
_MIN_SCREEN_SZ = 0
_MAX_SCREEN_SZ = 48 # for our custom testing map; 64 for Simple64 Map

class SimpleBot(sc2.BotAI):
    tagToObs = None
    steps = 0

    
    '''
    want movement_speed, armor,  weapons, ability_id, 
    cooldowns,
    '''
    def extract_data(self, unit):
        data = [unit.tag, unit.is_visible, unit.tag, unit.position, unit.facing, unit.radius,
                unit.detect_range, unit.radar_range, unit.cloak, unit.is_blip, 
                unit.is_powered, unit.is_burrowed, unit.health, unit.health_max,
                unit.shield, unit.shield_max, unit.energy, unit._type_data.name,
                unit._type_data.attributes, unit._type_data.cost]
        return data


    '''
    make_move takes in a selected units x and y coordinates, and a move:
    move of 0 is for move backward, away from enemy
    move of 1 is move toward enemy
    move of 2 is attack enemy
    movements are determined by comparing the distances NESW of the unit with the 
    enemy location
    '''
    def make_move(self, move, x, y, enemy_x, enemy_y):
        distance = 10 # how far to move in x and y direction
        #enemy_x = 30#self.enemy_loc[0]
        #enemy_y = 30#self.enemy_loc[1]
        north_y = y + distance
        south_y = y - distance
        east_x = x + distance
        west_x = x - distance
        # Conditions to avoid having an out of bound coordinate
        if north_y < _MIN_SCREEN_SZ:
            north_y = _MIN_SCREEN_SZ
        if south_y < _MIN_SCREEN_SZ:
            south_y = _MIN_SCREEN_SZ
        if east_x < _MIN_SCREEN_SZ:
            east_x = _MIN_SCREEN_SZ
        if west_x < _MIN_SCREEN_SZ:
            west_x = _MIN_SCREEN_SZ

        if north_y > _MAX_SCREEN_SZ:
            north_y = _MAX_SCREEN_SZ
        if south_y > _MAX_SCREEN_SZ:
            south_y = _MAX_SCREEN_SZ
        if east_x > _MAX_SCREEN_SZ:
            east_x = _MAX_SCREEN_SZ
        if west_x > _MAX_SCREEN_SZ:
            west_x = _MAX_SCREEN_SZ

        if ( abs(enemy_x - east_x) > abs(enemy_x - west_x)):
            targetx0 = east_x
            targetx1 = west_x
            #print("east")
        else:
            targetx0 = west_x
            targetx1 = east_x
            #print("west")
        if ( abs(enemy_y - north_y) > abs(enemy_y - south_y)):
            targety0 = north_y
            targety1 = south_y
            #print("north")
        else:
            targety0 = south_y
            targety1 = north_y
            #print("south")

        if move == 0: #back
            #targety = y - distance
            #targetx = x - distance
            target = (targetx0, targety0)

        elif move == 1: #forward
            target = (targetx1, targety1)
            #target = [x + distance, y + distance]

        else: #move =2, attack
            attack = True
            target = (enemy_x, enemy_y)#[x,y]
        return Point2(target)

    async def on_step(self, iteration):
        print("iteration")
        print(self.steps)
        self.steps = self.steps+1
        print(self.known_enemy_units)
        enemies = self.known_enemy_units
        moves = [1,2]
        move = None
        enemy_loc = None
        if len(enemies) > 0:
            enemy = enemies[0]
            print(type(enemy))
            enemy_loc = Point2(enemy.position)
            print(enemy_loc)
            print(enemy.health)
        
        for worker in self.units:
            p = worker.position
            p2 = Point2(p)
            if self.tagToObs == None:
                self.tagToObs = worker.tag
            if self.tagToObs == worker.tag:
                newp = Point2((0,0))
                move = 0
            else:
                newp = Point2((40,40))
                move = 2
            if enemy_loc:
                target = self.make_move(move, p2.x,p2.y,enemy_loc.x, enemy_loc.y)
            else: 
                target = Point2((0,0))
            print("worker tag")
            print(worker.tag)
            print(p2.x, p2.y)            
            print("ally health")
            print(worker.health)
            data = self.extract_data(worker)
            print (data)
            if move == 0  or move==1:
                await self.do(worker.move(target))
            else:
                await self.do(worker.attack(target))


        '''
        for worker in self.units:
            p = worker.position
            p2 = Point2(p)
            if (iteration % 10) == 0:
                if self.tagToObs == None:
                    self.tagToObs = worker.tag
                if self.tagToObs == worker.tag:
                    print("worker tag")
                    print(worker.tag)
                    print(p2.x, p2.y)
            newp = Point2((30,30))
            '''
            #print (newp)
            #await self.do(worker.attack(self.enemy_start_locations[0]))
                #await self.do(worker.move(newp))

def main():
    sc2.run_game(sc2.maps.get("testing"), [
        Bot(Race.Terran, SimpleBot()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=False)

if __name__ == '__main__':
    main()
