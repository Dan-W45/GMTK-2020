import contextlib
with contextlib.redirect_stdout(None):
    import pygame, pygame.freetype, sys, fileinput, ctypes
    from pygame.locals import *
    from pygame.sprite import Sprite
    from pygame.sprite import RenderUpdates
screen_width, screen_height = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
'''
Function:
    Returns surface with text written onto it
Useage:
    createSurfaceWithText("Text", Resting font size, Text color, Background color)
Notes:
    Colors are rgb 255: (0-255, 0-255, 0-255)
    Background color can be None for transparency
    This can be swapped out for custom text/characters
'''
def createSurfaceWithText(text, size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", size, bold=True)
    surface, _ = font.render(text, text_rgb, bg_rgb)
    return surface.convert_alpha()
'''
Function:
    Returns a string from a text file
Useage:
    getVarFromFile("File path", "Variable")
Notes:
    File format cannot have spaces
'''
def getVarFromFile(filepath, variable=None):
    return_dict = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.split("=")
            return_dict[line[0]] = line[1]
    if variable is not None:
        return return_dict[variable].rstrip()
    else:
        return return_dict
'''
Function:
    Sets a string in a text file
Useage:
    setVarFromFile("File path", "Variable", "String value to change to")
Notes:
    File format cannot have spaces
'''
def setVarFromFile(filepath, variable, value):
    newvalue = variable+"="+value
    oldvalue = variable+"="+getVarFromFile(filepath, variable)
    with fileinput.input(filepath, inplace=True) as f:
        for line in f:
            new_line = line.replace(oldvalue, newvalue)
            print(new_line, end='')     #This prints to the file, remove it and I will kill you (A solid 20 minutes of "Why does this break without print statements?")

'''
Class:
    UI text based element that can be added to a surface
Usage:
    UITextElement(Title(T) or button(F)?, Text Center Position, "Text", Resting font size, Background Color, Font Color, Action)
Notes:
    Colors are rgb 255: (0-255, 0-255, 0-255)
    Title do not change size when hovered over
    Actions are not required for the UI element to render
'''
class UITextElement(Sprite):
    def __init__(self, title, center_pos, text, size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False
        self.action = action
        default_img = createSurfaceWithText(text, size, text_rgb, bg_rgb)
        if not title:
##            highlighted_img = createSurfaceWithText(text, size*1.2, text_rgb, bg_rgb)
            highlighted_img = createSurfaceWithText(text, size, (200,200,200), bg_rgb)
        else:
            highlighted_img = default_img
        self.images = [default_img, highlighted_img]
        self.rects = [default_img.get_rect(center=center_pos), highlighted_img.get_rect(center=center_pos)]
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_pos, mouse_up, selected):
        if self.rect.collidepoint(mouse_pos) or selected:
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


'''
Class:
    UI slider based element that can be added to a surface
Usage:
    Don't
    UISliderElement(central position (x,y), Label, Slider length, Numerical range, Background color, Foreground color)
Notes:
    It's gonna change
    It changed, and it's gonna change again
'''
class UISliderElement:
    def __init__(self, center_pos, text, scale, width, slider_range, bg_rgb, fg_rgb):
        self.range = slider_range
        self.pos = center_pos
        self.dimensions = width
        self.x = center_pos[0]-(width/2)
        self.bg_rgb = bg_rgb
        self.fg_rgb = fg_rgb
        self.font = pygame.font.SysFont("Courier", scale, bold=True)
        self.label = createSurfaceWithText(text, scale, fg_rgb, None)
        self.scale = scale

    def update(self, mouse_pos, mouse_down, selected):
        if mouse_down:
            mx, my = mouse_pos
            if mx+(self.scale/6)>int(self.pos[0]-(self.dimensions/2)) and mx-(self.scale/6)<int(self.pos[0]-(self.dimensions/2))+self.dimensions and my>self.pos[1]-(self.scale/3) and my<self.pos[1]+(self.scale/3):
                self.x=mx

        if self.x < self.pos[0]-(self.dimensions/2): self.x=self.pos[0]-(self.dimensions/2)
        elif self.x > (self.pos[0]-(self.dimensions/2))+self.dimensions: self.x=(self.pos[0]-(self.dimensions/2))+self.dimensions


    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_rgb, [int(self.pos[0]-(self.dimensions/2)),self.pos[1],self.dimensions,2], 0)     #Background
        pygame.draw.rect(surface, self.fg_rgb, [int(self.pos[0]-(self.dimensions/2)),self.pos[1],self.x-int(self.pos[0]-(self.dimensions/2)),2], 0)     #Progress
        pygame.draw.rect(surface, self.fg_rgb, [self.x-(self.scale/6),self.pos[1]-(self.scale/3),(self.scale/3),int(self.scale/1.36)], 0)      #Node

        text = self.font.render(str(int((self.x-int(self.pos[0]-(self.dimensions/2))+1)/(self.dimensions/100))), True, (255,255,255))
        num_loc = text.get_rect()
        ##surface.blit(text, [self.x-num_loc.center[0],self.pos[1]-32])
        surface.blit(self.label, [self.pos[0]-(self.dimensions/2),self.pos[1]-35])
        surface.blit(text, [self.pos[0]+(self.dimensions/2)+10,self.pos[1]-15])


'''
Class:
    Keeps track of the current menu the user is viewing
Usage:
    Yes? No?
Notes:
    Subject to change
'''
class MenuLevel:
    def __init__(self, level):
        self.level=[]
        self.level.append(level)
    def getLevel(self):
        return self.level[-1]
    def changeLevel(self, level):
        if level != "Back":
            self.level.append(level)
        elif level == "Back":
            self.level.pop()
    def backLevel(self):
        self.level.pop()

def main():
    menu = MenuLevel("Main")
    pygame.init()
##    pygame.mouse.set_cursor((16, 19), (0, 0), (128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129, 240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))
##    pygame.mouse.set_cursor(*pygame.cursors.arrow)
##    print(pygame.display.Info().current_w, pygame.display.Info().current_h)
    width = int(getVarFromFile("defaults.config", "width"))
    height = int(getVarFromFile("defaults.config", "height"))
    screen = pygame.display.set_mode([width,height], RESIZABLE)
    pygame.display.set_caption("Game")
    while True:
        level = menu.getLevel()
        if level == "Main":
            titleScreen(screen, menu)
        if level == "Singleplayer":
            singleplayerScreen(screen, menu)
        if level == "Multiplayer":
            multiplayerScreen(screen, menu)
        if level == "Options":
            optionsScreen(screen, menu)
        if level == "Language":
            languageScreen(screen, menu)
        if level == "Video":
            videoScreen(screen, menu)
        if level == "Audio":
            audioScreen(screen, menu)
        if level == "Controls":
            controlsScreen(screen, menu)
        if level == "Pause":
            pauseScreen(screen, menu)
        if level == "Quit":
            pygame.quit()
            sys.exit()
            return

def titleScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Game", int(50*(screen.get_height()/720)), None, (255,255,255))
    singleplayer_button = UITextElement(False, [screen.get_width()/2, int(360*(screen.get_height()/720))], "Singleplayer", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Singleplayer")
    multiplayer_button = UITextElement(False, [screen.get_width()/2, int(410*(screen.get_height()/720))], "Multiplayer", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Multiplayer")
    options_button = UITextElement(False, [screen.get_width()/2, int(460*(screen.get_height()/720))], "Options", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Options")
    quit_button = UITextElement(False, [screen.get_width()/2, int(510*(screen.get_height()/720))], "Quit", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Quit")

    buttons = RenderUpdates(title, singleplayer_button, multiplayer_button, options_button, quit_button)
    ##buttons.add(new_button)
    return menuLoop(screen, menu, buttons)

def singleplayerScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Singleplayer", int(50*(screen.get_height()/720)), None, (255,255,255))
    load_last = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], ("Continue"), int(30*(screen.get_height()/720)), None, (255,255,255))
    load_button = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], ("Load"), int(30*(screen.get_height()/720)), None, (255,255,255))
    new_button = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], ("New"), int(30*(screen.get_height()/720)), None, (255,255,255))
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, load_last, load_button, new_button, back_button)
    return menuLoop(screen, menu, buttons)

def multiplayerScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Multiplayer", int(50*(screen.get_height()/720)), None, (255,255,255))
    host_new = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], ("Host new"), int(30*(screen.get_height()/720)), None, (255,255,255))
    host_saved = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], ("Host saved"), int(30*(screen.get_height()/720)), None, (255,255,255))
    browse_public = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], ("Browse public servers"), int(30*(screen.get_height()/720)), None, (255,255,255))
    browse_lan = UITextElement(False, [screen.get_width()/2, int(310*(screen.get_height()/720))], ("Browse LAN servers"), int(30*(screen.get_height()/720)), None, (255,255,255))
    custom_connect = UITextElement(False, [screen.get_width()/2, int(360*(screen.get_height()/720))], "Connect to IP", int(30*(screen.get_height()/720)), None, (255,255,255))
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, host_new, host_saved, browse_public, browse_lan, custom_connect, back_button)
    return menuLoop(screen, menu, buttons)

def pauseScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Pause", int(50*(screen.get_height()/720)), None, (255,255,255))
    resume_button = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], ("Return"), int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")
    save_button = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], ("Save"), int(30*(screen.get_height()/720)), None, (255,255,255), "S.Save")
    options_button = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], ("Options"), int(30*(screen.get_height()/720)), None, (255,255,255), "M.Options")
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Exit to main menu", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Title")

    buttons = RenderUpdates(title, resume_button, save_button, options_button, back_button)
    return menuLoop(screen, menu, buttons)


def optionsScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Options", int(50*(screen.get_height()/720)), None, (255,255,255))
    language_button = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], "Language", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Language")
    video_button = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], "Video Settings", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Video")
    audio_button = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], "Audio", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Audio")
    controls_button = UITextElement(False, [screen.get_width()/2, int(310*(screen.get_height()/720))], "Controls", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Controls")
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, language_button, video_button, audio_button, controls_button, back_button)
    return menuLoop(screen, menu, buttons)

def languageScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Langauge", int(50*(screen.get_height()/720)), None, (255,255,255))
    english = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], "English", int(30*(screen.get_height()/720)), None, (255,255,255))
    murica = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], "American", int(30*(screen.get_height()/720)), None, (255,255,255))
    aussie = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], "Australian", int(30*(screen.get_height()/720)), None, (255,255,255))
    sorry = UITextElement(False, [screen.get_width()/2, int(310*(screen.get_height()/720))], "Canadian", int(30*(screen.get_height()/720)), None, (255,255,255))
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, english, murica, aussie, sorry, back_button)
    return menuLoop(screen, menu, buttons)

def videoScreen(screen, menu):
    fullscreen = getVarFromFile("defaults.config", "fullscreen")
    fps = getVarFromFile("defaults.config", "show-fps")
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Video Settings", int(50*(screen.get_height()/720)), None, (255,255,255))
    fullscreen_button = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], ("Fullscreen: "+str(fullscreen)), int(30*(screen.get_height()/720)), None, (255,255,255), "S.ToggleFullscreen")
    framerate_button = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], ("Display Framerate: "+str(fps)), int(30*(screen.get_height()/720)), None, (255,255,255), "S.ToggleShowFPS")
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, fullscreen_button, framerate_button, back_button)
    return menuLoop(screen, menu, buttons)

def audioScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Audio Settings", int(50*(screen.get_height()/720)), None, (255,255,255))
    master_volume = UISliderElement([screen.get_width()/2, int(160*(screen.get_height()/720))], "Master", int(30*(screen.get_height()/720)), int(300*(screen.get_width()/1280)), (0,100), (200,200,200), (255,255,255))
    music_volume = UISliderElement([screen.get_width()/2, int(210*(screen.get_height()/720))], "Music", int(30*(screen.get_height()/720)), int(300*(screen.get_width()/1280)), (0,100), (200,200,200), (255,255,255))
    effects_volume = UISliderElement([screen.get_width()/2, int(260*(screen.get_height()/720))], "Effects", int(30*(screen.get_height()/720)), int(300*(screen.get_width()/1280)), (0,100), (200,200,200), (255,255,255))
    players_volume = UISliderElement([screen.get_width()/2, int(310*(screen.get_height()/720))], "Players", int(30*(screen.get_height()/720)), int(300*(screen.get_width()/1280)), (0,100), (200,200,200), (255,255,255))
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, back_button)
    sliders = [master_volume, music_volume, effects_volume, players_volume]
    return menuLoop(screen, menu, buttons, sliders)

def controlsScreen(screen, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Controls", int(50*(screen.get_height()/720)), None, (255,255,255))
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

    buttons = RenderUpdates(title, back_button)
    return menuLoop(screen, menu, buttons)

def ToggleFullscreen():
    data = getVarFromFile("defaults.config", "fullscreen")
    if data == "true":
        setVarFromFile("defaults.config", "fullscreen", "false")
        pygame.display.set_mode((int(getVarFromFile("defaults.config", "width")),int(getVarFromFile("defaults.config", "height"))), RESIZABLE)
    else:
        setVarFromFile("defaults.config", "fullscreen", "true")
        pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)

def ToggleShowFPS():
    data = getVarFromFile("defaults.config", "show-fps")
    if data == "true":
        setVarFromFile("defaults.config", "show-fps", "false")
    else:
        setVarFromFile("defaults.config", "show-fps", "true")

def menuLoop(screen, menu, buttons, sliders=None):
    selected = False
    mouse_down = False
    font1=pygame.font.SysFont("Courier", 20, bold=True)
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == 27:
                if menu.getLevel() != "Main":
                    menu.backLevel()
                    return

            if event.type == VIDEORESIZE:
                if getVarFromFile("defaults.config", "fullscreen") == "true":
                    pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
                elif event.h < 90:
                    screen = pygame.display.set_mode((event.w, 90), RESIZABLE)
                else:
                    screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                mouse_down = False

        screen.fill([106,159,181])

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up, selected)
            if action is not None:
                if action[:1] == "M":
                    menu.changeLevel(action[2:])
                    return
                if action[:1] == "S":
                    value = eval(action[2:])()
                    return

        buttons.draw(screen)

        if sliders is not None:
            for slider in sliders:
                action = slider.update(pygame.mouse.get_pos(), mouse_down, selected)
                slider.draw(screen)

        try:
            if getVarFromFile("defaults.config", "show-fps") == "true": #Not sure on performance impact, might change
                fps = font1.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Green'))
                screen.blit(fps, [0,0])
        except OverflowError:
            print("Much frames")
            screen.blit(fps, [0,0])

        pygame.display.flip()
        clock.tick()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    main()













