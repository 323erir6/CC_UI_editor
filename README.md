# CC:Tweaked UI Editor

A visual desktop editor for designing text-mode interfaces for **CC:Tweaked** computers, turtles, pocket computers and external monitors.

The editor lets you draw a UI on a character grid and exports compact Lua that can be pasted directly into a CC:Tweaked computer.

## Features

- Visual CC:Tweaked character-grid editor.
- Presets for:
  - Computer terminal: `51 x 19` characters.
  - Turtle terminal: `39 x 13` characters.
  - Pocket computer / tablet: `26 x 20` characters.
  - External monitor with configurable physical width and height in blocks.
  - Custom terminal dimensions.
- External monitor text scale from `0.5` to `5.0`.
- Monitor character dimensions are calculated from the same geometry used by CC:Tweaked.
- Brush, text, line, rectangle, ellipse, fill, solid-cell, eraser and eyedropper tools.
- Filled or outlined shapes.
- Selection tool with copy, cut, paste and delete.
- Full CC:Tweaked 16-color palette.
- Separate text and background colors with quick swap.
- Undo and redo history.
- Editable live Lua preview.
- Lua-to-canvas preview for supported terminal and `paintutils` drawing commands.
- Project save/load using `.ccui.json`.
- Lua export using compact `term.blit()` rows or `paintutils.drawFilledBox()` where that is smaller.
- English and Russian application UI.

## Screen types

Choose **New** and select the target screen.

### Computer

Creates a `51 x 19` character canvas and exports code for the current terminal.

### Turtle

Creates a `39 x 13` character canvas for a turtle terminal.

### Pocket computer / tablet

Creates a `26 x 20` character canvas for a pocket computer.

### External monitor

Enter the physical monitor size in Minecraft blocks and choose the CC:Tweaked text scale. The editor automatically calculates the resulting character grid.

The exported Lua finds the first connected monitor with:

```lua
peripheral.find("monitor")
```

It then applies the selected text scale before drawing. `paintutils` output is redirected to that monitor as well, so optimized shape exports are drawn on the correct device.

### Custom terminal

Allows any canvas up to the editor limit of `200 x 100` characters.

## Drawing tools

- **Brush** - draw the selected character and colors.
- **Text** - insert a text string.
- **Rectangle** - draw filled or outlined rectangles.
- **Line** - draw straight lines.
- **Ellipse** - draw filled or outlined ellipses.
- **Select** - select an area and copy/cut/paste/delete it.
- **Fill** - flood-fill an area.
- **Solid cell** - fill a cell with the selected background color using a space character.
- **Eraser** - restore cells to the canvas background.
- **Eyedropper** - pick colors/characters from the canvas.

Selection shortcuts:

- `Ctrl+C` - copy.
- `Ctrl+X` - cut.
- `Ctrl+V` - paste.
- `Delete` - delete selection.

## Lua export

The exporter generates two representations and keeps the shorter one:

1. Character rows using `term.blit()`.
2. Solid background regions using `paintutils.drawFilledBox()` plus `term.blit()` for visible text.

For external monitors the generated program automatically selects the monitor and applies its configured text scale.

Use **Copy Lua** to copy the generated program, or **Export .lua** to save it as a file.

## Live Lua preview

The Lua panel can be edited directly. Supported drawing commands are parsed back into the canvas without executing arbitrary Lua code.

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

## Running from source

Requirements:

- Python 3.11 or newer recommended.
- Tkinter (included with the standard Windows Python installer).

Run:

```powershell
pythonw cc_terminal_ui_editor.pyw
```

or:

```powershell
python cc_terminal_ui_editor.pyw
```

## Windows executable

A prebuilt Windows executable is stored at:

```text
dist/CC_Terminal_UI_Editor.exe
```

No Python installation is required to run the `.exe`.

## Building the executable

Install PyInstaller:

```powershell
pip install pyinstaller
```

Then build with the included spec file:

```powershell
pyinstaller --clean --noconfirm CC_Terminal_UI_Editor.spec
```

The executable will be written to `dist/CC_Terminal_UI_Editor.exe`.

## Project files

`.ccui.json` files store the canvas, colors and target device profile. External-monitor projects also store the physical block dimensions and selected text scale, so reopening a project restores the same monitor configuration.

## License

No license has been specified for this repository yet.
