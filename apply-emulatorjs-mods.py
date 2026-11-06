
import sys


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
        // HAI: nut combo arcade — 1 nut bam nhieu nut cung luc (kieu nut
        // khach o trang online). Ten combo theo ten nut chinh A/B/X/Y:
        // nut X goc = Neo Geo C (input 1), nut Y goc = Neo Geo D
        // (input 9) — nen combo la AB/XY/ABX/BXY, khong phai AB/CD/
        // ABC/BCD (Hai chi ra sai ten 06/11). Mapping: A=0, B=8.
        // "combo" la truong moi do script them, xu ly o cho cham nut
        // ben duoi (khong phai API goc cua EmulatorJS).
        if (["arcade", "mame", "fbneo"].includes(this.ejs.getControlScheme())) {
            // Vi tri: 1 hang 4 nut nam NGAY TREN cum nut phai (top:-45),
            // ngon cai voi toi ma khong phai voi len cao. Ban dau xep 2
            // hang (hang tren top:-100) thi nut ABC/BCD nam giua man
            // hinh, che game va kho bam — Hai bao kho choi 06/11 nen
            // doi thanh 1 hang. Khong xep xuong duoi cum nut vi se
            // de len nut Fast/Slow o man hinh hep.
            // Hinh dang: "block": true nen nut combo la hinh chu nhat
            // bo goc (cao 31px) giong nut Start/Select, khac voi nut
            // tron A/B/X/Y — de phan biet nut ket hop voi nut don.
            info.push(
                { "type": "button", "text": "AB", "id": "ab", "location": "right", "left": -70, "top": -45, "bold": true, "fontSize": 15, "block": true, "input_value": 0, "combo": [0, 8] },
                { "type": "button", "text": "XY", "id": "cd", "location": "right", "left": -20, "top": -45, "bold": true, "fontSize": 15, "block": true, "input_value": 1, "combo": [1, 9] },
                { "type": "button", "text": "ABX", "id": "abc", "location": "right", "left": 30, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 0, "combo": [0, 8, 1] },
                { "type": "button", "text": "BXY", "id": "bcd", "location": "right", "left": 80, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": [8, 1, 9] }
            );
        }
'''


LOCALIZE_ANCHOR = '''        for (let i = 0; i < info.length; i++) {
            if (info[i].text) {
                info[i].text = this.localization(info[i].text);
            }
        }'''

AUTOFIRE_OLD = "if (this.ejs.isAutofireEnabled(0, value) && !isAnalog) {"
AUTOFIRE_NEW = "if ((info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo"


DISPLAY_LABEL_ANCHOR = '''    updateGamepadLabels() {
        for (let i = 0; i < this.gamepadLabels.length; i++) {
            this.gamepadLabels[i].innerHTML = ""
            const def = this.ejs.createElement("option");
            def.setAttribute("value", "notconnected");
            def.innerText = "Not Connected";
            this.gamepadLabels[i].appendChild(def);
            for (let j = 0; j < this.ejs.gamepad.gamepads.length; j++) {
                const opt = this.ejs.createElement("option");
                opt.setAttribute("value", this.ejs.gamepad.gamepads[j].id + "_" + this.ejs.gamepad.gamepads[j].index);
                opt.innerText = this.ejs.gamepad.gamepads[j].id + "_" + this.ejs.gamepad.gamepads[j].index;
                this.gamepadLabels[i].appendChild(opt);
            }
            this.gamepadLabels[i].value = this.gamepadSelection[i] || "notconnected";
        }
    }'''

DISPLAY_LABEL_HELPER = '''
    // HAI: dich ten nut goc (BUTTON_2, SELECT...) sang ky hieu cua tay
    // cam that dang cam (Sony ✕○□△ / Xbox A B X Y / Switch B A Y X).
    // CHI DE HIEN THI o man hinh Cai dat nut bam — khong doi value2
    // goc: doi la hong nut bam (loi 06/11: doi getButtonLabel sang ky
    // hieu lam nut bam that liet het, chi co can/analog chay duoc).
    getGamepadDisplayLabel(value2, playerIdx) {
        try {
            const map = { BUTTON_1: 0, BUTTON_2: 1, BUTTON_3: 2, BUTTON_4: 3, LEFT_TOP_SHOULDER: 4, RIGHT_TOP_SHOULDER: 5, LEFT_BOTTOM_SHOULDER: 6, RIGHT_BOTTOM_SHOULDER: 7, SELECT: 8, START: 9, LEFT_STICK: 10, RIGHT_STICK: 11, DPAD_UP: 12, DPAD_DOWN: 13, DPAD_LEFT: 14, DPAD_RIGHT: 15 };
            const idx = map[String(value2)];
            if (idx === undefined) return this.localization(value2);
            let gp = null;
            const sel = (this.gamepadSelection && this.gamepadSelection[playerIdx]) || "";
            if (sel) {
                const gi = sel.lastIndexOf("_");
                const gidx = parseInt(sel.slice(gi + 1), 10);
                gp = (this.ejs.gamepad.gamepads || []).find((g) => g && g.index === gidx) || null;
            }
            if (!gp) gp = (this.ejs.gamepad.gamepads || [])[0] || null;
            if (!gp || !gp.id) return this.localization(value2);
            const sym = this.ejs.gamepad.getGamepadSymbols(this.ejs.gamepad.detectGamepadType(gp.id))[idx];
            return sym || this.localization(value2);
        } catch (e) { return this.localization(value2); }
    }'''


def main(path):
    text = open(path, encoding="utf-8").read()
    changed = []

    if "    setVirtualGamepad() {" not in text:
        print("LOI: khong tim thay setVirtualGamepad() — ban goc doi ten ham roi", file=sys.stderr)
        return 2


    if "HAI: chi them nut thieu" in text:
        print("Nut them: da co roi, bo qua")
    else:
        if LOCALIZE_ANCHOR not in text:
            print("LOI: khong tim thay neo vong lap dich text — ban goc doi bo cuc roi", file=sys.stderr)
            return 2
        text = text.replace(LOCALIZE_ANCHOR, APPEND_BLOCK + LOCALIZE_ANCHOR, 1)
        changed.append("PS1: da them L1/R1/L2/R2; NES: da them Turbo A / Turbo B")


    MENU_SHOW_OLD = '''        const show = () => {
            clearTimeout(timeout);
            timeout = setTimeout(hide, 3000);
            this.elements.menu.classList.remove("ejs_menu_bar_hidden");
        }'''
    MENU_SHOW_NEW = '''        const show = () => {
            // HAI: tat tu mo menu khi load / cham man hinh — chi mo khi bam nut ☰
            return;
        }'''
    if MENU_SHOW_NEW in text:
        text = text.replace(MENU_SHOW_NEW, MENU_SHOW_OLD, 1)
        changed.append("Menu: da tra show() ve ban goc (PC mo menu bang chuot)")


    if "info[i].autofire === true" in text:
        print("Turbo: xu ly cham nut da co autofire, bo qua")
    else:
        if AUTOFIRE_OLD not in text:
            print("LOI: khong tim thay dong isAutofireEnabled — ban goc doi xu ly nut roi", file=sys.stderr)
            return 2
        text = text.replace(AUTOFIRE_OLD, AUTOFIRE_NEW, 1)
        changed.append("Turbo: da patch xu ly cham nut (autofire:true)")


    COMBO_DOWN_OLD = '''                        this.ejs.gameManager.simulateInput(0, value, downValue);
                        if ((info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo'''
    COMBO_DOWN_NEW = '''                        // HAI: nut combo — bam 1 nut ma gui nhieu nut cung luc (arcade AB/XY/ABX/BXY)
                        (info[i].combo || [value]).forEach((v) => this.ejs.gameManager.simulateInput(0, v, downValue));
                        if (!info[i].combo && (info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo'''
    COMBO_UP_OLD = '''                        window.setTimeout(() => {
                            this.ejs.stopAutofire(0, value);
                            this.ejs.gameManager.simulateInput(0, value, 0);
                        })'''
    COMBO_UP_NEW = '''                        window.setTimeout(() => {
                            (info[i].combo || [value]).forEach((v) => { this.ejs.stopAutofire(0, v); this.ejs.gameManager.simulateInput(0, v, 0); }); // HAI: nut combo
                        })'''


    if "HAI: nut combo — bam 1 nut" in text:
        print("Nut combo: xu ly cham nut da co combo, bo qua")
    else:
        if COMBO_DOWN_OLD not in text or COMBO_UP_OLD not in text:
            print("LOI: khong tim thay dong xu ly cham/nha nut — ban goc doi xu ly nut roi", file=sys.stderr)
            return 2
        text = text.replace(COMBO_DOWN_OLD, COMBO_DOWN_NEW, 1)
        text = text.replace(COMBO_UP_OLD, COMBO_UP_NEW, 1)
        changed.append("Nut combo: da patch xu ly cham nut (arcade AB/XY/ABX/BXY)")


    if "getGamepadDisplayLabel" in text:
        print("Ky hieu nut: da co hien thi ky hieu, bo qua")
    else:
        if text.count("value2 = this.localization(value2);") != 2:
            print("LOI: khong tim thay dung 2 cho hien thi value2 — ban goc doi man hinh Cai dat roi", file=sys.stderr)
            return 2
        if DISPLAY_LABEL_ANCHOR not in text:
            print("LOI: khong tim thay updateGamepadLabels() — ban goc doi frontend.js roi", file=sys.stderr)
            return 2
        text = text.replace(DISPLAY_LABEL_ANCHOR, DISPLAY_LABEL_ANCHOR + "\n" + DISPLAY_LABEL_HELPER, 1)
        text = text.replace("value2 = this.localization(value2);", "value2 = this.getGamepadDisplayLabel(value2, i);")
        changed.append("Ky hieu nut: hien ✕○□△/ABXY theo loai tay cam o man hinh Cai dat")

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


GAMEPAD_LABEL_BROKEN = """    getButtonLabel(index, gamepadIndex) {
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
    changed = []


    if GAMEPAD_LABEL_BROKEN in text:
        text = text.replace(GAMEPAD_LABEL_BROKEN, GAMEPAD_LABEL_OLD, 1)
        changed.append("Tay cam: da tra getButtonLabel ve nhan goc (BUTTON_1...)")

    if "detectGamepadType" in text:
        print("Tay cam: da co nhan loai tay cam, bo qua")
    else:
        if GAMEPAD_LABEL_OLD not in text:
            print("LOI: khong tim thay getButtonLabel() goc — ban goc doi gamepad.js roi", file=sys.stderr)
            return 2
        text = text.replace(GAMEPAD_LABEL_OLD, GAMEPAD_HELPER + "\n" + GAMEPAD_LABEL_OLD, 1)
        changed.append("Tay cam: da them nhan loai Sony/Xbox/Switch (chi de hien thi)")


    if "this.getButtonLabel(buttonIndex, gamepad.index)" in text:
        text = text.replace(
            "this.dispatchEvent('buttondown', {index: buttonIndex, label: this.getButtonLabel(buttonIndex, gamepad.index), gamepadIndex: gamepad.index});",
            "this.dispatchEvent('buttondown', {index: buttonIndex, label: this.getButtonLabel(buttonIndex), gamepadIndex: gamepad.index});",
            1)
        text = text.replace(
            "this.dispatchEvent('buttonup', {index: buttonIndex, label:this.getButtonLabel(buttonIndex, gamepad.index), gamepadIndex: gamepad.index});",
            "this.dispatchEvent('buttonup', {index: buttonIndex, label:this.getButtonLabel(buttonIndex), gamepadIndex: gamepad.index});",
            1)
        changed.append("Tay cam: da tra dispatchEvent ve dang goc")
    if changed:
        open(path, "w", encoding="utf-8").write(text)
        print("DA DOI: " + "; ".join(changed))
    else:
        print("Tay cam: khong co gi doi.")
    return 0


BUTTON_COLOR_CSS = '''
/* HAI: nut co mau v2 (chu co mau, nen mac dinh) — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_a, .ejs_virtualGamepad_button.b_ta { color: #4caf50 !important; }
.ejs_virtualGamepad_button.b_b, .ejs_virtualGamepad_button.b_tb { color: #e53935 !important; }
.ejs_virtualGamepad_button.b_x { color: #1e88e5 !important; }
.ejs_virtualGamepad_button.b_y { color: #fdd835 !important; }
.ejs_virtualGamepad_button_down { filter: brightness(1.4); }
'''


COMBO_COLOR_CSS = '''
/* HAI: nut combo mau — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_ab { color: #ff9800 !important; }
.ejs_virtualGamepad_button.b_cd { color: #ab47bc !important; }
.ejs_virtualGamepad_button.b_abc { color: #ec407a !important; }
.ejs_virtualGamepad_button.b_bcd { color: #26a69a !important; }
'''


MD_COLOR_CSS = '''
/* HAI: nut md mau — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_c { color: #ff9800 !important; }
.ejs_virtualGamepad_button.b_z { color: #ab47bc !important; }
'''


VOLUME_CSS = '''
/* HAI: volume hien ro — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_volume_parent input[type='range'] { --value: 50%; }
.ejs_volume_parent input[type='range']::-webkit-slider-runnable-track { background-image: linear-gradient(to right, #1e88e5 var(--value, 50%), rgba(255,255,255,0.25) var(--value, 50%)) !important; }
.ejs_volume_parent input[type='range']::-webkit-slider-thumb { background: #fff !important; border: 1px solid #999 !important; }
.ejs_volume_parent input[type='range']::-moz-range-progress { background: #1e88e5 !important; }
'''


def patch_css(path):
    text = open(path, encoding="utf-8").read()
    if ".ejs_virtualGamepad_button" not in text:
        print("LOI: khong tim thay .ejs_virtualGamepad_button trong emulator.css — ban goc doi CSS roi", file=sys.stderr)
        return 2
    out = text.rstrip()
    changed = []
    if "HAI: nut co mau v2" in text:
        print("Mau nut: da co roi, bo qua")
    else:

        if "HAI: nut co mau" in text:
            import re
            out = re.sub(r"\n/\* HAI: nut co mau —.*?\n\.ejs_dpad_main \{ opacity: \.9; \}\n", "\n", out, flags=re.S)
            print("Mau nut: da go mau cu v1, chen mau v2")
        out += "\n" + BUTTON_COLOR_CSS
        changed.append("Mau nut: da chen mau chu A xanh la / B do / X xanh duong / Y vang")
    if "HAI: nut combo mau" in text:
        print("Mau nut combo: da co roi, bo qua")
    else:
        out += COMBO_COLOR_CSS
        changed.append("Mau nut combo: da chen mau chu AB/XY/ABX/BXY")
    if "HAI: nut md mau" in text:
        print("Mau nut MD: da co roi, bo qua")
    else:
        out += MD_COLOR_CSS
        changed.append("Mau nut MD: da chen mau chu C/Z")
    if "HAI: volume hien ro" in text:
        print("Volume: da co roi, bo qua")
    else:
        out += VOLUME_CSS
        changed.append("Volume: da chen mau xanh + nut tron trang cho thanh truot volume")
    if changed:
        open(path, "w", encoding="utf-8").write(out)
        print("DA DOI: " + "; ".join(changed))
    else:
        print("Khong co gi doi — CSS mod da co san.")
    return 0


MENU_OPEN_OLD = "            this.frontend.menu.open();\n"
MENU_OPEN_NEW = "            // HAI: tat tu mo menu khi load game — chi mo khi bam nut ☰\n"


def patch_emulator(path):
    text = open(path, encoding="utf-8").read()
    if "HAI: tat tu mo menu" in text:
        print("Menu tu mo (emulator.js): da tat roi, bo qua")
        return 0
    if MENU_OPEN_OLD not in text:
        print("LOI: khong tim thay dong frontend.menu.open() — ban goc doi emulator.js roi", file=sys.stderr)
        return 2
    open(path, "w", encoding="utf-8").write(text.replace(MENU_OPEN_OLD, MENU_OPEN_NEW, 1))
    print("DA DOI: Menu: da xoa dong menu.open() khi game bat dau (emulator.js)")
    return 0


if __name__ == "__main__":
    import os
    _p = sys.argv[1] if len(sys.argv) > 1 else "src/frontend.js"
    _b = os.path.basename(_p)
    if "gamepad" in _b:
        sys.exit(patch_gamepad(_p))
    if _b == "emulator.css":
        sys.exit(patch_css(_p))
    if _b == "emulator.js":
        sys.exit(patch_emulator(_p))
    sys.exit(main(_p))
