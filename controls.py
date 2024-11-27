from ursina import held_keys, time, random
import config

def getInputs(PBall, PPlayer):
    # Move player left
    if held_keys['a'] and PPlayer.x - config.PlayerLength / 2 > config.LeftWall.x + 0.2 and config.GameState == "Playing":
        PPlayer.x -= 5 * time.dt * config.PlayerSpeed
    
    # Move player left
    if held_keys['d'] and PPlayer.x + config.PlayerLength / 2 < config.RightWall.x - 0.2 and config.GameState == "Playing":
        PPlayer.x += 5 * time.dt * config.PlayerSpeed
    
    # Unpause the game at start of levels
    if held_keys['space'] and config.GameState == "Paused":
        PBall.velocity.y = config.StartingSpeed
        PBall.velocity.x = random.choice([-config.StartingSpeed, config.StartingSpeed])
        config.GameState = "Playing"
