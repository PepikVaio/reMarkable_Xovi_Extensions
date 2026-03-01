# Font Support for Multiple Languages

This directory contains fonts required for non-Latin language support on reMarkable.

## Available Fonts

### Simplified Chinese (zh_CN)
- **NotoSansSC-Regular.ttf** - Noto Sans Simplified Chinese

## Installation

```bash
# On your reMarkable device
# Replace zh_CN with your language code if using other fonts
mount -o remount,rw /
mkdir -p /home/root/.local/share/fonts /usr/share/fonts/ttf/noto
cp zh_CN/NotoSansSC-Regular.ttf /home/root/.local/share/fonts/
cp zh_CN/NotoSansSC-Regular.ttf /usr/share/fonts/ttf/noto/
fc-cache -f
systemctl restart xochitl
```

## Note

Without this font, Chinese characters will not display correctly even if the translation is installed.

## Why Two Directories?

The font is installed to both locations for maximum compatibility:

1. **User directory** (`/home/root/.local/share/fonts/`)
   - Recommended by reMarkable official documentation
   - **Limitation**: Becomes inaccessible when device password is enabled
   - Survives system updates

2. **System directory** (`/usr/share/fonts/ttf/noto/`)
   - Works even when device password is enabled
   - **Limitation**: Will be cleared after system updates (requires reinstallation)

By installing to both directories, the font will work in most scenarios. After a system update, you may need to reinstall the font to the system directory.
