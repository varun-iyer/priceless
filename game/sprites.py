from ast import Call
from dataclasses import dataclass
from enum import Enum
from operator import truediv
from tkinter import Scale
from typing import Callable
import arcade


@dataclass
class Resource:
    name: str
    amount: int
    value: int

    def collect(self) -> int:
        if self.amount <= 0:
            return 0
        self.amount -= 10
        return 10

@dataclass
class UpgradeRequirement:
    rock: int
    wood: int
    water: int


@dataclass
class CityManager:
    totals = {
        "wood": 0,
        "water": 0,
        "rock" : 0
    }
    levels = [
        UpgradeRequirement(rock=500, wood=500, water=500),
        UpgradeRequirement(rock=1500, wood=1000, water=1000),
        UpgradeRequirement(rock=3000, wood=3000,  water=3000)
    ]
    current_level = -1
    value = 0

    def upgrade(self):
        if self.current_level == 3:
            return
        next_upgrade = self.levels[self.current_level + 1]
        if (self.totals["wood"] >= next_upgrade.wood and
            self.totals["water"] >= next_upgrade.water and 
            self.totals["rock"] >= next_upgrade.rock):
            self.current_level += 1
    

class City(arcade.Sprite):

    def __init__(self, city_manager) -> None:
        super().__init__(
            "assets/tiles.png", 
            image_y=3*16,  
            image_x=7*16,  
            image_width=16,
            image_height=16,
            scale = 1.0
        )
        self.city_manager = city_manager

    def add_resource(self, resource: str, amount: int) -> None:
        self.city_manager.totals[resource] += amount

    def get_current_level(self):
        return self.city_manager.current_level
    
    def get_totals(self):
        return self.city_manager.totals

    def get_city_value(self):
        return self.city_manager.value

    def upgrade(self):
        self.city_manager.upgrade()



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
        amount = sprite.resource.collect()
        self.backpack[sprite.resource.name] += amount
    

    def drop_off(self, city):
        city.add_resource("wood", self.backpack["wood"])
        city.add_resource("water", self.backpack["water"])
        city.add_resource("rock", self.backpack["rock"])

        self.backpack["wood"] = 0
        self.backpack["water"] = 0
        self.backpack["rock"] = 0
        self.backpack["space"] = 50