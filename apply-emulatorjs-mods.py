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
  4. Nut co mau — lam TRONG CODE giong nhu them nut (Hai chot 05/11,
     sua lai 06/11): chen them mau vao emulator.css goc (khong sua
     file index.html rieng). Mau la mau cua CHU, nen nut giu mac
     dinh cua EmulatorJS, cho giong nut tren tay cam that:
     A xanh la, B do, X xanh duong, Y vang; TA/TB cung mau A/B.
     Nut co class b_<id> nen CSS nham dung tung nut. Chen 1 lan,
     chay lai khong them trung.
  5. Tat menu tu mo khi load game (Hai chot 06/11): menu duoi cua
     EmulatorJS (Restart/Pause/Save State...) tu hien ra khi moi
     vao game. NGUYEN NHAN THAT: trong emulator.js, khi game bat
     dau chay thi code goc goi `this.frontend.menu.open()` — mo
     menu moi lan vao game (roi tu tat sau 3 giay). Patch show()
     o frontend.js khong du vi duong mo chinh la dong nay (da
     kiem chung: an danh van thay menu vi dong nay chua bi patch).
     Sua: xoa dong menu.open() do trong emulator.js + patch them
     ham show() o frontend.js lam lop phong thu thu hai. Menu
     chi mo khi bam nut ☰ goc tren phai (menu.toggle()).
  6. Nut combo arcade (Hai chot 06/11): game thung chi co 4 nut
     goc (Y/X/B/A) nen them 4 nut ket hop phia tren cum nut phai:
     AB, CD, ABC, BCD — giong nut khach o trang online cua Hai.
     Mapping Neo Geo: A=0, B=8, C=1, D=9 (nut X goc = C, Y goc = D).
     API goc chi cho 1 input_value/nut nen script them truong moi
     "combo": [..] vao nut, va patch cho xu ly cham/nha nut de
     gui/nha tat ca nut trong combo cung luc (khong autofire).
     Mau chu: AB cam, CD tim, ABC hong, BCD xanh ngoc.
  7. Chay lai lan 2 khong them trung (idempotent). Neu ban goc doi
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
        // HAI: nut combo arcade — 1 nut bam nhieu nut cung luc (kieu nut
        // khach o trang online: AB/CD/ABC/BCD). Mapping Neo Geo da xac
        // minh: A=0, B=8, C=1, D=9 (nut X goc = C, nut Y goc = D).
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
                { "type": "button", "text": "CD", "id": "cd", "location": "right", "left": -20, "top": -45, "bold": true, "fontSize": 15, "block": true, "input_value": 1, "combo": [1, 9] },
                { "type": "button", "text": "ABC", "id": "abc", "location": "right", "left": 30, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 0, "combo": [0, 8, 1] },
                { "type": "button", "text": "BCD", "id": "bcd", "location": "right", "left": 80, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": [8, 1, 9] }
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

    # --- 4. Tat menu tu mo khi load game: show() chi dung cho
    # tu mo khi click/chuot — nut ☰ goi menu.toggle() khong dung
    # show() nen van mo duoc binh thuong. ---
    MENU_SHOW_OLD = '''        const show = () => {
            clearTimeout(timeout);
            timeout = setTimeout(hide, 3000);
            this.elements.menu.classList.remove("ejs_menu_bar_hidden");
        }'''
    MENU_SHOW_NEW = '''        const show = () => {
            // HAI: tat tu mo menu khi load / cham man hinh — chi mo khi bam nut ☰
            return;
        }'''
    if "HAI: tat tu mo menu" in text:
        print("Menu tu mo: da tat roi, bo qua")
    else:
        if MENU_SHOW_OLD not in text:
            print("LOI: khong tim thay ham show() cua menu duoi — ban goc doi code roi", file=sys.stderr)
            return 2
        text = text.replace(MENU_SHOW_OLD, MENU_SHOW_NEW, 1)
        changed.append("Menu: da tat tu mo khi load game (chi mo bang nut ☰)")

    # --- 3. Patch xu ly cham nut de TA/TB that su turbo ---
    if "info[i].autofire === true" in text:
        print("Turbo: xu ly cham nut da co autofire, bo qua")
    else:
        if AUTOFIRE_OLD not in text:
            print("LOI: khong tim thay dong isAutofireEnabled — ban goc doi xu ly nut roi", file=sys.stderr)
            return 2
        text = text.replace(AUTOFIRE_OLD, AUTOFIRE_NEW, 1)
        changed.append("Turbo: da patch xu ly cham nut (autofire:true)")

    # --- 3b. Patch xu ly cham nut de nut combo (arcade) gui nhieu
    # nut cung luc. Chay SAU buoc turbo vi anchor la dong da patch
    # turbo o tren; dong nha nut thi lay tu ban goc. ---
    COMBO_DOWN_OLD = '''                        this.ejs.gameManager.simulateInput(0, value, downValue);
                        if ((info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo'''
    COMBO_DOWN_NEW = '''                        // HAI: nut combo — bam 1 nut ma gui nhieu nut cung luc (arcade AB/CD/ABC/BCD)
                        (info[i].combo || [value]).forEach((v) => this.ejs.gameManager.simulateInput(0, v, downValue));
                        if (!info[i].combo && (info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo'''
    COMBO_UP_OLD = '''                        window.setTimeout(() => {
                            this.ejs.stopAutofire(0, value);
                            this.ejs.gameManager.simulateInput(0, value, 0);
                        })'''
    COMBO_UP_NEW = '''                        window.setTimeout(() => {
                            (info[i].combo || [value]).forEach((v) => { this.ejs.stopAutofire(0, v); this.ejs.gameManager.simulateInput(0, v, 0); }); // HAI: nut combo
                        })'''
    # Chu y: phai kiem tra dau hieu cua CHO XU LY (dong comment trong
    # handler), khong kiem tra "HAI: nut combo" chung chung — vi khoi
    # nut moi chen o tren cung co chu do trong comment, kiem tra chung
    # se bo qua nham buoc nay (loi gap khi test 06/11).
    if "HAI: nut combo — bam 1 nut" in text:
        print("Nut combo: xu ly cham nut da co combo, bo qua")
    else:
        if COMBO_DOWN_OLD not in text or COMBO_UP_OLD not in text:
            print("LOI: khong tim thay dong xu ly cham/nha nut — ban goc doi xu ly nut roi", file=sys.stderr)
            return 2
        text = text.replace(COMBO_DOWN_OLD, COMBO_DOWN_NEW, 1)
        text = text.replace(COMBO_UP_OLD, COMBO_UP_NEW, 1)
        changed.append("Nut combo: da patch xu ly cham nut (arcade AB/CD/ABC/BCD)")

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


# --- 4. Nut co mau trong code: chen vao cuoi emulator.css goc ---
# Hai chot 06/11: mau la mau cua CHU, nen nut giu mac dinh cua
# EmulatorJS (xam mo), cho giong nut tren tay cam that:
#   A xanh la, B do, X xanh duong, Y vang (kieu tay Xbox).
# TA/TB la ban turbo cua A/B nen cung mau voi A/B.
BUTTON_COLOR_CSS = '''
/* HAI: nut co mau v2 (chu co mau, nen mac dinh) — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_a, .ejs_virtualGamepad_button.b_ta { color: #4caf50 !important; }
.ejs_virtualGamepad_button.b_b, .ejs_virtualGamepad_button.b_tb { color: #e53935 !important; }
.ejs_virtualGamepad_button.b_x { color: #1e88e5 !important; }
.ejs_virtualGamepad_button.b_y { color: #fdd835 !important; }
.ejs_virtualGamepad_button_down { filter: brightness(1.4); }
'''

# Mau chu cho nut combo arcade (AB/CD/ABC/BCD) — giong kieu nut
# khach o trang online cua Hai.
COMBO_COLOR_CSS = '''
/* HAI: nut combo mau — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_ab { color: #ff9800 !important; }
.ejs_virtualGamepad_button.b_cd { color: #ab47bc !important; }
.ejs_virtualGamepad_button.b_abc { color: #ec407a !important; }
.ejs_virtualGamepad_button.b_bcd { color: #26a69a !important; }
'''

# Mau chu cho 2 nut con lai cua tay Sega MD (A/B/X/Y da co mau
# kieu Xbox roi, chi thieu C va Z — anh Hai gui 06:27).
MD_COLOR_CSS = '''
/* HAI: nut md mau — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_c { color: #ff9800 !important; }
.ejs_virtualGamepad_button.b_z { color: #ab47bc !important; }
'''

# Thanh truot volume: ban goc to mau xanh bang currentColor +
# bien --value, ma --value chi duoc JS gan khi doi volume — luc
# moi load chua gan nen thanh truot toi thui, nut tron cung kho
# thay (anh Hai gui 05:04). Chen mau xanh co dinh + mac dinh
# --value 50% (JS van ghi de duoc qua inline style khi keo).
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
        # Neu file con mau cu v1 (nen to mau) thi go bo truoc khi chen v2
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
        changed.append("Mau nut combo: da chen mau chu AB/CD/ABC/BCD")
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


# --- 5b. Tat menu tu mo: xoa dong menu.open() trong emulator.js ---
# Dong nay chay moi lan game bat dau (sau this.started = true),
# mo menu duoi roi tu tat sau 3 giay — day moi la duong mo chinh.
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
