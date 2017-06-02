class Text(object):
    def __init__(self, spritesheet):
        self.sheet = spritesheet
        self.images = self.getTextImages()
        self.width, self.height = 16, 16
        
    def getTextImages(self):
        images = {}
        images['A'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['B'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['C'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['D'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['E'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['F'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['G'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['H'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['I'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['J'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['K'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['L'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['M'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['N'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['O'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['P'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['Q'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['R'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['S'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['T'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['U'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['V'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['W'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['X'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['Y'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['Z'] = self.sheet.getImage(17, 9, self.width, self.height)

        images['0'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['1'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['2'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['3'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['4'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['5'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['6'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['7'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['8'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['9'] = self.sheet.getImage(17, 9, self.width, self.height)

        return images

