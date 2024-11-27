from ursina import time, Entity, Vec2, Text, destroy, random
import config
import levels
import powerups

def moveBall(Ball):
    if config.GameState == "Playing":
        # Records the previous position for collision detection purposes (helpers.handleBrickIntersect())
        Ball.previous_x = Ball.x
        Ball.previous_y = Ball.y

        # Updates ball position
        Ball.x += Ball.velocity.x * time.dt
        Ball.y += Ball.velocity.y * time.dt

        # Records the edges for collision detection purposes (helpers.handleBrickIntersect())    
        Ball.left_edge = Ball.x - Ball.scale_x / 2
        Ball.right_edge = Ball.x + Ball.scale_x / 2
        Ball.top_edge = Ball.y + Ball.scale_y / 2
        Ball.bottom_edge = Ball.y - Ball.scale_y / 2


def looseLife(PLivesText: Entity):
    # Update the lives counter. If 0 lives, update GameState
    config.Lives -= 1
    PLivesText.text = str(config.Lives)
    if config.Lives == 0:
        config.GameState = "GameOver"

def resetLevel(PPlayer: Entity, PBall: Entity) -> None:
    # Reset player and ball position + velocity.
    config.LevelText.text = str(config.Level)
    PPlayer.position = (0, -3.5)
    PBall.position = (0, -2)
    PBall.velocity = Vec2(0, 0)

def handleBrickIntersect(PBrick: Entity, PBricks: list, PBall: Entity, PPointsText: Text) -> None:
    # Check if collision is with left, right, top or bottom edge.
    # This function uses the custom edge attributes for both the ball (set in helpers.move_ball) and bricks (set in levels.generateBricks)

    # How this works:
    # 1. Check if ball is with in bricks LEFT <-> RIGHT or TOP <-> BOTTOM boundries.
    # 2. If it is, in the opposite axis, check if with in the last frame the ball has moved from outside to inside brick.
    # 3. Reverse velocity accordingly.
    # 4. Remove brick
    # 5. Speed up ball
    # 6. Increment points

    if (PBall.right_edge > PBrick.left_edge) and (PBall.left_edge < PBrick.right_edge):
        if (PBall.previous_y + PBall.scale_y / 2 < PBrick.bottom_edge) and (PBall.top_edge > PBrick.bottom_edge):
            PBall.velocity.y *= -1 

        elif (PBall.previous_y - PBall.scale_y / 2 > PBrick.top_edge) and (PBall.bottom_edge < PBrick.top_edge):
            PBall.velocity.y *= -1

    if (PBall.top_edge > PBrick.bottom_edge) and (PBall.bottom_edge < PBrick.top_edge):
        if (PBall.previous_x + PBall.scale_x / 2 < PBrick.left_edge) and (PBall.right_edge > PBrick.left_edge):
            PBall.velocity.x *= -1 

        if (PBall.previous_x - PBall.scale_x / 2 > PBrick.right_edge) and (PBall.left_edge < PBrick.right_edge):
            PBall.velocity.x *= -1

    # For future debugging DONT DELETE :D
    # print(f"Bric Bot edge y: {round(PBrick.position[1] - PBrick.scale_y / 2, 5)} = Bric y: {round(PBrick.position[1], 4)} - Bric height: {round(PBrick.scale_y / 2, 4)}")
    # print(f"Ball Top edge y: {round(PBall.position[1] + PBall.scale_y / 2, 5)} = Ball y: {round(PBall.position[1], 4)} + Ball height: {round(PBall.scale_y / 2, 4)}")
    # print("")
    # print("")

    # Remove brick
    PBricks.remove(PBrick)
    destroy(PBrick)

    # Speed up ball
    speedUpBall(PBall)

    # Increment points state
    config.Points += config.Level * 10
    PPointsText.text = str(config.Points)

def speedUpBall(PBall: Entity) -> None:
    # Add SpeedUpBy ammount of speed on either x or y axis
    Change = config.SpeedUpBy + (config.Level / 5) * config.SpeedUpBy
    Choice = random.choice(["x", "y"])

    if Choice == "x":
        if PBall.velocity.x > 0:
            PBall.velocity.x += Change
        else:
            PBall.velocity.x -= Change

    elif Choice == "y":
        if PBall.velocity.y > 0:
            PBall.velocity.y += Change
        else:
            PBall.velocity.y -= Change

def checkForCollisions(PBall: Entity, PBricks: list, PPointsText: Entity):
    # Collision with player
    if PBall.intersects(config.Player).hit:
        PBall.position = (PBall.position.x, PBall.position.y + 0.1)
        PBall.velocity.y *= -1

    # Collision with right wall
    if PBall.intersects(config.RightWall).hit:
        PBall.position = (PBall.position.x - 0.1, PBall.position.y)
        PBall.velocity.x *= -1

    # Collision with left wall
    if PBall.intersects(config.LeftWall).hit:
        PBall.position = (PBall.position.x + 0.05, PBall.position.y)
        PBall.velocity.x *= -1

    # Collision with brick
    for Brick in PBricks:
        if PBall.intersects(Brick).hit:
            handleBrickIntersect(Brick, PBricks, PBall, PPointsText)

def checkForWin(PBall: Entity):
    if PBall.intersects(config.TopWall).hit:
        PBall.position = (PBall.position.x, PBall.position.y - 0.08)

        # Still levels left to go
        if config.Level < 10:
            # Update states
            config.Points += (50 * 2**config.Level) 
            config.PointsText.text = str(config.Points)
            config.Level += 1
            config.GameState = "WaitingForChoice"

            # Pick a powerup
            powerups.getOptions()

            # Go to next level (this happens already before the player can choose a powerup, but config.state stops player from playing before selection)
            resetLevel(config.Player, PBall)
            levels.getNewBricks()

        else:
            config.GameState = "Win"
            config.Points += (50 * 2**config.Level) 
            config.PointsText.text = str(config.Points)
            YOU_WIN_TEXT = Text(text="CONGRATULATIONS YOU WIN!", scale=4, position=(-0.71, -0.05), color=config.GUI_COLOR)
            FINAL_SCORE_TEXT = Text(text=f"FINAL SCORE: {config.Points}", scale=4, position=(-0.4, -0.2), color=config.GUI_COLOR)

def checkForLoose(PBall, PLivesText):
    if PBall.y < -4.2 and config.GameState == "Playing":
        # Decrement a life or check if game over
        looseLife(PLivesText)

        # If lifes left
        if config.GameState == "Playing":
            resetLevel(config.Player, PBall)
            config.GameState = "Paused"

        # If no lifes left
        elif config.GameState == "GameOver":
            GAME_OVER_TEXT = Text(text="GAME OVER", scale=6, position=(-0.43, 0.0), color=config.GUI_COLOR)
            
            FINAL_SCORE_TEXT = Text(text=f"FINAL SCORE: {config.Points}", scale=4, position=(-0.4, -0.2), color=config.GUI_COLOR)

if __name__ == "__main__":
    pass