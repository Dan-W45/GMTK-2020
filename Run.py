import pygame
import random
import math

Display=pygame.display.set_mode([1280,720])

pygame.font.init()

Font=pygame.font.Font(None,32)

Clock=pygame.time.Clock()

def LoadImage(FileLocation,Res,Trans=False):
    NormalImage=pygame.image.load(FileLocation)
    if Trans==False:
        NormalImage=pygame.image.load(FileLocation).convert()
    ScaleImage=pygame.transform.scale(NormalImage,Res)
    return ScaleImage

class Text:
    def __init__(self,Text):
        self.TextStr=Text
        self.Generate()
    def Generate(self):
        self.TextImage=Font.render(self.TextStr,False,(255,255,255),None)
    def Draw(self,X,Y):
        Display.blit(self.TextImage,[X,Y])

class Cell:
    def __init__(self,Name="CPUOffice"):
        self.TileMap=[]
        self.SizeX=50
        self.SizeY=50
        self.Name=Name
        self.Generate()
        self.Load()
    def Generate(self):
        self.TileMap=[]
        for x in range(0,self.SizeX):
            self.TileMap.append([])
            for y in range(0,self.SizeY):
                if x==1 or x==self.SizeX-2 or y==1 or y==self.SizeY-2:
                    self.TileMap[x].append([0,0])
                else:
                    self.TileMap[x].append([random.randint(0,2),random.randint(0,1)])
        self.Save()
    def Save(self):
        with open("Offices/"+str(self.Name)+".Map","w") as w:
            for x in self.TileMap:
                LineToWrite=""
                for y in x:
                    LineToWrite=LineToWrite+str(y[0])+"."+str(y[1])+","
                LineToWrite=LineToWrite+"\n"
                w.writelines(LineToWrite)
    def Load(self):
        self.TileMap=[]
        x=0
        with open("Offices/"+str(self.Name)+".Map","r") as r:
            for Line in r.readlines():
                self.TileMap.append([])
                Data=Line.split(",")
                for Tile in Data[0:-2]:
                    Tile=Tile.split(".")
                    self.TileMap[x].append([int(Tile[0]),int(Tile[1].strip("\n"))])
                x+=1
                
class Camera:
    def __init__(self):
        self.X=0
        self.Y=0
        self.ZoomX=12
        self.ZoomY=7
        self.DX=0
        self.DY=0
    def Collision(self):
        if self.X<0:
            self.X=0
        if self.Y<0:
            self.Y=0
        if self.X>CurrentOffice.SizeX-self.ZoomX:
            self.X=CurrentOffice.SizeX-self.ZoomX
        if self.Y>CurrentOffice.SizeY-self.ZoomY:
            self.Y=CurrentOffice.SizeY-self.ZoomY
    def Update(self):
        self.Collision()
        pass

CPUSide=LoadImage("Assets/CPU/WallSide.png",[128,128])
CPUBack=LoadImage("Assets/CPU/WallBack.png",[128,128])
CPUWindow=LoadImage("Assets/CPU/WallBackWindow.png",[128,128],Trans=True)

GPUSide=LoadImage("Assets/GPU/WallSide.png",[128,128])
GPUBack=LoadImage("Assets/GPU/WallBack.png",[128,128])
GPUWindow=LoadImage("Assets/GPU/WallBackWindow.png",[128,128],Trans=True)

RAMSide=LoadImage("Assets/RAM/WallSide.png",[128,128])
RAMBack=LoadImage("Assets/RAM/WallBack.png",[128,128])
RAMWindow=LoadImage("Assets/RAM/WallBackWindow.png",[128,128],Trans=True)

HDDSide=LoadImage("Assets/HDD/WallSide.png",[128,128])
HDDBack=LoadImage("Assets/HDD/WallBack.png",[128,128])
HDDWindow=LoadImage("Assets/HDD/WallBackWindow.png",[128,128],Trans=True)

PSUSide=LoadImage("Assets/PSU/WallSide.png",[128,128])
PSUBack=LoadImage("Assets/PSU/WallBack.png",[128,128])
PSUWindow=LoadImage("Assets/PSU/WallBackWindow.png",[128,128],Trans=True)

CCUSide=LoadImage("Assets/CCU/WallSide.png",[128,128])
CCUBack=LoadImage("Assets/CCU/WallBack.png",[128,128])
CCUWindow=LoadImage("Assets/CCU/WallBackWindow.png",[128,128],Trans=True)

Desk=LoadImage("Assets/CPU/Desk.png",[128,128],Trans=True)

PlayerOne=Camera()
FrameRateText=Text("Frames: ")

Tiles=[CPUSide,CPUBack,CPUWindow]
Entity=[None,Desk]
Selected=LoadImage("Assets/Selected.png",[128,128],Trans=True)

CurrentCell=Cell()
#CurrentCell.Generate()
Running=True
Editor=True

OfficeSelect=LoadImage("OfficeSelect.png",[1280,720])

CPUOffice=Cell(Name="CPUOffice")
GPUOffice=Cell(Name="GPUOffice")
RAMOffice=Cell(Name="RAMOffice")
HDDOffice=Cell(Name="HDDOffice")
PSUOffice=Cell(Name="PSUOffice")
CCUOffice=Cell(Name="CCUOffice")

CPUSelectText=Text("Central Processing Unit")
GPUSelectText=Text("Graphics Processing Unit")
RAMSelectText=Text("Random Access Memory")
HDDSelectText=Text("Hard Disk Drive")
PSUSelectText=Text("Power Supply Unit")
CCUSelectText=Text("Heat Sink")


def InCell():
    global DisplayState
    #DrawMap
    DrawX=DrawY=-128
    OffX=((math.floor(PlayerOne.X)-PlayerOne.X)*128)
    OffY=((math.floor(PlayerOne.Y)-PlayerOne.Y)*128)
    for x in range(math.floor(PlayerOne.X),math.ceil(PlayerOne.X+PlayerOne.ZoomX)):
        for y in range(math.floor(PlayerOne.Y),math.ceil(PlayerOne.Y+PlayerOne.ZoomY)):
            if CurrentOffice.SizeY-1>y:
                Display.blit(Tiles[CurrentOffice.TileMap[x][y][0]],[DrawX+OffX,DrawY+OffY])
                if CurrentOffice.TileMap[x][y][1]!=0:
                    Display.blit(Entity[CurrentOffice.TileMap[x][y][1]],[DrawX+OffX,DrawY+OffY])
            DrawY+=128
        DrawX+=128
        DrawY=-128
                
    #KeyBoard
    Keys=pygame.key.get_pressed()
    Sprint=1
    if Keys[pygame.K_LSHIFT]:
        Sprint=2
    if Keys[pygame.K_a]:
        PlayerOne.X-=(1/8)*Sprint

    if Keys[pygame.K_d]:
        PlayerOne.X+=(1/8)*Sprint

    if Keys[pygame.K_w]:
        PlayerOne.Y-=(1/8)*Sprint
        
    if Keys[pygame.K_s]:
        PlayerOne.Y+=(1/8)*Sprint

    if Keys[pygame.K_ESCAPE]:
        DisplayState="CellSelect"

    #Mouse
    MousePos=pygame.mouse.get_pos()
    MouseClick=pygame.mouse.get_pressed()
    Display.blit(Selected,[((MousePos[0]//128)*128)+OffX,((MousePos[1]//128)*128)+OffY])
    SelectedCoords=[PlayerOne.X+PlayerOne.ZoomX,PlayerOne.Y]

    #PlayerUpdate
    PlayerOne.Update()

def InSelect():
    global DisplayState,CurrentOffice,Tiles
    Display.blit(OfficeSelect,[0,0])
        
    CPUSelectText.Draw(50,50)
    GPUSelectText.Draw(350,50)
    RAMSelectText.Draw(650,50)
    HDDSelectText.Draw(200,400)
    PSUSelectText.Draw(500,400)
    CCUSelectText.Draw(800,400)

    MousePos=pygame.mouse.get_pos()
    MouseClick=pygame.mouse.get_pressed()

    if MouseClick[0]==True:
        if 50<MousePos[0]<350:
            if 50<MousePos[1]<400:
                CurrentOffice=CPUOffice
                Tiles=[CPUSide,CPUBack,CPUWindow]
                DisplayState="CellOffice"
                
        if 350<MousePos[0]<650:
            if 50<MousePos[1]<400:
                CurrentOffice=GPUOffice
                Tiles=[GPUSide,GPUBack,GPUWindow]
                DisplayState="CellOffice"
                
        if 650<MousePos[0]<950:
            if 50<MousePos[1]<400:
                CurrentOffice=RAMOffice
                Tiles=[RAMSide,RAMBack,RAMWindow]
                DisplayState="CellOffice"
                
        if 200<MousePos[0]<500:
            if 400<MousePos[1]<750:
                CurrentOffice=HDDOffice
                Tiles=[HDDSide,HDDBack,HDDWindow]
                DisplayState="CellOffice"
                
        if 500<MousePos[0]<800:
            if 400<MousePos[1]<750:
                CurrentOffice=PSUOffice
                Tiles=[PSUSide,PSUBack,PSUWindow]
                DisplayState="CellOffice"
                
        if 800<MousePos[0]<1100:
            if 400<MousePos[1]<750:
                CurrentOffice=CCUOffice
                Tiles=[CCUSide,CCUBack,CCUWindow]
                DisplayState="CellOffice"

DisplayState="CellSelect"

while Running==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    #ScreenFill
    Display.fill((155,155,155))

    if DisplayState=="CellOffice":
        InCell()
    elif DisplayState=="CellSelect":
        InSelect()

    #DrawText
    if str(round(Clock.get_fps()))!=FrameRateText.TextStr:
        FrameRateText.TextStr=str(round(Clock.get_fps()))
        FrameRateText.Generate()
    FrameRateText.Draw(0,0)

    #UpdatesDisplay
    Clock.tick(60)
    pygame.display.flip()
