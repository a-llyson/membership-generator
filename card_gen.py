from PIL import Image, ImageFont, ImageDraw
from decouple import config
import requests
import base64

API_KEY = config('KEY')

# CONSTANTS
# (R,G,B,Opacity)
WHITE_OPAQUE = (255, 255, 255, 225)
GREEN_OPAQUE = (51, 201, 102, 225)
GOLD_OPAQUE = (254, 201, 1, 255)
BLACK_OPAQUE = (0, 0, 0, 255)
WHITE_TRANSPARENT = (255, 255, 255, 0)
CARD_TEMPLATE = "bg.png"
NAME_COORDINATES = (35, 200) 
TIER_COORDINATES = (695, 90)  
EXPIRY_COORDINATES = (695, 210)  
CODE_COORDINATES = (35, 385)  
NAME_FONT_SIZE = 53
TIER_FONT_SIZE = 29
EXPIRY_FONT_SIZE = 33
CODE_FONT_SIZE = 59

months = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "Aug",
    "09": "Sept",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec"
}

bg = Image.open(CARD_TEMPLATE).convert('RGB')

def convertDate(date):
    date = date.split("-")
    year = date[0]
    month = months[date[1]]
    day = date[2]
    return f"{month} {day}, {year}"

def toBinary(image):
    return base64.b64encode(open("result.png", "rb").read())

class AccessCard:
    def __init__(self, name, code, tier, exp):
        self.name = name
        self.code = code
        self.tier = tier
        self.exp = convertDate(exp)
        self.image = bg.copy()

        self.nameFont = ImageFont.truetype(
            'GalanoGrotesqueRegular.ttf', NAME_FONT_SIZE)
        self.tierFont = ImageFont.truetype(
            'Myriad Pro Semibold.ttf', TIER_FONT_SIZE)
        self.codeFont = ImageFont.truetype(
            'GalanoGrotesqueRegular.ttf', CODE_FONT_SIZE)
        self.expFont = ImageFont.truetype(
            'GalanoGrotesqueRegular.ttf', EXPIRY_FONT_SIZE)


    # Generic function 
    def generateCard(self):
        self.writeName()
        self.writeTier()
        self.writeCode()
        self.writeExp()
        return self
    
    def drawText(self, coordinates, text, font, colour):
        context = ImageDraw.Draw(self.image)
        context.multiline_text(coordinates, text, font=font, fill=colour)
        return self

    def writeName(self):
        self.drawText(NAME_COORDINATES, self.name, self.nameFont, (WHITE_OPAQUE))
        return self

    def writeTier(self):
        colour = GOLD_OPAQUE
        if "gold" not in self.tier.lower():
            colour = GREEN_OPAQUE
        
        self.drawText(TIER_COORDINATES, self.tier.upper(), self.tierFont, colour)
        return self
    
    def writeCode(self):
        self.drawText(CODE_COORDINATES, self.code, self.codeFont, WHITE_OPAQUE)
        return self

    def writeExp(self):
        self.drawText(EXPIRY_COORDINATES, self.exp.upper(), self.expFont, WHITE_OPAQUE)
        return self

    def showImage(self):
        self.image.show()
        return self

    def saveImage(self):
        self.image.save("result.png")
        return self
    
    def uploadImgbb(self):
        url = "https://api.imgbb.com/1/upload"
        payload = {
            'key' : API_KEY,
            'image' : toBinary('result.png'),
            'expiration' : 60
        }
        headers = {}
        res = requests.post(url, data=payload, headers=headers)
        data = res.json() 
        print(data)
        return data['data']['url_viewer']


    def wrapper(self):
        return self.generateCard().saveImage().uploadImgbb()

    


# print(bg.format, bg.size, bg.mode)
# card = AccessCard("Temp", "12345", "platinum level", "1999-01-01").generateCard().saveImage()
