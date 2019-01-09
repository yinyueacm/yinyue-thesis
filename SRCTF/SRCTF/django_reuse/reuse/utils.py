from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime
import os
import math, string
import json
from .models import Category

project_path = os.getcwd()
project_path = project_path[0:project_path.rfind('/')]

def cats(context):
    return {'cats':Category.objects.all()}
    
def server_domain(context):
    s_domain = "127.0.0.1"
    try:
        s_domain = os.environ["S_DOMAIN"]
    except:
        s_domain = "127.0.0.1"
    
    return {'s_domain': s_domain}

class ImageChar():

    def __init__(self, size = (200,40), bgColor = (255,255,255), fontSize = 20):
        self.size = size
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.image = Image.new('RGB', size, bgColor)
    
    def rotate(self):
        self.image.rotate(random.randint(0,30), expand = 0)
    
    def drawText(self, pos, txt, font, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=font, fill=fill)
        del draw
    
    def randRGB(self):
        return (random.randint(0, 255),
               random.randint(0, 255),
               random.randint(0, 255))
               
    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))  

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB())
        del draw  
        
    def draw_word(self, txt):
        num = len(txt)
        gap = 5
        start = 0
        font = ImageFont.truetype(os.path.join("/home/ictf/.fonts/" , "Anonymice Powerline Bold.ttf" ), 20)
        for i in range(0, num):
            char = txt[i]
            x = start + self.fontSize * i + gap * i
            self.drawText((x, random.randint(-5, 5)), char, fill="#000000", font=font)
            self.rotate()
        self.randLine(18) 
        
    def save(self, path):
        self.image.save(path)
        

def getConf(filedir):
    with open(filedir, 'r') as f:
        config = json.load(f)
    '''for cmd in config['execs']:
        print cmd['cmd'] + "user_1_2" + cmd['extra']'''
        
    return config

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    random.seed(datetime.now())
    return ''.join(random.choice(chars) for _ in range(size))
    
def pswd_generator(size=6, chars=string.ascii_lowercase + string.digits):
    # select your own random seed
    random.seed(datetime.now())
    return ''.join(random.choice(chars) for _ in range(size))
    
    
#getConf("/home/ictf/cs@uga/ctfs/reuse_buffer_overflow/conf.json")
        
#ic = ImageChar()
#ic.draw_word('123456')
#ic.save('/tmp/ictext.png')
# a =pswd_generator()
# print str(a)