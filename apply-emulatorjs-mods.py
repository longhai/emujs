
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


GP_LAYOUT_ANCHOR = '''        this.virtualGamepad.appendChild(up);
        this.virtualGamepad.appendChild(down);
        this.virtualGamepad.appendChild(left);
        this.virtualGamepad.appendChild(right);'''

GP_LAYOUT_JS = '''
        // HAI: chinh vi tri + do mo cum nut v6 — nhan giu chon nut/D-pad, doi co bang thanh truot
        try {
        const _gpScheme = this.ejs.getControlScheme();
        const _gpOrient = () => (window.innerWidth > window.innerHeight ? "landscape" : "portrait");
        let _gpCurOrient = _gpOrient();
        const _gpKeyFor = (o) => "ejs-gamepad-layout-" + _gpScheme + "-" + o;
        const _gpBtnKeyFor = (o) => "ejs-gamepad-buttons-" + _gpScheme + "-" + o;
        const _gpLoad = (k, oldK) => {
            let v = null;
            try { v = JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { v = null; }
            if (!v && oldK) { try { v = JSON.parse(localStorage.getItem(oldK) || "null"); } catch (e) { v = null; } }
            return v || {};
        };
        let _gpPos = _gpLoad(_gpKeyFor(_gpCurOrient), "ejs-gamepad-layout-" + _gpScheme);
        let _gpBtnPos = _gpLoad(_gpBtnKeyFor(_gpCurOrient), "ejs-gamepad-buttons-" + _gpScheme);
        const _gpClusters = { top: up, center: down, left: left, right: right };
        const _gpGetSetting = (id) => { try { return this.ejs.getSettingValue(id); } catch (e) { return null; } };
        const _gpApplyOpacity = () => {
            const _op = _gpGetSetting("virtual-gamepad-opacity");
            const _v = _op ? parseFloat(_op) : 1;
            if (isNaN(_v)) return;
            for (const _k in _gpClusters) _gpClusters[_k].style.opacity = String(_v);
        };
        const _gpBtnId = (el) => {
            if (!el || !el.classList) return null;
            for (const c of el.classList) { if (c.indexOf("b_") === 0) return c.slice(2); }
            return null;
        };
        const _gpBtnTransform = (el, d) => {
            const _x = (d && d.x) || 0, _y = (d && d.y) || 0, _s = (d && d.s) || 1;
            el.style.transform = "translate(" + _x + "px," + _y + "px)" + (_s !== 1 ? " scale(" + _s + ")" : "");
        };
        const _gpApplyAll = () => {
            for (const _k in _gpClusters) {
                const _el = _gpClusters[_k];
                const _p = _gpPos[_k];
                _el.style.transform = (_p && (typeof _p.x === "number" || typeof _p.y === "number")) ? "translate(" + ((_p.x) || 0) + "px," + ((_p.y) || 0) + "px)" : "";
                const _btns = _el.querySelectorAll(".ejs_virtualGamepad_button");
                for (const _b of _btns) {
                    const _id = _gpBtnId(_b);
                    _gpBtnTransform(_b, _id ? _gpBtnPos[_id] : null);
                }
                const _dp = _el.querySelector(".b_dpad");
                if (_dp) _gpBtnTransform(_dp, _gpBtnPos["dpad"] || null);
            }
        };
        _gpApplyAll();
        const _gpBar = document.createElement("div");
        _gpBar.style.cssText = "position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:9999;display:none;gap:10px;";
        const _gpMkBtn = (txt, bg) => {
            const _b = document.createElement("button");
            _b.textContent = txt;
            _b.style.cssText = "padding:10px 18px;border-radius:999px;border:0;background:" + bg + ";color:#fff;font-size:15px;font-weight:700;box-shadow:0 2px 12px rgba(0,0,0,.4);";
            return _b;
        };
        const _gpDone = _gpMkBtn("✓ Xong", "rgba(52,130,255,.95)");
        const _gpReset = _gpMkBtn("↺ Đặt lại", "rgba(90,90,90,.92)");
        _gpDone.addEventListener("click", () => {
            try { this.changeSettingOption("virtual-gamepad-edit-layout", "disabled"); } catch (e) {}
            _gpBar.style.display = "none";
            _gpSelect(null, null);
        });
        _gpReset.addEventListener("click", () => {
            try {
                ["portrait", "landscape"].forEach((o) => {
                    localStorage.removeItem(_gpKeyFor(o));
                    localStorage.removeItem(_gpBtnKeyFor(o));
                });
                localStorage.removeItem("ejs-gamepad-layout-" + _gpScheme);
                localStorage.removeItem("ejs-gamepad-buttons-" + _gpScheme);
            } catch (e) {}
            _gpPos = {}; _gpBtnPos = {};
            _gpApplyAll();
            _gpSelect(null, null);
        });
        _gpBar.appendChild(_gpDone);
        _gpBar.appendChild(_gpReset);
        document.body.appendChild(_gpBar);
        const _gpSliderStyle = document.createElement("style");
        _gpSliderStyle.textContent = "._gpSizeRange{accent-color:#3482ff;}._gpSizeRange::-webkit-slider-thumb{width:32px;height:32px;border-radius:50%;background:#3482ff;border:3px solid #fff;box-shadow:0 1px 6px rgba(0,0,0,.5);}";
        document.head.appendChild(_gpSliderStyle);
        const _gpSlider = document.createElement("div");
        _gpSlider.style.cssText = "position:fixed;top:64px;left:50%;transform:translateX(-50%);z-index:10000;display:none;align-items:center;gap:12px;background:rgba(0,0,0,.78);border-radius:18px;padding:12px 16px;color:#fff;box-shadow:0 2px 16px rgba(0,0,0,.5);";
        const _gpSliderLabel = document.createElement("span");
        _gpSliderLabel.style.cssText = "font-size:16px;font-weight:700;min-width:52px;text-align:center;";
        const _gpRange = document.createElement("input");
        _gpRange.type = "range";
        _gpRange.min = "0.5";
        _gpRange.max = "2.5";
        _gpRange.step = "0.05";
        _gpRange.value = "1";
        _gpRange.className = "_gpSizeRange";
        _gpRange.style.cssText = "width:min(56vw,240px);height:40px;";
        const _gpPct = document.createElement("span");
        _gpPct.style.cssText = "font-size:16px;font-weight:700;min-width:52px;text-align:center;";
        _gpPct.textContent = "100%";
        _gpSlider.appendChild(_gpSliderLabel);
        _gpSlider.appendChild(_gpRange);
        _gpSlider.appendChild(_gpPct);
        document.body.appendChild(_gpSlider);
        const _gpSyncBar = () => {
            try { _gpBar.style.display = (_gpGetSetting("virtual-gamepad-edit-layout") === "enabled") ? "flex" : "none"; } catch (e) { _gpBar.style.display = "none"; }
            if (_gpBar.style.display === "none") _gpSelect(null, null);
        };
        let _gpSel = null;
        let _gpSelId = null;
        const _gpSelect = (el, id) => {
            _gpSel = el;
            _gpSelId = id;
            if (!el || !id) {
                _gpSlider.style.display = "none";
                return;
            }
            el.style.outline = "2px dashed rgba(255,255,255,.9)";
            el.style.outlineOffset = "2px";
            const _d = _gpBtnPos[id] || { x: 0, y: 0, s: 1 };
            const _s = _d.s || 1;
            _gpSliderLabel.textContent = (id === "dpad") ? "D-pad" : id.toUpperCase();
            _gpRange.value = String(_s);
            _gpPct.textContent = Math.round(_s * 100) + "%";
            _gpSlider.style.display = "flex";
            try { if (navigator.vibrate) navigator.vibrate(15); } catch (e) {}
        };
        _gpRange.addEventListener("input", () => {
            if (!_gpSel || !_gpSelId) return;
            const _s = parseFloat(_gpRange.value) || 1;
            _gpPct.textContent = Math.round(_s * 100) + "%";
            const _d = _gpBtnPos[_gpSelId] || { x: 0, y: 0, s: 1 };
            _d.s = _s;
            _gpBtnTransform(_gpSel, _d);
            _gpBtnPos[_gpSelId] = _d;
            try { localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos)); } catch (err) {}
        });
        let _gpDrag = null;
        let _gpHoldTimer = null;
        const _gpClearHold = () => { if (_gpHoldTimer !== null) { clearTimeout(_gpHoldTimer); _gpHoldTimer = null; } };
        const _gpStart = (e) => {
            if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") return;
            if (_gpDrag) return;
            e.preventDefault();
            e.stopPropagation();
            _gpApplyOpacity();
            _gpSyncBar();
            const _t = (e.touches && e.touches[0]) || e;
            const _btn = (e.target && e.target.closest) ? e.target.closest(".ejs_virtualGamepad_button") : null;
            const _dpad = (!_btn && e.target && e.target.closest) ? e.target.closest(".b_dpad") : null;
            let _selEl = null, _selId = null;
            if (_btn) {
                const _id = _gpBtnId(_btn);
                if (_id) { _selEl = _btn; _selId = _id; }
            } else if (_dpad) {
                _selEl = _dpad; _selId = "dpad";
            }
            if (_selEl && _selId) {
                if (_selId === "dpad") {
                    const _ck = Object.keys(_gpClusters).find((k) => _gpClusters[k].contains(_selEl)) || "left";
                    const _p = _gpPos[_ck] || { x: 0, y: 0 };
                    _gpDrag = { el: _gpClusters[_ck], kind: "cluster", id: _ck, sx: _t.clientX, sy: _t.clientY, ox: _p.x || 0, oy: _p.y || 0, nx: null, ny: null, moved: false };
                } else {
                    const _p = _gpBtnPos[_selId] || { x: 0, y: 0, s: 1 };
                    _gpDrag = { el: _selEl, kind: "btn", id: _selId, sx: _t.clientX, sy: _t.clientY, ox: _p.x || 0, oy: _p.y || 0, nx: null, ny: null, moved: false };
                }
                _gpClearHold();
                _gpHoldTimer = setTimeout(() => { _gpHoldTimer = null; if (_gpDrag) _gpDrag.held = true; _gpSelect(_selEl, _selId); }, 1000);
            } else {
                const _ck = Object.keys(_gpClusters).find((k) => _gpClusters[k] === e.currentTarget) || "left";
                const _p = _gpPos[_ck] || { x: 0, y: 0 };
                _gpDrag = { el: e.currentTarget, kind: "cluster", id: _ck, sx: _t.clientX, sy: _t.clientY, ox: _p.x || 0, oy: _p.y || 0, nx: null, ny: null, moved: false };
            }
            _gpDrag.el.style.outline = "2px dashed rgba(255,255,255,.9)";
            _gpDrag.el.style.outlineOffset = "2px";
        };
        const _gpBlock = (e) => {
            if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") return;
            e.preventDefault();
            e.stopPropagation();
        };
        const _gpMove = (e) => {
            if (!_gpDrag) return;
            const _t = (e.touches && e.touches[0]) || e;
            const _dx = _t.clientX - _gpDrag.sx, _dy = _t.clientY - _gpDrag.sy;
            if (Math.abs(_dx) + Math.abs(_dy) > 10) { _gpDrag.moved = true; _gpClearHold(); }
            const _nx = _gpDrag.ox + _dx;
            const _ny = _gpDrag.oy + _dy;
            if (_gpDrag.kind === "btn") {
                const _d = _gpBtnPos[_gpDrag.id] || { x: 0, y: 0, s: 1 };
                _gpBtnTransform(_gpDrag.el, { x: _nx, y: _ny, s: _d.s || 1 });
            } else {
                _gpDrag.el.style.transform = "translate(" + _nx + "px," + _ny + "px)";
            }
            _gpDrag.nx = _nx; _gpDrag.ny = _ny;
        };
        const _gpEnd = () => {
            _gpClearHold();
            if (!_gpDrag) return;
            const _d = _gpDrag;
            _d.el.style.outline = "";
            _d.el.style.outlineOffset = "";
            if (_d.moved && typeof _d.nx === "number") {
                try {
                    if (_d.kind === "btn") {
                        const _old = _gpBtnPos[_d.id] || { x: 0, y: 0, s: 1 };
                        _gpBtnPos[_d.id] = { x: Math.round(_d.nx), y: Math.round(_d.ny), s: _old.s || 1 };
                        localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos));
                    } else {
                        _gpPos[_d.id] = { x: Math.round(_d.nx), y: Math.round(_d.ny) };
                        localStorage.setItem(_gpKeyFor(_gpCurOrient), JSON.stringify(_gpPos));
                    }
                } catch (err) {}
            } else if (!_d.moved && _d.kind !== "btn" && !_d.held) {
                _gpSelect(null, null);
            }
            _gpDrag = null;
        };
        for (const _gpK in _gpClusters) {
            _gpClusters[_gpK].addEventListener("pointerdown", _gpStart, true);
            _gpClusters[_gpK].addEventListener("touchstart", _gpBlock, true);
        }
        window.addEventListener("pointermove", _gpMove);
        window.addEventListener("pointerup", _gpEnd);
        window.addEventListener("pointercancel", _gpEnd);
        _gpApplyOpacity();
        _gpSyncBar();
        this.virtualGamepad.addEventListener("pointerdown", () => { _gpApplyOpacity(); _gpSyncBar(); });
        setTimeout(_gpApplyAll, 100);
        window.addEventListener("resize", () => {
            const _o = _gpOrient();
            if (_o === _gpCurOrient) return;
            _gpCurOrient = _o;
            _gpPos = _gpLoad(_gpKeyFor(_o), "ejs-gamepad-layout-" + _gpScheme);
            _gpBtnPos = _gpLoad(_gpBtnKeyFor(_o), "ejs-gamepad-buttons-" + _gpScheme);
            _gpSelect(null, null);
            _gpApplyAll();
        });
        } catch (_gpErr) {}'''






GP_LAYOUT_MENU_ANCHOR = '''            addToMenu(this.localization("Left Handed Mode"), "virtual-gamepad-left-handed-mode", {
                "enabled": this.localization("Enabled"),
                "disabled": this.localization("Disabled")
            }, "disabled", virtualGamepad, true);'''

GP_LAYOUT_MENU = '''
            addToMenu(this.localization("Chỉnh vị trí nút"), "virtual-gamepad-edit-layout", {
                "enabled": this.localization("Enabled"),
                "disabled": this.localization("Disabled")
            }, "disabled", virtualGamepad, true); // HAI: chinh vi tri cum nut
            addToMenu(this.localization("Độ mờ nút"), "virtual-gamepad-opacity", {
                "1": "100%",
                "0.8": "80%",
                "0.6": "60%",
                "0.4": "40%"
            }, "1", virtualGamepad, true); // HAI: do mo cum nut'''


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

    if "cum nut v6" in text:
        print("Chinh cum nut: da co ban v6 (thanh truot doi co + D-pad), bo qua")
    else:
        import re
        old_pat = re.compile(r"        // HAI: chinh vi tri \+ do mo cum nut v5 — nhan giu 1s chon nut, nut goc to de keo, vuot doc doi co\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n")
        _m = old_pat.search(text)
        if _m:
            text = text[:_m.start()] + text[_m.end():]
            print("Chinh cum nut: da go ban v5, chen ban v6")
        else:
            old_pat4 = re.compile(r"        // HAI: chinh vi tri \+ do mo cum nut v4 — keo tung nut, keo goc doi co, ngang/doc rieng, Dat lai\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n")
            _m4 = old_pat4.search(text)
            if _m4:
                text = text[:_m4.start()] + text[_m4.end():]
                print("Chinh cum nut: da go ban v4, chen ban v6")
            else:
                old_pat3 = re.compile(r"        // HAI: chinh vi tri \+ do mo cum nut v3 — keo tung nut / cum nut, nut Xong thoat\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n")
                _m3 = old_pat3.search(text)
                if _m3:
                    text = text[:_m3.start()] + text[_m3.end():]
                    print("Chinh cum nut: da go ban v3, chen ban v6")
                else:
                    old_pat2 = re.compile(r"        // HAI: chinh vi tri \+ do mo cum nut v2 — keo de doi vi tri, luu theo he may\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n")
                    _m2 = old_pat2.search(text)
                    if _m2:
                        text = text[:_m2.start()] + text[_m2.end():]
                        print("Chinh cum nut: da go ban v2, chen ban v6")
                    else:
                        old_pat1 = re.compile(r"        // HAI: chinh vi tri \+ do mo cum nut — keo de doi vi tri, luu theo he may\n[\s\S]*?        this\.virtualGamepad\.addEventListener\(\"pointerdown\", _gpApplyOpacity\);\n")
                        _m1 = old_pat1.search(text)
                        if _m1:
                            text = text[:_m1.start()] + text[_m1.end():]
                            print("Chinh cum nut: da go ban v1 (gay ket game), chen ban v6")
        if GP_LAYOUT_ANCHOR not in text:
            print("LOI: khong tim thay cho append 4 cum nut — ban goc doi setVirtualGamepad roi", file=sys.stderr)
            return 2
        text = text.replace(GP_LAYOUT_ANCHOR, GP_LAYOUT_ANCHOR + GP_LAYOUT_JS, 1)
        changed.append("Chinh cum nut: da them v6 (thanh truot doi co + D-pad)")

    if "HAI: do mo cum nut" in text:
        print("Menu do mo: da co roi, bo qua")
    else:
        if GP_LAYOUT_MENU_ANCHOR not in text:
            print("LOI: khong tim thay menu Left Handed Mode — ban goc doi menu roi", file=sys.stderr)
            return 2
        text = text.replace(GP_LAYOUT_MENU_ANCHOR, GP_LAYOUT_MENU_ANCHOR + GP_LAYOUT_MENU, 1)
        changed.append("Menu: da them 'Chinh vi tri nut' + 'Do mo nut' vao muc Virtual Gamepad")

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


SHADER_2XSAL = """#if defined(VERTEX)

   #if __VERSION__ >= 130
      #define COMPAT_VARYING out
      #define COMPAT_ATTRIBUTE in
      #define COMPAT_TEXTURE texture
   #else
      #define COMPAT_VARYING varying
      #define COMPAT_ATTRIBUTE attribute
      #define COMPAT_TEXTURE texture2D
   #endif

   #ifdef GL_ES
      #define COMPAT_PRECISION mediump
   #else
      #define COMPAT_PRECISION
   #endif

COMPAT_ATTRIBUTE vec4 VertexCoord;
COMPAT_ATTRIBUTE vec4 COLOR;
COMPAT_ATTRIBUTE vec4 TexCoord;
COMPAT_VARYING vec4 COL0;
COMPAT_VARYING vec4 TEX0;

uniform mat4 MVPMatrix;
uniform COMPAT_PRECISION int FrameDirection;
uniform COMPAT_PRECISION int FrameCount;
uniform COMPAT_PRECISION vec2 OutputSize;
uniform COMPAT_PRECISION vec2 TextureSize;
uniform COMPAT_PRECISION vec2 InputSize;

#define vTexCoord TEX0.xy
#define SourceSize vec4(TextureSize, 1.0 / TextureSize)
#define outsize vec4(OutputSize, 1.0 / OutputSize)

void main()
{
      gl_Position = MVPMatrix * VertexCoord;
      COL0 = COLOR;
      TEX0.xy = TexCoord.xy;
}

#elif defined(FRAGMENT)

   #if __VERSION__ >= 130
      #define COMPAT_VARYING in
      #define COMPAT_TEXTURE texture
      out vec4 FragColor;
   #else
      #define COMPAT_VARYING varying
      #define FragColor gl_FragColor
      #define COMPAT_TEXTURE texture2D
   #endif

   #ifdef GL_ES
      #ifdef GL_FRAGMENT_PRECISION_HIGH
         precision highp float;
      #else
         precision mediump float;
      #endif

      #define COMPAT_PRECISION mediump
   #else
      #define COMPAT_PRECISION
   #endif

uniform COMPAT_PRECISION int FrameDirection;
uniform COMPAT_PRECISION int FrameCount;
uniform COMPAT_PRECISION vec2 OutputSize;
uniform COMPAT_PRECISION vec2 TextureSize;
uniform COMPAT_PRECISION vec2 InputSize;
uniform sampler2D Texture;
COMPAT_VARYING vec4 TEX0;

#define Source Texture
#define vTexCoord TEX0.xy
#define SourceSize vec4(TextureSize, 1.0 / TextureSize)
#define outsize vec4(OutputSize, 1.0 / OutputSize)

void main()
{
    vec2 texsize = SourceSize.xy;
    float dx     = pow(texsize.x, -1.0) * 0.25;
    float dy     = pow(texsize.y, -1.0) * 0.25;
    vec3  dt     = vec3(1.0, 1.0, 1.0);

    vec2 UL = vTexCoord + vec2(-dx, -dy);
    vec2 UR = vTexCoord + vec2( dx, -dy);
    vec2 DL = vTexCoord + vec2(-dx,  dy);
    vec2 DR = vTexCoord + vec2( dx,  dy);

    vec3 c00 = COMPAT_TEXTURE(Source, UL).xyz;
    vec3 c20 = COMPAT_TEXTURE(Source, UR).xyz;
    vec3 c02 = COMPAT_TEXTURE(Source, DL).xyz;
    vec3 c22 = COMPAT_TEXTURE(Source, DR).xyz;

    float m1 = dot(abs(c00 - c22), dt) + 0.001;
    float m2 = dot(abs(c02 - c20), dt) + 0.001;

    FragColor = vec4((m1*(c02 + c20) + m2*(c22 + c00))/(2.0*(m1 + m2)), 1.0);
}
#endif
"""
SHADER_DOTMASK = """#pragma parameter shadowMask "Mask Style" 3.0 0.0 4.0 1.0
#pragma parameter BGR "RGB/BGR subpixels" 0.0 0.0 1.0 1.0
#pragma parameter DOTMASK_STRENGTH "CGWG Dot Mask Strength" 0.3 0.0 1.0 0.01
#pragma parameter maskDark "Lottes maskDark" 0.5 0.0 2.0 0.1
#pragma parameter maskLight "Lottes maskLight" 1.5 0.0 2.0 0.1

#if defined(VERTEX)

   #if __VERSION__ >= 130
      #define COMPAT_VARYING out
      #define COMPAT_ATTRIBUTE in
      #define COMPAT_TEXTURE texture
   #else
      #define COMPAT_VARYING varying
      #define COMPAT_ATTRIBUTE attribute
      #define COMPAT_TEXTURE texture2D
   #endif

   #ifdef GL_ES
      #define COMPAT_PRECISION mediump
   #else
      #define COMPAT_PRECISION
   #endif

COMPAT_ATTRIBUTE vec4 VertexCoord;
COMPAT_ATTRIBUTE vec4 COLOR;
COMPAT_ATTRIBUTE vec4 TexCoord;
COMPAT_VARYING vec4 COL0;
COMPAT_VARYING vec4 TEX0;

uniform mat4 MVPMatrix;
uniform COMPAT_PRECISION int FrameDirection;
uniform COMPAT_PRECISION int FrameCount;
uniform COMPAT_PRECISION vec2 OutputSize;
uniform COMPAT_PRECISION vec2 TextureSize;
uniform COMPAT_PRECISION vec2 InputSize;


#define vTexCoord TEX0.xy
#define SourceSize vec4(TextureSize, 1.0 / TextureSize)
#define outsize vec4(OutputSize, 1.0 / OutputSize)

void main()
{
      gl_Position = MVPMatrix * VertexCoord;
      COL0 = COLOR;
      TEX0.xy = TexCoord.xy;
}

#elif defined(FRAGMENT)

   #if __VERSION__ >= 130
      #define COMPAT_VARYING in
      #define COMPAT_TEXTURE texture
      out vec4 FragColor;
   #else
      #define COMPAT_VARYING varying
      #define FragColor gl_FragColor
      #define COMPAT_TEXTURE texture2D
   #endif

   #ifdef GL_ES
      #ifdef GL_FRAGMENT_PRECISION_HIGH
         precision highp float;
      #else
         precision mediump float;
      #endif

      #define COMPAT_PRECISION mediump
   #else
      #define COMPAT_PRECISION
   #endif

uniform COMPAT_PRECISION int FrameDirection;
uniform COMPAT_PRECISION int FrameCount;
uniform COMPAT_PRECISION vec2 OutputSize;
uniform COMPAT_PRECISION vec2 TextureSize;
uniform COMPAT_PRECISION vec2 InputSize;
uniform sampler2D Texture;
COMPAT_VARYING vec4 TEX0;


#define Source Texture
#define vTexCoord TEX0.xy
#define SourceSize vec4(TextureSize, 1.0 / TextureSize)
#define outsize vec4(OutputSize, 1.0 / OutputSize)

#ifdef PARAMETER_UNIFORM

uniform COMPAT_PRECISION float shadowMask;
uniform COMPAT_PRECISION float BGR;
uniform COMPAT_PRECISION float DOTMASK_STRENGTH;
uniform COMPAT_PRECISION float maskDark;
uniform COMPAT_PRECISION float maskLight;
#else
#define shadowMask 3.0
#define BGR 0.0
#define DOTMASK_STRENGTH 0.3
#define maskDark 0.5
#define maskLight 1.5
#endif

#define mod_factor vTexCoord.x * outsize.x/InputSize.x* SourceSize.x


vec3 Mask(vec2 pos)
{
   vec3 mask = vec3(maskDark, maskDark, maskDark);


   if (shadowMask == 1.0)
   {
      float line = maskLight;
      float odd  = 0.0;

      if (fract(pos.x/6.0) < 0.5)
         odd = 1.0;
      if (fract((pos.y + odd)/2.0) < 0.5)
         line = maskDark;

      pos.x = fract(pos.x/3.0);

      if (pos.x<0.3333) mask.rgb = (BGR == 1.0) ? vec3(mask.r, mask.g, maskLight) : vec3(maskLight, mask.g, mask.b);
      else if (pos.x<0.6666)         mask.g = maskLight;
      else          mask.rgb = (BGR == 1.0) ? vec3(maskLight, mask.g, mask.b) : vec3(mask.r, mask.g, maskLight);
      mask*=line;
   }


   else if (shadowMask == 2.0)
   {
      pos.x = fract(pos.x/3.0);

      if (pos.x<0.3333) mask.rgb = (BGR == 1.0) ? vec3(mask.r, mask.g, maskLight) : vec3(maskLight, mask.g, mask.b);
      else if (pos.x<0.6666)         mask.g = maskLight;
      else          mask.rgb = (BGR == 1.0) ? vec3(maskLight, mask.g, mask.b) : vec3(mask.r, mask.g, maskLight);
   }


   else if (shadowMask == 3.0)
   {
      pos.x += pos.y*3.0;
      pos.x  = fract(pos.x/6.0);

      if (pos.x<0.3333) mask.rgb = (BGR == 1.0) ? vec3(mask.r, mask.g, maskLight) : vec3(maskLight, mask.g, mask.b);
      else if (pos.x<0.6666)         mask.g = maskLight;
      else          mask.rgb = (BGR == 1.0) ? vec3(maskLight, mask.g, mask.b) : vec3(mask.r, mask.g, maskLight);
   }


   else if (shadowMask == 4.0)
   {
      pos.xy = floor(pos.xy*vec2(1.0, 0.5));
      pos.x += pos.y*3.0;
      pos.x  = fract(pos.x/6.0);

      if (pos.x<0.3333) mask.rgb = (BGR == 1.0) ? vec3(mask.r, mask.g, maskLight) : vec3(maskLight, mask.g, mask.b);
      else if (pos.x<0.6666)         mask.g = maskLight;
      else          mask.rgb = (BGR == 1.0) ? vec3(maskLight, mask.g, mask.b) : vec3(mask.r, mask.g, maskLight);
   }

   return mask;
}

void main()
{
   vec3 res = pow(COMPAT_TEXTURE(Source, vTexCoord).rgb, vec3(2.2,2.2,2.2));

   float mask = 1.0 - DOTMASK_STRENGTH;



   vec3 dotMaskWeights = mix(vec3(1.0, mask, 1.0),
                             vec3(mask, 1.0, mask),
                             floor(mod(mod_factor, 2.0)));
   if (shadowMask == 0.)
   {
      res *= dotMaskWeights;
   }
   else
   {
      res *= Mask(floor(1.000001 * gl_FragCoord.xy + vec2(0.5,0.5)));
   }

      FragColor = vec4(pow(res, vec3(1.0/2.2, 1.0/2.2, 1.0/2.2)), 1.0);
}
#endif
"""
SHADER_4XSOFT = """#pragma parameter RESOLUTION_X "4xSoft Input Resolution X" 0.0 0.0 1920.0 1.0
#pragma parameter RESOLUTION_Y "4xSoft Input Resolution Y" 0.0 0.0 1920.0 1.0
#pragma parameter CONTRAST "4xSoft Contrast" 3.0 0.0 10.0 0.1

#if defined(VERTEX)

   #if __VERSION__ >= 130
      #define COMPAT_VARYING out
      #define COMPAT_ATTRIBUTE in
      #define COMPAT_TEXTURE texture
   #else
      #define COMPAT_VARYING varying
      #define COMPAT_ATTRIBUTE attribute
      #define COMPAT_TEXTURE texture2D
   #endif

   #ifdef GL_ES
      #define COMPAT_PRECISION mediump
   #else
      #define COMPAT_PRECISION
   #endif

COMPAT_ATTRIBUTE vec4 VertexCoord;
COMPAT_ATTRIBUTE vec4 COLOR;
COMPAT_ATTRIBUTE vec4 TexCoord;
COMPAT_VARYING vec4 COL0;
COMPAT_VARYING vec4 TEX0;
COMPAT_VARYING vec4 t1;
COMPAT_VARYING vec4 t2;
COMPAT_VARYING vec4 t3;
COMPAT_VARYING vec4 t4;
COMPAT_VARYING vec4 t5;
COMPAT_VARYING vec4 t6;

uniform mat4 MVPMatrix;
uniform COMPAT_PRECISION int FrameDirection;
uniform COMPAT_PRECISION int FrameCount;
uniform COMPAT_PRECISION vec2 OutputSize;
uniform COMPAT_PRECISION vec2 TextureSize;
uniform COMPAT_PRECISION vec2 InputSize;

#define vTexCoord TEX0.xy
#define SourceSize vec4(TextureSize, 1.0 / TextureSize)
#define outsize vec4(OutputSize, 1.0 / OutputSize)

#ifdef PARAMETER_UNIFORM
uniform COMPAT_PRECISION float RESOLUTION_X;
uniform COMPAT_PRECISION float RESOLUTION_Y;
uniform COMPAT_PRECISION float CONTRAST;
#else
#define RESOLUTION_X 0.0
#define RESOLUTION_Y 0.0
#define CONTRAST 3.0
#endif

#define RESOLUTION_X_DEF SourceSize.x
#define RESOLUTION_Y_DEF SourceSize.y

void main()
{
   vec2 ps = vec2(1.0/((RESOLUTION_X == 0.0) ? RESOLUTION_X_DEF : RESOLUTION_X), 1.0/((RESOLUTION_Y == 0.0) ? RESOLUTION_Y_DEF : RESOLUTION_Y));

   float dx = ps.x;
   float dy = ps.y;
   float sx = ps.x * 0.5;
   float sy = ps.y * 0.5;
   gl_Position = MVPMatrix * VertexCoord;
   vTexCoord = TexCoord.xy;
   t1 = vec4(vTexCoord,vTexCoord) + vec4(-dx, -dy, dx, -dy);
   t2 = vec4(vTexCoord,vTexCoord) + vec4(dx, dy, -dx, dy);
   t3 = vec4(vTexCoord,vTexCoord) + vec4(-sx, -sy, sx, -sy);
   t4 = vec4(vTexCoord,vTexCoord) + vec4(sx, sy, -sx, sy);
   t5 = vec4(vTexCoord,vTexCoord) + vec4(-dx, 0, dx, 0);
   t6 = vec4(vTexCoord,vTexCoord) + vec4(0, -dy, 0, dy);
}

#elif defined(FRAGMENT)

   #if __VERSION__ >= 130
      #define COMPAT_VARYING in
      #define COMPAT_TEXTURE texture
      out vec4 FragColor;
   #else
      #define COMPAT_VARYING varying
      #define FragColor gl_FragColor
      #define COMPAT_TEXTURE texture2D
   #endif

   #ifdef GL_ES
      #ifdef GL_FRAGMENT_PRECISION_HIGH
         precision highp float;
      #else
         precision mediump float;
      #endif

      #define COMPAT_PRECISION mediump
   #else
      #define COMPAT_PRECISION
   #endif

uniform COMPAT_PRECISION int FrameDirection;
uniform COMPAT_PRECISION int FrameCount;
uniform COMPAT_PRECISION vec2 OutputSize;
uniform COMPAT_PRECISION vec2 TextureSize;
uniform COMPAT_PRECISION vec2 InputSize;
uniform sampler2D Texture;
COMPAT_VARYING vec4 TEX0;
COMPAT_VARYING vec4 t1;
COMPAT_VARYING vec4 t2;
COMPAT_VARYING vec4 t3;
COMPAT_VARYING vec4 t4;
COMPAT_VARYING vec4 t5;
COMPAT_VARYING vec4 t6;

#define Source Texture
#define vTexCoord TEX0.xy
#define SourceSize vec4(TextureSize, 1.0 / TextureSize)
#define outsize vec4(OutputSize, 1.0 / OutputSize)

#ifdef PARAMETER_UNIFORM
uniform COMPAT_PRECISION float RESOLUTION_X;
uniform COMPAT_PRECISION float RESOLUTION_Y;
uniform COMPAT_PRECISION float CONTRAST;
#else
#define RESOLUTION_X 0.0
#define RESOLUTION_Y 0.0
#define CONTRAST 3.0
#endif

const vec3 dt = vec3(1.0, 1.0, 1.0);

void main()
{
  vec3 c11 = COMPAT_TEXTURE(Source, vTexCoord).xyz;
  vec3 c00 = COMPAT_TEXTURE(Source, t1.xy).xyz;
  vec3 c20 = COMPAT_TEXTURE(Source, t1.zw).xyz;
  vec3 c22 = COMPAT_TEXTURE(Source, t2.xy).xyz;
  vec3 c02 = COMPAT_TEXTURE(Source, t2.zw).xyz;
  vec3 s00 = COMPAT_TEXTURE(Source, t3.xy).xyz;
  vec3 s20 = COMPAT_TEXTURE(Source, t3.zw).xyz;
  vec3 s22 = COMPAT_TEXTURE(Source, t4.xy).xyz;
  vec3 s02 = COMPAT_TEXTURE(Source, t4.zw).xyz;
  vec3 c01 = COMPAT_TEXTURE(Source, t5.xy).xyz;
  vec3 c21 = COMPAT_TEXTURE(Source, t5.zw).xyz;
  vec3 c10 = COMPAT_TEXTURE(Source, t6.xy).xyz;
  vec3 c12 = COMPAT_TEXTURE(Source, t6.zw).xyz;

  float d1=dot(abs(c00-c22),dt)+0.0001;
  float d2=dot(abs(c20-c02),dt)+0.0001;
  float hl=dot(abs(c01-c21),dt)+0.0001;
  float vl=dot(abs(c10-c12),dt)+0.0001;
  float m1=dot(abs(s00-s22),dt)+0.001;
  float m2=dot(abs(s02-s20),dt)+0.001;

  vec3 t1=(hl*(c10+c12)+vl*(c01+c21)+(hl+vl)*c11)/(CONTRAST *(hl+vl));
  vec3 t2=(d1*(c20+c02)+d2*(c00+c22)+(d1+d2)*c11)/(CONTRAST *(d1+d2));

   FragColor = vec4(0.25*(t1+t2+(m2*(s00+s22)+m1*(s02+s20))/(m1+m2)),1.0);
}
#endif
"""
SHADER_XBR_LV2 = """#pragma parameter XBR_Y_WEIGHT "Y Weight" 48.0 0.0 100.0 1.0
#pragma parameter XBR_EQ_THRESHOLD "Eq Threshold" 15.0 0.0 50.0 1.0
#pragma parameter XBR_LV1_COEFFICIENT "Lv1 Coefficient" 0.5 0.0 30.0 0.5
#pragma parameter XBR_LV2_COEFFICIENT "Lv2 Coefficient" 2.0 1.0 3.0 0.1
#pragma parameter small_details "Preserve Small Details" 0.0 0.0 1.0 1.0





#define CORNER_C


#ifndef CORNER_A
  #define SMOOTH_TIPS
#endif

#define XBR_SCALE 3.0

#define lv2_cf XBR_LV2_COEFFICIENT

#define texCoord TEX0
#define t1 TEX1
#define t2 TEX2
#define t3 TEX3
#define t4 TEX4
#define t5 TEX5
#define t6 TEX6
#define t7 TEX7

#if defined(VERTEX)

#if __VERSION__ >= 130
#define OUT out
#define IN  in
#define tex2D texture
#else
#define OUT varying
#define IN attribute
#define tex2D texture2D
#endif

#ifdef GL_ES
#define PRECISION mediump
#else
#define PRECISION
#endif


IN  vec4 VertexCoord;
IN  vec4 Color;
IN  vec2 TexCoord;

OUT vec4 color;
OUT vec2 texCoord;
OUT vec4 t1;
OUT vec4 t2;
OUT vec4 t3;
OUT vec4 t4;
OUT vec4 t5;
OUT vec4 t6;
OUT vec4 t7;

uniform mat4 MVPMatrix;
uniform PRECISION int FrameDirection;
uniform PRECISION int FrameCount;
uniform PRECISION vec2 OutputSize;
uniform PRECISION vec2 TextureSize;
uniform PRECISION vec2 InputSize;

void main()
{
    gl_Position = MVPMatrix * VertexCoord;
    color = Color;

    float dx = (1.0/TextureSize.x);
    float dy = (1.0/TextureSize.y);

    texCoord     = TexCoord;
	texCoord.x *= 1.00000001;
    t1 = TexCoord.xxxy + vec4( -dx, 0, dx,-2.0*dy);
    t2 = TexCoord.xxxy + vec4( -dx, 0, dx,    -dy);
    t3 = TexCoord.xxxy + vec4( -dx, 0, dx,      0);
    t4 = TexCoord.xxxy + vec4( -dx, 0, dx,     dy);
    t5 = TexCoord.xxxy + vec4( -dx, 0, dx, 2.0*dy);
    t6 = TexCoord.xyyy + vec4(-2.0*dx,-dy, 0,  dy);
    t7 = TexCoord.xyyy + vec4( 2.0*dx,-dy, 0,  dy);
}


#elif defined(FRAGMENT)

#if __VERSION__ >= 130
#define IN in
#define tex2D texture
out vec4 FragColor;
#else
#define IN varying
#define FragColor gl_FragColor
#define tex2D texture2D
#endif

#ifdef GL_ES
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
#define PRECISION mediump
#else
#define PRECISION
#endif

uniform PRECISION int FrameDirection;
uniform PRECISION int FrameCount;
uniform PRECISION vec2 OutputSize;
uniform PRECISION vec2 TextureSize;
uniform PRECISION vec2 InputSize;
uniform sampler2D Texture;
IN vec2 texCoord;
IN vec4 t1;
IN vec4 t2;
IN vec4 t3;
IN vec4 t4;
IN vec4 t5;
IN vec4 t6;
IN vec4 t7;

#ifdef PARAMETER_UNIFORM
uniform PRECISION float XBR_Y_WEIGHT;
uniform PRECISION float XBR_EQ_THRESHOLD;
uniform PRECISION float XBR_LV1_COEFFICIENT;
uniform PRECISION float XBR_LV2_COEFFICIENT;
uniform PRECISION float small_details;
#else
#define XBR_Y_WEIGHT 48.0
#define XBR_EQ_THRESHOLD 15.0
#define XBR_LV1_COEFFICIENT 0.5
#define XBR_LV2_COEFFICIENT 2.0
#define small_details 0.0
#endif


const float coef         = 2.0;
const vec3 rgbw          = vec3(14.352, 28.176, 5.472);
const vec4 eq_threshold  = vec4(15.0, 15.0, 15.0, 15.0);


const  vec4 Ao = vec4( 1.0, -1.0, -1.0, 1.0 );
const  vec4 Bo = vec4( 1.0,  1.0, -1.0,-1.0 );
const  vec4 Co = vec4( 1.5,  0.5, -0.5, 0.5 );
const  vec4 Ax = vec4( 1.0, -1.0, -1.0, 1.0 );
const  vec4 Bx = vec4( 0.5,  2.0, -0.5,-2.0 );
const  vec4 Cx = vec4( 1.0,  1.0, -0.5, 0.0 );
const  vec4 Ay = vec4( 1.0, -1.0, -1.0, 1.0 );
const  vec4 By = vec4( 2.0,  0.5, -2.0,-0.5 );
const  vec4 Cy = vec4( 2.0,  0.0, -1.0, 0.5 );
const  vec4 Ci = vec4(0.25, 0.25, 0.25, 0.25);

const vec3 Y = vec3(0.2126, 0.7152, 0.0722);


vec4 df(vec4 A, vec4 B)
{
    return vec4(abs(A-B));
}


vec4 diff(vec4 A, vec4 B)
{
    return vec4(notEqual(A, B));
}


vec4 eq(vec4 A, vec4 B)
{
    return (step(df(A, B), vec4(XBR_EQ_THRESHOLD)));
}


vec4 neq(vec4 A, vec4 B)
{
    return (vec4(1.0, 1.0, 1.0, 1.0) - eq(A, B));
}


vec4 wd(vec4 a, vec4 b, vec4 c, vec4 d, vec4 e, vec4 f, vec4 g, vec4 h)
{
    return (df(a,b) + df(a,c) + df(d,e) + df(d,f) + 4.0*df(g,h));
}

vec4 weighted_distance(vec4 a, vec4 b, vec4 c, vec4 d, vec4 e, vec4 f, vec4 g, vec4 h, vec4 i, vec4 j, vec4 k, vec4 l)
{
	return (df(a,b) + df(a,c) + df(d,e) + df(d,f) + df(i,j) + df(k,l) + 2.0*df(g,h));
}

float c_df(vec3 c1, vec3 c2)
{
      vec3 df = abs(c1 - c2);
      return df.r + df.g + df.b;
}

void main()
{
    vec4 delta = vec4(1.0/XBR_SCALE, 1.0/XBR_SCALE, 1.0/XBR_SCALE, 1.0/XBR_SCALE);
    vec4 delta_l = vec4(0.5/XBR_SCALE, 1.0/XBR_SCALE, 0.5/XBR_SCALE, 1.0/XBR_SCALE);
    vec4 delta_u = delta_l.yxwz;
    vec4 edri, edr, edr_l, edr_u, px;
    vec4 irlv0, irlv1, irlv2l, irlv2u, block_3d;
    vec4 fx, fx_l, fx_u;

    vec2 fp  = fract(texCoord*TextureSize);

    vec3 A1 = tex2D(Texture, t1.xw ).xyz;
    vec3 B1 = tex2D(Texture, t1.yw ).xyz;
    vec3 C1 = tex2D(Texture, t1.zw ).xyz;
    vec3 A  = tex2D(Texture, t2.xw ).xyz;
    vec3 B  = tex2D(Texture, t2.yw ).xyz;
    vec3 C  = tex2D(Texture, t2.zw ).xyz;
    vec3 D  = tex2D(Texture, t3.xw ).xyz;
    vec3 E  = tex2D(Texture, t3.yw ).xyz;
    vec3 F  = tex2D(Texture, t3.zw ).xyz;
    vec3 G  = tex2D(Texture, t4.xw ).xyz;
    vec3 H  = tex2D(Texture, t4.yw ).xyz;
    vec3 I  = tex2D(Texture, t4.zw ).xyz;
    vec3 G5 = tex2D(Texture, t5.xw ).xyz;
    vec3 H5 = tex2D(Texture, t5.yw ).xyz;
    vec3 I5 = tex2D(Texture, t5.zw ).xyz;
    vec3 A0 = tex2D(Texture, t6.xy ).xyz;
    vec3 D0 = tex2D(Texture, t6.xz ).xyz;
    vec3 G0 = tex2D(Texture, t6.xw ).xyz;
    vec3 C4 = tex2D(Texture, t7.xy ).xyz;
    vec3 F4 = tex2D(Texture, t7.xz ).xyz;
    vec3 I4 = tex2D(Texture, t7.xw ).xyz;

    vec4 b  = vec4(dot(B ,rgbw), dot(D ,rgbw), dot(H ,rgbw), dot(F ,rgbw));
    vec4 c  = vec4(dot(C ,rgbw), dot(A ,rgbw), dot(G ,rgbw), dot(I ,rgbw));
    vec4 d  = b.yzwx;
    vec4 e  = vec4(dot(E,rgbw));
    vec4 f  = b.wxyz;
    vec4 g  = c.zwxy;
    vec4 h  = b.zwxy;
    vec4 i  = c.wxyz;

	vec4 i4, i5, h5, f4;

	float y_weight = XBR_Y_WEIGHT;

	if (small_details < 0.5)
	{
		i4 = vec4(dot(I4,rgbw), dot(C1,rgbw), dot(A0,rgbw), dot(G5,rgbw));
		i5 = vec4(dot(I5,rgbw), dot(C4,rgbw), dot(A1,rgbw), dot(G0,rgbw));
		h5 = vec4(dot(H5,rgbw), dot(F4,rgbw), dot(B1,rgbw), dot(D0,rgbw));
	}
	else
	{
		i4 = vec4( dot(I4, y_weight*Y), dot(C1, y_weight*Y), dot(A0, y_weight*Y), dot(G5, y_weight*Y) );
		i5 = vec4( dot(I5, y_weight*Y), dot(C4, y_weight*Y), dot(A1, y_weight*Y), dot(G0, y_weight*Y) );
		h5 = vec4( dot(H5, y_weight*Y), dot(F4, y_weight*Y), dot(B1, y_weight*Y), dot(D0, y_weight*Y) );
	}
    f4 = h5.yzwx;


    fx   = (Ao*fp.y+Bo*fp.x);
    fx_l = (Ax*fp.y+Bx*fp.x);
    fx_u = (Ay*fp.y+By*fp.x);

    irlv1 = irlv0 = diff(e,f) * diff(e,h);

#ifdef CORNER_B
    irlv1      = (irlv0 * ( neq(f,b) * neq(h,d) + eq(e,i) * neq(f,i4) * neq(h,i5) + eq(e,g) + eq(e,c) ) );
#endif
#ifdef CORNER_D
    vec4 c1 = i4.yzwx;
    vec4 g0 = i5.wxyz;
    irlv1     = (irlv0  *  ( neq(f,b) * neq(h,d) + eq(e,i) * neq(f,i4) * neq(h,i5) + eq(e,g) + eq(e,c) ) * (diff(f,f4) * diff(f,i) + diff(h,h5) * diff(h,i) + diff(h,g) + diff(f,c) + eq(b,c1) * eq(d,g0)));
#endif
#ifdef CORNER_C
    irlv1     = (irlv0  * ( neq(f,b) * neq(f,c) + neq(h,d) * neq(h,g) + eq(e,i) * (neq(f,f4) * neq(f,i4) + neq(h,h5) * neq(h,i5)) + eq(e,g) + eq(e,c)) );
#endif

    irlv2l = diff(e,g) * diff(d,g);
    irlv2u = diff(e,c) * diff(b,c);

    vec4 fx45i = clamp((fx   + delta   -Co - Ci)/(2.0*delta  ), 0.0, 1.0);
    vec4 fx45  = clamp((fx   + delta   -Co     )/(2.0*delta  ), 0.0, 1.0);
    vec4 fx30  = clamp((fx_l + delta_l -Cx     )/(2.0*delta_l), 0.0, 1.0);
    vec4 fx60  = clamp((fx_u + delta_u -Cy     )/(2.0*delta_u), 0.0, 1.0);

    vec4 wd1, wd2;
	if (small_details < 0.5)
	{
		wd1 = wd( e, c,  g, i, h5, f4, h, f);
		wd2 = wd( h, d, i5, f, i4,  b, e, i);
	}
	else
	{
		wd1 = weighted_distance( e, c, g, i, f4, h5, h, f, b, d, i4, i5);
		wd2 = weighted_distance( h, d, i5, f, b, i4, e, i, g, h5, c, f4);
	}

    edri  = step(wd1, wd2) * irlv0;
    edr   = step(wd1 + vec4(0.1, 0.1, 0.1, 0.1), wd2) * step(vec4(0.5, 0.5, 0.5, 0.5), irlv1);
    edr_l = step( lv2_cf*df(f,g), df(h,c) ) * irlv2l * edr;
    edr_u = step( lv2_cf*df(h,c), df(f,g) ) * irlv2u * edr;

    fx45  = edr   * fx45;
    fx30  = edr_l * fx30;
    fx60  = edr_u * fx60;
    fx45i = edri  * fx45i;

    px = step(df(e,f), df(e,h));

#ifdef SMOOTH_TIPS
    vec4 maximos = max(max(fx30, fx60), max(fx45, fx45i));
#endif
#ifndef SMOOTH_TIPS
    vec4 maximos = max(max(fx30, fx60), fx45);
#endif

    vec3 res1 = E;
    res1 = mix(res1, mix(H, F, px.x), maximos.x);
    res1 = mix(res1, mix(B, D, px.z), maximos.z);

    vec3 res2 = E;
    res2 = mix(res2, mix(F, B, px.y), maximos.y);
    res2 = mix(res2, mix(D, H, px.w), maximos.w);

    vec3 res = mix(res1, res2, step(c_df(E, res1), c_df(E, res2)));

    FragColor.xyz = res;
}
#endif
"""


def shader_preset_a(scale):
    return """shaders = 3

shader0 = "2xsal.glsl"
filter_linear0 = false
scale_type0 = source
scale0 = """ + scale + """

shader1 = "dotmask.glsl"
filter_linear1 = true
scale_type1 = viewport
scale_type_x1 = viewport
scale_type_y1 = source
scale1 = 1.0

shader2 = "4xsoft.glsl"
filter_linear2 = false
scale_type2 = source
scale2 = 1

parameters = "DOTMASK_STRENGTH;maskDark;maskLight;shadowMask"
DOTMASK_STRENGTH = 0.3
maskDark = 0.6
maskLight = 1.3
shadowMask = 1.0
"""


def shader_preset_b(scale):
    return """shaders = 4

shader0 = "xbr-lv2.glsl"
filter_linear0 = false
scale_type0 = source
scale0 = """ + scale + """

shader1 = "dotmask.glsl"
filter_linear1 = true
scale_type1 = viewport
scale1 = 1.0

shader2 = "4xsoft.glsl"
filter_linear2 = false
scale_type2 = source
scale2 = 1

shader3 = "2xsal.glsl"
filter_linear3 = false
scale_type3 = source
scale3 = 1

parameters = "maskDark; maskLight"
maskDark = 0.6
maskLight = 1.2
"""


def shader_preset_xbr_only(scale):
    return """shaders = 1

shader0 = "xbr-lv2.glsl"
filter_linear0 = false
scale_type0 = source
scale0 = """ + scale + """

parameters = "XBR_Y_WEIGHT;XBR_EQ_THRESHOLD;XBR_LV1_COEFFICIENT;XBR_LV2_COEFFICIENT;small_details"
XBR_Y_WEIGHT = 48.0
XBR_EQ_THRESHOLD = 15.0
XBR_LV1_COEFFICIENT = 0.5
XBR_LV2_COEFFICIENT = 2.0
small_details = 0.0
"""


SHADER_RES_A = [("2xsal.glsl", SHADER_2XSAL), ("dotmask.glsl", SHADER_DOTMASK), ("4xsoft.glsl", SHADER_4XSOFT)]
SHADER_RES_B = [("xbr-lv2.glsl", SHADER_XBR_LV2), ("dotmask.glsl", SHADER_DOTMASK), ("4xsoft.glsl", SHADER_4XSOFT), ("2xsal.glsl", SHADER_2XSAL)]
SHADER_RES_XBR = [("xbr-lv2.glsl", SHADER_XBR_LV2)]
SHADER_ENTRIES = [
    ("2xsal dotmask 4xsoft", shader_preset_a("1"), SHADER_RES_A),
    ("2xsal dotmask 4xsoft lv1.5", shader_preset_a("1.5"), SHADER_RES_A),
    ("2xsal dotmask 4xsoft lv2", shader_preset_a("2"), SHADER_RES_A),
    ("xbr dotmask 4xsoft 2xsal lv1", shader_preset_b("1"), SHADER_RES_B),
    ("xbr dotmask 4xsoft 2xsal lv1.5", shader_preset_b("1.5"), SHADER_RES_B),
    ("xbr dotmask 4xsoft 2xsal lv2", shader_preset_b("2"), SHADER_RES_B),
    ("xbr", shader_preset_xbr_only("2"), SHADER_RES_XBR),
]


SHADER_OLD_NAMES = [
    "2xsal-dotmask-4xsoft.glslp",
    "2xsal-dotmask-4xsoft-lv1.5.glslp",
    "2xsal-dotmask-4xsoft-lv2.glslp",
    "xbr-dotmask-4xsoft-2xsal-lv1.glslp",
    "xbr-dotmask-4xsoft-2xsal-lv1.5.glslp",
    "xbr-dotmask-4xsoft-2xsal-lv2.glslp",
]


def shader_entry_block(name, preset, resources):
    import base64
    p = preset.replace('"', '\\"').replace("\n", "\\n")
    block = '    "' + name + '": {\n'
    block += '        "shader": {\n'
    block += '            "type": "text",\n'
    block += '            "value": "' + p + '",\n'
    block += '        },\n'
    block += '        "resources": [\n'
    for rname, src in resources:
        block += '            {\n'
        block += '                "name": "' + rname + '",\n'
        block += '                "type": "base64",\n'
        block += '                "value": "' + base64.b64encode(src.encode("utf-8")).decode("ascii") + '",\n'
        block += '            },\n'
    block += '        ],\n'
    block += '    },\n'
    return block


def patch_shaders(path):
    import re
    text = open(path, encoding="utf-8").read()
    anchor = "export const EJS_SHADERS = {\n"
    if anchor not in text:
        print("LOI: khong tim thay EJS_SHADERS — ban goc doi shaders.js roi", file=sys.stderr)
        return 2
    changed = []
    for old in SHADER_OLD_NAMES:
        pat = re.compile(r'    "' + re.escape(old) + r'": \{[\s\S]*?\n    \},\n')
        found = pat.search(text)
        if found:
            text = text[:found.start()] + text[found.end():]
            changed.append(old + " (da go ten cu)")
    missing_blocks = []
    for name, preset, resources in SHADER_ENTRIES:
        block = shader_entry_block(name, preset, resources)
        pat = re.compile(r'    "' + re.escape(name) + r'": \{[\s\S]*?\n    \},\n')
        found = pat.search(text)
        if found:
            if found.group(0) != block:
                text = text[:found.start()] + block + text[found.end():]
                changed.append(name + " (cap nhat)")
        else:
            missing_blocks.append(block)
            changed.append(name)
    if missing_blocks:
        text = text.replace(anchor, anchor + "".join(missing_blocks), 1)
    if not changed:
        print("Shader: ca " + str(len(SHADER_ENTRIES)) + " shader da co roi, bo qua")
        return 0
    open(path, "w", encoding="utf-8").write(text)
    print("DA DOI: Shader: " + ", ".join(changed))
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
    if "shaders" in _b:
        sys.exit(patch_shaders(_p))
    sys.exit(main(_p))
