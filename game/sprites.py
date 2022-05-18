from dataclasses import dataclass
from enum import Enum
from tkinter import Scale
from typing import Callable
import arcade

@dataclass
class Resource:
    name: str
    amount: int
    value: int

@dataclass
class UpgradeRequirement:
    rock: int
    wood: int
    water: int

class City(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png", 
            image_y=3*16,  
            image_x=7*16,  
            image_width=16,
            image_height=16,
            scale = 1.0
        )
        self.totals  = {
            "wood": 0,
            "water": 0,
            "rock" : 0
        }
        self.levels = [
            UpgradeRequirement(rock=500, wood=500, water=500),
            UpgradeRequirement(rock=1500, wood=1000, water=1000),
            UpgradeRequirement(rock=3000, wood=3000,  water=3000)
        ]
        self.current_level = 0
        self.current_value = 0

    def upgrade(self):
        if self.current_level == 3:
            return
        if  (self.totals["wood"] >= self.levels[self.current_level].wood and
             self.totals["water"] >= self.levels[self.current_level].water and
             self.totals["rock"] >= self.levels[self.current_level].rock):
             self.current_level += 1



class SparseGrass(arcade.Sprite):

    def __init__(self):
        super().__init__("assets/tiles.png", 1, image_y=16*8, image_x=0, image_width=16, image_height=16)


class Mountain(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png", 
            image_y=7*16,  
            image_x=6*16,  
            image_width=16,
            image_height=16,
            scale = 1.0
        )
        self.resource = Resource("rock", amount=100, value=10)
                

class Water(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png",
            image_y=3*16,
            image_x=5*16,
            image_width=16,
            image_height=16,
            scale=1.0
        )
        self.resource = Resource("water", amount=100, value=25)
        

class Tree(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png",
            image_y=9*16,
            image_x=4*16,
            image_width=16,
            image_height=16,
            scale=1.0
        )
        self.resource = Resource("wood", amount=20, value=10)


class Player(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png",
            image_y=8*16,
            image_x=6*16,
            image_width=16,
            image_height=16,
            scale = 1.0
        )
        self.backpack = {
            "space": 50,
            "wood": 0,
            "water": 0,
            "rock": 0 
        }
        

    def gather(self, sprite):
        # No space check
        # think of amount as space available
        if self.backpack["space"] <= 0:
            return 
        self.backpack["space"] -= 10
        self.backpack[sprite.resource.name] += 10
        sprite.resource.amount -= 10
    

    def drop_off(self, city):
        city.totals["wood"] += self.backpack["wood"]
        city.totals["water"] += self.backpack["water"]
        city.totals["rock"] += self.backpack["rock"]

        self.backpack["wood"] = 0
        self.backpack["water"] = 0
        self.backpack["rock"] = 0
        self.backpack["space"] = 50