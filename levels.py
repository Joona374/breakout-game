from ursina import Entity, random, destroy
import config

Bricks = []

def generateBricks():
    global Bricks

    for i in range(config.Level):
        if i != 9: # If not final level
            # Even numbered rows
            if i % 2 == 0:
                for j in range(12):
                    Brick = Entity(model="quad", color=(random.random(), random.random(), random.random(), 1), scale=(0.9, 0.4), position=(-5.5 + j * 1, -0.5 + i * 0.5), collider="box")
                    Bricks.append(Brick)

            # Odd numbered rows
            else:
                for j in range(11):
                    Brick = Entity(model="quad", color=(random.random(), random.random(), random.random(), 1), scale=(0.9, 0.4), position=(-5.0 + j * 1, -0.5 + i * 0.5), collider="box")
                    Bricks.append(Brick)

        else:   # FINALBOSS aka level 10!
            for j in range(24): 
                Brick = Entity(model="quad", color=(random.random(), random.random(), random.random(), 1), scale=(0.40, 0.4), position=(-5.75 + j * 0.5, -1), collider="box")                
                Bricks.append(Brick)

    # Set the edge coordinates for brick. These are used in collision detection
    for JustMadeBrick in Bricks:
        JustMadeBrick.left_edge = JustMadeBrick.x - JustMadeBrick.scale_x / 2
        JustMadeBrick.right_edge = JustMadeBrick.x + JustMadeBrick.scale_x / 2
        JustMadeBrick.bottom_edge = JustMadeBrick.y - JustMadeBrick.scale_y / 2
        JustMadeBrick.top_edge = JustMadeBrick.y + JustMadeBrick.scale_y / 2   

    if config.ReduceBricks > 0:
        for Brick in Bricks:
            if random.random() < config.ReduceBricks:
                Bricks.remove(Brick)
                destroy(Brick)

def getNewBricks() -> list:
    global Bricks
    # Remove old brick entities and clear the list
    for Brick in Bricks:
        destroy(Brick)
    Bricks.clear()
    
    # Make new bricks
    generateBricks()