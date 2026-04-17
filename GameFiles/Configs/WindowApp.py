W, H = 1600, 900
WH = (W, H)
RESOLUTION = WH

Center = (W // 2, H // 2)
Center_left_box = (Center[0] // 2, Center[1])
Center_right_box = (Center[0] + Center_left_box[0], Center[1])

Center_top_box = (Center[0], Center[1] // 2)
Center_bottom_box = (Center[0], Center[1] + Center_top_box[1])

bottomLights = Center_bottom_box[1] - 100

#offsets
Left = 30
Right = 30
Top = 30
Bottom = 30

# calculated offsets
right = W - Right
bottom = H - Bottom

## Pointers
top_left = (Left, Top)
top_right = (right, Top)
bottom_left = (Left, bottom)
bottom_right = (right, bottom)

bottom_left_gradient = (bottom_left[0], bottom_left[1] - 11)

#Debug Text
debug_text = (bottom_left[0] + 20, bottom_left[1] - 80)
debug_matches = (debug_text[0], debug_text[1] - 40)

#Audio Progress
Audio_thickness = 10
Audio_margin = 6
Audio_Y = bottom_left[1] - Audio_margin

Audio_left = bottom_left[0] - 1
Audio_right = bottom_right[0] + 2

Audio_total_width = Audio_right - Audio_left

Audio_Left = (Audio_left, Audio_Y)
Audio_Right = (Audio_right, Audio_Y)

# Game Paused Surface
Surface = (Center[0], H - 120)

MusicKit = (right - 170, H - 120)

H_Hidden = H + 10

# vsync = True
vsync = False

FPS = 165
# FPS = 90
# FPS = 60
# FPS = 10
# FPS = 10000

FPS += 10

# FPS = 0
# FPS = 10

if vsync:
    FPS = 0

# Calculate player offset collision
from GameFiles.Settings.Player import Offset_collision
with_player_collision = (Left + Offset_collision[0], right - Offset_collision[0])
