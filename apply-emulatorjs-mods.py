
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
                { "type": "button", "text": "AB", "id": "ab", "location": "right", "left": -70, "top": -90, "bold": true, "fontSize": 15, "block": true, "input_value": 0, "combo": [0, 8] },
                { "type": "button", "text": "XY", "id": "cd", "location": "right", "left": -20, "top": -90, "bold": true, "fontSize": 15, "block": true, "input_value": 1, "combo": [1, 9] },
                { "type": "button", "text": "ABX", "id": "abc", "location": "right", "left": 30, "top": -90, "bold": true, "fontSize": 14, "block": true, "input_value": 0, "combo": [0, 8, 1] },
                { "type": "button", "text": "BXY", "id": "bcd", "location": "right", "left": 80, "top": -90, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": [8, 1, 9] }
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
        // HAI: can doi loai — them D-pad loai con lai de doi qua lai trong menu chinh sua.
        // Game thung dung vung tron (zone, nipplejs) -> them chu thap (dpad). NES dung chu
        // thap -> them vung tron. Chi 1 trong 2 hien tuy theo lua chon (luu localStorage),
        // cai con lai an (display:none) nen khong nhan cham. id khac nhau (dpadx/dpadz)
        // de khoi dung id "dpad" goc; menu doi loai se bat/tat theo id nay.
        if (["arcade", "mame", "fbneo"].includes(this.ejs.getControlScheme())) {
            info.push(
                { "type": "dpad", "id": "dpadx", "location": "left", "left": "50%", "top": "50%", "joystickInput": false, "inputValues": [4, 5, 6, 7] }
            );
        } else if ("nes" === this.ejs.getControlScheme()) {
            info.push(
                { "type": "zone", "id": "dpadz", "location": "left", "left": "50%", "top": "50%", "joystickInput": false, "inputValues": [4, 5, 6, 7] }
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
        // HAI: chinh vi tri + do mo cum nut v12 — nhan giu chon nut/cum, nut icon nho + truot dung gon + nut Tat rieng, truot doi co ca cum (khung to theo), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu + contextmenu + mousemove + rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut + chu trang, truot D-pad doi co cum (hien dung co thuc), menu tab co bieu tuong (✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu), chon hinh dang nut (Tron/Vuong/Chu nhat + thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut ket hop an mac dinh (lay ra o tab Ket hop); nut chuc nang giu mac dinh; turbo dung chung cai dat), keo cum giu ti le phong to, man hinh sach luc choi (khong nut noi), thanh truot khong nen den
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
        const _gpGetSetting = (id) => { try { const _v = this.ejs.getSettingValue(id); if (_v) return _v; } catch (e) {} try { if (this.settings && this.settings[id]) return this.settings[id]; } catch (e) {} try { if (this.ejs && this.ejs.allSettings && this.ejs.allSettings[id]) return this.ejs.allSettings[id]; } catch (e) {} return null; };
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
        const _gpHiddenKeyFor = (o) => "ejs-gamepad-hidden-" + _gpScheme + "-" + o;
        let _gpHidden = _gpLoad(_gpHiddenKeyFor(_gpCurOrient), "ejs-gamepad-hidden-" + _gpScheme);
        const _gpComboIds = ["ab", "cd", "abc", "bcd"];
        const _gpDefaultHiddenIds = () => {
            // Nut ket hop (AB/XY/ABX/BXY) an mac dinh o moi he; khi nao muon
            // them thi vao Cai dat (tab Ket hop) lay ra. Turbo (TA/TB/TAB)
            // da bo, dung chung qua Cai dat (Autofire) nen khong con trong
            // danh sach an mac dinh nua.
            if (_gpScheme === "nes") return ["ab", "cd", "abc", "bcd"];
            if (["arcade", "mame", "fbneo"].includes(_gpScheme)) return ["ab", "cd", "abc", "bcd"];
            return [];
        };
        try { if (!localStorage.getItem(_gpHiddenKeyFor(_gpCurOrient))) _gpDefaultHiddenIds().forEach((id) => { _gpHidden[id] = true; }); } catch (e) {}
        const _gpBtnEl = (id) => (this.virtualGamepad ? this.virtualGamepad.querySelector(".b_" + id) : null);
        const _gpApplyHidden = () => {
            if (!this.virtualGamepad) return;
            this.virtualGamepad.querySelectorAll(".ejs_virtualGamepad_button").forEach((_b) => {
                const _id = _gpBtnId(_b);
                if (!_id) return;
                _b.style.display = _gpHidden[_id] ? "none" : "";
            });
            const _dp = this.virtualGamepad.querySelector(".b_dpad");
            if (_dp) _dp.style.display = _gpHidden["dpad"] ? "none" : "";
        };
        const _gpDpadTypeKeyFor = (o) => "ejs-gamepad-dpadtype-" + _gpScheme + "-" + o;
        const _gpNativeDpadType = (["arcade", "mame", "fbneo"].includes(_gpScheme)) ? "zone" : "dpad";
        let _gpDpadType = _gpNativeDpadType;
        try { const _sv = localStorage.getItem(_gpDpadTypeKeyFor(_gpCurOrient)) || localStorage.getItem("ejs-gamepad-dpadtype-" + _gpScheme); if (_sv === "dpad" || _sv === "zone") _gpDpadType = _sv; } catch (e) {}
        const _gpDpadTypeOf = (id) => {
            if (id === "dpadx") return "dpad";
            if (id === "dpadz") return "zone";
            return _gpNativeDpadType;
        };
        const _gpApplyDpadType = () => {
            if (!this.virtualGamepad) return;
            ["dpad", "dpadx", "dpadz"].forEach((id) => {
                const _el = this.virtualGamepad.querySelector(".b_" + id);
                if (!_el) return;
                _el.style.display = (_gpDpadTypeOf(id) === _gpDpadType && !_gpHidden["dpad"]) ? "" : "none";
            });
        };
        const _gpSetDpadType = (ty) => {
            _gpDpadType = ty;
            try { localStorage.setItem(_gpDpadTypeKeyFor(_gpCurOrient), ty); } catch (e) {}
            _gpApplyDpadType();
        };
        // Hinh dang nut: dang (tron/vuong/chu nhat) + do bo goc (0-50%).
        // Tron = vuong + bo 50%; chu nhat rong gap 1,6 lan cao. Luu theo he + xoay man hinh.
        // Khong chon nut thi doi tat ca nut (xoa dang rieng cua tung nut); dang chon 1 nut
        // (bam giu vao nut) thi chi doi dang nut do. Doc ca gia tri cu v25 ("round"/"square"/"rounded").
        const _gpShapeKeyFor = (o) => "ejs-gamepad-shape-" + _gpScheme + "-" + o;
        const _gpBtnShapeKeyFor = (o) => "ejs-gamepad-btnshape-" + _gpScheme + "-" + o;
        const _gpShapeFrom = (v) => {
            if (v && typeof v === "object" && (v.form === "circle" || v.form === "square" || v.form === "rect")) return {form: v.form, round: (typeof v.round === "number" ? Math.max(0, Math.min(50, v.round)) : 50)};
            if (v === "square") return {form: "square", round: 0};
            if (v === "rounded") return {form: "square", round: 20};
            return {form: "circle", round: 50};
        };
        let _gpBtnShape = {form: "circle", round: 50};
        try {
            const _sv = localStorage.getItem(_gpShapeKeyFor(_gpCurOrient)) || localStorage.getItem("ejs-gamepad-shape-" + _gpScheme);
            if (_sv) { let _parsed = null; try { _parsed = JSON.parse(_sv); } catch (e) { _parsed = null; } _gpBtnShape = _gpShapeFrom(_parsed !== null ? _parsed : _sv); }
        } catch (e) {}
        let _gpBtnShapeMap = {};
        try {
            const _mv = localStorage.getItem(_gpBtnShapeKeyFor(_gpCurOrient)) || localStorage.getItem("ejs-gamepad-btnshape-" + _gpScheme);
            if (_mv) { const _o = JSON.parse(_mv); if (_o && typeof _o === "object") _gpBtnShapeMap = _o; }
        } catch (e) {}
        // Nut combo mac dinh hinh chu nhat nhu nut goc (khi chua tung doi hinh dang).
        // Chi ap dung khi chua co hinh dang nao duoc luu; khi nguoi choi doi hinh dang
        // (toan cuc hay rieng nut) thi nut combo doi theo nhu nut thuong.
        let _gpHasSavedShape = false;
        try { _gpHasSavedShape = !!(localStorage.getItem(_gpShapeKeyFor(_gpCurOrient)) || localStorage.getItem("ejs-gamepad-shape-" + _gpScheme) || localStorage.getItem(_gpBtnShapeKeyFor(_gpCurOrient)) || localStorage.getItem("ejs-gamepad-btnshape-" + _gpScheme)); } catch (e) {}
        const _gpSaveShape = () => { try { localStorage.setItem(_gpShapeKeyFor(_gpCurOrient), JSON.stringify(_gpBtnShape)); } catch (e) {} };
        const _gpSaveBtnShapeMap = () => { try { localStorage.setItem(_gpBtnShapeKeyFor(_gpCurOrient), JSON.stringify(_gpBtnShapeMap)); } catch (e) {} };
        const _gpShapeOf = (id) => {
            if (_gpBtnShapeMap && _gpBtnShapeMap[id]) return _gpShapeFrom(_gpBtnShapeMap[id]);
            // Nut ket hop (AB/XY/ABX/BXY, Fast/Slow) lay giao dien giong bo nut
            // A/B/X/Y: cung hinh dang chung, mac dinh tron, doi duoc tron/vuong/
            // chu nhat nhu nut thuong.
            return _gpBtnShape;
        };
        const _gpApplyShapeTo = (_b, _s) => {
            // Moi nut (ca nut A/B/X/Y lan nut khoi combo AB/XY/ABX/BXY, Fast/Slow)
            // deu doi duoc tron/vuong/chu nhat nhu nhau, va nut khoi co cung co voi
            // nut A/B/X/Y (50px) thay vi 31px nhu goc.
            const _id = _gpBtnId(_b);
            const _isCombo = _id && _gpComboIds.indexOf(_id) >= 0;
            const _h = _isCombo ? 50 : (_b.offsetHeight || 56);
            if (_s.form === "rect") {
                _b.style.width = Math.round(_h * 1.6) + "px";
                _b.style.height = _h + "px";
            } else {
                _b.style.width = _h + "px";
                _b.style.height = _h + "px";
            }
            // Chu can giua doc + ngang nhu nut A/B/X/Y: line-height bang chieu
            // cao nut (nut khoi goc line-height 31px nen chu bi lech len tren
            // khi doi cao 50px).
            _b.style.lineHeight = _h + "px";
            _b.style.textAlign = "center";
            _b.style.borderRadius = (_s.form === "circle") ? "50%" : (_s.round + "%");
        };
        const _gpApplyShape = () => {
            if (!this.virtualGamepad) return;
            // Chi ap hinh dang cho nut game (mat/combo/turbo/D-pad); nut chuc
            // nang (−/▶/▶▶/½×...) giu nguyen mac dinh cua EmulatorJS.
            const _gameIds = ["a", "b", "x", "y", "dpad", "dpadx", "dpadz"].concat(_gpComboIds);
            this.virtualGamepad.querySelectorAll(".ejs_virtualGamepad_button").forEach((_b) => {
                const _id = _gpBtnId(_b);
                if (_id && _gameIds.indexOf(_id) < 0) return;
                _gpApplyShapeTo(_b, _gpShapeOf(_id));
            });
        };
        const _gpSetShape = (form, round) => {
            const _apply = (_cur) => {
                let _f = (form !== undefined && form !== null) ? form : _cur.form;
                let _r = (typeof round === "number") ? round : _cur.round;
                if ((form === undefined || form === null) && _cur.form === "circle" && typeof round === "number" && round < 50) _f = "square";
                if (_f === "circle") _r = 50;
                return {form: _f, round: _r};
            };
            if (_gpSelId) {
                _gpBtnShapeMap[_gpSelId] = _apply(_gpShapeOf(_gpSelId));
                _gpSaveBtnShapeMap();
            } else {
                _gpBtnShape = _apply(_gpBtnShape);
                _gpSaveShape();
                _gpBtnShapeMap = {};
                _gpSaveBtnShapeMap();
            }
            _gpHasSavedShape = true;
            _gpApplyShape();
        };
        // Xep nut cum phai thanh luoi ngang (man hinh ngang): 3 hang x 3 cot.
        // Hang tren: (trong) ABX BXY; hang giua: XY X Y; hang duoi: AB A B.
        // ABX thang cot voi X, A; BXY thang cot voi Y, B. Luu theo huong hien tai.
        const _gpArrangeRows = () => {
            const _right = _gpClusters["right"];
            if (!_right) return;
            const _grid = [["", "abc", "bcd"], ["cd", "x", "y"], ["ab", "a", "b"]];
            const _cell = 60;
            const _items = [];
            let _minX = 1e9, _minY = 1e9, _maxX = -1e9, _maxY = -1e9, _maxR = -1e9;
            _grid.forEach((_row) => _row.forEach((_id) => {
                if (!_id) return;
                const _el = _gpBtnEl(_id);
                if (!_el || _el.style.display === "none") return;
                const _r = _el.getBoundingClientRect();
                const _cr = _right.getBoundingClientRect();
                const _cx = _r.left - _cr.left + _r.width / 2;
                const _cy = _r.top - _cr.top + _r.height / 2;
                _items.push({id: _id, el: _el, cx: _cx, cy: _cy});
                _minX = Math.min(_minX, _cx); _maxX = Math.max(_maxX, _cx);
                _minY = Math.min(_minY, _cy); _maxY = Math.max(_maxY, _cy);
                _maxR = Math.max(_maxR, _cx + _r.width / 2);
            }));
            if (!_items.length) return;
            const _ccy = (_minY + _maxY) / 2;
            const _gw = 3 * _cell, _gh = 3 * _cell;
            // Neo mep phai luoi vao mep phai nut dang co (khong can giua) de cot trai
            // (XY, AB) khong bi man hinh game che mat.
            const _ox = Math.max(0, _maxR - _gw), _oy = _ccy - _gh / 2;
            _grid.forEach((_row, _ri) => {
                _row.forEach((_id, _ci) => {
                    if (!_id) return;
                    const _it = _items.find((_q) => _q.id === _id);
                    if (!_it) return;
                    const _el = _it.el;
                    const _tcx = _ox + _ci * _cell + _cell / 2;
                    const _tcy = _oy + _ri * _cell + _cell / 2;
                    const _w = _el.offsetWidth || 50, _h = _el.offsetHeight || 50;
                    const _tx = _tcx - _w / 2, _ty = _tcy - _h / 2;
                    let _ox0 = _el.offsetLeft, _oy0 = _el.offsetTop;
                    if (_el.offsetParent !== _right) {
                        const _r = _el.getBoundingClientRect();
                        const _cr = _right.getBoundingClientRect();
                        const _cur = _gpBtnPos[_id] || {x: 0, y: 0};
                        _ox0 = (_r.left - _cr.left) - _cur.x;
                        _oy0 = (_r.top - _cr.top) - _cur.y;
                    }
                    const _old = _gpBtnPos[_id] || {x: 0, y: 0, s: 1};
                    _gpBtnPos[_id] = {x: Math.round(_tx - _ox0), y: Math.round(_ty - _oy0), s: _old.s || 1};
                });
            });
            try { localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos)); } catch (e) {}
            _gpApplyAll();
        };
        const _gpApplyAll = () => {
            for (const _k in _gpClusters) {
                const _el = _gpClusters[_k];
                const _p = _gpPos[_k];
                const _cs = (_p && _p.s) || 1;
                _el.style.transform = (_p && (typeof _p.x === "number" || typeof _p.y === "number" || typeof _p.s === "number")) ? "translate(" + ((_p.x) || 0) + "px," + ((_p.y) || 0) + "px)" + (_cs !== 1 ? " scale(" + _cs + ")" : "") : "";
                const _btns = _el.querySelectorAll(".ejs_virtualGamepad_button");
                for (const _b of _btns) {
                    const _id = _gpBtnId(_b);
                    _gpBtnTransform(_b, _id ? _gpBtnPos[_id] : null);
                }
                const _dm = _el.querySelector(".ejs_dpad_main");
                if (_dm && _dm.parentElement) {
                    const _dp = _dm.parentElement;
                    _dp.style.position = "absolute";
                    _dp.style.left = "0";
                    _dp.style.top = "0";
                    _dp.style.right = "auto";
                    _dp.style.width = "100%";
                    _dp.style.height = "100%";
                    _gpBtnTransform(_dp, _gpBtnPos["dpad"] || null);
                }
            }
            _gpApplyHidden();
            _gpApplyDpadType();
            _gpApplyShape();
        };
        _gpApplyAll();
        const _gpMiniStyle = document.createElement("style");
        _gpMiniStyle.textContent = "._gpMiniRange{accent-color:#3482ff;}._gpMiniRange::-webkit-slider-thumb{width:24px;height:24px;border-radius:50%;background:#3482ff;border:2px solid #fff;box-shadow:0 1px 5px rgba(0,0,0,.5);}._gpEditMenuBar{scrollbar-width:none;}._gpEditMenuBar::-webkit-scrollbar{display:none;}";
        document.head.appendChild(_gpMiniStyle);
        const _gpMiniBar = document.createElement("div");
        _gpMiniBar.style.cssText = "position:fixed;z-index:10000;display:none;gap:6px;";
        const _gpMkMini = (txt, bg) => {
            const _b = document.createElement("button");
            _b.textContent = txt;
            _b.style.cssText = "padding:7px 11px;border-radius:999px;border:0;background:" + bg + ";color:#fff;font-size:15px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.4);white-space:nowrap;";
            return _b;
        };
        const _gpMiniDone = _gpMkMini("✓", "rgba(52,130,255,.95)");
        const _gpMiniReset = _gpMkMini("↺", "rgba(90,90,90,.92)");
        _gpMiniBar.appendChild(_gpMiniDone);
        _gpMiniBar.appendChild(_gpMiniReset);
        this.elements.parent.appendChild(_gpMiniBar);
        // Dong bo khi che do chinh sua doi: chan chuot phai + hien/an thanh menu.
        // Khong co nut noi luc choi (man hinh sach); vao che do chinh sua bang menu game
        // (☰) → Virtual Gamepad → "Chỉnh vị trí nút"; thoat bang nut ✕ ben phai thanh menu.
        const _gpSyncOffBtn = () => { _gpSyncRightClick(); try { _gpSyncEditMenu(); } catch (err) {} };
        const _gpSyncRightClick = () => { try { if (!this.ejs.config.buttonOpts) this.ejs.config.buttonOpts = {}; this.ejs.config.buttonOpts.rightClick = (_gpGetSetting("virtual-gamepad-edit-layout") === "enabled") ? false : true; } catch (err) {} };
        const _gpMiniSlider = document.createElement("div");
        _gpMiniSlider.style.cssText = "position:fixed;z-index:10000;display:none;flex-direction:column;align-items:center;gap:6px;background:transparent;border-radius:12px;padding:6px 3px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.8);";
        const _gpMiniRange = document.createElement("input");
        _gpMiniRange.type = "range";
        _gpMiniRange.min = "0.5";
        _gpMiniRange.max = "2.5";
        _gpMiniRange.step = "0.05";
        _gpMiniRange.value = "1";
        _gpMiniRange.className = "_gpMiniRange";
        _gpMiniRange.style.cssText = "width:20px;height:100px;writing-mode:vertical-lr;direction:rtl;";
        const _gpMiniPct = document.createElement("span");
        _gpMiniPct.style.cssText = "font-size:11px;font-weight:700;min-width:26px;text-align:center;";
        _gpMiniPct.textContent = "100%";
        _gpMiniSlider.appendChild(_gpMiniRange);
        _gpMiniSlider.appendChild(_gpMiniPct);
        this.elements.parent.appendChild(_gpMiniSlider);
        const _gpEditMenu = document.createElement("div");
        _gpEditMenu.style.cssText = "position:fixed;top:8px;left:50%;transform:translateX(-50%);z-index:10002;display:none;max-width:96vw;background:rgba(0,0,0,.85);border-radius:12px;padding:6px 8px;box-shadow:0 2px 12px rgba(0,0,0,.5);flex-direction:column;gap:6px;";
        this.elements.parent.appendChild(_gpEditMenu);
        const _gpChip = (label, on, onClick) => {
            const _c = document.createElement("button");
            _c.textContent = label;
            _c.style.cssText = "padding:5px 11px;border-radius:999px;border:0;font-size:12px;font-weight:700;white-space:nowrap;flex:0 0 auto;background:" + (on ? "#3482ff" : "#2a2a2a") + ";color:" + (on ? "#fff" : "#bbb") + ";";
            _c.addEventListener("click", () => { onClick(); _gpBuildEditMenu(); });
            return _c;
        };
        let _gpMenuTab = "combo";
        const _gpTabBtn = (key, label) => {
            const _b = document.createElement("button");
            _b.textContent = label;
            const _on = _gpMenuTab === key;
            _b.style.cssText = "padding:5px 12px;border-radius:999px;border:0;font-size:12px;font-weight:700;white-space:nowrap;flex:1;background:" + (_on ? "#3482ff" : "#2a2a2a") + ";color:" + (_on ? "#fff" : "#bbb") + ";";
            _b.addEventListener("click", () => { _gpMenuTab = key; _gpBuildEditMenu(); });
            return _b;
        };
        const _gpSaveHidden = () => { try { localStorage.setItem(_gpHiddenKeyFor(_gpCurOrient), JSON.stringify(_gpHidden)); } catch (e) {} };
        const _gpBuildEditMenu = () => {
            _gpEditMenu.innerHTML = "";
            _gpEditMenu.style.display = "flex";
            const _tabs = document.createElement("div");
            _tabs.style.cssText = "display:flex;gap:6px;align-items:center;";
            _tabs.appendChild(_gpTabBtn("stick", "✛ Cần"));
            _tabs.appendChild(_gpTabBtn("btn", "◉ Nút"));
            _tabs.appendChild(_gpTabBtn("combo", "⊕ Kết hợp"));
            _tabs.appendChild(_gpTabBtn("shape", "▣ Hình dạng"));
            const _exit = document.createElement("button");
            _exit.textContent = "✕";
            _exit.style.cssText = "padding:5px 11px;border-radius:999px;border:0;font-size:12px;font-weight:700;white-space:nowrap;flex:0 0 auto;background:rgba(200,60,60,.95);color:#fff;";
            _exit.addEventListener("click", () => {
                _gpSelect(null, null);
                try { this.changeSettingOption("virtual-gamepad-edit-layout", "disabled"); } catch (err) {}
                _gpSyncOffBtn();
            });
            _tabs.appendChild(_exit);
            _gpEditMenu.appendChild(_tabs);
            const _row = document.createElement("div");
            _row.classList.add("_gpEditMenuBar");
            _row.style.cssText = "display:flex;gap:6px;align-items:center;overflow-x:auto;";
            const _tog = (id, label) => {
                _row.appendChild(_gpChip(label, !_gpHidden[id], () => {
                    _gpHidden[id] = !_gpHidden[id];
                    _gpSaveHidden();
                    _gpApplyHidden();
                    _gpApplyDpadType();
                }));
            };
            if (_gpMenuTab === "combo") {
                _gpComboIds.forEach((id) => {
                    const _el = _gpBtnEl(id);
                    if (!_el) return;
                    _tog(id, _el.innerText || id.toUpperCase());
                });
            } else if (_gpMenuTab === "btn") {
                if (this.virtualGamepad) {
                    this.virtualGamepad.querySelectorAll(".ejs_virtualGamepad_button").forEach((_b) => {
                        const _id = _gpBtnId(_b);
                        if (!_id || _gpComboIds.includes(_id)) return;
                        _tog(_id, _b.innerText || _id.toUpperCase());
                    });
                }
            } else if (_gpMenuTab === "shape") {
                const _cur = _gpSelId ? _gpShapeOf(_gpSelId) : _gpBtnShape;
                const _scope = document.createElement("span");
                _scope.textContent = _gpSelId ? ("Nút " + String(_gpSelId).toUpperCase()) : "Tất cả nút";
                _scope.style.cssText = "font-size:12px;font-weight:700;color:#fff;white-space:nowrap;flex:0 0 auto;";
                _row.appendChild(_scope);
                _row.appendChild(_gpChip("● Tròn", _cur.form === "circle", () => { _gpSetShape("circle", 50); }));
                _row.appendChild(_gpChip("■ Vuông", _cur.form === "square", () => { _gpSetShape("square", 0); }));
                _row.appendChild(_gpChip("▬ Chữ nhật", _cur.form === "rect", () => { _gpSetShape("rect", 0); }));
                const _sl = document.createElement("input");
                _sl.type = "range";
                _sl.min = "0"; _sl.max = "50"; _sl.step = "1";
                _sl.value = String(_cur.round);
                _sl.className = "_gpMiniRange";
                _sl.style.cssText = "width:120px;flex:0 0 auto;";
                const _pct = document.createElement("span");
                _pct.textContent = "Bo góc " + _cur.round + "%";
                _pct.style.cssText = "font-size:12px;font-weight:700;color:#fff;white-space:nowrap;flex:0 0 auto;min-width:64px;";
                _sl.addEventListener("input", () => {
                    const _v = parseInt(_sl.value, 10) || 0;
                    _pct.textContent = "Bo góc " + _v + "%";
                    _gpSetShape(null, _v);
                });
                _row.appendChild(_sl);
                _row.appendChild(_pct);
            } else {
                if (this.virtualGamepad && this.virtualGamepad.querySelector(".b_dpad, .b_dpadx, .b_dpadz")) {
                    _tog("dpad", "Cần");
                }
                if (this.virtualGamepad && this.virtualGamepad.querySelector(".b_dpadx, .b_dpadz")) {
                    _row.appendChild(_gpChip("＋", _gpDpadType === "dpad", () => { _gpSetDpadType("dpad"); }));
                    _row.appendChild(_gpChip("◯", _gpDpadType === "zone", () => { _gpSetDpadType("zone"); }));
                }
            }
            _gpEditMenu.appendChild(_row);
        };
        const _gpSyncEditMenu = () => {
            try {
                const _on = _gpGetSetting("virtual-gamepad-edit-layout") === "enabled";
                _gpEditMenu.style.display = _on ? "flex" : "none";
                if (_on) _gpBuildEditMenu();
            } catch (err) {}
        };
        let _gpSel = null;
        let _gpSelId = null;
        const _gpPlaceBar = () => {
            if (!_gpSel) return;
            const _r = _gpSel.getBoundingClientRect();
            const _cx = _r.left + _r.width / 2;
            let _top = _r.top - 40;
            if (_top < 4) _top = _r.bottom + 6;
            _gpMiniBar.style.left = Math.max(4, Math.min(window.innerWidth - 4, _cx)) + "px";
            _gpMiniBar.style.top = _top + "px";
            _gpMiniBar.style.transform = "translateX(-50%)";
        };
        const _gpPlaceSlider = () => {
            if (!_gpSel) return;
            const _r = _gpSel.getBoundingClientRect();
            const _cy = _r.top + _r.height / 2;
            const _sw = _gpMiniSlider.offsetWidth || 32;
            const _sh = _gpMiniSlider.offsetHeight || 137;
            let _sx = _r.right + 8;
            if (_sx + _sw > window.innerWidth - 4) _sx = _r.left - _sw - 8;
            if (_sx < 4) _sx = 4;
            let _sy = _cy - _sh / 2;
            if (_sy < 4) _sy = 4;
            if (_sy + _sh > window.innerHeight - 4) _sy = window.innerHeight - _sh - 4;
            _gpMiniSlider.style.left = _sx + "px";
            _gpMiniSlider.style.top = _sy + "px";
            _gpMiniSlider.style.transform = "";
        };
        const _gpPlaceMini = () => { _gpPlaceBar(); if (_gpMiniSlider.style.display !== "none") _gpPlaceSlider(); };
        const _gpClusterBtnIds = (clusterEl) => {
            const _ids = [];
            if (!clusterEl || !clusterEl.querySelectorAll) return _ids;
            clusterEl.querySelectorAll(".ejs_virtualGamepad_button").forEach((_b) => { const _id = _gpBtnId(_b); if (_id) _ids.push(_id); });
            if (clusterEl.querySelector(".b_dpad")) _ids.push("dpad");
            return _ids;
        };
        const _gpDpadClusterKey = (el) => {
            if (!el) return null;
            let _n = el;
            while (_n) {
                for (const _k in _gpClusters) { if (_gpClusters[_k] === _n) return _k; }
                _n = _n.parentElement;
            }
            return Object.keys(_gpClusters).find((k) => _gpClusters[k].contains(el)) || null;
        };
        const _gpSelect = (el, id) => {
            _gpSyncOffBtn();
            if (_gpSel && _gpSel !== el) {
                _gpSel.style.outline = "";
                _gpSel.style.outlineOffset = "";
            }
            _gpSel = el;
            _gpSelId = id;
            if (!el || !id) {
                _gpMiniBar.style.display = "none";
                _gpMiniSlider.style.display = "none";
                return;
            }
            el.style.outline = "2px dashed rgba(255,255,255,.9)";
            el.style.outlineOffset = "2px";
            if (_gpClusters[id]) {
                const _cp = _gpPos[id] || {};
                const _s = _cp.s || 1;
                _gpMiniRange.value = String(_s);
                _gpMiniPct.textContent = Math.round(_s * 100) + "%";
                _gpMiniSlider.style.display = "flex";
            } else if (id === "dpad") {
                const _ck = _gpDpadClusterKey(el);
                const _cs = (_ck && _gpPos[_ck] && _gpPos[_ck].s) || 1;
                const _ds = (_gpBtnPos["dpad"] && _gpBtnPos["dpad"].s) || 1;
                const _s = _cs * _ds;
                _gpMiniRange.value = String(_s);
                _gpMiniPct.textContent = Math.round(_s * 100) + "%";
                _gpMiniSlider.style.display = "flex";
            } else {
                const _d = _gpBtnPos[id] || { x: 0, y: 0, s: 1 };
                const _s = _d.s || 1;
                _gpMiniRange.value = String(_s);
                _gpMiniPct.textContent = Math.round(_s * 100) + "%";
                _gpMiniSlider.style.display = "flex";
            }
            _gpMiniBar.style.display = "flex";
            _gpPlaceMini();
            try { if (navigator.vibrate) navigator.vibrate(15); } catch (e) {}
        };
        _gpMiniDone.addEventListener("click", () => { _gpSelect(null, null); });
        _gpMiniReset.addEventListener("click", () => {
            if (!_gpSel || !_gpSelId) return;
            try {
                if (_gpClusters[_gpSelId]) {
                    delete _gpPos[_gpSelId];
                    localStorage.setItem(_gpKeyFor(_gpCurOrient), JSON.stringify(_gpPos));
                    _gpClusterBtnIds(_gpSel).forEach((_cid) => { delete _gpBtnPos[_cid]; });
                    localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos));
                } else {
                    delete _gpBtnPos[_gpSelId];
                    localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos));
                    if (_gpSelId === "dpad") {
                        const _ck = _gpDpadClusterKey(_gpSel);
                        if (_ck) {
                            delete _gpPos[_ck];
                            localStorage.setItem(_gpKeyFor(_gpCurOrient), JSON.stringify(_gpPos));
                        }
                    }
                }
            } catch (err) {}
            _gpApplyAll();
            _gpSelect(_gpSel, _gpSelId);
        });
        _gpMiniRange.addEventListener("input", () => {
            if (!_gpSel || !_gpSelId) return;
            const _s = parseFloat(_gpMiniRange.value) || 1;
            _gpMiniPct.textContent = Math.round(_s * 100) + "%";
            if (_gpClusters[_gpSelId]) {
                const _cp = _gpPos[_gpSelId] || { x: 0, y: 0 };
                _cp.s = _s;
                _gpPos[_gpSelId] = _cp;
                _gpClusterBtnIds(_gpSel).forEach((_cid) => {
                    const _cd = _gpBtnPos[_cid] || { x: 0, y: 0, s: 1 };
                    _cd.s = 1;
                    _gpBtnPos[_cid] = _cd;
                });
                _gpApplyAll();
                try { localStorage.setItem(_gpKeyFor(_gpCurOrient), JSON.stringify(_gpPos)); } catch (err) {}
                try { localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos)); } catch (err) {}
                return;
            }
            if (_gpSelId === "dpad") {
                const _ck = _gpDpadClusterKey(_gpSel);
                if (_ck) {
                    const _cp = _gpPos[_ck] || { x: 0, y: 0 };
                    _cp.s = _s;
                    _gpPos[_ck] = _cp;
                    const _dd = _gpBtnPos["dpad"] || { x: 0, y: 0, s: 1 };
                    _dd.s = 1;
                    _gpBtnPos["dpad"] = _dd;
                    _gpApplyAll();
                    try { localStorage.setItem(_gpKeyFor(_gpCurOrient), JSON.stringify(_gpPos)); } catch (err) {}
                    try { localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos)); } catch (err) {}
                }
                return;
            }
            const _d = _gpBtnPos[_gpSelId] || { x: 0, y: 0, s: 1 };
            _d.s = _s;
            _gpBtnTransform(_gpSel, _d);
            _gpBtnPos[_gpSelId] = _d;
            try { localStorage.setItem(_gpBtnKeyFor(_gpCurOrient), JSON.stringify(_gpBtnPos)); } catch (err) {}
            _gpPlaceBar();
        });
        _gpMiniRange.addEventListener("change", () => { _gpPlaceMini(); });
        let _gpDrag = null;
        let _gpHoldTimer = null;
        const _gpClearHold = () => { if (_gpHoldTimer !== null) { clearTimeout(_gpHoldTimer); _gpHoldTimer = null; } };
        const _gpStart = (e) => {
            if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") { _gpSelect(null, null); return; }
            if (_gpDrag) return;
            e.preventDefault();
            e.stopPropagation();
            _gpApplyOpacity();
            _gpSyncOffBtn();
            _gpSyncRightClick();
            const _t = (e.touches && e.touches[0]) || e;
            const _btn = (e.target && e.target.closest) ? e.target.closest(".ejs_virtualGamepad_button") : null;
            const _dpad = (!_btn && e.target && e.target.closest) ? e.target.closest(".b_dpad, .b_dpadx, .b_dpadz") : null;
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
                const _clEl = e.currentTarget;
                _gpDrag = { el: _clEl, kind: "cluster", id: _ck, sx: _t.clientX, sy: _t.clientY, ox: _p.x || 0, oy: _p.y || 0, nx: null, ny: null, moved: false };
                _gpClearHold();
                _gpHoldTimer = setTimeout(() => { _gpHoldTimer = null; if (_gpDrag) _gpDrag.held = true; _gpSelect(_clEl, _ck); }, 1000);
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
                const _cp = _gpPos[_gpDrag.id] || {};
                const _cs = _cp.s || 1;
                _gpDrag.el.style.transform = "translate(" + _nx + "px," + _ny + "px)" + (_cs !== 1 ? " scale(" + _cs + ")" : "");
            }
            _gpDrag.nx = _nx; _gpDrag.ny = _ny;
            if (_gpSel) _gpPlaceMini();
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
                        const _oldP = _gpPos[_d.id] || { x: 0, y: 0 };
                        _gpPos[_d.id] = { x: Math.round(_d.nx), y: Math.round(_d.ny), s: _oldP.s || 1 };
                        localStorage.setItem(_gpKeyFor(_gpCurOrient), JSON.stringify(_gpPos));
                    }
                } catch (err) {}
            } else if (!_d.moved && _d.kind !== "btn" && !_d.held) {
                _gpSelect(null, null);
            }
            try { _gpApplyAll(); } catch (err) {}
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
        this.virtualGamepad.addEventListener("pointerdown", () => { _gpApplyOpacity(); _gpSyncOffBtn(); if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") _gpSelect(null, null); });
        window.addEventListener("click", (e) => {
            try {
                if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") return;
                if (this.isChild(this.elements.menu, e.target) || this.isChild(this.elements.menuToggle, e.target)) return;
                if (_gpMiniBar.contains(e.target) || _gpMiniSlider.contains(e.target) || _gpEditMenu.contains(e.target)) return;
                e.stopPropagation();
            } catch (_err) {}
        }, true);
        window.addEventListener("contextmenu", (e) => {
            try {
                if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") return;
                e.preventDefault();
                e.stopPropagation();
            } catch (_err) {}
        }, true);
        window.addEventListener("mousemove", (e) => {
            try {
                if (_gpGetSetting("virtual-gamepad-edit-layout") !== "enabled") return;
                e.stopPropagation();
            } catch (_err) {}
        }, true);
        // Tu dong xep luoi ngang 1 lan duy nhat khi vao man hinh ngang (arcade):
        // neu chua xep bao gio thi xep luoi 3x3 roi danh dau, lan sau khong xep lai
        // de khong de len cho chinh tay cua nguoi choi. Xep lai tay bang nut Xep ngang.
        const _gpMaybeAutoRows = () => {
            // Da bo luoi tu dong: nut ket hop an mac dinh, khong tu xep nua.
            return;
        };
        setTimeout(_gpApplyAll, 100);
        setTimeout(_gpSyncOffBtn, 100);
        setTimeout(_gpMaybeAutoRows, 300);
        window.addEventListener("resize", () => {
            const _o = _gpOrient();
            if (_o === _gpCurOrient) return;
            _gpCurOrient = _o;
            _gpPos = _gpLoad(_gpKeyFor(_o), "ejs-gamepad-layout-" + _gpScheme);
            _gpBtnPos = _gpLoad(_gpBtnKeyFor(_o), "ejs-gamepad-buttons-" + _gpScheme);
            // Bo cuc doc/ngang rieng nhau: nap lai ca hinh dang, nut an, loai can theo huong moi.
            _gpBtnShape = {form: "circle", round: 50};
            try {
                const _sv = localStorage.getItem(_gpShapeKeyFor(_o)) || localStorage.getItem("ejs-gamepad-shape-" + _gpScheme);
                if (_sv) { let _parsed = null; try { _parsed = JSON.parse(_sv); } catch (e) { _parsed = null; } _gpBtnShape = _gpShapeFrom(_parsed !== null ? _parsed : _sv); }
            } catch (e) {}
            _gpBtnShapeMap = {};
            try {
                const _mv = localStorage.getItem(_gpBtnShapeKeyFor(_o)) || localStorage.getItem("ejs-gamepad-btnshape-" + _gpScheme);
                if (_mv) { const _om = JSON.parse(_mv); if (_om && typeof _om === "object") _gpBtnShapeMap = _om; }
            } catch (e) {}
            try { _gpHasSavedShape = !!(localStorage.getItem(_gpShapeKeyFor(_o)) || localStorage.getItem("ejs-gamepad-shape-" + _gpScheme) || localStorage.getItem(_gpBtnShapeKeyFor(_o)) || localStorage.getItem("ejs-gamepad-btnshape-" + _gpScheme)); } catch (e) {}
            _gpHidden = _gpLoad(_gpHiddenKeyFor(_o), "ejs-gamepad-hidden-" + _gpScheme);
            try { if (!localStorage.getItem(_gpHiddenKeyFor(_o))) _gpDefaultHiddenIds().forEach((id) => { _gpHidden[id] = true; }); } catch (e) {}
            _gpDpadType = _gpNativeDpadType;
            try { const _sv = localStorage.getItem(_gpDpadTypeKeyFor(_o)) || localStorage.getItem("ejs-gamepad-dpadtype-" + _gpScheme); if (_sv === "dpad" || _sv === "zone") _gpDpadType = _sv; } catch (e) {}
            _gpSelect(null, null);
            _gpApplyAll();
            setTimeout(_gpMaybeAutoRows, 150);
        });
        } catch (_gpErr) {}
'''

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
        changed.append("PS1: da them L1/R1/L2/R2; NES: da them combo AB/XY/ABX/BXY")

    # Migration: khong dung nut TA/TB/TAB rieng nua (Hai 13/11) — moi he dung
    # chung turbo qua muc Cai dat (Autofire), chi giu combo AB/XY/ABX/BXY
    # (menu chinh nut dung chung cho tat ca). Xoa cac dong TA/TB/TAB khoi file
    # da patch: NES nhan biet bang "right": 5 / "right": 75 va TAB
    # "left": -70, "top": -45; arcade nhan biet bang "left": -70/-20/30,
    # "top": -90. Ca hai kieu input_value (0/8) deu xoa.
    import re as _re
    _turbo_pat = _re.compile(
        r'[ \t]*\{ "type": "button", "text": "T(?:A|B)", "id": "t[ab]", "location": "right", "right": (?:5|75), "top": 0, "bold": true, "input_value": [08], "autofire": true \},\n'
        r'|[ \t]*\{ "type": "button", "text": "TAB", "id": "tab", "location": "right", "left": -70, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": \[8, 0\], "autofire": true \},\n'
        r'|[ \t]*\{ "type": "button", "text": "T(?:A|B)", "id": "t[ab]", "location": "right", "left": (?:-70|-20), "top": -90, "bold": true, "fontSize": 14, "block": true, "input_value": [08], "autofire": true \},\n'
        r'|[ \t]*\{ "type": "button", "text": "TAB", "id": "tab", "location": "right", "left": 30, "top": -90, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": \[8, 0\], "autofire": true \},?\n'
    )
    _new_text, _n_removed = _turbo_pat.subn('', text)
    if _n_removed:
        text = _new_text
        changed.append("Turbo: da bo %d nut TA/TB/TAB rieng, moi he dung chung turbo qua Cai dat" % _n_removed)

    _nes_old = '''        if ("nes" === this.ejs.getControlScheme()) {
            info.push(
                { "type": "button", "text": "TA", "id": "ta", "location": "right", "right": 5, "top": 0, "bold": true, "input_value": 8, "autofire": true },
                { "type": "button", "text": "TB", "id": "tb", "location": "right", "right": 75, "top": 0, "bold": true, "input_value": 0, "autofire": true }
            );
        }'''
    _nes_new = '''        if ("nes" === this.ejs.getControlScheme()) {
            info.push(
                { "type": "button", "text": "AB", "id": "ab", "location": "right", "left": -70, "top": -90, "bold": true, "fontSize": 15, "block": true, "input_value": 0, "combo": [0, 8] },
                { "type": "button", "text": "XY", "id": "cd", "location": "right", "left": -20, "top": -90, "bold": true, "fontSize": 15, "block": true, "input_value": 1, "combo": [1, 9] },
                { "type": "button", "text": "ABX", "id": "abc", "location": "right", "left": 30, "top": -90, "bold": true, "fontSize": 14, "block": true, "input_value": 0, "combo": [0, 8, 1] },
                { "type": "button", "text": "BXY", "id": "bcd", "location": "right", "left": 80, "top": -90, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": [8, 1, 9] }
            );
        }'''
    _arc_old = '''                { "type": "button", "text": "BXY", "id": "bcd", "location": "right", "left": 80, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": [8, 1, 9] }
            );'''
    _arc_new = '''                { "type": "button", "text": "BXY", "id": "bcd", "location": "right", "left": 80, "top": -45, "bold": true, "fontSize": 14, "block": true, "input_value": 8, "combo": [8, 1, 9] }
            );'''
    if _nes_old in text and '"TAB"' not in text:
        text = text.replace(_nes_old, _nes_new, 1)
        changed.append("Nut them: migration NES cu -> them combo AB/XY/ABX/BXY (hang 2)")
    if _arc_old in text and text.count('"TAB"') < 2:
        text = text.replace(_arc_old, _arc_new, 1)
        changed.append("Nut them: migration arcade cu -> them combo AB/XY/ABX/BXY (hang 2)")

    _dpad_alt = "        // HAI: can doi loai — them D-pad loai con lai de doi qua lai trong menu chinh sua.\n        // Game thung dung vung tron (zone, nipplejs) -> them chu thap (dpad). NES dung chu\n        // thap -> them vung tron. Chi 1 trong 2 hien tuy theo lua chon (luu localStorage),\n        // cai con lai an (display:none) nen khong nhan cham. id khac nhau (dpadx/dpadz)\n        // de khoi dung id \"dpad\" goc; menu doi loai se bat/tat theo id nay.\n        if ([\"arcade\", \"mame\", \"fbneo\"].includes(this.ejs.getControlScheme())) {\n            info.push(\n                { \"type\": \"dpad\", \"id\": \"dpadx\", \"location\": \"left\", \"left\": \"50%\", \"top\": \"50%\", \"joystickInput\": false, \"inputValues\": [4, 5, 6, 7] }\n            );\n        } else if (\"nes\" === this.ejs.getControlScheme()) {\n            info.push(\n                { \"type\": \"zone\", \"id\": \"dpadz\", \"location\": \"left\", \"left\": \"50%\", \"top\": \"50%\", \"joystickInput\": false, \"inputValues\": [4, 5, 6, 7] }\n            );\n        }"
    _arc_tab = "                { \"type\": \"button\", \"text\": \"TAB\", \"id\": \"tab\", \"location\": \"right\", \"left\": 30, \"top\": -90, \"bold\": true, \"fontSize\": 14, \"block\": true, \"input_value\": 8, \"combo\": [8, 0], \"autofire\": true }\n            );\n        }"
    if '"dpadx"' not in text and '"dpadz"' not in text and _arc_tab in text:
        text = text.replace(_arc_tab, _arc_tab + "\n" + _dpad_alt, 1)
        changed.append("Can doi loai: migration -> chen D-pad doi loai (dpadx/dpadz) sau khoi arcade")

    _xy_remove_lines = [
        '                { "type": "button", "text": "X", "id": "x", "location": "right", "right": 5, "top": -70, "bold": true, "input_value": 8, "autofire": true },\n',
        '                { "type": "button", "text": "X", "id": "x", "location": "right", "right": 5, "top": -70, "bold": true, "input_value": 8 },\n',
        '                { "type": "button", "text": "Y", "id": "y", "location": "right", "right": 75, "top": -70, "bold": true, "input_value": 0, "autofire": true },\n',
        '                { "type": "button", "text": "Y", "id": "y", "location": "right", "right": 75, "top": -70, "bold": true, "input_value": 0 },\n',
    ]
    _xy_removed = False
    for _xy_ln in _xy_remove_lines:
        if _xy_ln in text:
            text = text.replace(_xy_ln, "", 1)
            _xy_removed = True
    if _xy_removed:
        changed.append("Nut X/Y: da go nut X/Y tren man hinh khoi NES (v32, theo yeu cau)")

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

    # 10/11: cham man hinh khi dang choi vo tinh mo menu, bam nham trung "Chay lai"
    # lam game khoi dong lai. Code goc chi chan pointerType "touch" nhung click
    # tong hop sau khi nut tay cam chan touchstart co pointerType rong nen van
    # lot qua show(). Chi cho chuot that mo menu khi bam man hinh; cham thi mo
    # bang nut ☰ tren goc. Dao nguoc quyet dinh 07/11 (luc do giu cham-mo-menu).
    CLICK_MENU_OLD = '''            const clickListener = (e) => {
                if (e.pointerType === "touch") return;'''
    CLICK_MENU_NEW = '''            const clickListener = (e) => {
                // HAI: chi chuot moi mo menu khi bam man hinh — cham (touch) khong mo nua, mo bang nut ☰
                if (e.pointerType !== "mouse") return;'''
    if "HAI: chi chuot moi mo menu" in text:
        print("Menu cham man hinh: da tat roi, bo qua")
    elif CLICK_MENU_OLD not in text:
        print("LOI: khong tim thay clickListener mo menu — ban goc doi frontend.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(CLICK_MENU_OLD, CLICK_MENU_NEW, 1)
        changed.append("Menu: chi chuot moi mo menu khi bam man hinh (cham khong mo nua, mo bang nut ☰)")

    # 10/11 (tiep): ban v5 len live nhung cham man hinh van mo menu — con duong
    # thu hai: cham vao vung trong (khong phai nut tay cam) sinh su kien chuot
    # tuong thich (mousemove) ma mouseListener hieu la di chuot xuong/mep duoi
    # -> show(). Nut tay cam co preventDefault nen khong sinh su kien nay.
    # Chan bang sourceCapabilities.firesTouchEvents (Chrome): chi chuot that
    # moi duoc mo menu bang di chuot; chuot tong hop tu cham thi bo qua.
    MOUSE_MENU_OLD = '''            const mouseListener = (e) => {
                if (!this.ejs.started || ignoreEvents || document.pointerLockElement === this.canvas) return;'''
    MOUSE_MENU_NEW = '''            const mouseListener = (e) => {
                // HAI: chi chuot that moi mo menu khi di chuot — su kien chuot tong hop tu cham (touch) khong mo nua
                if (e.sourceCapabilities && e.sourceCapabilities.firesTouchEvents) return;
                if (!this.ejs.started || ignoreEvents || document.pointerLockElement === this.canvas) return;'''
    if "HAI: chi chuot that moi mo menu khi di chuot" in text:
        print("Menu di chuot: da tat roi, bo qua")
    elif MOUSE_MENU_OLD not in text:
        print("LOI: khong tim thay mouseListener mo menu — ban goc doi frontend.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(MOUSE_MENU_OLD, MOUSE_MENU_NEW, 1)
        changed.append("Menu: chi chuot that moi mo menu khi di chuot (cham khong mo nua, mo bang nut ☰)")

    # 10/11 (tiep): menu chinh da het hien khi cham, nhung con menu chuot phai
    # (Chup man hinh / Start Screen Recording / Luu nhanh / Nap nhanh) mo ra
    # khi GIU LAU (long-press) tren vung game — do la su kien contextmenu.
    # Chan bang pointerType "touch"; chuot phai that tren PC van mo duoc.
    CTX_MENU_OLD = '''        this.ejs.addEventListener(this.game, "contextmenu", (e) => {
            e.preventDefault();
            if ((this.ejs.config.buttonOpts && this.ejs.config.buttonOpts.rightClick === false) || !this.ejs.started || this.ejs.lightgunActive) return;'''
    CTX_MENU_NEW = '''        this.ejs.addEventListener(this.game, "contextmenu", (e) => {
            e.preventDefault();
            // HAI: giu lau (long-press) tren cam ung khong mo menu chuot phai — chi chuot phai that moi mo
            if (e.pointerType === "touch") return;
            if ((this.ejs.config.buttonOpts && this.ejs.config.buttonOpts.rightClick === false) || !this.ejs.started || this.ejs.lightgunActive) return;'''
    if "HAI: giu lau (long-press) tren cam ung khong mo menu chuot phai" in text:
        print("Menu chuot phai: da tat long-press roi, bo qua")
    elif CTX_MENU_OLD not in text:
        print("LOI: khong tim thay handler contextmenu — ban goc doi frontend.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(CTX_MENU_OLD, CTX_MENU_NEW, 1)
        changed.append("Menu chuot phai: giu lau tren cam ung khong mo nua (chi chuot phai that moi mo)")

    # 10/11 (tiep): menu Gian lan mo ra nhung khong co danh sach game/ma du file
    # nes.json da co tren web. Nguyen nhan: downloadFile tra ve cacheItem
    # (res.data la doi tuong cache, khong phai chuoi JSON) nhung fetchCheatJson
    # lai tra thang res.data ve — code sau do hieu cacheItem la kho cheat nen
    # danh sach game toan ten thuoc tinh (key, files, added...). Sua: giai ma
    # JSON tu files[0].bytes nhu cho doc bao cao (line 587 emulator.js) roi
    # tra ve chuoi de code san co JSON.parse tiep.
    CHEAT_FETCH_OLD = '''                        const fetchCheatJson = async (url) => {
                            const res = await this.ejs.downloadFile(url, "cheats", null, true, { responseType: "text", method: "GET" });
                            if (res === -1) return null;
                            return res.data;
                        };'''
    CHEAT_FETCH_NEW = '''                        const fetchCheatJson = async (url) => {
                            const res = await this.ejs.downloadFile(url, "cheats", null, true, { responseType: "text", method: "GET" });
                            if (res === -1) return null;
                            // HAI: downloadFile tra ve cacheItem — giai ma JSON tu files[0].bytes
                            const payload = res.data;
                            if (typeof payload === "string") return payload;
                            if (payload && Array.isArray(payload.files) && payload.files[0] && payload.files[0].bytes) {
                                return new TextDecoder().decode(payload.files[0].bytes);
                            }
                            if (payload && typeof payload === "object") return payload;
                            return null;
                        };'''
    if "HAI: downloadFile tra ve cacheItem" in text:
        print("Cheat fetch: da giai ma cacheItem roi, bo qua")
    elif CHEAT_FETCH_OLD not in text:
        print("LOI: khong tim thay fetchCheatJson — ban goc doi frontend.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(CHEAT_FETCH_OLD, CHEAT_FETCH_NEW, 1)
        changed.append("Cheat: fetchCheatJson giai ma dung JSON tu cacheItem (danh sach game hien dung)")

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
                        if ((info[i].autofire === true || (!info[i].combo && this.ejs.isAutofireEnabled(0, value))) && !isAnalog) { // HAI: nut turbo'''
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

    _old_combo_if = '                        if (!info[i].combo && (info[i].autofire === true || this.ejs.isAutofireEnabled(0, value)) && !isAnalog) { // HAI: nut turbo'
    _new_combo_if = '                        if ((info[i].autofire === true || (!info[i].combo && this.ejs.isAutofireEnabled(0, value))) && !isAnalog) { // HAI: nut turbo'
    _old_af = '                            this.ejs.startAutofire(0, value, downValue);'
    _new_af = '                            (info[i].combo || [value]).forEach((v) => this.ejs.startAutofire(0, v, downValue));'
    if _old_combo_if in text:
        text = text.replace(_old_combo_if, _new_combo_if, 1)
        changed.append("Turbo combo: dong if cu (chan combo autofire) -> cho combo+autofire")
    if 'HAI: nut combo' in text and _old_af in text and _new_af not in text:
        text = text.replace(_old_af, _new_af, 1)
        changed.append("Turbo combo: startAutofire ap dung cho ca combo (TAB)")

    if "HAI: nut X/Y gan chuc nang" in text:
        import re as _re32

        text = _re32.sub(r"                    // HAI: nut X/Y gan chuc nang[^\n]*\n", "", text, count=1)
        _xy_calc = '''                    let _gpVal = value;
                    let _gpAuto = (info[i].autofire === true);
                    let _gpCombo = info[i].combo;
                    if ((info[i].id === "x" || info[i].id === "y") && this.ejs.getControlScheme() === "nes") {
                        const _gpF = (this._gpBtnFunc && this._gpBtnFunc[info[i].id]) || null;
                        if (_gpF && typeof _gpF.input === "number") {
                            _gpVal = _gpF.input;
                            _gpAuto = !!_gpF.autofire;
                            _gpCombo = null;
                        }
                    }
                    const isAnalog = this.ejs.analogAxes.includes(_gpVal);'''
        _xy_calc_orig = '''                    const isAnalog = this.ejs.analogAxes.includes(value);'''
        if _xy_calc in text:
            text = text.replace(_xy_calc, _xy_calc_orig, 1)
        text = text.replace("(_gpCombo || [_gpVal])", "(info[i].combo || [value])")
        _xy_if_new = "if ((_gpAuto || (!_gpCombo && this.ejs.isAutofireEnabled(0, _gpVal))) && !isAnalog) { // HAI: nut turbo"
        _xy_if_old = "if ((info[i].autofire === true || (!info[i].combo && this.ejs.isAutofireEnabled(0, value))) && !isAnalog) { // HAI: nut turbo"
        if _xy_if_new in text:
            text = text.replace(_xy_if_new, _xy_if_old, 1)
        changed.append("Nut X/Y: da go touch handler XYFUNC, tra ve ban goc (v32)")
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

    if "cum nut v12" in text:
        print("Chinh cum nut: da co ban v12, bo qua")
    else:
        import re
        _gp_vers = [
            ("v12", r"        // HAI: chinh vi tri \+ do mo cum nut v12[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v11", r"        // HAI: chinh vi tri \+ do mo cum nut v11[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v10", r"        // HAI: chinh vi tri \+ do mo cum nut v10[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v9", r"        // HAI: chinh vi tri \+ do mo cum nut v9[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v8", r"        // HAI: chinh vi tri \+ do mo cum nut v8[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v7", r"        // HAI: chinh vi tri \+ do mo cum nut v7[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v6", r"        // HAI: chinh vi tri \+ do mo cum nut v6[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v5", r"        // HAI: chinh vi tri \+ do mo cum nut v5[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v4", r"        // HAI: chinh vi tri \+ do mo cum nut v4[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v3", r"        // HAI: chinh vi tri \+ do mo cum nut v3[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v2", r"        // HAI: chinh vi tri \+ do mo cum nut v2[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v1", r"        // HAI: chinh vi tri \+ do mo cum nut v1 — nhan giu chon nut/cum, nut icon nho \+ truot dung gon \+ nut Tat rieng, truot doi co ca cum \(khung to theo\), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu \+ contextmenu \+ mousemove \+ rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut \+ chu trang, truot D-pad doi co cum \(hien dung co thuc\), menu tab co bieu tuong \(✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu\), TAB turbo A\+B 40ms \(~12 phat/giay\), chon hinh dang nut \(Tron/Vuong/Chu nhat \+ thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut khoi combo/Fast/Slow giu chu nhat mac dinh chi doi bo goc\), keo cum giu ti le phong to, man hinh sach luc choi \(khong nut noi\), thanh truot khong nen den\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v32", r"        // HAI: chinh vi tri \+ do mo cum nut v32 — nhan giu chon nut/cum, nut icon nho \+ truot dung gon \+ nut Tat rieng, truot doi co ca cum \(khung to theo\), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu \+ contextmenu \+ mousemove \+ rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut \+ chu trang, truot D-pad doi co cum \(hien dung co thuc\), menu tab co bieu tuong \(✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu\), TAB turbo A\+B 40ms \(~12 phat/giay\), chon hinh dang nut \(Tron/Vuong/Chu nhat \+ thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut khoi combo/Fast/Slow giu chu nhat mac dinh chi doi bo goc\), keo cum giu ti le phong to, man hinh sach luc choi \(khong nut noi\), thanh truot khong nen den\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v31", r"        // HAI: chinh vi tri \+ do mo cum nut v31 — nhan giu chon nut/cum, nut icon nho \+ truot dung gon \+ nut Tat rieng, truot doi co ca cum \(khung to theo\), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu \+ contextmenu \+ mousemove \+ rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut \+ chu trang, truot D-pad doi co cum \(hien dung co thuc\), menu tab co bieu tuong \(✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu\), TAB turbo A\+B 40ms \(~12 phat/giay\), chon hinh dang nut \(Tron/Vuong/Chu nhat \+ thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut khoi combo/Fast/Slow giu chu nhat mac dinh chi doi bo goc\), keo cum giu ti le phong to, man hinh sach luc choi \(khong nut noi\), thanh truot khong nen den, nut X/Y NES gan chuc nang \(mac dinh A/B thuong, doi duoc A/B/Turbo/Len/Xuong/Trai/Phai/Start/Select, nhan luon X/Y\)\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v30", r"        // HAI: chinh vi tri \+ do mo cum nut v30 — nhan giu chon nut/cum, nut icon nho \+ truot dung gon \+ nut Tat rieng, truot doi co ca cum \(khung to theo\), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu \+ contextmenu \+ mousemove \+ rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut \+ chu trang, truot D-pad doi co cum \(hien dung co thuc\), menu tab co bieu tuong \(✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu\), TAB turbo A\+B 40ms \(~12 phat/giay\), chon hinh dang nut \(Tron/Vuong/Chu nhat \+ thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut khoi combo/Fast/Slow giu chu nhat mac dinh chi doi bo goc\), keo cum giu ti le phong to, man hinh sach luc choi \(khong nut noi\), thanh truot khong nen den, nut X/Y NES gan chuc nang \(mac dinh Turbo A/B, doi duoc A/B/Turbo/Len/Xuong/Trai/Phai/Start/Select, nhan luon X/Y\)\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v29", r"        // HAI: chinh vi tri \+ do mo cum nut v29 — nhan giu chon nut/cum, nut icon nho \+ truot dung gon \+ nut Tat rieng, truot doi co ca cum \(khung to theo\), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu \+ contextmenu \+ mousemove \+ rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut \+ chu trang, truot D-pad doi co cum \(hien dung co thuc\), menu tab co bieu tuong \(✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu\), TAB turbo A\+B 40ms \(~12 phat/giay\), chon hinh dang nut \(Tron/Vuong/Chu nhat \+ thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut khoi combo/Fast/Slow giu chu nhat mac dinh chi doi bo goc\), keo cum giu ti le phong to, man hinh sach luc choi \(khong nut noi\), thanh truot khong nen den, nut X/Y NES gan chuc nang \(mac dinh Turbo A/B, doi duoc A/B/Turbo/Len/Xuong/Trai/Phai/Start/Select\)\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
            ("v27", r"        // HAI: chinh vi tri \+ do mo cum nut v27 — nhan giu chon nut/cum, nut icon nho \+ truot dung gon \+ nut Tat rieng, truot doi co ca cum \(khung to theo\), Dat lai cum xoa het nut trong cum, Dat lai D-pad/cum ve mac dinh, xoa vien khi bo chon, chan menu \+ contextmenu \+ mousemove \+ rightClick khi dang chinh, hien duoc khi fullscreen, bam nut to mau cua nut \+ chu trang, truot D-pad doi co cum \(hien dung co thuc\), menu tab co bieu tuong \(✛ Can/◉ Nut/⊕ Ket hop/▣ Hinh dang, bam tab moi hien nut bo do, nut ✕ thoat ben phai thanh menu\), TAB turbo A\+B 40ms \(~12 phat/giay\), chon hinh dang nut \(Tron/Vuong/Chu nhat \+ thanh truot bo goc, ap tat ca hoac rieng nut dang chon; nut khoi combo/Fast/Slow giu chu nhat mac dinh chi doi bo goc\), keo cum giu ti le phong to, man hinh sach luc choi \(khong nut noi\), thanh truot khong nen den\n[\s\S]*?        \} catch \(_gpErr\) \{\}\n"),
        ]
        for _lbl, _pat in _gp_vers:
            _mm = re.compile(_pat).search(text)
            if _mm:
                text = text[:_mm.start()] + text[_mm.end():]
                print("Chinh cum nut: da go ban " + _lbl + ", chen ban v12")
                break
        if GP_LAYOUT_ANCHOR not in text:
            print("LOI: khong tim thay cho append 4 cum nut — ban goc doi setVirtualGamepad roi", file=sys.stderr)
            return 2
        text = text.replace(GP_LAYOUT_ANCHOR, GP_LAYOUT_ANCHOR + GP_LAYOUT_JS, 1)
        changed.append("Chinh cum nut: da them v12 (bo nut TA/TB/TAB rieng, turbo dung chung qua Cai dat; nut ket hop an mac dinh)")

    if "HAI: do mo cum nut" in text:
        print("Menu do mo: da co roi, bo qua")
    else:
        if GP_LAYOUT_MENU_ANCHOR not in text:
            print("LOI: khong tim thay menu Left Handed Mode — ban goc doi menu roi", file=sys.stderr)
            return 2
        text = text.replace(GP_LAYOUT_MENU_ANCHOR, GP_LAYOUT_MENU_ANCHOR + GP_LAYOUT_MENU, 1)
        changed.append("Menu: da them 'Chinh vi tri nut' + 'Do mo nut' vao muc Virtual Gamepad")

    _ctl_nes_old = '''        } else if ("nes" === this.ejs.getControlScheme()) {
            buttons = [
                { id: 8, label: this.localization("A") },
                { id: 0, label: this.localization("B") },
                { id: 2, label: this.localization("SELECT") },'''
    _ctl_nes_new = '''        } else if ("nes" === this.ejs.getControlScheme()) {
            buttons = [
                { id: 8, label: this.localization("A") },
                { id: 0, label: this.localization("B") },
                // HAI: NES X/Y bang dieu khien (Nestopia: X=Turbo A, Y=Turbo B; FCEUmm khong doc)
                { id: 9, label: this.localization("X") },
                { id: 1, label: this.localization("Y") },
                { id: 2, label: this.localization("SELECT") },'''
    if "HAI: NES X/Y bang dieu khien" in text:
        print("Bang dieu khien NES: da co X/Y roi, bo qua")
    elif _ctl_nes_old in text:
        text = text.replace(_ctl_nes_old, _ctl_nes_new, 1)
        changed.append("Bang dieu khien NES: da them hang X (id 9) / Y (id 1) — Nestopia doc X=Turbo A, Y=Turbo B")
    else:
        import re as _rexy
        _mxy = _rexy.search(r'\} else if \("nes" === this\.ejs\.getControlScheme\(\)\) \{\s*buttons = \[(.*?)\];', text, _rexy.S)
        if _mxy and "{ id: 9," in _mxy.group(1):
            print("Bang dieu khien NES: X/Y da co san (ban sua tay), bo qua")
        else:
            print("LOI: khong tim thay list NES trong createControlSettingMenu — ban goc doi roi", file=sys.stderr)
            return 2

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
.ejs_virtualGamepad_button.b_tab { color: #00bcd4 !important; }
'''

MD_COLOR_CSS = '''
/* HAI: nut md mau — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button.b_c { color: #ff9800 !important; }
.ejs_virtualGamepad_button.b_z { color: #ab47bc !important; }
'''

BUTTON_PRESS_CSS = '''
/* HAI: nut bam co mau — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_virtualGamepad_button_down.b_a, .ejs_virtualGamepad_button_down.b_ta { background: rgba(76,175,80,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_b, .ejs_virtualGamepad_button_down.b_tb { background: rgba(229,57,53,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_x { background: rgba(30,136,229,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_y { background: rgba(253,216,53,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_ab, .ejs_virtualGamepad_button_down.b_c { background: rgba(255,152,0,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_cd, .ejs_virtualGamepad_button_down.b_z { background: rgba(171,71,188,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_abc { background: rgba(236,64,122,.55) !important; color: #fff !important; }
.ejs_virtualGamepad_button_down.b_bcd { background: rgba(38,166,154,.55) !important; color: #fff !important; }
'''

VOLUME_CSS = '''
/* HAI: volume hien ro — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_volume_parent input[type='range'] { --value: 50%; }
.ejs_volume_parent input[type='range']::-webkit-slider-runnable-track { background-image: linear-gradient(to right, #1e88e5 var(--value, 50%), rgba(255,255,255,0.25) var(--value, 50%)) !important; }
.ejs_volume_parent input[type='range']::-webkit-slider-thumb { background: #fff !important; border: 1px solid #999 !important; }
.ejs_volume_parent input[type='range']::-moz-range-progress { background: #1e88e5 !important; }
'''

# 10/11: nut bat/tat cheat (nut gat) bi tran ra ngoai mep trai, chi thay vien
# nen kho biet da bat hay chua. Nguyen nhan goc: .ejs_cheat_row ghi
# padding-left: 2.25rem roi dong padding: .2em 0; (shorthand) ghi de mat
# padding-left ve 0, nen nut gat (label::before, left: -2.25rem) loi ra ngoai
# hang 36px — tren dien thoai 360px thi nut nam ngoai man hinh. Sua bang cach
# ghi lai padding day du de sau rule goc, cung do uu tien nen se thang.
CHEAT_TOGGLE_CSS = '''
/* HAI: sua nut bat/tat cheat bi tran ra ngoai — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_cheat_row { padding: .2em 0 .2em 2.25rem; }
'''

# 10/11 (tiep): Hai muon nut bat/tat cheat trong danh sach dung cung kieu
# chon tron nhu trong dropdown chon ma (Android: tron xanh co cham trang la
# dang chon, tron rong la chua chon) cho dong bo. Doi nut gat goc (thanh truot)
# thanh nut tron: ::before la vong tron, ::after la cham giua; bat thi vong
# xanh la (#22c55e) + cham trang, tat thi vong xam rong. Ghi de sau rule goc,
# cung do uu tien nen se thang; vi tri giu ben trai nhu cu (nut × van o phai).
CHEAT_RADIO_CSS = '''
/* HAI: nut bat/tat cheat dang tron giong chon trong dropdown — chen boi apply-emulatorjs-mods.py, chay lai khong them trung */
.ejs_cheat_row label::before { width: 1.15rem; height: 1.15rem; border-radius: 50%; border: 2px solid #adb5bd; background-color: transparent; }
.ejs_cheat_row input:checked+label::before { background-color: #22c55e; border-color: #22c55e; }
.ejs_cheat_row label::after { width: .55rem; height: .55rem; border-radius: 50%; background-color: transparent; left: calc(-2.25rem + .3rem); top: calc(0rem + .3rem); transform: none; transition: none; }
.ejs_cheat_row input:checked+label::after { background-color: #fff; transform: none; }
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
        # Migration: them mau chu cho nut TAB neu ban cu chua co; neu TAB dang
        # mau cam (v14) thi doi sang cyan cho khoi trung voi AB/Y.
        if ".b_tab" not in text:
            out = out.replace(".ejs_virtualGamepad_button.b_bcd { color: #26a69a !important; }", ".ejs_virtualGamepad_button.b_bcd { color: #26a69a !important; }\n.ejs_virtualGamepad_button.b_tab { color: #00bcd4 !important; }", 1)
            changed.append("Mau nut combo: da them mau chu cho nut TAB (cyan)")
        elif ".ejs_virtualGamepad_button.b_tab { color: #ff9800 !important; }" in text:
            out = out.replace(".ejs_virtualGamepad_button.b_tab { color: #ff9800 !important; }", ".ejs_virtualGamepad_button.b_tab { color: #00bcd4 !important; }", 1)
            changed.append("Mau nut combo: da doi mau chu nut TAB tu cam sang cyan (khoi trung AB/Y)")
    else:
        out += COMBO_COLOR_CSS
        changed.append("Mau nut combo: da chen mau chu AB/XY/ABX/BXY/TAB")
    if "HAI: nut md mau" in text:
        print("Mau nut MD: da co roi, bo qua")
    else:
        out += MD_COLOR_CSS
        changed.append("Mau nut MD: da chen mau chu C/Z")
    if "HAI: nut bam co mau" in text:
        print("Mau nut bam: da co roi, bo qua")
    else:
        out += BUTTON_PRESS_CSS
        changed.append("Mau nut bam: bam nut thi nen to mau cua nut, chu trang")
    if "HAI: volume hien ro" in text:
        print("Volume: da co roi, bo qua")
    else:
        out += VOLUME_CSS
        changed.append("Volume: da chen mau xanh + nut tron trang cho thanh truot volume")
    if "HAI: sua nut bat/tat cheat bi tran ra ngoai" in text:
        print("Cheat toggle: da sua roi, bo qua")
    else:
        out += CHEAT_TOGGLE_CSS
        changed.append("Cheat toggle: sua padding-left de nut bat/tat nam gon trong hang, nhin ro bat/tat")
    if "HAI: nut bat/tat cheat dang tron giong chon trong dropdown" in text:
        print("Cheat radio: da doi dang tron roi, bo qua")
    else:
        out += CHEAT_RADIO_CSS
        changed.append("Cheat radio: nut bat/tat dang tron xanh giong chon trong dropdown (bat: xanh co cham trang, tat: tron xam rong)")
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

BIOS_DONTEXTRACT_OLD = '            "bios": { "name": "BIOS", "dontCache": false, "dontExtractIfCore": ["arcade", "fbneo", "fbalpha2012_cps1", "fbalpha2012_cps2", "same_cdi", "mame", "mame2003_plus", "mame2003"] },\n'
BIOS_DONTEXTRACT_NEW = '            "bios": { "name": "BIOS", "dontCache": false, "dontExtractIfCore": [] }, // HAI: giai nen BIOS de lay du BIOS cac hang (fbneo/mame)\n'

# 10/11: file goc (parent) cua game thung: EmulatorJS mac dinh GIAI NEN parent
# thanh file le, nhung core fbneo/mame tim file goc theo dang file .zip con
# nguyen (giong nhu tim neogeo.zip cho BIOS) nen khong thay -> bao thieu file.
# Giu nguyen zip cho cac core thung, he khac van giai nen nhu cu.
PARENT_DONTEXTRACT_OLD = '            "parent": { "name": "Parent", "dontCache": false },\n'
PARENT_DONTEXTRACT_NEW = '            "parent": { "name": "Parent", "dontCache": false, "dontExtractIfCore": ["arcade", "fbneo", "fbalpha2012_cps1", "fbalpha2012_cps2", "same_cdi", "mame", "mame2003_plus", "mame2003"] }, // HAI: giu nguyen zip file goc cho game thung (fbneo/mame tim file goc dang .zip)\n'

GPAD_TURBO_MARKER = "HAI: tay cam X = Turbo A, Y = Turbo B (chi he NES)"
GPAD_TURBO_ANCHOR = "        if (this.frontend.isSettingsMenuOpen() || this.frontend.isPopupOpen()) return;\n"
GPAD_TURBO_NEW = """        // HAI: tay cam X = Turbo A, Y = Turbo B (chi he NES) — nut X/Y tren tay that
        // thua vi NES chi co A/B, gan X->turbo A (input 8), Y->turbo B (input 0).
        // Chi ap khi he NES de he khac (SNES/arcade) van dung X/Y nhu nut that cua no.
        // Toc do turbo dung chung cai dat trong Settings (getAutofireInterval),
        // khong dat rieng nua.
        if ((e.type === "buttondown" || e.type === "buttonup") && this.getControlScheme() === "nes") {
            const _gpTurboByIndex = { 2: 8, 3: 0 };
            const _gpTurboByLabel = { "BUTTON_3": 8, "BUTTON_4": 0 };
            const _gpTurboInput = _gpTurboByIndex[e.index] !== undefined ? _gpTurboByIndex[e.index] : _gpTurboByLabel[e.label];
            if (_gpTurboInput !== undefined) {
                if (e.type === "buttonup") {
                    this.stopAutofire(gamepadIndex, _gpTurboInput);
                } else {
                    if (!this.controls[gamepadIndex]) this.controls[gamepadIndex] = [];
                    if (!this.controls[gamepadIndex][_gpTurboInput]) this.controls[gamepadIndex][_gpTurboInput] = {};
                    this.startAutofire(gamepadIndex, _gpTurboInput, 1);
                }
                return;
            }
        }
"""

LOADER_MINIFIED_OLD = '''    if (debug) {
        EmulatorJS = await loadScript("emulator.js");
        await loadStyle("emulator.css");
    } else {
        EmulatorJS = await loadScript("emulator.min.js");
        await loadStyle("emulator.min.css");
    }'''

LOADER_MINIFIED_NEW = '''    // HAI: tai thang file thuong, bo qua file nen (repo khong co emulator.min.js/.css — thu la 404 roi moi roi ve file thuong)
    EmulatorJS = await loadScript("emulator.js");
    await loadStyle("emulator.css");'''

def patch_loader(path):
    text = open(path, encoding="utf-8").read()
    changed = []
    if "HAI: tai thang file thuong" in text:
        print("Loader (loader.js): da tai thang file thuong roi, bo qua")
    elif LOADER_MINIFIED_OLD not in text:
        print("LOI: khong tim thay khoi if/else tai file nen — ban goc doi loader.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(LOADER_MINIFIED_OLD, LOADER_MINIFIED_NEW, 1)
        changed.append("Loader: da bo duong tai file nen, tai thang emulator.js + emulator.css (loader.js)")
    if changed:
        open(path, "w", encoding="utf-8").write(text)
        for _c in changed:
            print("DA DOI: " + _c)
    return 0

def patch_emulator(path):
    text = open(path, encoding="utf-8").read()
    changed = []
    if "HAI: tat tu mo menu" in text:
        print("Menu tu mo (emulator.js): da tat roi, bo qua")
    elif MENU_OPEN_OLD not in text:
        print("LOI: khong tim thay dong frontend.menu.open() — ban goc doi emulator.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(MENU_OPEN_OLD, MENU_OPEN_NEW, 1)
        changed.append("Menu: da xoa dong menu.open() khi game bat dau (emulator.js)")

    if "HAI: giai nen BIOS" in text:
        print("BIOS (emulator.js): da giai nen roi, bo qua")
    elif BIOS_DONTEXTRACT_OLD not in text:
        print("LOI: khong tim thay dong bios dontExtractIfCore — ban goc doi emulator.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(BIOS_DONTEXTRACT_OLD, BIOS_DONTEXTRACT_NEW, 1)
        changed.append("BIOS: da cho giai nen BIOS cho fbneo/mame (emulator.js)")

    if "HAI: giu nguyen zip file goc" in text:
        print("Parent (emulator.js): da giu zip roi, bo qua")
    elif PARENT_DONTEXTRACT_OLD not in text:
        print("LOI: khong tim thay dong parent downloadType — ban goc doi emulator.js roi", file=sys.stderr)
        return 2
    else:
        text = text.replace(PARENT_DONTEXTRACT_OLD, PARENT_DONTEXTRACT_NEW, 1)
        changed.append("Parent: da giu nguyen zip file goc cho fbneo/mame (emulator.js)")

    if GPAD_TURBO_MARKER in text:
        if GPAD_TURBO_NEW in text:
            text = text.replace(GPAD_TURBO_NEW, "", 1)
            changed.append("Tay cam: da go X = Turbo A, Y = Turbo B (v32, theo yeu cau)")
        else:
            print("Tay cam X/Y turbo: co marker nhung khong tim thay khoi ma — bo qua", file=sys.stderr)
    else:
        print("Tay cam X/Y turbo (emulator.js): khong co, bo qua")
    if changed:
        open(path, "w", encoding="utf-8").write(text)
        for _c in changed:
            print("DA DOI: " + _c)
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
    if _b == "loader.js":
        sys.exit(patch_loader(_p))
    if "shaders" in _b:
        sys.exit(patch_shaders(_p))
    sys.exit(main(_p))
