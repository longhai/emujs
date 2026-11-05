#!/usr/bin/env python3
"""Tu dong them nut mod vao file goc EmulatorJS sau khi sync.
Vi du MOI, doc lap — khong lien quan code cu cua Hai.

Chay:
  python3 apply-emulatorjs-mods.py vendor/emulatorjs-data/src/frontend.js
  python3 apply-emulatorjs-mods.py vendor/emulatorjs-data/src/gamepad.js
Quy tac — CHI THEM NUT, KHONG VIET LAI BO NUT GOC:
  Nut goc cua EmulatorJS da co san het roi, script chi khai bao
  them nut thieu, chen vao sau khi bo nut goc da dung xong.
  1. PS1: bo nut goc (Y/X/B/A + D-pad + Start/Select) giu nguyen,
     chi them L1/R1/L2/R2 (input 10/11/12/13) bang info.push().
  2. NES: bo nut goc giu nguyen, chi them Turbo A / Turbo B
     (TA = input 8 giong A, TB = input 0 giong B, "autofire": true),
     va patch them cho xu ly cham nut de no that su tu dong ban
     lien tuc — vi mac dinh EmulatorJS chi autofire khi nguoi dung
     tick o cai dat Controls, neu chi them nut ma khong patch cho
     nay thi TA/TB chi la nut A/B thu hai.
  3. Tay cam that: tu nhan loai tay cam qua Gamepad API (gamepad.id)
     roi doi ky hieu nut cho dung loai do — Sony: ✕ ○ □ △,
     Xbox: A B X Y, Nintendo Switch: B A Y X (vi tri dao nhau),
     khac: ve chu Xbox. Cho nay sua trong gamepad.js, ham
     getButtonLabel() goc chi tra BUTTON_1/2/3/4 chung chung.
     Nhan dien dua vao chuoi id cua trinh duyet, khong phai luc
     nao cung chinh xac 100% (tay la, tay che do XInput, Safari
     chi bao "Standard Gamepad") — khi khong nhan ra thi ve
     ky hieu Xbox mac dinh, khong bao loi.
  4. Chay lai lan 2 khong them trung (idempotent). Neu ban goc doi
     ten ham / doi cau truc khien khong tim thay neo (anchor),
     script thoat loi (exit 2) — workflow DUNG lai, khong mo PR
     ghi de, Hai xem lai neo moi.
"""
import sys

# Chi them nut thieu, chen ngay sau khi bo nut goc dung xong,
# ngay truoc vong lap dich text cua nut. Nut goc giu nguyen 100%.
APPEND_BLOCK = '''        // HAI: chi them nut thieu, nut goc giu nguyen — xem apply-emulatorjs-mods.py
        if ("psx" === this.ejs.getControlScheme()) {
            info.push(
                { "type": "button", "text": "L1", "id": "l1", "location": "left", "left": 3, "top": -90, "bold": true, "block": true, "input_value": 10 },
                { "type": "button", "text": "R1", "id": "r1", "location": "right", "right": 3, "top": -90, "bold": true, "block": true, "input_value": 11 },
                { "type": "button", "text": "L2", "id": "l2", "location": "left", "left": 3, "top": -50, "bold": true, "block": true, "input_value": 12 },
                { "type": "button", "text": "R2", "id": "r2", "location": "right", "right": 3, "top": -50, "bold": true, "block": true, "input_value": 13 }
            );
        }
        if ("nes" === this.ejs.getControlScheme()) {
            info.push(
                { "type": "button", "text": "TA", "id": "ta", "location": "right", "right": 5, "top": 0, "bold": true, "input_value": 8, "autofire": true },
                { "type": "button", "text": "TB", "id": "tb", "location": "right", "right": 75, "top": 0, "bold": true, "input_value": 0, "autofire": true }
            );
        }
'''

# Neo: vong lap dich text, nam ngay sau khi bo nut goc dung xong.
LOCALIZE_ANCHOR = '''        for (let i = 0; i < info.length; i++) {
            if (info[i].text) {
                info[i].text = this.localization(info[i].text);
            }
        }'''

AUTOFIRE_OLD = "if (this.ejs.isAutofireEnabled(0, value) && !isAnalog) {"
AUTOFIRE_NEW = "if ((info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo"


def main(path):
    text = open(path, encoding="utf-8").read()
    changed = []

    if "    setVirtualGamepad() {" not in text:
        print("LOI: khong tim thay setVirtualGamepad() — ban goc doi ten ham roi", file=sys.stderr)
        return 2

    # --- 1+2. Chi them nut thieu (PS1 RL + NES Turbo), 1 cho duy nhat ---
    if "HAI: chi them nut thieu" in text:
        print("Nut them: da co roi, bo qua")
    else:
        if LOCALIZE_ANCHOR not in text:
            print("LOI: khong tim thay neo vong lap dich text — ban goc doi bo cuc roi", file=sys.stderr)
            return 2
        text = text.replace(LOCALIZE_ANCHOR, APPEND_BLOCK + LOCALIZE_ANCHOR, 1)
        changed.append("PS1: da them L1/R1/L2/R2; NES: da them Turbo A / Turbo B")

    # --- 3. Patch xu ly cham nut de TA/TB that su turbo ---
    if "info[i].autofire === true" in text:
        print("Turbo: xu ly cham nut da co autofire, bo qua")
    else:
        if AUTOFIRE_OLD not in text:
            print("LOI: khong tim thay dong isAutofireEnabled — ban goc doi xu ly nut roi", file=sys.stderr)
            return 2
        text = text.replace(AUTOFIRE_OLD, AUTOFIRE_NEW, 1)
        changed.append("Turbo: da patch xu ly cham nut (autofire:true)")

    if changed:
        open(path, "w", encoding="utf-8").write(text)
        print("DA DOI: " + "; ".join(changed))
    else:
        print("Khong co gi doi — mod da co san.")
    return 0


GAMEPAD_HELPER = '''
    // HAI: tu nhan loai tay cam that qua Gamepad API (gamepad.id).
    // W3C "standard mapping": nut 0 o duoi, 1 ben phai, 2 ben trai,
    // 3 o tren — chi khac nhau o KY HIEU in tren tay, vi tri giong nhau.
    // Sony: 0=✕ 1=○ 2=□ 3=△ | Xbox: 0=A 1=B 2=X 3=Y
    // Switch: 0=B 1=A 2=Y 3=X (dao vi tri so voi Xbox)
    detectGamepadType(id) {
        const s = String(id || "").toLowerCase();
        if (/sony|dualsense|dualshock|playstation|054c|wireless controller/.test(s)) return "sony";
        if (/nintendo|switch|pro controller|057e|joy-con/.test(s)) return "nintendo";
        if (/xbox|microsoft|xinput|045e|8bitdo.*x|gamesir.*x/.test(s)) return "xbox";
        if (/8bitdo/.test(s)) return "xbox"; // 8BitDo mac dinh che do XInput
        return "xbox"; // khong nhan ra: ve chu Xbox, khong bao loi
    }
    getGamepadSymbols(type) {
        const maps = {
            sony: { 0: "✕", 1: "○", 2: "□", 3: "△", 4: "L1", 5: "R1", 6: "L2", 7: "R2", 8: "Share", 9: "Options", 10: "L3", 11: "R3", 12: "↑", 13: "↓", 14: "←", 15: "→" },
            xbox: { 0: "A", 1: "B", 2: "X", 3: "Y", 4: "LB", 5: "RB", 6: "LT", 7: "RT", 8: "View", 9: "Menu", 10: "LS", 11: "RS", 12: "↑", 13: "↓", 14: "←", 15: "→" },
            nintendo: { 0: "B", 1: "A", 2: "Y", 3: "X", 4: "L", 5: "R", 6: "ZL", 7: "ZR", 8: "−", 9: "+", 10: "L Stick", 11: "R Stick", 12: "↑", 13: "↓", 14: "←", 15: "→" },
        };
        return maps[type] || maps.xbox;
    }
'''

GAMEPAD_LABEL_OLD = """    getButtonLabel(index) {
        if (index === null || index === undefined) {
            return null;
        }
        if (this.buttonLabels[index] === undefined) {
            return `GAMEPAD_${index}`;
        }
        return this.buttonLabels[index];
    }"""
GAMEPAD_LABEL_NEW = """    getButtonLabel(index, gamepadIndex) {
        if (index === null || index === undefined) {
            return null;
        }
        // HAI: doi ky hieu theo loai tay cam that dang cam
        try {
            const gp = (gamepadIndex !== undefined && gamepadIndex !== null)
                ? this.gamepads.find((g) => g && g.index === gamepadIndex)
                : (this.gamepads[0] || null);
            if (gp && gp.id) {
                const sym = this.getGamepadSymbols(this.detectGamepadType(gp.id))[index];
                if (sym) return sym;
            }
        } catch (e) { /* ve nhan mac dinh ben duoi */ }
        if (this.buttonLabels[index] === undefined) {
            return `GAMEPAD_${index}`;
        }
        return this.buttonLabels[index];
    }"""


def patch_gamepad(path):
    text = open(path, encoding="utf-8").read()
    if "detectGamepadType" in text:
        print("Tay cam: da co nhan loai tay cam, bo qua")
        return 0
    if GAMEPAD_LABEL_OLD not in text:
        print("LOI: khong tim thay getButtonLabel() goc — ban goc doi gamepad.js roi", file=sys.stderr)
        return 2
    # Chen helper truoc getButtonLabel, roi thay ham do
    text = text.replace(GAMEPAD_LABEL_OLD, GAMEPAD_HELPER + "\n" + GAMEPAD_LABEL_NEW, 1)
    # Truyen gamepadIndex vao 2 cho goi getButtonLabel() khi bam/nha nut
    text = text.replace(
        "this.dispatchEvent('buttondown', {index: buttonIndex, label: this.getButtonLabel(buttonIndex), gamepadIndex: gamepad.index});",
        "this.dispatchEvent('buttondown', {index: buttonIndex, label: this.getButtonLabel(buttonIndex, gamepad.index), gamepadIndex: gamepad.index});",
        1)
    text = text.replace(
        "this.dispatchEvent('buttonup', {index: buttonIndex, label:this.getButtonLabel(buttonIndex), gamepadIndex: gamepad.index});",
        "this.dispatchEvent('buttonup', {index: buttonIndex, label:this.getButtonLabel(buttonIndex, gamepad.index), gamepadIndex: gamepad.index});",
        1)
    open(path, "w", encoding="utf-8").write(text)
    print("DA DOI: Tay cam: da them nhan loai Sony/Xbox/Switch + ky hieu nut")
    return 0


if __name__ == "__main__":
    import os
    _p = sys.argv[1] if len(sys.argv) > 1 else "vendor/emulatorjs-data/src/frontend.js"
    if "gamepad" in os.path.basename(_p):
        sys.exit(patch_gamepad(_p))
    sys.exit(main(_p))
