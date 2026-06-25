# State Machine Lite — Godot 4

Free lightweight finite state machine for Godot 4 via autoload. Clean per-node state handling with enter/update/exit callbacks. Lite supports up to 16 states.

## Features (Lite — Free)

- `create(owner_node, initial_state)` — make a state machine handle
- `add_state(handle, name, ...)` — register states with callbacks
- `start(handle)` / `transition(handle, to)` / `update(handle, delta)`
- `current_state(handle)` / `destroy(handle)`
- Signal: `state_changed(from, to)`
- Up to 16 states · zero dependencies · pure GDScript autoload

## Quick Start

```gdscript
# Add addons/state_machine_lite/state_machine.gd as autoload named "StateMachine"
var sm = StateMachine.create(self, "idle")
StateMachine.add_state(sm, "idle")
StateMachine.add_state(sm, "run")
StateMachine.start(sm)
StateMachine.transition(sm, "run")
```

## Upgrade to PRO

[State Machine PRO](https://godot-forge.itch.io/state-machine-for-godot-4) adds hierarchical states, transition guards, history and a visual debugger.

---
Made with ♥ by [GodotForge](https://itch.io/profile/godot-forge)
