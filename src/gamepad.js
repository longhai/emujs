class GamepadHandler {
    constructor() {
        this.buttonLabels = {
            0: 'BUTTON_1',
            1: 'BUTTON_2',
            2: 'BUTTON_3',
            3: 'BUTTON_4',
            4: 'LEFT_TOP_SHOULDER',
            5: 'RIGHT_TOP_SHOULDER',
            6: 'LEFT_BOTTOM_SHOULDER',
            7: 'RIGHT_BOTTOM_SHOULDER',
            8: 'SELECT',
            9: 'START',
            10: 'LEFT_STICK',
            11: 'RIGHT_STICK',
            12: 'DPAD_UP',
            13: 'DPAD_DOWN',
            14: 'DPAD_LEFT',
            15: 'DPAD_RIGHT',
        };
        this.gamepads = [];
        this.listeners = {};
        this.timeout = setTimeout(this.loop.bind(this), 0);
    }
    terminate() {
        window.clearTimeout(this.timeout);
    }
    getGamepads() {
        return navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
    }
    loop() {
        this.updateGamepadState();
        this.timeout = setTimeout(this.loop.bind(this), 10);
    }
    updateGamepadState() {
        let gamepads = Array.from(this.getGamepads());
        if (!gamepads) return;
        if (!Array.isArray(gamepads) && gamepads.length) {
            let gp = [];
            for (let i=0; i<gamepads.length; i++) {
                gp.push(gamepads[i]);
            }
            gamepads = gp;
        } else if (!Array.isArray(gamepads)) return;

        gamepads.forEach((gamepad, index) => {
            if (!gamepad) return;
            let hasGamepad = false;
            this.gamepads.forEach((oldGamepad, oldIndex) => {
                if (oldGamepad.index !== gamepad.index) return;
                const gamepadToSave = {
                    axes: [],
                    buttons: {},
                    index: oldGamepad.index,
                    id: oldGamepad.id
                }
                hasGamepad = true;

                oldGamepad.axes.forEach((axis, axisIndex) => {
                    const val = (axis < 0.01 && axis > -0.01) ? 0 : axis;
                    const newVal = (gamepad.axes[axisIndex] < 0.01 && gamepad.axes[axisIndex] > -0.01) ? 0 : gamepad.axes[axisIndex];
                    if (newVal !== val) {
                        let axis = ['LEFT_STICK_X', 'LEFT_STICK_Y', 'RIGHT_STICK_X', 'RIGHT_STICK_Y'][axisIndex];
                        if (!axis) {
                            axis = "EXTRA_STICK_" + axisIndex;
                        }
                        this.dispatchEvent('axischanged', {
                            axis: axis,
                            value: newVal,
                            oldValue: val,
                            index: gamepad.index,
                            label: this.getAxisLabel(axis, newVal),
                            gamepadIndex: gamepad.index,
                        });
                    }
                    gamepadToSave.axes[axisIndex] = newVal;
                })

                gamepad.buttons.forEach((button, buttonIndex) => {
                    let pressed = oldGamepad.buttons[buttonIndex] === 1.0;
                    if (typeof oldGamepad.buttons[buttonIndex] === "object") {
                        pressed = oldGamepad.buttons[buttonIndex].pressed;
                    }
                    let pressed2 = button === 1.0;
                    if (typeof button === "object") {
                        pressed2 = button.pressed;
                    }
                    gamepadToSave.buttons[buttonIndex] = {pressed:pressed2};
                    if (pressed !== pressed2) {
                        if (pressed2) {
                            this.dispatchEvent('buttondown', {index: buttonIndex, label: this.getButtonLabel(buttonIndex), gamepadIndex: gamepad.index});
                        } else {
                            this.dispatchEvent('buttonup', {index: buttonIndex, label:this.getButtonLabel(buttonIndex), gamepadIndex: gamepad.index});
                        }
                    }

                })
                this.gamepads[oldIndex] = gamepadToSave;
            })
            if (!hasGamepad) {
                this.gamepads.push(gamepads[index]);
                this.gamepads.sort((a, b) => {
                    if (a == null && b == null) return 0;
                    if (a == null) return 1;
                    if (b == null) return -1;
                    return a.index - b.index;
                });
                this.dispatchEvent('connected', {gamepadIndex: gamepad.index});
            }
        });

        for (let j=0; j<this.gamepads.length; j++) {
            if (!this.gamepads[j]) continue;
            let has = false;
            for (let i=0; i<gamepads.length; i++) {
                if (!gamepads[i]) continue;
                if (this.gamepads[j].index === gamepads[i].index) {
                    has = true;
                    break;
                }
            }
            if (!has) {
                this.dispatchEvent('disconnected', {gamepadIndex: this.gamepads[j].index});
                this.gamepads.splice(j, 1);
                j--;
            }
        }
    }
    dispatchEvent(name, arg) {
        if (typeof this.listeners[name] !== 'function') return;
        if (!arg) arg={};
        arg.type = name;
        this.listeners[name](arg);
    }
    on(name, cb) {
        this.listeners[name.toLowerCase()] = cb;
    }


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

    getButtonLabel(index) {
        if (index === null || index === undefined) {
            return null;
        }
        if (this.buttonLabels[index] === undefined) {
            return `GAMEPAD_${index}`;
        }
        return this.buttonLabels[index];
    }
    getAxisLabel(axis, value) {
        let valueLabel = null;
        if (value > 0.5 || value < -0.5) {
            if (value > 0) {
                valueLabel = '+1';
            } else {
                valueLabel = '-1';
            }
        }
        if (!axis || !valueLabel) {
            return null;
        }
        return `${axis}:${valueLabel}`;
    }
}

export { GamepadHandler };
