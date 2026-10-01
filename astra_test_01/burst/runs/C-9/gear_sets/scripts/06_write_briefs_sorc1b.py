# R-C9-98 stage 1b, the sorceress (Matt's look at GS-SBM: the bowl helm fits badly and varies across views).
# Conductor's design: from the high play camera a bowl reads as a grey dome and hides the braid, so
#   GS-SCROWN (2 calls, two draws of the RECOMMENDED design): the EMBER CROWN-HELM (brow band + cheek guards + two flame wings, no bowl)
#   GS-SHOOD  (1 call, the alternative): a scarlet HOOD over a mail coif with a steel diadem and ember gem
# Both are EDITs of GS-SBM_b (registered best: feet 0 px every view, face 0 px in 3 of 4) that change ONLY the head, and also
# fix b's sash knot (one hip in all views) and the greave-over-boot shape. 1 call of the 4 is held for a retry.
# PROMPT RULE: no game or franchise name; the register is described (refs_guard FORBID).
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
REGISTER = ("a painted storybook illustration with watercolour washes and confident ink linework, an illuminated-manuscript tactics "
            "role-playing register")
GRID = ("(1024x1536 portrait, 2x2 grid: top-left FRONT, top-right her RIGHT side facing the viewer's right, bottom-left BACK, "
        "bottom-right her LEFT side facing the viewer's left)")


def head(tid, title, design, faults, n):
    calls = ("Two image_gen EDIT calls: variants a and b." if n == 2 else "ONE image_gen EDIT call.")
    outs = (f"Copy outputs to out/{tid}_a.png and out/{tid}_b.png with sha256." if n == 2 else f"Copy the output to out/{tid}.png with its sha256.")
    return (
        f"GENERATE BURST {tid} -- Run C-9 Phase 2, new armour sets (Matt R-C9-98, his second look): the fire sorceress's battle-mage set "
        f"with a NEW HEADPIECE: {title}. task_id \"{tid}\".\n\n"
        f"IMAGE 1 is her steel battle-mage set, four views {GRID}: open-faced bowl helm, steel breastplate with ember-red etched runes, "
        "spaulders, mail sleeves and skirt over a quilted charcoal arming gown, plate gauntlets and vambraces, cuisses, knee cops and greaves "
        "over dark leggings, an ember-red tabard with a gold-rune border, an ember-red sash, tall brown boots. IMAGE 2 is her approved base "
        "body (the same woman unarmoured): her face, her long dark hair with the LEFT side of her head shaved, and her ONE thick braid down "
        "her back -- the hair to restore wherever the old helm hid it. IMAGE 3 is a STYLE reference ONLY.\n"
        "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose, scale, "
        "ground lines and positions; her face, her boots and soles on EXACTLY the same pixels as IMAGE 1. A 3D model will be built from "
        "these views, so the headpiece must be IDENTICAL in all four views -- the same shape, the same size, sitting at the same height on "
        "her head -- seen from four sides.\n"
        "CHANGE ONLY THE HEAD: REMOVE the bowl helm entirely and give her this headpiece instead:\n"
        f"{design}\n"
        "TWO SMALL FIXES elsewhere, nothing more: the ember-red SASH knot sits on her LEFT hip in EVERY view (seen at the viewer's right in "
        "the front view, at the viewer's left in the back view, toward the viewer in the left-side view, hidden behind her in the right-side "
        "view); and the GREAVES end the same way over the boots in every view -- the steel greave covering the shin down to the instep, the "
        "brown boot shaft showing behind and below it.\n"
        "EVERYTHING ELSE stays exactly as IMAGE 1 paints it: the breastplate and its runes, spaulders, mail, gown, gauntlets, vambraces, "
        "cuisses, knee cops, greaves, leggings, tabard, boots.\n"
        f"Paint as {REGISTER}: IMAGE 3's warm ink line that varies in weight, transparent washes that pool and bloom, fine hatching, cream "
        "paper highlights; the steel painted with soft wash and ink, not chrome. Soft even light, no glow, no cast shadows, no ground, no "
        "text, no labels.\n"
        "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
        f"{calls} NO RETRIES (the image budget is fixed): if a result has a fault, deliver it anyway and NAME it in concerns -- the "
        f"headpiece differing between views in shape, size or height, {faults}, her face covered, her braid missing, her pose, position or "
        f"scale changed, the sash on different hips, or any other piece changed. {outs} No code. No other files. No web.\n"
        f"RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE "
        "number of image_gen calls; status; concerns. Never PASS/FAIL.")


CROWN = ("THE EMBER CROWN-HELM, an OPEN steel half-helm with NO skull bowl: a steel BROW BAND that circles her head just above the brows "
         "and over the ears, with two small hinged steel CHEEK GUARDS hanging from it beside her cheekbones (her whole face open); from "
         "each TEMPLE a swept-back steel FLAME WING rises -- a stylised tongue of flame about a hand tall, curving up and back past the "
         "crown of her head, with ember-red enamel in its hollows; at the centre of the brow a faceted EMBER GEM, orange-red, set in a "
         "small steel claw mount. The top of her head is NOT covered: her dark hair, the shaved LEFT side and her braid all show, the "
         "braid falling down her back from under the band at the back. Simple, bold shapes: one band, two wings, one gem.")
HOOD = ("A SCARLET HOOD over a fine MAIL COIF: a hood of ember-red wool in IMAGE 1's tabard red, with a narrow gold-rune border at its "
        "face opening, worn UP over her head; beneath it a fine steel mail coif framing her face; across her brow, over the coif and "
        "under the hood's edge, a slim steel DIADEM holding a faceted orange-red EMBER GEM at its centre. The hood falls to a SHORT "
        "SHOULDER CAPE over the top of the breastplate and spaulders. Her whole face stays open (eyes, nose, mouth, chin); at the back her "
        "dark braid falls OUT of the hood down her back.")

T = {
    'GS-SCROWN': (head('GS-SCROWN', 'the EMBER CROWN-HELM', CROWN,
                       'a bowl or cap covering the top of her head, the two flame wings unequal or at different heights between views', 2), 2),
    'GS-SHOOD': (head('GS-SHOOD', 'a SCARLET HOOD with a mail coif and an ember diadem', HOOD,
                      'the hood down or missing, the braid hidden inside the hood, the cape longer than the top of the breastplate', 1), 1),
}
for tid, (text, n) in T.items():
    task = dict(text=text, references=[
        dict(path=A + 'GS-SBM/GS-SBM_b.png', role="IMAGE 1 -- her battle-mage set to EDIT (GS-SBM variant b, R-C9-98; registered best): change only the head, fix the sash and greaves"),
        dict(path=A + 'CS9-guides/SO-1_b_harvest.png', role="IMAGE 2 -- her approved base body (SO-1 variant b, the D7 base): her face, hair, shaved side and braid"),
        dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
        image_cap=n, minutes_cap=15, tool_call_cap=12,
        outputs=[f'out/{tid}_a.png', f'out/{tid}_b.png'] if n == 2 else [f'out/{tid}.png'],
        effort='high', add_dirs=[], experiment='R-C9-98-gear-sets')
    p = BURST / 'briefs/C-9' / f'{tid}.task.json'
    assert not p.exists(), f'{p} exists; never overwrite'
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n')
    print('wrote', p)
