import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, random, math,os
    from pygame.locals import *


Display=pygame.display.set_mode([1280,720])
os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"

pygame.font.init()

Font=pygame.font.Font("Coder's Crux.ttf",32)

Clock=pygame.time.Clock()

TileScales=[32,64,128,256,512]
TileScale=TileScales[2]

Names=[]
with open("Names/Names.txt","r") as r:
    for line in r.readlines():
        line=line.strip("\n")
        Names.append(line)

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

class Person:
    def __init__(self,Name="Dave",Office=None):
        self.X=2
        self.Y=2
        self.CurrentOffice=Office
        self.Name=Name
        self.Happy=100
        self.Task="WorkAtDesk"
        self.PrevTask="WorkAtDesk"
        self.Image=LoadImage("Player.png",[TileScale,TileScale],Trans=True)
    def Move(self):
        if random.randint(0,7)==0:
            self.Happy-=(self.CurrentOffice.Production/self.CurrentOffice.NumOfDesks)
        '''
        if self.Happy<25:
            print(self.Name,"Im very mad gr")
        elif self.Happy<50:
            print(self.Name,"Im mad")
        elif self.Happy<75:
            print(self.Name,"Mood")'''
        if self.Happy>100:
            self.Happy=100
        if self.Task=="Wonder":
            DeltaMove=0
            if random.randint(0,20)==0:
                DeltaMove=random.randint(-1,1)
            if self.CurrentOffice.TileMap[self.X+DeltaMove][self.Y][0]!=0:
                self.X+=DeltaMove
            if random.randint(0,10)==0:
                for Elv in self.CurrentOffice.Elevators:
                    if Elv[0]==[self.X+1,self.Y+1]:
                        self.Y=Elv[1][1]-1
                    elif Elv[1]==[self.X+1,self.Y+1]:
                        self.Y=Elv[0][1]-1
            if random.randint(0,60)==0:#Done Wondering
                self.Happy+=15
                self.Task="WorkAtDesk"
                self.PrevTask="Wonder"
        elif self.Task=="WorkAtDesk":
            if random.randint(0,20)==0:
                DistL=0
                DistR=0
                try:
                    while self.CurrentOffice.TileMap[self.X-DistL+1][self.Y+1][1]!=1:
                        DistL+=1
                except IndexError:
                    DistL=999
                try:
                    while self.CurrentOffice.TileMap[self.X+DistR+1][self.Y+1][1]!=1:
                        DistR+=1
                except IndexError:
                    DistR=999
                if DistL==DistR==0:
                    NewTask=random.randint(0,10)
                    if NewTask==0:#Goes for a walk
                        #print(self.Name, "OOO Wonder time")
                        self.Task="Wonder"
                    elif NewTask==1:#Needs to drink some water
                        #print(self.Name, "I need dat H2O stuff")
                        self.Task="DontDydrate"
                    elif NewTask==2:#Needs To smell some plants
                       # print(self.Name, "Finding Plants")
                        self.Task="#PlantGang"
                    else:
                        #print(self.Name, "Working")
                        self.Happy-=1
                elif DistL<=DistR:
                    self.X-=1
                elif DistL>DistR:
                    self.X+=1
                if DistL==DistR==999:
                    self.PrevTask="WorkAtDesk"
                    self.Task="SeekElevator"
        elif self.Task=="SeekElevator":
            if random.randint(0,30)==0:
                DistL=0
                DistR=0
                try:
                    while self.CurrentOffice.TileMap[self.X-DistL+1][self.Y+1][0]!=3:
                        DistL+=1
                except IndexError:
                    DistL=999
                try:
                    while self.CurrentOffice.TileMap[self.X+DistR+1][self.Y+1][0]!=3:
                        DistR+=1
                except IndexError:
                    DistR=999
                if DistL<DistR:
                    self.X-=1
                elif DistL>DistR:
                    self.X+=1
                elif DistL==DistR==0:#Found Elevator
                    for Elv in self.CurrentOffice.Elevators:
                        if Elv[0]==[self.X+1,self.Y+1]:
                            self.Y=Elv[1][1]-1
                        elif Elv[1]==[self.X+1,self.Y+1]:
                            self.Y=Elv[0][1]-1
                    self.Task=self.PrevTask
                    self.PrevTask="SeekElevator"
                elif DistL==DistR==999:
                    self.Task=self.PrevTask
                    self.PrevTest="SeekElevator"
        elif self.Task=="DontDydrate":
            if random.randint(0,50)==0:
                DistL=0
                DistR=0
                try:
                    while self.CurrentOffice.TileMap[self.X-DistL+1][self.Y+1][1]!=2:
                        DistL+=1
                except IndexError:
                    DistL=999
                try:
                    while self.CurrentOffice.TileMap[self.X+DistR+1][self.Y+1][1]!=2:
                        DistR+=1
                except IndexError:
                    DistR=999
                if DistL<DistR:
                    self.X-=1
                elif DistL>DistR:
                    self.X+=1
                elif DistL==DistR==0:#Drunk some water
                    self.Happy+=15
                    if random.randint(0,3)==0:
                        self.Task="WorkAtDesk"
                        self.PrevTest="DontDydrate"
                elif DistL==DistR==999:
                    self.PrevTask=self.Task
                    self.Task="SeekElevator"
        elif self.Task=="#PlantGang":
            if random.randint(0,50)==0:
                DistL=0
                DistR=0
                try:
                    while self.CurrentOffice.TileMap[self.X-DistL+1][self.Y+1][1]!=3:
                        DistL+=1
                except IndexError:
                    DistL=999
                try:
                    while self.CurrentOffice.TileMap[self.X+DistR+1][self.Y+1][1]!=3:
                        DistR+=1
                except IndexError:
                    DistR=999
                if DistL<DistR:
                    self.X-=1
                elif DistL>DistR:
                    self.X+=1
                elif DistL==DistR==0:#Smelling the plants
                    self.Happy+=15
                    if random.randint(0,3)==0:
                        self.Task="WorkAtDesk"
                        self.PrevTest="#PlantGang"
                elif DistL==DistR==999:
                    self.PrevTask=self.Task
                    self.Task="SeekElevator"
    def Draw(self):
        Display.blit(self.Image,[(self.X-MainCamera.X)*TileScale,(self.Y-MainCamera.Y)*TileScale])

class Cell:
    def __init__(self,Name="CPUOffice"):
        self.TileMap=[]
        self.SizeX=50
        self.SizeY=50
        self.Level=1
        self.Name=Name
        self.People=[]
        self.NumOfDesks=0
        self.AverageHappy=100
        self.Power=100
        self.PowerReq=100
        self.Production=1
        self.Load("Offices/Tier"+str(self.Level)+"Office.Map")
    def Save(self):
        with open("Offices/"+str(self.Name)+".Map","w") as w:
            for x in self.TileMap:
                LineToWrite=""
                for y in x:
                    LineToWrite=LineToWrite+str(y[0])+"."+str(y[1])+","
                LineToWrite=LineToWrite+"\n"
                w.writelines(LineToWrite)
    def Load(self,Location=None):
        self.People=[]
        self.NumOfDesks=0
        if Location==None:
            Location="Offices/Tier"+str(self.Level)+"Office.Map"
        self.TileMap=[]
        x=0
        with open(Location,"r") as r:
            for Line in r.readlines():
                self.TileMap.append([])
                Data=Line.split(",")
                for Tile in Data:
                    if Tile!="\n":
                        Tile=Tile.split(".")
                        if int(Tile[1].strip("\n"))==1:
                            self.NumOfDesks+=1
                        self.TileMap[x].append([int(Tile[0]),int(Tile[1].strip("\n"))])
                x+=1
        for I in range(0,self.NumOfDesks):
            self.People.append(Person(Name=Names[random.randint(0,len(Names)-1)]+"|"+str(self.Name),Office=self))
        self.FindElevators()
    def FindElevators(self):
        self.Elevators=[]
        IndexX=0
        IndexY=0
        for y in self.TileMap:
            for x in y:
                if x[0]==3:
                    IncY=1
                    ElevatorOrigin=[IndexX,IndexY]
                    while self.TileMap[ElevatorOrigin[0]][ElevatorOrigin[1]+IncY][0]==4:
                        IncY+=1
                    if IncY!=1:
                        self.Elevators.append([ElevatorOrigin,[ElevatorOrigin[0],ElevatorOrigin[1]+IncY]])
                IndexY+=1
            IndexX+=1
            IndexY=0
    def Update(self):
        AvgHappy=0
        for Person in self.People:
            Person.Move()
            AvgHappy+=Person.Happy
        self.PowerReq=self.NumOfDesks*100
        self.AverageHappy=AvgHappy/len(self.People)
        #print(self.Name, self.AverageHappy)
        self.Production=(((self.Power/self.PowerReq)*100)/(self.AverageHappy*10))
            
class Camera:
    def __init__(self):
        self.X=0
        self.Y=0
        self.ZoomX=12*(128/TileScale)
        self.ZoomY=7*(128/TileScale)
        self.DX=0
        self.DY=0
        self.SelectedIndex=[0,0]
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

def LoadImages():
    global CPUSide,CPUSideBlank,CPUBack,CPUWindow,GPUSide,GPUSideBlank,GPUBack,GPUWindow
    global RAMSide,RAMSideBlank,RAMBack,RAMWindow,HDDSide,HDDSideBlank,HDDBack,HDDWindow
    global PSUSide,PSUSideBlank,PSUBack,PSUWindow,CCUSide,CCUSideBlank,CCUBack,CCUWindow
    global Desk,Selected,ElevatorEnter,ElevatorShaft,WaterCooler,Plant
    CPUSide=LoadImage("Assets/CPU/WallSide.png",[TileScale,TileScale])
    CPUSideBlank=LoadImage("Assets/CPU/WallSideBlank.png",[TileScale,TileScale])
    CPUBack=LoadImage("Assets/CPU/WallBack.png",[TileScale,TileScale])
    CPUWindow=LoadImage("Assets/CPU/WallBackWindow.png",[TileScale,TileScale],True)

    GPUSide=LoadImage("Assets/GPU/WallSide.png",[TileScale,TileScale])
    GPUSideBlank=LoadImage("Assets/GPU/WallSideBlank.png",[TileScale,TileScale])
    GPUBack=LoadImage("Assets/GPU/WallBack.png",[TileScale,TileScale])
    GPUWindow=LoadImage("Assets/GPU/WallBackWindow.png",[TileScale,TileScale],True)

    RAMSide=LoadImage("Assets/RAM/WallSide.png",[TileScale,TileScale])
    RAMSideBlank=LoadImage("Assets/RAM/WallSideBlank.png",[TileScale,TileScale])
    RAMBack=LoadImage("Assets/RAM/WallBack.png",[TileScale,TileScale])
    RAMWindow=LoadImage("Assets/RAM/WallBackWindow.png",[TileScale,TileScale],True)

    HDDSide=LoadImage("Assets/HDD/WallSide.png",[TileScale,TileScale])
    HDDSideBlank=LoadImage("Assets/HDD/WallSideBlank.png",[TileScale,TileScale])
    HDDBack=LoadImage("Assets/HDD/WallBack.png",[TileScale,TileScale])
    HDDWindow=LoadImage("Assets/HDD/WallBackWindow.png",[TileScale,TileScale],True)

    PSUSide=LoadImage("Assets/PSU/WallSide.png",[TileScale,TileScale])
    PSUSideBlank=LoadImage("Assets/PSU/WallSideBlank.png",[TileScale,TileScale])
    PSUBack=LoadImage("Assets/PSU/WallBack.png",[TileScale,TileScale])
    PSUWindow=LoadImage("Assets/PSU/WallBackWindow.png",[TileScale,TileScale],True)

    CCUSide=LoadImage("Assets/CCU/WallSide.png",[TileScale,TileScale])
    CCUSideBlank=LoadImage("Assets/CCU/WallSideBlank.png",[TileScale,TileScale])
    CCUBack=LoadImage("Assets/CCU/WallBack.png",[TileScale,TileScale])
    CCUWindow=LoadImage("Assets/CCU/WallBackWindow.png",[TileScale,TileScale],True)

    Desk=LoadImage("Assets/Desk.png",[TileScale,TileScale],True)
    WaterCooler=LoadImage("Assets/WaterCooler.png",[TileScale,TileScale],True)
    Plant=LoadImage("Assets/Plant.png",[TileScale,TileScale],True)

    Selected=LoadImage("Assets/Selected.png",[TileScale,TileScale],Trans=True)

    ElevatorEnter=LoadImage("Assets/ElevatorEnter.png",[TileScale,TileScale])
    ElevatorShaft=LoadImage("Assets/ElevatorShaft.png",[TileScale,TileScale])

LoadImages()

MainCamera=Camera()
FrameRateText=Text("Frames: ")

Tiles=[CPUSide,CPUBack,CPUWindow]
Entitys=[None,Desk,WaterCooler,Plant,Desk]

CurrentCell=Cell()
#CurrentCell.Generate()
Running=True
Editor=False
Debug=False

if Debug==True:
    Dave=Person(Name="Dave")
    Dave.X=1
    Dave.Y=5
    Dave.Task="DontDydrate"
    George=Person(Name="George")
    George.X=2
    George.Y=2
    George.Task="WorkAtDesk"
    Petty=Person(Name="Petty")
    Petty.X=1
    Petty.Y=5
    Petty.Task="#PlantGang"
    MadLad=Person(Name="Mr.Walsh")
    MadLad.X=5
    MadLad.Y=2

OfficeSelect=LoadImage("OfficeSelect.png",[1280,720])
CPUFan=LoadImage("Fan.png",[135,135],True)

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

Peoples=LoadImage("Player.png",[round(TileScale*0.5),round(TileScale*0.75)],Trans=True)

KeyDelay=0
BuyTile=False
BuyEntity=False

Money=0
MoneyText=Text(Text="Money: "+str(Money))

def InCell():
    global DisplayState,KeyDelay,BuyTile,BuyEntity,TileScale
    #DrawMap
    DrawX=DrawY=-TileScale
    OffX=((math.floor(MainCamera.X)-MainCamera.X)*TileScale)
    OffY=((math.floor(MainCamera.Y)-MainCamera.Y)*TileScale)
    for x in range(math.floor(MainCamera.X),math.ceil(MainCamera.X+MainCamera.ZoomX)+1):
        for y in range(math.floor(MainCamera.Y),math.ceil(MainCamera.Y+MainCamera.ZoomY)+1):
            if CurrentOffice.SizeY-1>y:
##                if CurrentOffice.TileMap[x][y][0] == 0:
##                    Display.blit(Tiles[random.choice([0,5,5,5,5,5,5,5])],[DrawX+OffX,DrawY+OffY])   ##Ooh funsies
##                else:
                Display.blit(Tiles[CurrentOffice.TileMap[x][y][0]],[DrawX+OffX,DrawY+OffY])
                if CurrentOffice.TileMap[x][y][1]!=0:
                    Display.blit(Entitys[CurrentOffice.TileMap[x][y][1]],[DrawX+OffX,DrawY+OffY])
            DrawY+=TileScale
        DrawX+=TileScale
        DrawY=-TileScale
                
    #KeyBoard
    Keys=pygame.key.get_pressed()
    Sprint=1
    if Keys[pygame.K_LSHIFT]:
        Sprint=2
    if Keys[pygame.K_a]:
        MainCamera.X-=(1/8)*Sprint

    if Keys[pygame.K_d]:
        MainCamera.X+=(1/8)*Sprint

    if Keys[pygame.K_w]:
        MainCamera.Y-=(1/8)*Sprint
        
    if Keys[pygame.K_s]:
        MainCamera.Y+=(1/8)*Sprint

    if Keys[pygame.K_F1]:
        print("Saving")
    if Keys[pygame.K_F2]:
        print("Loading")
        
    if KeyDelay<=0:
        if Keys[pygame.K_q]:
            KeyDelay=10
            BuyTile=not BuyTile
            BuyEntity=False
        if Keys[pygame.K_e]:
            KeyDelay=10
            BuyEntity=not BuyEntity
            BuyTile=False
        if Keys[pygame.K_F3]:
            TileScale*=2
            if TileScale>512:
                TileScale=32
            LoadImages()
            KeyDelay=10
        if Keys[pygame.K_u]:
            CurrentOffice.Level+=1
            if CurrentOffice.Level>=7:
                CurrentOffice.Level=6
            CurrentOffice.Load()
            KeyDelay=20
    else:
        KeyDelay-=1
        

    if Keys[pygame.K_ESCAPE]:
        DisplayState="CellSelect"

    #Mouse
    MousePos=pygame.mouse.get_pos()
    MouseClick=pygame.mouse.get_pressed()
    if Editor==True:
        #DrawSelectedArea
        if BuyTile==True:
            SelectedCoords=[MousePos[0]//TileScale,MousePos[1]//TileScale]
            if SelectedCoords[0]<1:
                MainCamera.SelectedIndex=[0,SelectedCoords[1]]
        elif BuyEntity==True:
            SelectedCoords=[MousePos[0]//TileScale,MousePos[1]//TileScale]
            if SelectedCoords[0]<1:
                MainCamera.SelectedIndex=[1,SelectedCoords[1]]
        else:
            Display.blit(Selected,[((MousePos[0]//TileScale)*TileScale)+OffX,((MousePos[1]//TileScale)*TileScale)+OffY])
            SelectedCoords=[MainCamera.X+MainCamera.ZoomX,MainCamera.Y]
            if MouseClick[0]==1:
                CurrentOffice.TileMap[(MousePos[0]//TileScale)+round(MainCamera.X)+1][(MousePos[1]//TileScale)+round(MainCamera.Y)+1][MainCamera.SelectedIndex[0]]=MainCamera.SelectedIndex[1]

        #ShowingSelectedTile
        if BuyTile==True:
            pygame.draw.rect(Display,(255,255,255),[[0,0],[TileScale*1.2,720]])
            y=8
            Index=0
            for Tile in Tiles:
                if MainCamera.SelectedIndex[0]==0 and MainCamera.SelectedIndex[1]==Index:
                    pygame.draw.rect(Display,(0,0,255),[[TileScale*0.1,y],[TileScale,TileScale]],16)
                Display.blit(Tile,[TileScale*0.1,y])
                y+=144
                Index+=1
        if BuyEntity==True:
            pygame.draw.rect(Display,(255,255,255),[[0,0],[TileScale*1.2,720]])
            y=8
            Index=0
            for Entity in Entitys:
                if Entity!=None:
                    if MainCamera.SelectedIndex[0]==1 and MainCamera.SelectedIndex[1]==Index:
                        pygame.draw.rect(Display,(0,0,255),[[TileScale*0.1,y],[TileScale,TileScale]],16)
                    Display.blit(Entity,[TileScale*0.1,y])
                y+=144
                Index+=1

    #peoples
    for Person in CurrentOffice.People:
        Person.Draw()
    
    #PlayerUpdate
    MainCamera.Update()

def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
##    pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)


angle=0
def InSelect():
    global DisplayState,CurrentOffice,Tiles, angle
    Display.blit(OfficeSelect,[0,0])


    angle+=21
    blitRotate(Display, CPUFan, [456,119], (67,67), angle)
    if angle >= 360:
        angle = 0

    
        
##    CPUSelectText.Draw(50,50)
##    GPUSelectText.Draw(350,50)
##    RAMSelectText.Draw(650,50)
##    HDDSelectText.Draw(200,400)
##    PSUSelectText.Draw(500,400)
##    CCUSelectText.Draw(800,400)

    MousePos=pygame.mouse.get_pos()
    MouseClick=pygame.mouse.get_pressed()

    if MouseClick[0]==True:
        if 435<MousePos[0]<474:#145,33,13,13
            if 99<MousePos[1]<138:
                CurrentOffice=CPUOffice
                Tiles=[CPUSide,CPUBack,CPUWindow,ElevatorEnter,ElevatorShaft,CPUSideBlank]
                DisplayState="CellOffice"

        elif 387<MousePos[0]<522:#129,17,45,45
            if 51<MousePos[1]<186:
                CurrentOffice=CCUOffice
                Tiles=[CCUSide,CCUBack,CCUWindow,ElevatorEnter,ElevatorShaft,CCUSideBlank]
                DisplayState="CellOffice"

        if 303<MousePos[0]<670:#101,111,125,18
            if 333<MousePos[1]<387:
                CurrentOffice=GPUOffice
                Tiles=[GPUSide,GPUBack,GPUWindow,ElevatorEnter,ElevatorShaft,GPUSideBlank]
                DisplayState="CellOffice"

                
        if 576<MousePos[0]<621:#192,7,15,66
            if 21<MousePos[1]<219:
                CurrentOffice=RAMOffice
                Tiles=[RAMSide,RAMBack,RAMWindow,ElevatorEnter,ElevatorShaft,RAMSideBlank]
                DisplayState="CellOffice"
                
        if 759<MousePos[0]<888:#253,162,43,58
            if 486<MousePos[1]<660:
                CurrentOffice=HDDOffice
                Tiles=[HDDSide,HDDBack,HDDWindow,ElevatorEnter,ElevatorShaft,HDDSideBlank]
                DisplayState="CellOffice"
                
        if 303<MousePos[0]<573:#101,180,90,60
            if 540<MousePos[1]<720:
                CurrentOffice=PSUOffice
                Tiles=[PSUSide,PSUBack,PSUWindow,ElevatorEnter,ElevatorShaft,PSUSideBlank]
                DisplayState="CellOffice"
                


def InMenu():
    pass

DisplayState="CellSelect"

while Running==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    #ScreenFill
    Display.fill((155,155,155))

    PowerOutput=PSUOffice.NumOfDesks*400

    CPUOffice.Update()
    GPUOffice.Update()
    RAMOffice.Update()
    HDDOffice.Update()
    PSUOffice.Update()
    CCUOffice.Update()

    if DisplayState=="CellOffice":
        InCell()
    elif DisplayState=="CellSelect":
        InSelect()

    Money+=(CPUOffice.Production+GPUOffice.Production+RAMOffice.Production+HDDOffice.Production)/4/10
    MoneyText.TextStr="Money's: "+str(round(Money))
    MoneyText.Generate()
    MoneyText.Draw(2,20)

    #DrawText
    if str(round(Clock.get_fps()))!=FrameRateText.TextStr:
        FrameRateText.TextStr="FPS: "+str(round(Clock.get_fps()))
        FrameRateText.Generate()
    FrameRateText.Draw(2,2)

    #UpdatesDisplay
    Clock.tick(60)
    pygame.display.flip()
