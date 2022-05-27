from ast import Call
from dataclasses import dataclass
from enum import Enum
from operator import truediv
from tkinter import Scale
from typing import Callable
import arcade

from conf import SPRITE_SCALE


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
            scale=SPRITE_SCALE
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



class Grass(arcade.Sprite):

    def __init__(self):
        super().__init__("assets/tiles.png", image_y=16*8, image_x=0, image_width=16, image_height=16, scale=SPRITE_SCALE)
        self.resource = Resource("grass", 0, 0)

    def degrade(self):
        pass


class Mountain(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png", 
            image_y=7*16,  
            image_x=7*16,  
            image_width=16,
            image_height=16,
            scale=SPRITE_SCALE
        )
        self.resource = Resource("rock", amount=100, value=10)
        self.textures = [
            arcade.load_texture("assets/tiles.png", x=7*16, y=7*16,width=16,height=16),
            arcade.load_texture("assets/tiles.png", x=6*16, y=7*16,width=16,height=16),
            arcade.load_texture("assets/tiles.png", x=0*16, y=9*16,width=16,height=16),
        ]
        self.texture_stage = 0

    def degrade(self) -> None:
        if self.resource.amount > 0:
            self.resource = Resource("rock", amount=self.resource.amount/2, value=self.resource.value/2)
            self.texture_stage += 1
            if self.texture_stage >= len(self.textures):
                self.texture_stage -= 1
            self.texture = self.textures[self.texture_stage]
             

class Water(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png",
            image_y=2*16,
            image_x=5*16,
            image_width=16,
            image_height=16,
            scale=SPRITE_SCALE
        )
        self.resource = Resource("water", amount=100, value=25)
        self.textures = [
            arcade.load_texture("assets/tiles.png", x=5*16, y=2*16,width=16,height=16),
            arcade.load_texture("assets/tiles.png", x=5*16, y=3*16,width=16,height=16),
            arcade.load_texture("assets/tiles.png", x=2*16, y=10*16,width=16,height=16),
        ]
        self.texture_stage = 0

    def degrade(self) -> None:
        if self.resource.amount > 0:
            self.resource = Resource("water", amount=self.resource.amount/2, value=self.resource.value/2)
            self.texture_stage += 1
            if self.texture_stage >= len(self.textures):
                self.texture_stage -= 1
            self.texture = self.textures[self.texture_stage]
        

class Tree(arcade.Sprite):

    def __init__(self) -> None:
        super().__init__(
            "assets/tiles.png",
            image_y=9*16,
            image_x=4*16,
            image_width=16,
            image_height=16,
            scale=SPRITE_SCALE
        )
        self.resource = Resource("wood", amount=20, value=10)
        self.textures = [
            arcade.load_texture("assets/tiles.png", x=4*16, y=9*16,width=16,height=16),
            arcade.load_texture("assets/tiles.png", x=4*16, y=10*16,width=16,height=16),
            arcade.load_texture("assets/tiles.png", x=2*16, y=8*16,width=16,height=16),
        ]
        self.texture_stage = 0

    def degrade(self) -> None:
        if self.resource.amount > 0:
            self.resource = Resource("wood", amount=self.resource.amount/2, value=self.resource.value/2)
            self.texture_stage += 1
            if self.texture_stage >= len(self.textures):
                self.texture_stage -= 1
            self.texture = self.textures[self.texture_stage]


class Player(arcade.Sprite):

    def __init__(self, x, y) -> None:
        super().__init__(
            "assets/characters.png",
            image_y=0*16,
            image_x=7*16,
            image_width=16,
            image_height=16,
            scale=SPRITE_SCALE
        )
        self.backpack = {
            "space": 50,
            "wood": 0,
            "water": 0,
            "rock": 0,
            "grass": 0
        }
        self.delta_x = 0
        self.delta_y = 0
        self.true_x = x
        self.true_y = y
        

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

    def update(self, *args):
        self.center_x = (self.true_x // (16 * SPRITE_SCALE)) * 16 * SPRITE_SCALE
        self.center_y = (self.true_y // (16 * SPRITE_SCALE)) * 16 * SPRITE_SCALE
        self.true_x += self.delta_x
        self.true_y += self.delta_y
        super().update(*args)
