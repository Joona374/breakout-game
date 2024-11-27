from ursina import color, Entity, Vec2, Text

# Color constants
ENTITY_COLOR = color.white # Color for walls and the ball
GUI_COLOR = color.white    # Color for GUI

# Game states
GameState = "Paused"    # Paused, WaitingForChoice, Playing, GameOver, Win
Level = 1               # The current level (1-8) played
Lives = 3               # Set the starting amount of lifes. This variable is updated when a life is lost or gained
Points = 0              # Stores points. Per brick 10 * level. Per level 50 * 2^level.
ReduceBricks = 0        # Percentage of bricks to reduce. 0 = no reduction, 1 = all reduction. Currently increments 0.15 per powerup.

# Player settings
PlayerSpeed = 1.4       # Player movement per frame
PlayerLength = 2        # Player width

#Ball settings
StartingSpeed = 3       # Ball movement per frame
SpeedUpBy = 0.1         # How much the ball speeds up in either x or y direction per brick hit


# Set up Entities
######################################################################################################
Player = Entity(model="quad", color=color.red, scale=(PlayerLength, 0.2), position=(0, -3.5), collider="box")

Ball = Entity(model="circle", color=ENTITY_COLOR, scale=(0.2, 0.2), position=(0, -2), collider="box", velocity=Vec2(0, 0), previous_x=0, previous_y=-2)
    
RightWall = Entity(model="quad", color=ENTITY_COLOR, scale=(0.1, 8), position=(6, 0), collider="box")
LeftWall = Entity(model="quad", color=ENTITY_COLOR, scale=(0.1, 8), position=(-6, 0), collider="box")
TopWall = Entity(model="quad", color=ENTITY_COLOR, scale=(11.9, 0.1), position=(0, 3.95), collider="box")

# Functions to return entities
def returnPlayer() -> Entity:
    return Player

def returnBall() -> Entity:
    return Ball

def returnRightWall() -> Entity:
    return RightWall

def returnLeftWall() -> Entity:
    return LeftWall

def returnTopWall() -> Entity:
    return TopWall
######################################################################################################


# Set up GUI
######################################################################################################
def initGUI():
    global LEVEL_HEADER, LevelText, LIVE_HEADER, LivesText, POINTS_HEADER, PointsText, POWERUPS_HEADER
    GUI_SCALE = 1.1 # Scale for GUI text

    LEVEL_HEADER = Text(text="Level:", scale=GUI_SCALE, position=(-0.88, 0.48), color=GUI_COLOR)
    LevelText = Text(text=str(Level), scale=GUI_SCALE, position=(-0.78, 0.48), color=GUI_COLOR)

    LIVE_HEADER = Text(text="Lives:", scale=GUI_SCALE, position=(-0.88, 0.38), color=GUI_COLOR)
    LivesText = Text(text=str(Lives), scale=GUI_SCALE, position=(-0.78, 0.38), color=GUI_COLOR)
    
    POINTS_HEADER = Text(text="Points:", scale=GUI_SCALE, position=(-0.88, 0.28), color=GUI_COLOR)
    PointsText = Text(text=str(Points), scale=GUI_SCALE, position=(-0.88, 0.24), color=GUI_COLOR)

    POWERUPS_HEADER = Text(text="Powerups", scale=GUI_SCALE, position=(-0.88, 0.18), color=GUI_COLOR)

def returnLevelText() -> Text:
    return LevelText

def returnLivesText() -> Text:
    return LivesText

def returnPointsText() -> Text:
    return PointsText
######################################################################################################