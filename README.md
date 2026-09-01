# CC:Tweaked UI Editor

A visual desktop editor for designing text-mode interfaces for **CC:Tweaked** computers, turtles, pocket computers and external monitors.

The editor lets you draw a UI on a character grid and exports compact Lua that can be pasted directly into CC:Tweaked.

## Features

- Visual CC:Tweaked character-grid editor.
- Screen presets for computers, turtles and pocket computers.
- External monitor editor with physical monitor size in Minecraft blocks.
- Monitor text scale from `0.5` to `5.0`.
- Monitor character dimensions calculated from the same geometry used by CC:Tweaked.
- Custom terminal dimensions up to `200 x 100` characters.
- Brush, text, line, rectangle, ellipse, fill, solid-cell, eraser and eyedropper tools.
- Filled or outlined shapes.
- Selection tool with copy, cut, paste and delete.
- Full CC:Tweaked 16-color palette.
- Separate text and background colors with quick swap.
- Undo and redo history.
- Editable live Lua preview.
- Safe Lua-to-canvas parser for supported terminal and `paintutils` drawing commands.
- Project save/load using `.ccui.json`.
- Compact Lua export using `term.blit()` and, where appropriate, `paintutils`.
- English and Russian application UI.

## Supported screen types

Open **New** and select the target screen.

### Computer

Default grid:

```text
51 x 19
```

### Turtle

Grid:

```text
39 x 13
```

### Pocket computer / tablet

Grid:

```text
26 x 20
```

### External monitor

For external monitors you configure:

- width in blocks;
- height in blocks;
- CC:Tweaked text scale.

The editor automatically calculates the resulting character grid. The calculation matches CC:Tweaked's `ServerMonitor` sizing logic.

The generated Lua finds the first attached monitor using:

```lua
peripheral.find("monitor")
```

and applies the selected text scale before drawing.

The finished version also prevents monitor projects from exporting optimized `paintutils` shapes to the computer terminal by mistake. External-monitor export uses explicit drawing through the selected monitor.

### Custom terminal

Allows manual width and height values up to the editor limit of `200 x 100` characters.

## Drawing tools

- **Brush** - draw the selected character and colors.
- **Text** - insert a text string.
- **Line** - draw a straight line.
- **Rectangle** - draw filled or outlined rectangles.
- **Ellipse** - draw filled or outlined ellipses.
- **Fill** - flood-fill an area.
- **Solid cell** - fill a cell with the selected background color using a space character.
- **Eraser** - restore cells to the canvas background.
- **Eyedropper** - pick character and color information from the canvas.
- **Select** - select an area for clipboard operations.

Selection shortcuts:

```text
Ctrl+C   Copy
Ctrl+X   Cut
Ctrl+V   Paste
Delete   Delete selection
```

## Lua export

For ordinary terminal targets the exporter compares two representations and keeps the shorter one:

1. rows rendered with `term.blit()`;
2. solid background regions rendered with `paintutils.drawFilledBox()` plus `term.blit()` for visible text.

External-monitor targets use monitor-safe export so all generated output is directed to the selected monitor.

Use **Copy Lua** to copy the generated program to the clipboard, or **Export .lua** to save it to a file.

## Live Lua preview

The generated Lua panel is editable. Supported drawing commands are parsed back into the canvas without executing arbitrary Lua code.

Supported commands include:

- `setBackgroundColor`
- `setTextColor`
- `clear`
- `clearLine`
- `setCursorPos`
- `write`
- `blit`
- `paintutils.drawPixel`
- `paintutils.drawLine`
- `paintutils.drawBox`
- `paintutils.drawFilledBox`

## Project files

Projects are stored as `.ccui.json` files.

The project format stores:

- canvas width and height;
- cell characters and colors;
- default foreground/background colors;
- selected target device profile;
- external-monitor block dimensions and text scale when applicable.

This means reopening a monitor project restores the same physical monitor configuration.

## Running from source

The finished entry point is:

```text
cc_terminal_ui_editor_fixed.pyw
```

It loads the original editor core and applies the completed device/monitor fixes before starting the application.

Recommended requirements:

- Python 3.11 or newer;
- Tkinter, included with the standard Windows Python installer.

Run it with:

```powershell
pythonw cc_terminal_ui_editor_fixed.pyw
```

or:

```powershell
python cc_terminal_ui_editor_fixed.pyw
```

## Building the Windows executable

Install PyInstaller:

```powershell
pip install pyinstaller
```

Then run:

```powershell
pyinstaller --clean --noconfirm CC_Terminal_UI_Editor.spec
```

The included spec builds the finished launcher and bundles the original editor core automatically.

Expected output:

```text
dist/CC_Terminal_UI_Editor.exe
```

## Repository layout

```text
cc_terminal_ui_editor.pyw          Original editor core
cc_terminal_ui_editor_fixed.pyw    Finished entry point with device fixes
CC_Terminal_UI_Editor.spec         PyInstaller build configuration
README.md                          Project documentation
```

## Notes on the monitor fix

The unfinished version already contained the correct monitor character-grid formula, but two integration issues remained:

1. switching to **External monitor** did not immediately recalculate the canvas, so a stale terminal size could be accepted;
2. optimized `paintutils` export could draw against `term.current()` instead of the external monitor.

The finished launcher fixes both cases while preserving the rest of the editor behavior.

## License

No license has been specified for this repository yet.
