## StateMachine Lite — finite state machine for Godot 4
## Free version: up to 16 states, basic transitions, enter/exit callbacks.
## Upgrade to PRO for unlimited states, history, nested FSMs, debug overlay.
extends Node

signal state_changed(from: String, to: String)

const MAX_STATES := 16

var _states: Dictionary = {}
var _current: String = ""
var _owner_node: Node = null


func _ready() -> void:
	set_process(false)
	set_physics_process(false)


## Create an FSM bound to `owner_node`. Returns a handle Dictionary.
func create(owner_node: Node, initial_state: String = "") -> Dictionary:
	var id := str(owner_node.get_instance_id())
	_states[id] = {
		"owner": owner_node,
		"states": {},
		"current": "",
		"initial": initial_state,
	}
	return {"_id": id}


## Add a state. Callbacks are Callables: enter(), exit(), update(delta).
func add_state(handle: Dictionary, name: String,
		enter: Callable = Callable(),
		exit: Callable = Callable(),
		update: Callable = Callable()) -> void:
	var id: String = handle["_id"]
	if not _states.has(id):
		push_error("StateMachine: invalid handle")
		return
	var fsm: Dictionary = _states[id]
	if fsm["states"].size() >= MAX_STATES:
		push_warning("StateMachine Lite: max %d states reached. Upgrade to PRO for unlimited states." % MAX_STATES)
		return
	fsm["states"][name] = {"enter": enter, "exit": exit, "update": update}
	if fsm["initial"] == "" or fsm["initial"] == name and fsm["current"] == "":
		fsm["initial"] = name


## Start the FSM (enters initial state).
func start(handle: Dictionary) -> void:
	var id: String = handle["_id"]
	var fsm: Dictionary = _states[id]
	if fsm["states"].is_empty():
		push_error("StateMachine: no states added")
		return
	var init: String = fsm["initial"] if fsm["states"].has(fsm["initial"]) else fsm["states"].keys()[0]
	_enter_state(id, init)


## Transition to a new state.
func transition(handle: Dictionary, to: String) -> void:
	var id: String = handle["_id"]
	if not _states.has(id):
		return
	var fsm: Dictionary = _states[id]
	if not fsm["states"].has(to):
		push_error("StateMachine: unknown state '%s'" % to)
		return
	var from: String = fsm["current"]
	if from == to:
		return
	_exit_state(id, from)
	_enter_state(id, to)
	state_changed.emit(from, to)


## Call this from _process or _physics_process.
func update(handle: Dictionary, delta: float) -> void:
	var id: String = handle["_id"]
	if not _states.has(id):
		return
	var fsm: Dictionary = _states[id]
	var cur: String = fsm["current"]
	if cur == "" or not fsm["states"].has(cur):
		return
	var cb: Callable = fsm["states"][cur]["update"]
	if cb.is_valid():
		cb.call(delta)


## Returns current state name.
func current_state(handle: Dictionary) -> String:
	var id: String = handle["_id"]
	return _states[id]["current"] if _states.has(id) else ""


## Remove FSM (call on owner free).
func destroy(handle: Dictionary) -> void:
	var id: String = handle["_id"]
	_states.erase(id)


func _enter_state(id: String, name: String) -> void:
	_states[id]["current"] = name
	var cb: Callable = _states[id]["states"][name]["enter"]
	if cb.is_valid():
		cb.call()


func _exit_state(id: String, name: String) -> void:
	if name == "":
		return
	var cb: Callable = _states[id]["states"][name]["exit"]
	if cb.is_valid():
		cb.call()
