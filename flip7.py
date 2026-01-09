from presto import Presto
from picovector import ANTIALIAS_BEST, PicoVector
import sys
import time
from touch import Button

machine.freq(150_000_000)

print('Programm          : Flip7 - CardCounter\n')
print(f"Machine-Id        : {machine.unique_id()}")
print(f"Machine-Freq      : {machine.freq()/1000000} MHz")
print(f"sys.implementation: {sys.implementation}\n")

if "Presto" in sys.implementation._machine:
    print("OK, Presto found\n")
else:
    print("ERROR, Presto not found... Exiting")
    raise SystemExit

presto  = Presto(full_res = True, ambient_light = False)
display = presto.display
touch   = presto.touch
vector  = PicoVector(display)
vector.set_antialiasing(ANTIALIAS_BEST)

WIDTH, HEIGHT = display.get_bounds()

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

AQUA    = display.create_pen(0,255,255)
FUCHSIA = display.create_pen(255,0,255)
LIME    = display.create_pen(0,255,0)
OLIVE   = display.create_pen(128,128,0)
BLACK   = display.create_pen(0,0,0)
MAROON  = display.create_pen(128,0,0)
PURPLE  = display.create_pen(128,0,128)
TEAL    = display.create_pen(0,128,128)
NAVY    = display.create_pen(0,0,128)
WHITE   = display.create_pen(255,255,255)
YELLOW  = display.create_pen(255,255,0)

MEDIUMVIOLETRED = display.create_pen(199,21,133) #     0
SILVER          = display.create_pen(192,192,192) #    1
OLIVEDRAB       = display.create_pen(192,255,62) #     2
FIREBRICK       = display.create_pen(238,44,44) #      3
AQUA            = display.create_pen(0,255,255) #      4
GREEN           = display.create_pen(0,255,0) #        5
PURPLE          = display.create_pen(145,44,238) #     6
LIGHTPINK       = display.create_pen(238,162,173) #    7
LIGHTGREEN      = display.create_pen(144, 238, 144) #  8
ORANGE          = display.create_pen(255,165,0) #      9
RED             = display.create_pen(255,0,0) #       10
MEDIUMSLATEBLUE = display.create_pen(123,104,238) #   11
GRAY            = display.create_pen(128,128,128) #   12
BLUE            = display.create_pen(0,0,255) #       Aktion und Bonus

COLORS     = {}
COLORS[0]  = MEDIUMVIOLETRED
COLORS[1]  = SILVER
COLORS[2]  = OLIVEDRAB
COLORS[3]  = FIREBRICK
COLORS[4]  = AQUA
COLORS[5]  = GREEN
COLORS[6]  = PURPLE
COLORS[7]  = LIGHTPINK
COLORS[8]  = LIGHTGREEN
COLORS[9]  = ORANGE
COLORS[10] = RED
COLORS[11] = MEDIUMSLATEBLUE
COLORS[12] = GRAY


def init():
    global buttons
    global karten
    global karten_gesamt
    
    buttons       = {}
    karten        = {}
    karten_gesamt = 0
    x = 10
    y = 80
    for karte in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, "AKTION", "BONUS", "RESET"):
        if karte == "AKTION":
            karten[karte] = KARTE(wert = karte, vorhanden = 9, color = BLUE, x = x, y = y)
        elif karte == "BONUS":
            karten[karte] = KARTE(wert = karte, vorhanden = 6, color = BLUE, x = x, y = y)
        elif karte == "RESET":
            karten[karte] = KARTE(wert = karte, vorhanden = 0, color = RED, x = x, y = y)
        elif karte < 2:
            karten[karte] = KARTE(wert = karte, vorhanden = 1, color = COLORS[karte], x = x, y = y)
        else:
            karten[karte] = KARTE(wert = karte, vorhanden = karte, color = COLORS[karte], x = x, y = y)
        buttons[karte] = Button(x, y, 100, 60)
        x += 120
        if x > 370:
            x = 10
            y += 90
        karten_gesamt += karten[karte].vorhanden


def show_title(text, center = False, background = GRAY, foreground = WHITE, update = False):
    display.set_pen(background)
    display.rectangle(0,0,480,40)
    display.set_pen(foreground)
    vector.set_font("fonts/Roboto-Medium.af", 30)
    vector.set_font_letter_spacing(100)
    vector.set_font_word_spacing(100)
    if (center == True):
        _, _, text_width, text_height = vector.measure_text(text, x=0, y=0, angle=None)
        vector.text(text, int(WIDTH // 2 - text_width // 2), 30, angle=0, max_width=480, max_height=50)
    else:
        vector.text(text, 0, 30, angle=0, max_width=480, max_height=50)
    if update == True:
        presto.partial_update(0,0,480,40)


def show_footer(text, center = False, background = GRAY, foreground = WHITE, update = False):
    display.set_pen(background)
    display.rectangle(0,450,480,30)
    display.set_pen(foreground)
    vector.set_font("fonts/Roboto-Medium.af", 20)
    vector.set_font_letter_spacing(100)
    vector.set_font_word_spacing(100)
    if (center == True):
        _, _, text_width, text_height = vector.measure_text(text, x=0, y=0, angle=None)
        vector.text(text, int(WIDTH // 2 - text_width // 2), 470, angle=0, max_width=480, max_height=50)
    else:
        vector.text(text, 0, 470, angle=0, max_width=480, max_height=50)
    if update == True:
        presto.partial_update(0,450,480,30)


class KARTE:
    def __init__(self, wert = None, vorhanden = None, color = None, x = None, y = None):
        self.wert = wert
        self.vorhanden = vorhanden
        self.color = color
        self.x = x
        self.y = y
    
    def show(self, karten_gesamt = None, update = None):
        display.set_pen(self.color)
        display.rectangle(self.x, self.y, 100, 60)
        
        display.set_pen(BLACK)
        if False:
            vector.set_font("fonts/Roboto-Medium.af", 40)
            vector.set_font_letter_spacing(100)
            vector.set_font_word_spacing(100)
            text = str(self.wert)
            _, _, text_width, text_height = vector.measure_text(text, x=0, y=0, angle=None)
            vector.text(text, self.x + 50 - int(text_width // 2), self.y + 30, angle=0, max_width=120, max_height=50)
        else:
            display.set_font("bitmap8")
            text = f"[ {str(self.wert)} ]"
            text_width = display.measure_text(text, scale = 3)
            display.text(text, self.x + 50 - int(text_width // 2), self.y + 10, scale = 3)
        
        if self.wert == "RESET":
            pass
        else:
            if self.vorhanden == 0:
                text = "Keine Karte"
            elif self.vorhanden == 1:
                text = "1 Karte"
            else:
                text = str(self.vorhanden) + " Karten"
            if False:
                vector.set_font("fonts/Roboto-Medium.af", 15)
                vector.text(text, self.x + 3, self.y + 55, angle=0, max_width=120, max_height=50)
            else:
                display.text(text, self.x + 3, self.y + 50, scale = 1)
                
            
            if karten_gesamt is not None:
                if karten_gesamt == 0:
                    text = "0 %"
                else:
                    text = str(int(100 / karten_gesamt * self.vorhanden)) + " %"
                
                if False:
                    _, _, text_width, text_height = vector.measure_text(text, x=0, y=0, angle=None)
                    vector.text(text, self.x + 100 - 4 - int(text_width), self.y + 55, angle=0, max_width=120, max_height=50)
                else:
                    text_width = display.measure_text(text, scale = 2)
                    display.text(text, self.x + 100 - 4 - text_width, self.y + 43, scale = 2)
        
        if update == True:
            presto.update()


display.set_pen(BLACK)
display.clear()

show_title("Flip7 - Das beste Kartenspiel aller Zeiten", center = True, background = RED, foreground = WHITE)

init()
for _ in karten:
    karte = karten[_]
    karte.show(karten_gesamt)

show_footer(f"Im Stapel befinden sich noch {karten_gesamt} Karten...", center = True, background = RED, foreground = WHITE)

presto.update()


while True:
    
    touch.poll()
    
    update_benoetigt = False
    
    for _ in buttons:
        button = buttons[_]
        if button.is_pressed():
            while button.is_pressed():
                touch.poll()
                time.sleep(.01)
            karte = karten[_]
            if _ == "RESET":
                init()
                update_benoetigt = True
            else:
                if karte.vorhanden > 0:
                    karte.vorhanden -= 1
                    karten_gesamt -= 1
                    update_benoetigt = True
    
    if update_benoetigt == True:
        for _ in karten:
            karte = karten[_]
            karte.show(karten_gesamt = karten_gesamt)
        if karten_gesamt == 0:
            show_footer(f"Der Stapel ist aufgebraucht, bitte neu mischen...", center = True, background = RED, foreground = WHITE)
        elif karten_gesamt == 1:
            show_footer(f"Im Stapel befinden sich noch 1 Karte...", center = True, background = RED, foreground = WHITE)
        else:
            show_footer(f"Im Stapel befinden sich noch {karten_gesamt} Karten...", center = True, background = RED, foreground = WHITE)
        presto.update()

    time.sleep(.01)
