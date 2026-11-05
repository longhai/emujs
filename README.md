# emujs

EmulatorJS tự host của Hải — đồng bộ có chọn lọc từ EmulatorJS gốc, giữ lại nút mod của mình.

## Cách hoạt động

- `.github/workflows/sync-emulatorjs.yml` — mỗi tuần (hoặc bấm tay) tải code gốc mới về, chỉ copy `loader.js`, `emulator.css`, `version.json`, `src/*.js`, `localization/` vào `vendor/emulatorjs-data/`, rồi mở PR để xem trước khi gộp. Không đụng tới file `.html` hay bố cục riêng của Hải.
- `apply-emulatorjs-mods.py` — sau khi tải code gốc về, tự động thêm lại nút mod, chỉ thêm nút thiếu, không viết lại bộ nút gốc:
  - PS1: thêm L1/R1/L2/R2
  - NES: thêm Turbo A / Turbo B
  - Tay cầm thật: tự nhận Sony / Xbox / Switch qua Gamepad API, đổi ký hiệu cho đúng (Sony `✕ ○ □ △`, Xbox `A B X Y`, Switch `B A Y X`)
- `.github/workflows/cleanup-old-files.yml` — dọn 1 lần duy nhất, xóa file EmulatorJS cũ (`data/`, `index.html`, `nes/`).

