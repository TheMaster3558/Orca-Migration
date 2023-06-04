import subprocess
import threading
import time
from typing import TYPE_CHECKING

from cmu_graphics import *
import random

randint = random.randint
choice = random.choice

from buttons import Button

subprocess.Popen(["python", "-m", "black", "."])

if TYPE_CHECKING:
    from cmu_types import (
        Group,
        Image,
        Label,
        Rect,
        Star,
        app,
        cmu_graphics,
        pythonRound,
        randrange,
    )

app.explosions = None
app.starsleft = 11
app.arnav_health = 100
app.arnav_label = Label(
    f"Health {app.arnav_health}",
    -500,
    -600,
    size=30,
)
app.arnav_picture = Image("arnav.png", -500, -500, visible=False)
app.arnav = Group(app.arnav_picture, app.arnav_label)


def attackArnav():
    if app.arnav_health > 0:
        app.arnav_health -= 1
    if orca.health > 1:
        orca.health -= 0.2
        orca.health = pythonRound(orca.health, 2)
    if app.arnav_health == 0:
        Label("you win!", 300, 150, size=50)
        Label(
            "Fewer than 75 Southern Resident orcas remain today, among the lowest in decades.",
            300,
            200,
            size=15,
        )
        Label(" Why are orcas dying?", 300, 180, size=20)
        Label(
            "Vessel noise and water pollution in the Puget Sound ",
            300,
            250,
            size=15,
        )
        Label("play a role, but primarily, scientists", 300, 280)

        Label(
            "point to the disappearance of Chinook salmon—the orcas’ main food source.",
            300,
            300,
            size=15,
        )
        app.stop()
        return

    app.arnav_label.value = f"Health {app.arnav_health}"


sun = Circle(600, 0, 20, fill="yellow")
fishes = Group()
fishes.toFront()
app.level2label = Label("Level 2", 300, 300, size=50, visible=False)
app.level2instructions = Label(
    "Avoid the trash and the poisoned fish!", 300, 350, size=25, visible=False
)
# Title screen
water = Rect(
    0,
    0,
    600,
    400,
    fill=gradient(rgb(200, 200, 240), "white", rgb(255, 255, 204), start="bottom-left"),
)
air = Rect(0, 200, 600, 400, fill=gradient("lightBlue", rgb(0, 0, 170), start="top"))
hills = Group()
hills.toBack()
air.toBack()
water.toBack()

app.trashleft = 15
app.current_level = 0
app.fishesleft = 15
app.stepCount = 0
air = Rect(0, 200, 600, 400, fill="skyBlue")


startGroup = Group(
    Label("Orca's Migration", 300, 50, size=35, bold=True),
    Label("Help an orca on its journey throught the Puget Sound", 300, 90, size=18),
    Label("Progress through the levels of the game to ", 300, 115, size=15),
    Label("find the struggles in an orcas journey.", 300, 135, size=15),
    Label("Use the arrow keys to move", 300, 450, size=18),
)
##wave = Image("waves.jpg", 200,200)
for i in range(2):
    hill = Image("hills.png", i * 986, 70)
    hill.height *= 0.5
    hill.width *= 0.5
    hill.toBack()
    hills.add(hill)
hills.toBack()
air.toBack()
water.toBack()
tail = Image("orca 1-split (1).png", 100, 150)
tail.goingup = True
orca = Group(Image("orca 1-split.png", 210, 210), tail)
orca.rotateAngle = 0
orca.height *= 0.2
orca.width *= 0.2
orca.health = 100
orca.food = 50
orca.centerY = 300
orca.centerX = 300
healthLabel = Label(f"Health: {orca.health}", 50, 500)
healthBar = Rect(20, 520, 50, 20, fill="green")
foodLabel = Label(f"Food: {orca.food}", 50, 550)
foodBar = Rect(20, 570, 50, 20, fill="yellow")
app.current_orca_index = 0

arrow_keys = {
    "left": {"pressed": False, "momentum": 0},
    "right": {"pressed": False, "momentum": 0},
    "up": {"pressed": False, "momentum": 0},
    "down": {"pressed": False, "momentum": 0},
}
health_and_food = Group(healthLabel, foodLabel, foodBar, healthBar)
health_and_food.visible = False

trash1 = "trash1.png"
trash2 = "apple core.png"
trash3 = "shoe.png"
trashGroup = Group()
trashList = [trash1, trash2, trash3]
trashSpeed = 5


def update_orca_position():
    acceleration = 0.5
    friction = 0.2
    max_speed = 5

    for key, key_state in arrow_keys.items():
        if key_state["pressed"]:
            key_state["momentum"] += acceleration
            if key_state["momentum"] > max_speed:
                key_state["momentum"] = max_speed
        else:
            key_state["momentum"] -= friction
            if key_state["momentum"] < 0:
                key_state["momentum"] = 0

    speed = max([key_state["momentum"] for key_state in arrow_keys.values()])

    if arrow_keys["left"]["pressed"]:
        if orca.centerX > 0:
            orca.centerX -= speed
    if arrow_keys["right"]["pressed"]:
        if orca.centerX < 600:
            orca.centerX += speed
    if arrow_keys["up"]["pressed"]:
        if orca.centerY > 200:
            orca.centerY -= speed
    if arrow_keys["down"]["pressed"]:
        if orca.centerY < 600:
            orca.centerY += speed


# health and food bars
def onStep():
    for hill in hills.children:
        if hill.right < 0:
            hill.left = 800
    hills.centerX -= 3
    app.stepCount += 1
    if app.stepCount % 15 == 0 and app.current_level == 3:
        spawnFish()
        app.arnav.top = randint(100, 500)
        app.arnav.left = randint(100, 500)

    if app.current_level == 3 and orca.hitsShape(app.arnav):
        attackArnav()

    if tail.goingup:
        tail.rotateAngle += 3
        if tail.rotateAngle >= 40:
            tail.goingup = False
    else:
        tail.rotateAngle -= 3
        if tail.rotateAngle <= 0:
            tail.goingup = True

    if orca.food < 1 or orca.health < 1:
        Label("You died. Please try again!", 300, 300)
        app.stop()
        return
    if app.current_level > 1 and app.stepCount % 20 == 0:
        orca.food -= 1
    if app.current_orca_index == 2:
        app.current_orca_index = 0
    else:
        app.current_orca_index += 1
    if (
        app.level2label.visible or app.level2instructions.visible
    ) and app.stepCount % 100 == 0:
        app.level2label.visible = False
        app.level2instructions.visible = False
    if orca.food == 100 and app.current_level == 1:
        fishes.clear()
        level2()
        orca.centerY = 300
        orca.centerX = 50
        app.current_level = 2
    app.stepCount += 1
    interval = 25 if app.current_level == 1 else 12
    if app.stepCount % interval == 0 and app.fishesleft > 0:
        app.fishesleft -= 1
        spawnFish()

    if app.stepCount % 25 == 0 and app.trashleft > 0 and app.current_level == 2:
        app.trashleft -= 1
        spawnTrash()

    if app.current_level > 0:
        update_orca_position()

        if orca.health < 1 or orca.food < 1:
            Label("you died", 300, 300, size=100)
            app.stop()
            return
        healthBar.width = orca.health
        foodBar.width = orca.food
        healthLabel.value = f"Health: {orca.health}"
        foodLabel.value = f"Food: {orca.food}"

        if app.current_level == 1:
            if fishes.children:
                for fish in fishes.children:
                    fish.centerX -= 5
                    if fish.centerY > 220:
                        fish.centerY += randrange(-10, 10)
                    else:
                        fish.centerY += randrange(0, 10)
                    if fish.hitsShape(orca):
                        fishes.remove(fish)
                        fish.visible = False
                        if orca.food < 100:
                            orca.food += 5

                    if fish.centerX < 0:
                        fishes.remove(fish)
            if app.fishesleft == 0 and not fishes.children and orca.food != 100:
                Label("You didn't eat enough food", 300, 300, size=30)
                app.stop()

        elif app.current_level == 2:
            if (
                not trashGroup.children
                and not fishes.children
                and app.fishesleft == 0
                and app.trashleft == 0
            ):
                level3()
            if trashGroup.children:
                for trash in trashGroup.children:
                    trash.centerX -= trashSpeed
                    if trash.centerY > 220:
                        trash.centerY += randrange(-10, 10)
                    else:
                        trash.centerY += randrange(0, 10)

                    if trash.hitsShape(orca):
                        trashGroup.remove(trash)

                        if orca.health > 0:
                            orca.health -= 10
                    if trash.centerX < 0:
                        trashGroup.remove(trash)

            if fishes.children:
                for fish in fishes.children:
                    if fish.centerX < 0:
                        fishes.remove(fish)
                    if fish.hitsShape(orca):
                        orca.health -= 5
                        orca.food -= 5
                        fishes.remove(fish)
                    fish.centerX -= 5
                    if fish.centerY > 220:
                        fish.centerY += randrange(-10, 10)
                    else:
                        fish.centerY += randrange(0, 10)



# Directions screen
def onMousePress(mouseX, mouseY):
    Button.process(mouseX, mouseY)


def onKeyPress(key):
    if key in arrow_keys:
        arrow_keys[key]["pressed"] = True
        update_orca_position()


# Event handler for key release events
def onKeyRelease(key):
    if key in arrow_keys:
        arrow_keys[key]["pressed"] = False


def spawnFish():
    y = randint(200, 600)
    if y > 600:
        y = 600
    x = randint(600, 800)
    fish = Image(
        "red fish.png"
        if app.current_level < 2
        else "pngtree-puffed-out-fugu-fish-png-image_1996174-removebg-preview.png",
        x,
        y,
    )
    fish.toFront()
    fish.width *= 0.075
    fish.height *= 0.075
    fishes.add(fish)


def spawnTrash():
    y = randint(200, 600)
    x = randint(600, 800)
    trash = Image(choice(trashList), x, y)
    trashGroup.add(trash)
    trash.toFront()
    trash.width *= 0.1
    trash.height *= 0.1


# First level screen
def start():
    health_and_food.visible = True
    startButton.rect.visible = False
    startButton.label.visible = False
    startGroup.visible = False

    app.current_level += 1
    if app.current_level == 1:
        print("level is 1")
        level1()


def level1():
    orca.centerY = 300
    orca.centerX = 50
    app.fishesleft = 15


startButton = Button("Start", Rect(200, 500, 200, 50, fill="green"), start)


# level 2
def level2():
    app.level2label.visible = True
    app.level2instructions.visible = True
    app.fishesleft = 30
    app.current_level = 2

    # Define a function to hide the Level 2 labels
    def hideLevel2Labels():
        app.level2label.visible = False
        app.level2instructions.visible = False
        timer.cancel()

    # Schedule the hideLevel2Labels() function to run after 1 second
    timer = threading.Timer(1, hideLevel2Labels)
    timer.start()


def level3():
    Label("get the shark!", 300, 50, size=25)
    app.current_level = 3
    app.arnav.visible = True
    app.arnav.toFront()
    app.arnav_label.centerX = 250
    app.arnav_label.centerY = 190
    app.arnav_picture.left, app.arnav_picture.top = 200, 200


"""
details: 
- ships as borders 
- mini islands/rocks as obstacles
- polluted water poisons you
- health bar to keep track of health 
- if you die you get sent back to the start
- healthy fish and bad fish; eating healthy fish gives you a health #boost while bad fish take away health
- special fish can give you a speed boost or temporary immortality or bad ones slow you down 
- ships occassionally coming through which can kill you instantly 

level 1: 
no challenge, moving through the water w/ obstacle 

level 2: 
trash - eating fish poisons you, have to dodge trash 

level 3: 
ships - maze, have to pass it in 30 seconds or the ships will come through

level 4:
disease - animals are trying to eat you 

level 5: 
oil spill adds sense of urgency, humans are trying to kill you (multiple difficulties of humans) 
"""


app._app.width, app._app.height = 600, 600
cmu_graphics.run()
