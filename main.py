from ursina import Ursina, window

import levels
import config
import helpers
import controls

# Init App
App = Ursina()
window.fullscreen = True
window.entity_counter.enabled = False
window.fps_counter.enabled = False
window.collider_counter.enabled = False

# Set up Entities
Player = config.returnPlayer()
Ball = config.returnBall()
RightWall = config.returnRightWall()
LeftWall = config.returnLeftWall()
TopWall = config.returnTopWall()

# Set up GUI
config.initGUI()
LevelText = config.returnLevelText()
LivesText = config.returnLivesText()
PointsText = config.returnPointsText()

# Generate bricks for starting level
levels.generateBricks()

def update():
    # Move the ball
    helpers.moveBall(Ball)

    # Check for collisions between ball and bricks or walls.
    helpers.checkForCollisions(Ball, levels.Bricks, PointsText)

    # Listen for and handle contorl inputs
    controls.getInputs(Ball, Player)

    # Check if player wins a level
    helpers.checkForWin(Ball)

    # Check if player looses a level
    helpers.checkForLoose(Ball, LivesText)
    
# Run the App
App.run()