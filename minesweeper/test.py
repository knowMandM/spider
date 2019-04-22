import numpy as np
import pygame
import sys
from pygame.locals import *
import traceback
import other
# import Game

pygame.init()
pygame.mixer.init()

# 参数
#   surface 被画的表面
#   pos 矩形中心点坐标
#   width 宽度
#   height 高度
#   color 线条颜色
#   degree 线条粗细
# 返回值
#   返回左上角和右下角坐标
def drawRect(surface, midpos, width, height, color = (0,0,0), degree = 0):
    upperLeft = (midpos[0] - (width//2), midpos[1] - (height//2))
    lowRight = (midpos[0] + (width//2), midpos[1] + (height//2))
    pygame.draw.rect(surface, color, (upperLeft, (width, height)), degree)    
    return (upperLeft, lowRight)

# 根据矩形坐标和宽高计算矩形范围
def calcRect(midpos, width, height):
    upperLeft = (midpos[0] - (width//2), midpos[1] - (height//2))
    lowRight = (midpos[0] + (width//2), midpos[1] + (height//2))
    return (upperLeft, lowRight)

# 判断一个点是否在矩形区域内
def isInRect(pos, rect):
    x, y = pos[0], pos[1]
    minX, maxX = rect[0][0], rect[1][0]
    minY, maxY = rect[0][1], rect[1][1]
    return minX < x < maxX and  minY < y < maxY

# 读取一张图片
def loadImg(imgPath, contentSize = None, alpha=True):
    imgMinus = None
    if alpha:
        imgMinus = pygame.image.load(imgPath).convert_alpha()
    else:
        imgMinus = pygame.image.load(imgPath)

    if contentSize:
        imgMinus = pygame.transform.smoothscale(imgMinus, contentSize)
    return imgMinus

# 难度选择器
class DifficultSelect():
    mapLevel2Descrition = {
        0 : "level1",
        1 : "level2",
        2 : "level3"
    }

    def __init__(self):
        self.screen = pygame.display.set_mode([600,400])
        self.imgMinus = loadImg("left.png", (80, 70))
        self.imgAdd = loadImg("right.png", (80, 70))
        self.imgMinusPress = loadImg("left_pressed.png", (80, 70))
        self.imgAddPress = loadImg("right_pressed.png", (80, 70))
        self.s_font=pygame.font.Font('msyhl.ttc',50)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("选择等级")

    # 选择界面
    def fresh_select(self, levelDesc, leftPressed = False, rightPressed = False, startPressed = False):
        # 背景色
        self.screen.fill((237,237,237))

        # 开始游戏按钮
        if startPressed:

            self.rectStartGame = drawRect(self.screen, midpos = (300, 300), width=200, height=80, color=(51, 153, 255), degree=0)
            self.rectStartGame = drawRect(self.screen, midpos = (300, 300), width=200, height=80, color=(0, 0, 0), degree=4)
        else:
            self.rectStartGame = drawRect(self.screen, midpos = (300, 300), width=200, height=80, color=(0, 0, 0), degree=4)
        self.screen.blit(self.s_font.render(str("start"),True,(0,0,0)),(250, 260))

        #rectLevel = drawRect(self.screen, midpos = (300, 100), width=200, height=80, degree=1)
        # 游戏难度
        self.screen.blit(self.s_font.render(str(levelDesc),True,(0,0,0)),(215, 60))

        # 减小难度按钮 
        self.rectMinus = calcRect((150, 100), 100, 80) #drawRect(self.screen, midpos = (150, 100), width=100, height=80, degree=1)
        minusImg = leftPressed and self.imgMinusPress or self.imgMinus
        self.screen.blit(minusImg,(110, 65))

        # 增加难度按钮
        self.rectAdd = calcRect((450, 100), 100, 80) #drawRect(self.screen, midpos = (450, 100), width=100, height=80, degree=1)
        addImg = rightPressed and self.imgAddPress or self.imgAdd
        self.screen.blit(addImg,(410, 60))

        pygame.display.flip()

    def run(self, zhanghao=None):
        decade=1
        self.fresh_select(self.mapLevel2Descrition[decade])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if isInRect(event.pos, self.rectAdd):
                            decade = (decade + 1) % 3
                            self.fresh_select(self.mapLevel2Descrition[decade])
                        if isInRect(event.pos, self.rectMinus):
                            decade = (decade - 1) % 3
                            self.fresh_select(self.mapLevel2Descrition[decade])
                        if isInRect(event.pos, self.rectStartGame):
                            exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if isInRect(event.pos, self.rectAdd):
                            self.fresh_select(self.mapLevel2Descrition[decade], rightPressed=True)
                        if isInRect(event.pos, self.rectMinus):
                            self.fresh_select(self.mapLevel2Descrition[decade], leftPressed=True)
                        if isInRect(event.pos, self.rectStartGame):
                            self.fresh_select(self.mapLevel2Descrition[decade], startPressed=True)

            #cap the framerate
            self.clock.tick(40)
            
    def runGame(self):
        pass # TODO
if __name__ == "__main__":
    DifficultSelect().run()