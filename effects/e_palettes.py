# modules
import numpy as np
from itertools import cycle

from palettable.cartocolors.diverging import ArmyRose_7, Earth_7, Fall_7, Geyser_7, TealRose_7, Temps_7, Tropic_7
from palettable.cartocolors.qualitative import Antique_10, Bold_10, Pastel_10, Prism_10, Safe_10, Vivid_10
from palettable.cartocolors.sequential import BluGrn_7, BluYl_7, BrwnYl_7, Burg_7, BurgYl_7, DarkMint_7, Emrld_7, Magenta_7, Mint_7, OrYel_7, Peach_7, PinkYl_7, Purp_7, PurpOr_7, RedOr_7, Sunset_7, SunsetDark_7, Teal_7, TealGrn_7, agGrnYl_7, agSunset_7
from palettable.cmocean.diverging import Curl_20, Delta_20
from palettable.cmocean.sequential import Algae_20, Amp_20, Deep_20, Dense_20, Gray_20, Haline_20, Ice_20, Matter_20, Oxy_20, Phase_20, Solar_20, Speed_20, Tempo_20, Thermal_20, Turbid_20
from palettable.colorbrewer.diverging import BrBG_11, PRGn_11, PiYG_11, PuOr_11, RdBu_11, RdGy_11, RdYlBu_11, RdYlGn_11, Spectral_11
from palettable.colorbrewer.qualitative import Accent_8, Dark2_8, Paired_12, Pastel1_8, Pastel2_8, Set1_9, Set2_8, Set3_12
from palettable.colorbrewer.sequential import Blues_9, BuGn_9, BuPu_9, GnBu_9, Greens_9, Greys_9, OrRd_9, Oranges_9, PuBu_9, PuBuGn_9, PuRd_9, Purples_9, RdPu_9, Reds_9, YlGn_9, YlGnBu_9, YlOrBr_9, YlOrRd_9
from palettable.lightbartlein.diverging import BlueDarkOrange12_12, BlueDarkOrange18_18, BlueDarkRed12_12, BlueDarkRed18_18, BlueGray_8, BlueGreen_14, BlueGrey_8, BlueOrange10_10, BlueOrange12_12, BlueOrange8_8, BlueOrangeRed_13, BlueOrangeRed_14, BrownBlue10_10, BrownBlue12_12, GreenMagenta_16, RedYellowBlue_11
from palettable.lightbartlein.sequential import Blues10_10, Blues7_7
from palettable.matplotlib import Inferno_20, Magma_20, Plasma_20, Viridis_20
from palettable.mycarta import Cube1_20, CubeYF_20, LinearL_20
from palettable.scientific.diverging import  Berlin_20, Broc_20, Cork_20, Lisbon_20, Roma_20, Tofino_20, Vik_20
from palettable.scientific.sequential import Acton_20, Bamako_20, Batlow_20, Bilbao_20, Buda_20, Davos_20, GrayC_20, Hawaii_20, Imola_20, LaJolla_20, LaPaz_20, Nuuk_20, Oleron_20, Oslo_20, Tokyo_20, Turku_20
from palettable.tableau import BlueRed_12, ColorBlind_10, Gray_5, GreenOrange_12, PurpleGray_12, Tableau_20, TableauMedium_10, TrafficLight_9

# install with pip3 install --user palettable

class e_palettes:

    def __init__(self):
        # assemble palette list
        self.palettes = [ArmyRose_7
                        ,Earth_7
                        ,Fall_7
                        ,Geyser_7
                        ,TealRose_7
                        ,Temps_7
                        ,Tropic_7
                        ,Antique_10
                        ,Bold_10
                        ,Pastel_10
                        ,Prism_10
                        ,Safe_10
                        ,Vivid_10
                        ,BluGrn_7
                        ,BluYl_7
                        ,BrwnYl_7
                        ,Burg_7
                        ,BurgYl_7
                        ,DarkMint_7
                        ,Emrld_7
                        ,Magenta_7
                        ,Mint_7
                        ,OrYel_7
                        ,Peach_7
                        ,PinkYl_7
                        ,Purp_7
                        ,PurpOr_7
                        ,RedOr_7
                        ,Sunset_7
                        ,SunsetDark_7
                        ,Teal_7
                        ,TealGrn_7
                        ,agGrnYl_7
                        ,agSunset_7
                        ,Curl_20
                        ,Delta_20
                        ,Algae_20
                        ,Amp_20
                        ,Deep_20
                        ,Dense_20
                        ,Gray_20
                        ,Haline_20
                        ,Ice_20
                        ,Matter_20
                        ,Oxy_20
                        ,Phase_20
                        ,Solar_20
                        ,Speed_20
                        ,Tempo_20
                        ,Thermal_20
                        ,Turbid_20
                        ,BrBG_11
                        ,PRGn_11
                        ,PiYG_11
                        ,PuOr_11
                        ,RdBu_11
                        ,RdGy_11
                        ,RdYlBu_11
                        ,RdYlGn_11
                        ,Spectral_11
                        ,Accent_8
                        ,Dark2_8
                        ,Paired_12
                        ,Pastel1_8
                        ,Pastel2_8
                        ,Set1_9
                        ,Set2_8
                        ,Set3_12
                        ,Blues_9
                        ,BuGn_9
                        ,BuPu_9
                        ,GnBu_9
                        ,Greens_9
                        ,Greys_9
                        ,OrRd_9
                        ,Oranges_9
                        ,PuBu_9
                        ,PuBuGn_9
                        ,PuRd_9
                        ,Purples_9
                        ,RdPu_9
                        ,Reds_9
                        ,YlGn_9
                        ,YlGnBu_9
                        ,YlOrBr_9
                        ,YlOrRd_9
                        ,BlueDarkOrange12_12
                        ,BlueDarkOrange18_18
                        ,BlueDarkRed12_12
                        ,BlueDarkRed18_18
                        ,BlueGray_8
                        ,BlueGreen_14
                        ,BlueGrey_8
                        ,BlueOrange10_10
                        ,BlueOrange12_12
                        ,BlueOrange8_8
                        ,BlueOrangeRed_13
                        ,BlueOrangeRed_14
                        ,BrownBlue10_10
                        ,BrownBlue12_12
                        ,GreenMagenta_16
                        ,RedYellowBlue_11
                        ,Blues10_10
                        ,Blues7_7
                        ,Inferno_20
                        ,Magma_20
                        ,Plasma_20
                        ,Viridis_20
                        ,Cube1_20
                        ,CubeYF_20
                        ,LinearL_20
                        ,Berlin_20
                        ,Broc_20
                        ,Cork_20
                        ,Lisbon_20
                        ,Roma_20
                        ,Tofino_20
                        ,Vik_20
                        ,Acton_20
                        ,Bamako_20
                        ,Batlow_20
                        ,Bilbao_20
                        ,Buda_20
                        ,Davos_20
                        #,Devon_2
                        ,GrayC_20
                        ,Hawaii_20
                        ,Imola_20
                        ,LaJolla_20
                        ,LaPaz_20
                        ,Nuuk_20
                        ,Oleron_20
                        ,Oslo_20
                        ,Tokyo_20
                        ,Turku_20
                        ,BlueRed_12
                        ,ColorBlind_10
                        ,GreenOrange_12
                        ,PurpleGray_12
                        ,Tableau_20
                        ,TableauMedium_10
                        ,TrafficLight_9]
        self.waiting_frames = 1
        self.palette = cycle(self.palettes[0].colors)
        self.step = 0
        self.palette_id = 0
        self.red = 0
        self.blue = 0
        self.green = 0
        print(' initialize e_palettes')

    #strings for GUI
    def return_values(self):
        return [b'palettes', b'Palette ID', b'', b'', b'']

    def __call__(self, world, args):
        # parsing input and check for new palette
        if int((args[0]-0.001)*len(self.palettes)) != self.palette_id:
            self.palette_id = int((args[0]-0.001)*len(self.palettes))
            self.palette = cycle(self.palettes[self.palette_id].colors)

        self.waiting_frames = int(args[1]*10)+1

        # generate color
        if self.step % self.waiting_frames == 0:
            self.red, self.blue, self.green = next(self.palette)

        self.step += 1

        world[0, :, :, :] = world[0, :, :, :]*self.red/255.0
        world[1, :, :, :] = world[1, :, :, :]*self.green/255.0
        world[2, :, :, :] = world[2, :, :, :]*self.blue/255.0

        return np.clip(world, 0, 1)
