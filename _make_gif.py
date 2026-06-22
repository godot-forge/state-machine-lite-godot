from PIL import Image, ImageDraw, ImageFont
import os

BASE   = os.path.dirname(os.path.abspath(__file__))
ORANGE = (230, 126, 34)
DARK   = (24, 26, 38)
PANEL  = (33, 36, 52)
WHITE  = (235, 238, 245)
MUTED  = (140, 148, 168)
CODE   = (130, 220, 160)
GREEN  = (52, 211, 153)
W, H   = 640, 400

try:
    title_f = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
    code_f  = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
    badge_f = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    small_f = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    node_f  = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
except:
    title_f = code_f = badge_f = small_f = node_f = ImageFont.load_default()

STEPS = [
    {"badge": "🔧 Create FSM in one line", "lines": [
        ("# bind FSM to any node:", MUTED),
        ('fsm = StateMachine.create(self, "Idle")', CODE),
        ("", WHITE),
        ("# add states with callbacks:", MUTED),
        ('StateMachine.add_state(fsm, "Idle", on_enter, on_exit)', CODE),
    ], "active": "Idle"},
    {"badge": "⚡ Auto-transitions via conditions", "lines": [
        ("# condition fires automatically on update:", MUTED),
        ('StateMachine.add_condition(fsm,', CODE),
        ('  "Walk", "Run", func(): return speed > 5.0)', CODE),
        ("", WHITE),
        ('StateMachine.update(fsm, delta)  # in _process', CODE),
    ], "active": "Walk"},
    {"badge": "↩ History & transition_back", "lines": [
        ("# go back to previous state:", MUTED),
        ('StateMachine.transition(fsm, "Attack")', CODE),
        ('StateMachine.transition_back(fsm)  # → Walk', CODE),
        ("", WHITE),
        ('var hist = StateMachine.history(fsm)', CODE),
    ], "active": "Attack"},
    {"badge": "📡 Signals & debug overlay", "lines": [
        ("# react to any state change:", MUTED),
        ('StateMachine.state_changed.connect(', CODE),
        ('  func(from, to): print(from, " → ", to))', CODE),
        ("", WHITE),
        ('StateMachine.set_debug(true)  # console log', CODE),
    ], "active": "Run"},
]

def draw_fsm_diagram(d, cx, cy, active_state):
    import math
    states = ["Idle", "Walk", "Run", "Attack"]
    for i, name in enumerate(states):
        angle = math.radians(i * 90 - 90)
        x = int(cx + 68 * math.cos(angle))
        y = int(cy + 48 * math.sin(angle))
        is_active = name == active_state
        fill = (*GREEN, 40) if is_active else PANEL
        outline = GREEN if is_active else MUTED
        lw = 2 if is_active else 1
        d.rounded_rectangle([x-30, y-13, x+30, y+13], radius=7,
                             fill=fill, outline=outline, width=lw)
        d.text((x, y), name, font=node_f,
               fill=GREEN if is_active else MUTED, anchor="mm")
    for i in range(4):
        a1 = math.radians(i * 90 - 90)
        a2 = math.radians(((i+1) % 4) * 90 - 90)
        x1 = int(cx + 50 * math.cos(a1))
        y1 = int(cy + 36 * math.sin(a1))
        x2 = int(cx + 50 * math.cos(a2))
        y2 = int(cy + 36 * math.sin(a2))
        d.line([(x1,y1),(x2,y2)], fill=(*ORANGE,80), width=1)

def make_frame(step):
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0,0,W,4], fill=ORANGE)
    d.text((20,16), "State Machine PRO", font=title_f, fill=WHITE)
    d.text((20,50), "for Godot 4", font=small_f, fill=MUTED)
    badge_txt = step["badge"]
    bw = int(d.textlength(badge_txt, font=badge_f)) + 24
    d.rounded_rectangle([20,78,20+bw,106], radius=13, fill=(44,48,68))
    d.rectangle([20,78,34,106], fill=ORANGE)
    d.rounded_rectangle([20,78,34,106], radius=13, fill=ORANGE)
    d.text((46,92), badge_txt, font=badge_f, fill=WHITE, anchor="lm")
    draw_fsm_diagram(d, W-110, 62, step.get("active","Idle"))
    d.rounded_rectangle([16,118,W-16,H-18], radius=10, fill=PANEL)
    y = 136
    for text, col in step["lines"]:
        if text: d.text((34,y), text, font=code_f, fill=col)
        y += 36
    d.text((20,H-14), "godot-forge.itch.io/state-machine-godot", font=small_f, fill=MUTED)
    return img

frames, durations = [], []
for step in STEPS:
    img = make_frame(step)
    for _ in range(14): frames.append(img); durations.append(120)
    for i in range(4):
        fade = Image.blend(img, Image.new("RGB",(W,H),DARK), (i+1)/5*0.5)
        frames.append(fade); durations.append(60)

out = os.path.join(BASE, "state_machine_demo.gif")
frames[0].save(out, save_all=True, append_images=frames[1:],
               loop=0, duration=durations, optimize=False)
print(f"wrote {out} ({len(frames)} frames)")
