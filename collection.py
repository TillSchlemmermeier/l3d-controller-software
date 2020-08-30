from generators.g_blank import *
from generators.g_random import *
from generators.g_planes import *
from generators.g_gauss import *
from generators.g_growing_sphere import *
from generators.g_wavepattern import *
from generators.g_squares import *
from generators.g_trees import *
from generators.g_wave import *
from generators.g_rising_square import *
#from generators.g_planes_falling import *
from generators.g_growingface import *
from generators.g_snake import *
from generators.g_soundcube import *
from generators.g_soundrandom import *
#from generators.g_sphere import *
from generators.g_shooting_star import *
from generators.g_rotate_plane import *
from generators.g_randomlines import *
from generators.g_randomcross import *
from generators.g_rain import *
from generators.g_orbiter import *
from generators.g_pyramid import *
from generators.g_pyramid_upsidedown import *
from generators.g_inandout import *
from generators.g_growing_corner import *
from generators.g_falling import *
from generators.g_drop import *
from generators.g_cut import *
from generators.g_cube import *
from generators.g_cube_edges import *
from generators.g_corner import *
from generators.g_corner_grow import *
from generators.g_columns import *
from generators.g_circles import *
from generators.g_grow import *
#from generators.g_torus import *
from generators.g_sound_lines import *
#from generators.g_centralglow import *
from generators.a_multi_cube_edges import *
from generators.a_orbbot import *
from generators.g_multicube import *
from generators.a_random_cubes import *
from generators.a_squares_cut import *
from generators.a_testbot import *
from generators.g_soundsphere import *
from generators.g_swell import *
from generators.g_sides import *
# from generators.g_grid import *
from generators.g_pong import *
from generators.g_edgelines import *
from generators.g_obliqueplaneXYZ import *
from generators.g_growing_sphere_rand import *
from generators.g_text import *

from effects.e_blank import *
from effects.e_rainbow import *
from effects.e_tremolo import *
from effects.e_rotation import *
from effects.e_staticcolor import *
from effects.e_palettes import *
from effects.e_s2l import *
from effects.e_gradient import *
from effects.e_blur import *
from effects.e_bright_osci import *
from effects.e_cut_cube import *
from effects.e_fade2blue import *
from effects.e_growing_sphere import *
from effects.e_mean import *
from effects.e_mean_vertical import *
from effects.e_newgradient import *
from effects.e_outer_shadow import *
from effects.e_prod_hue import *
from effects.e_prod_saturation import *
from effects.e_random_brightness import *
from effects.e_rare_strobo import *
from effects.e_redyellow import *
from effects.e_remove_random import *
from effects.e_rotating_black_color import *
from effects.e_rotating_black_white import *
from effects.e_rotating_blue_orange import *
#from effects.e_sound_color import *
from effects.e_squared import *
from effects.e_violetblue import *
from effects.e_zoom import e_zoom
from effects.e_rotating_rainbow import *
from effects.e_radial_gradient import *
from effects.e_sound_color import *

generators = []

#row 1
generators.append(g_blank)
generators.append(g_random)
generators.append(g_planes)
generators.append(g_cube)
generators.append(g_wave)
generators.append(g_growing_sphere)
generators.append(g_squares)

#row 2
generators.append(g_trees)
generators.append(g_rising_square)
generators.append(g_obliqueplaneXYZ)
generators.append(g_growingface)
generators.append(g_snake)
generators.append(g_sides)
generators.append(g_sound_lines)
generators.append(g_shooting_star)

#row 3
generators.append(g_rotate_plane)
generators.append(g_randomlines)
generators.append(g_randomcross)
generators.append(g_rain)
generators.append(g_orbiter)
generators.append(g_growing_sphere_rand)
generators.append(g_text)
generators.append(g_pyramid)

#row 4
generators.append(g_pyramid_upsidedown)
generators.append(g_inandout)
generators.append(g_growing_corner)
generators.append(g_falling)
generators.append(g_drop)
generators.append(g_blank)
generators.append(g_cut)
generators.append(g_multicube)

#row 5
generators.append(g_cube_edges)
generators.append(g_corner)
generators.append(g_corner_grow)
generators.append(g_columns)
generators.append(g_circles)
generators.append(g_grow)
generators.append(g_soundsphere)
generators.append(g_swell)

#row 6
generators.append(g_blank)
generators.append(a_multi_cube_edges)
generators.append(g_blank)
generators.append(a_orbbot)
generators.append(g_blank)
generators.append(g_pong)
generators.append(g_edgelines)
generators.append(g_soundcube)

# row 7
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)

# row 8
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)
generators.append(g_blank)


effects = []

#row 1: colors
effects.append(e_blank)
effects.append(e_rainbow)
effects.append(e_staticcolor)
effects.append(e_gradient)
effects.append(e_newgradient)
effects.append(e_palettes)
effects.append(e_redyellow)

#row 2: brightness
effects.append(e_s2l)
effects.append(e_tremolo)
effects.append(e_rare_strobo)
#effects.append(e_blur)
effects.append(e_bright_osci)
effects.append(e_mean)
effects.append(e_mean_vertical)
effects.append(e_random_brightness)
effects.append(e_squared)

#row 4: rotation
effects.append(e_rotating_black_color)
effects.append(e_rotating_black_white)
effects.append(e_rotating_blue_orange)
effects.append(e_rotation)
effects.append(e_rotating_rainbow)
effects.append(e_radial_gradient)
effects.append(e_sound_color)
effects.append(e_blank)

#row 3: empty
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)

#row 4: empty
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)

#row 5: empty
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)

#row 6: empty
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)

#row 7: empty
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)

#row 8: empty
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
effects.append(e_blank)
