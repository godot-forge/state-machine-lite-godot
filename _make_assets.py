from PIL import Image, ImageDraw, ImageFont
import os, math

BASE   = os.path.dirname(os.path.abspath(__file__))
ORANGE = (230, 126, 34)
DARK   = (24, 26, 38)
PANEL  = (33, 36, 52)
WHITE  = (235, 238, 245)
MUTED  = (140, 148, 168)
GREEN  = (52, 211, 153)

try:
    bf = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)
    sf = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    cf = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
except:
    bf = sf = cf = ImageFont.load_default()

def draw_fsm(d, cx, cy, r=38, active="Idle"):
    states = {"Idle": (0,-r), "Walk": (r,0), "Run": (0,r), "Attack": (-r,0)}
    colors = {"Idle": GREEN if active=="Idle" else MUTED,
              "Walk": GREEN if active=="Walk" else MUTED,
              "Run":  GREEN if active=="Run"  else MUTED,
              "Attack": GREEN if active=="Attack" else MUTED}
    for name, (dx,dy) in states.items():
        x, y = cx+dx*1.6, cy+dy*1.6
        col = colors[name]
        d.ellipse([x-22,y-14,x+22,y+14], fill=PANEL, outline=col, width=2)
        d.text((x,y), name, font=sf, fill=col, anchor="mm")
    arrows = [("Idle","Walk"),("Walk","Run"),("Run","Attack"),("Attack","Idle")]
    for src, dst in arrows:
        sx,sy = cx+states[src][0]*1.6, cy+states[src][1]*1.6
        ex,ey = cx+states[dst][0]*1.6, cy+states[dst][1]*1.6
        mx,my = (sx+ex)//2,(sy+ey)//2
        d.line([(sx,sy),(ex,ey)], fill=(*ORANGE,120), width=1)

# icon 128x128
img = Image.new("RGB",(128,128),DARK)
d = ImageDraw.Draw(img)
d.rectangle([0,0,128,4], fill=ORANGE)
draw_fsm(d, 64, 64, r=32, active="Walk")
img.save(os.path.join(BASE,"icon.png"))

# cover 630x500
img = Image.new("RGB",(630,500),DARK)
d = ImageDraw.Draw(img)
d.rectangle([0,0,630,5], fill=ORANGE)
d.text((315,38), "State Machine PRO", font=bf, fill=WHITE, anchor="mm")
d.text((315,66), "for Godot 4", font=sf, fill=MUTED, anchor="mm")
draw_fsm(d, 315, 260, r=80, active="Walk")
d.text((315,460), "godot-forge.itch.io/state-machine-godot", font=sf, fill=MUTED, anchor="mm")
img.save(os.path.join(BASE,"cover.png"))

# preview 1280x720
img = Image.new("RGB",(1280,720),DARK)
d = ImageDraw.Draw(img)
d.rectangle([0,0,1280,6], fill=ORANGE)
d.text((640,50), "State Machine PRO — GodotForge", font=bf, fill=WHITE, anchor="mm")
draw_fsm(d, 320, 360, r=110, active="Attack")
d.rounded_rectangle([640,120,1240,600], radius=12, fill=PANEL)
lines = [
    ("# create FSM", MUTED), ('fsm = StateMachine.create(self, "Idle")', (130,220,160)),
    ("", WHITE),
    ('StateMachine.add_state(fsm, "Idle",', (130,220,160)),
    ('  enter, exit)', (130,220,160)),
    ("", WHITE),
    ('StateMachine.add_condition(fsm,', (130,220,160)),
    ('  "Walk", "Run", func(): return speed > 5)', (130,220,160)),
    ("", WHITE),
    ('StateMachine.transition(fsm, "Attack")', (130,220,160)),
    ('StateMachine.transition_back(fsm)', (130,220,160)),
]
y = 148
for text, col in lines:
    if text: d.text((660, y), text, font=cf, fill=col)
    y += 38
img.save(os.path.join(BASE,"preview.png"))
print("assets done")
