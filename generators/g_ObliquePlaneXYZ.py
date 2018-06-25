class g_ObliquePlaneXYZ():

    def __init__(self):
        self.wait = 1
        self.voxreader = g_voxreader(./voxFiles/ObliqueplaneXYZ/)

    def control(self, wait, blub0, blub1):
        self.wait = wait
        self.voxreader.control(wait,0,0)

    def label(self):
        return ['wait',round(self.wait,2),'empty', 'empty','empty','empty']
