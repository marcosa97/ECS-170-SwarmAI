import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import *
from sc2.unit import *

'''
Commented out line 38 of sc2.game_info.py to make the map "testing" work.
Changed unit.py and game_data.py to get more data
'''
#Screen attributes
_MIN_SCREEN_SZ = 0
_MAX_SCREEN_SZ = 47.9999999 # for our custom testing map; 64 for Simple64 Map

class SimpleBot(sc2.BotAI):
    tagToObs = None
    steps = 0
    tags = []
    enemy_to_attack = None

    
    '''
    want movement_speed, armor,  weapons, ability_id, 
    cooldowns, etc
    '''
    def extract_data(self, unit):
        weapons = unit._type_data.weapons
        weapon_data = []
        for w in range(3):
            if len(weapons) > w:
                weapon_data.append(weapons[w].range)
                weapon_data.append(weapons[w].damage)
                weapon_data.append(weapons[w].speed)
            else:
                weapon_data.extend([0,0,0]) # if unit does not have weapons


        data = [unit._type_data.name, unit.tag, unit.is_visible, unit.position, unit.facing, unit.radius,
                unit.detect_range, unit.radar_range, unit.cloak, unit.is_blip, 
                unit.is_powered, unit.is_burrowed, unit.health, unit.health_max,
                unit.shield, unit.shield_max, unit.energy, 
                unit._type_data.attributes, unit._type_data.cost.minerals, 
                unit._type_data.cost.vespene, unit._type_data.cost.time,
                unit._type_data.movement_speed, unit._type_data.armor, 
                #unit._type_data.weapons[0].range, unit._type_data.weapons[0].damage,
               # unit._type_data.weapons[0].speed, 
                unit.weapon_cooldown,
                unit.position.to2.x, unit.position.to2.y]
        data.extend(weapon_data)
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

    '''
    makes a target to move with codes 0-7 signifying NESW location (8 diff directions)
    '''

    def make_move2(self, move, x, y):
        distance = 10 # how far to move in x and y direction

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

        '''
        north 0, northeast 1, east 2, southeast 3, south 4,
        southwest 5, west 6, northwest 7
        '''

        if move == 0: 
            target = (x, north_y)

        elif move == 1: 
            target = (east_x, north_y)
        
        elif move == 2: 
            target = (east_x, y)

        elif move == 3:
            target = (east_x, south_y)

        elif move == 4: 
            target = (x, south_y)

        elif move == 5: 
            target = (west_x, south_y)
        
        elif move == 6: 
            target = (west_x, y)
            
        elif move == 7:
            target = (west_x, north_y)

        else:
            if self.enemy_to_attack:
                target = (Point2(self.enemy_to_attack.position).x, Point2(self.enemy_to_attack.position).y)
            else:
                return self.enemy_start_locations[0]

        return Point2(target)

    async def on_step(self, iteration):
        print("iteration")
        print(iteration)

        print(self.known_enemy_units)
        enemies = self.known_enemy_units
        #move vector (will be replaced by real AI move vector)
        #Note: 8,9,10,11 not defined at the moment
        moves = [0,1,2,3,4,5,6,7,8,9,10,11] 
        move = None
        enemy_loc = None
        tagPos = 0
        all_data = []
        '''
        To end game and save the replay after certain condition, just make an illegal command
        example: a=b, where b is undefined
        Next 2 lines Will end game after 50th iteration
        '''
        if iteration == 50:
            a=b

        if len(enemies) > 0:
            enemy = enemies[0] # just gets first enemy
            self.enemy_to_attack = enemy
            enemy_loc = Point2(enemy.position)
            data = self.extract_data(enemy)
            print (data)
        
        '''
        How I'm guessing the machine learning will work:
        First loop through all units and make an array of arrays containing data of every unit
        '''
        for unit in self.units:
            data = self.extract_data(unit)
            print (data)
            all_data.append(data)


        '''
        Do machine learning/ AI commands with all_data, and get move vector
        '''

        '''
        Loop through all units again, and make the appropriate move for each unit
        ***units should be in same order as above***
        '''
        for i in range(len(self.units)):
            p = self.units[i].position
            p2 = Point2(p)
            data = self.extract_data(self.units[i])
            move = moves[i % len(moves)]
            print("move")
            print(move)
            target = self.make_move2(move, p2.x, p2.y)
            if move < 8:
                await self.do(self.units[i].move(target))
            else:
                await self.do(self.units[i].attack(target))

            '''
            using fixed target points to just check that all ally units moving at the same time to different points
            from the new_agent2.py, can remove if you want
            
            if tagPos ==0:
                target = Point2((30,30))
            if tagPos ==1:
                target = Point2((10,10))
            if tagPos ==2:
                target = Point2((20,20))
            if tagPos == 3:
                target = Point2((10,20))
            if tagPos ==4:
                target = Point2((30,30))
            if tagPos ==5:
                target = Point2((40,40))
            if tagPos ==6:
                target = Point2((30,20))
            if tagPos ==7:
                target = Point2((20,30))
            if tagPos == 8:
                target = Point2((40,20))
            if tagPos ==9:
                target = Point2((40,30))
            if tagPos ==10:
                target = Point2((5,5))
            if tagPos ==11:
                target = Point2((30,10))
            if tagPos ==12:
                target = Point2((30,40))
            if iteration > 0:
                tagPos = tagPos+1

            tagPos = tagPos %len(self.tags)
            await self.do(self.tags[tagPos].move(target))
            '''


            '''
            if move == 0  or move==1:
                await self.do(worker.move(target))
            else:
                await self.do(worker.attack(target))
            '''

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
    sc2.run_game(sc2.maps.get("testing"), [ #can change map from testing to whatever other map: ex: "Simple64"
        Bot(Race.Terran, SimpleBot()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=False, save_replay_as="Example3.SC2Replay") #remove the save_replay_as="..." if you do not want to save a replay

if __name__ == '__main__':
    main()
