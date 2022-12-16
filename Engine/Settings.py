
class Settings:
    WIN_WIDTH = 1800
    WIN_HEIGHT = 1000

    SCREEN1_WIDTH = int(WIN_WIDTH)
    SCREEN1_HEIGHT = int(WIN_HEIGHT*0.75)

    SCREEN2_WIDTH = WIN_WIDTH
    SCREEN2_HEIGHT = WIN_HEIGHT - SCREEN1_HEIGHT

    FPS = 60
    SPEED = 1
    DT_FRACTION = 0.1
    N_DT_STEPS = int(SPEED/DT_FRACTION)
    DT = DT_FRACTION/FPS

    global VISUAL_ON
    VISUAL_ON = True

    SOUND_ON = False
    DRAW_COORDINATES = True
    SAVE_TO_FILE = True

    GRAVITY_ON = False
    ELECTRICITY_ON = True

    RECORD_ACTIVE = False