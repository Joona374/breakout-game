from ursina import random, Button, Text, color, destroy
import config
import levels

PowerUps = ["Extra Life", "Speed Up", "Slow Down", "Get Wider", "Reduce Bricks"]
ActivePowerUps = []
Buttons = []

def createButtons():
    global Buttons

    LocalPowerUps = list(PowerUps) # Create local copy, so can remove from the list.

    for _ in range(3): # Create 3 buttons
        Choice = random.choice(LocalPowerUps)
        LocalPowerUps.remove(Choice)

        PowerUpButton = Button(text=Choice, color=color.azure, scale=(0.3, 0.1), position=(0, 0))
        if Choice == "Extra Life":
            PowerUpButton.on_click = getExtraLife
        elif Choice == "Speed Up":
            PowerUpButton.on_click = getSpeedUp
        elif Choice == "Slow Down":
            PowerUpButton.on_click = getSlowDown
        elif Choice == "Get Wider":
            PowerUpButton.on_click = getWider
        elif Choice == "Reduce Bricks":
            PowerUpButton.on_click = getReduceBricks

        Buttons.append(PowerUpButton) # Append to global Buttons list

def getOptions() -> None:
    # Create three buttons to pick powerup
    createButtons()

    # Place buttons correctly
    for i in range(len(Buttons)):
        Buttons[i].position = (-0.5 + i * 0.5, -0.25)

    # Create the Label text
    Label = Text(text="Choose a powerup", scale=2, position=(-0.22, -0.1), color=config.GUI_COLOR)
    Buttons.append(Label)

def drawPowerUpText(PowerupName: str) -> None:
    # For each powerup, add the name to GUI list
    global ActivePowerUps

    Quantity = len(ActivePowerUps)
    Label = Text(text=PowerupName, scale=0.8, position=(-0.88, 0.14 - Quantity * 0.04), color=config.GUI_COLOR)
    ActivePowerUps.append(PowerupName)

def endButtonClick() -> None:
    # This is the clean up after selection. Update gamestate, and remove the buttons.
    config.GameState = "Paused" 
    
    # Clear the Buttons
    for Button in Buttons[:]: 
        if Button:
            destroy(Button)
    Buttons.clear()
    

# Powerup functions to be called when one is selected
#############################################################
def getExtraLife() -> None:
    config.Lives += 1
    config.LivesText.text = str(config.Lives)
    drawPowerUpText("Extra Life")
    endButtonClick()

def getSpeedUp() -> None:
    config.PlayerSpeed += 0.5
    drawPowerUpText("Speed Up")
    endButtonClick()

def getSlowDown() -> None:
    config.SpeedUpBy /= 1.5
    drawPowerUpText("Slow Down")
    endButtonClick()

def getWider() -> None:
    config.PlayerLength += 0.6
    config.Player.scale = (config.PlayerLength, 0.2)
    drawPowerUpText("Get Wider")
    endButtonClick()

def getReduceBricks() -> None:
    if config.ReduceBricks < 0.9:
        config.ReduceBricks += 0.2
    levels.getNewBricks()
    drawPowerUpText("Reduce Bricks")
    endButtonClick()
#############################################################