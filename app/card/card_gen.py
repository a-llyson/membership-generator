from PIL import Image, ImageFont, ImageDraw
from dotenv import load_dotenv
import requests
import base64
import os 

# CONSTANTS
# (R,G,B,Opacity)
WHITE_OPAQUE = (255, 255, 255, 225)
GREEN_OPAQUE = (51, 201, 102, 225)
GOLD_OPAQUE = (254, 201, 1, 255)
BLACK_OPAQUE = (0, 0, 0, 255)
WHITE_TRANSPARENT = (255, 255, 255, 0)
NAME_COORDINATES = (35, 200) 
TIER_COORDINATES = (695, 90)  
EXPIRY_COORDINATES = (695, 210)  
CODE_COORDINATES = (35, 385)  
NAME_FONT_SIZE = 53
TIER_FONT_SIZE = 29
EXPIRY_FONT_SIZE = 33
CODE_FONT_SIZE = 59

# If card_gen.py is run alone or by heroku
if "card" in os.getcwd():
    CARD_TEMPLATE_PATH = "../images/bg.png"
    CARD_RESULT_PATH = "../images/result.png"
    GALANO_FONT_PATH = "../fonts/GalanoGrotesqueRegular.ttf"
    MYRIAD_FONT_PATH = "../fonts/MyriadProSemibold.ttf"
else:
    CARD_TEMPLATE_PATH = "./app/images/bg.png"
    CARD_RESULT_PATH = "./app/images/result.png"
    GALANO_FONT_PATH = "./app/fonts/GalanoGrotesqueRegular.ttf"
    MYRIAD_FONT_PATH = "./app/fonts/MyriadProSemibold.ttf"


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

# Get env variables
load_dotenv()

# Convert card template
bg = Image.open(CARD_TEMPLATE_PATH).convert('RGB')

def convertDate(date):
    date = date.split("-")
    year = date[0]
    month = months[date[1]]
    day = date[2]
    return f"{month} {day}, {year}"

def toBinary():
    return base64.b64encode(open(CARD_RESULT_PATH, "rb").read())

class AccessCard:
    def __init__(self, name, code, tier, exp):
        self.name = name
        self.code = code
        self.tier = tier
        self.exp = convertDate(exp)
        self.image = bg.copy()

        self.nameFont = ImageFont.truetype(GALANO_FONT_PATH, NAME_FONT_SIZE)
        self.tierFont = ImageFont.truetype(MYRIAD_FONT_PATH, TIER_FONT_SIZE)
        self.codeFont = ImageFont.truetype(GALANO_FONT_PATH, CODE_FONT_SIZE)
        self.expFont = ImageFont.truetype(GALANO_FONT_PATH, EXPIRY_FONT_SIZE)


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
        self.image.save(CARD_RESULT_PATH)
        return self
    
    def uploadImgbb(self):
        url = "https://api.imgbb.com/1/upload"
        payload = {
            'key' : os.getenv('API_KEY'),
            'image' : toBinary(),
            'expiration' : 60
        }
        headers = {}
        res = requests.post(url, data=payload, headers=headers)
        data = res.json() 
        print(data)
        return data['data']['url_viewer']


    def wrapper(self):
        return self.generateCard().saveImage().uploadImgbb()

    



# AccessCard("first last", "12345", "platinum level", "1999-01-01").generateCard().showImage()
