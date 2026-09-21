#!/usr/bin/env python3
"""Add a held WHIRLWIND touch button to the web overlay -- Warlord builds only.

Matt, on the live page: "The only problem is that there is no button for
whirlwind." The overlay shipped MOVE + CAST / JUMP / VFX and nothing for attack,
so on a phone there was no way to whirlwind at all.

WHY THIS IS A PATCH AND NOT AN EDIT UPSTREAM: the overlay lives in
~/Games/reincarnated-godot/web/_overlay/touch_controls.gd, which is read-only
this session. apply_overlay.py copies that file into <project>/scripts/ on every
run, so this patches the COPY inside the staged build, after the overlay's
second pass. Idempotent, and it fails loudly rather than half-applying.

STRUCTURAL GATE -- the reason this script reads project.godot at all:
the Keeper and Necromancer builds have no `attack` input action, no
whirlwind.gd and no attack branch in keeper.gd. Their degradation is an
ABSENCE, not a guard, and a dead button would read as a bug rather than as an
absence. So this refuses to add the button unless the project actually declares
an `attack` action. It cannot be aimed at the wrong build by mistake.

THE HOLD. The whirlwind is a HELD channel, not a tap -- keeper.gd drops to idle
the instant `Input.is_action_pressed("attack")` goes false (the spin costs you
your sprint, which is the D2/PoE trade and Matt's own design). The overlay's
existing button path is ALREADY press-and-hold -- `Input.action_press` on touch
down, `action_release` on touch up -- so the channel semantics come free and the
button is wired exactly like CAST. What does NOT come free is drag-off release,
which this patch adds: a finger that slides off the button releases the action
instead of leaving the player stuck spinning.

usage: whirlwind_button_patch.py <project_dir>
exit 0 applied or already applied · 0 with SKIP when there is no attack action
"""
import pathlib
import re
import sys

MARKER = 'PATCH(drax whirlwind_button)'

# Anchored from the bottom-right like the others; radius 95 in the 1920x1080
# design space. Clearances against the existing three, computed at that size --
# CAST (1730,870) r110 -> 256 apart, 51 clear; JUMP (1500,950) r80 -> 242 apart,
# 67 clear; VFX (1770,610) r62 -> 260 apart, 103 clear. Sits in the RIGHT half,
# so it can never swallow a touch meant for the left-half joystick.
BUTTON = ('\t{"action": "attack", "label": "WHIRLWIND", "anchor": Vector2(-390, -370),'
          ' "radius": 95.0, "font_size": 24},  # ' + MARKER + '\n')

BUTTONS_ANCHOR = '\t{"action": "vfx_cycle", "label": "VFX", "anchor": Vector2(-150, -470), "radius": 62.0},\n'

# "WHIRLWIND" is nine characters; the existing sizing rule would pick 36 for a
# radius over 90 and overflow the circle. Honour a per-button font_size.
DRAW_FROM = '\t\t_draw_label(center, button.label, 36 if button.radius > 90.0 else 28)'
DRAW_TO = ('\t\t# ' + MARKER + ': per-button font size; "WHIRLWIND" needs a\n'
           '\t\t# smaller face than the radius rule would choose.\n'
           '\t\t_draw_label(center, button.label,\n'
           '\t\t\t\tbutton.get("font_size", 36 if button.radius > 90.0 else 28))')

DRAG_FROM = """	elif event is InputEventScreenDrag:
		if event.index == _joy_index:
			_update_joystick(event.position)
			get_viewport().set_input_as_handled()
"""
DRAG_TO = """	elif event is InputEventScreenDrag:
		if event.index == _joy_index:
			_update_joystick(event.position)
			get_viewport().set_input_as_handled()
		elif _button_touch.has(event.index):
			# PATCH(drax whirlwind_button): a finger that slides OFF a button
			# releases it. Without this a dragged-off whirlwind stays pressed
			# until touch-up, and a dropped touch-up leaves the player spinning
			# with no way to stop. Matters far more for a HELD channel than for
			# the tap-ish CAST/JUMP/VFX, but applying it uniformly is simpler
			# and strictly safer.
			_drag_button(event.index, event.position)
			get_viewport().set_input_as_handled()
"""

DRAG_FUNC = '''

func _drag_button(index: int, pos: Vector2) -> void:
	## PATCH(drax whirlwind_button): release a held button once the finger
	## leaves it. The release margin (1.6r) is deliberately wider than the
	## press margin (1.15r) -- hysteresis, so a thumb that wobbles on the spot
	## does not stutter the channel on and off mid-spin.
	var action: String = _button_touch[index]
	for button in BUTTONS:
		if button.action == action:
			if pos.distance_to(_button_center(button)) > button.radius * 1.6:
				Input.action_release(action)
				_button_touch.erase(index)
				_overlay.queue_redraw()
			return
'''


def fail(msg: str) -> None:
    print('WHIRLWIND BUTTON PATCH FAIL: ' + msg, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    if len(sys.argv) != 2:
        fail('usage: whirlwind_button_patch.py <project_dir>')
    root = pathlib.Path(sys.argv[1]).resolve()
    project = root / 'project.godot'
    script = root / 'scripts' / 'touch_controls.gd'
    if not project.is_file():
        fail(f'not a Godot project: {root}')
    if not script.is_file():
        fail(f'no touch overlay at {script} -- run apply_overlay.py first')

    # The structural gate. No attack action -> no button, and say so.
    if not re.search(r'^attack=\{', project.read_text(), flags=re.M):
        print('  whirlwind button: SKIP -- this build declares no `attack` '
              'input action (Keeper/Necromancer); the button stays ABSENT, '
              'not present-and-inert')
        return

    text = script.read_text()
    if MARKER in text:
        print('  whirlwind button: already applied (idempotent no-op)')
        return

    if BUTTONS_ANCHOR not in text:
        fail('BUTTONS list does not look as expected -- the overlay moved; '
             're-derive the anchors before patching')
    text = text.replace(BUTTONS_ANCHOR, BUTTONS_ANCHOR + BUTTON, 1)

    if text.count(DRAW_FROM) != 1:
        fail('label-draw line not found exactly once')
    text = text.replace(DRAW_FROM, DRAW_TO, 1)

    if text.count(DRAG_FROM) != 1:
        fail('drag branch not found exactly once')
    text = text.replace(DRAG_FROM, DRAG_TO, 1)

    anchor = '\n\nfunc _update_joystick('
    if text.count(anchor) != 1:
        fail('_update_joystick anchor not found exactly once')
    # DRAG_FUNC already opens with a blank-line pair and closes with a newline,
    # so concatenating the anchor back on leaves the two blank lines GDScript
    # wants between top-level functions. (An earlier rjust() here produced a
    # LEADING SPACE on `func _update_joystick(`, which is a top-level
    # indentation error -- caught by compiling the patched script below.)
    text = text.replace(anchor, DRAG_FUNC + anchor, 1)

    script.write_text(text)

    # Post-conditions, checked rather than assumed.
    after = script.read_text()
    for needed in ('"action": "attack"', '"label": "WHIRLWIND"', 'func _drag_button(',
                   'button.get("font_size"'):
        if needed not in after:
            fail('post-condition missing after write: ' + needed)

    # Every top-level `func` must sit at column 0. GDScript indentation is
    # significant and a spliced-in function is exactly where a stray leading
    # space gets introduced -- the first version of this patch did precisely
    # that, and nothing else here would have noticed.
    for number, line in enumerate(after.splitlines(), 1):
        if line.lstrip().startswith('func ') and line != line.lstrip():
            fail(f'indented top-level func at line {number}: {line!r}')
    if '\t' in after and any(line.startswith('    ') and line.lstrip().startswith('_')
                             for line in after.splitlines()):
        fail('space indentation introduced into a tab-indented script')
    print('  whirlwind button: APPLIED (held channel, drag-off release, '
          'WHIRLWIND label at font 24, r95 bottom-right)')


if __name__ == '__main__':
    main()
