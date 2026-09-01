"""Visual UI editor and compact Lua exporter for CC:Tweaked terminals."""

from __future__ import annotations

import ast
import json
import math
import os
import re
import tkinter as tk
from collections import deque
from tkinter import filedialog, messagebox, simpledialog, ttk


APP_NAME = "CC:Tweaked UI Editor"
PROJECT_EXTENSION = ".ccui.json"
CELL_WIDTH = 14
CELL_HEIGHT = 22
MAX_HISTORY = 60
MONITOR_TEXT_SCALES = tuple(step / 2 for step in range(1, 11))
DEVICE_SIZES = {
    "computer": (51, 19),
    "turtle": (39, 13),
    "pocket": (26, 20),
}

# Order is the hexadecimal order required by term.blit(): 0..f.
CC_COLORS = [
    ("white", "Білий", "#f0f0f0"),
    ("orange", "Помаранчевий", "#f2b233"),
    ("magenta", "Пурпуровий", "#e57fd8"),
    ("lightBlue", "Світло-блакитний", "#99b2f2"),
    ("yellow", "Жовтий", "#dede6c"),
    ("lime", "Лаймовий", "#7fcc19"),
    ("pink", "Рожевий", "#f2b2cc"),
    ("gray", "Сірий", "#4c4c4c"),
    ("lightGray", "Світло-сірий", "#999999"),
    ("cyan", "Бірюзовий", "#4c99b2"),
    ("purple", "Фіолетовий", "#b266e5"),
    ("blue", "Синій", "#3366cc"),
    ("brown", "Коричневий", "#7f664c"),
    ("green", "Зелений", "#57a64e"),
    ("red", "Червоний", "#cc4c4c"),
    ("black", "Чорний", "#111111"),
]

COLOR_NAMES = {
    "en": [
        "White", "Orange", "Magenta", "Light blue", "Yellow", "Lime", "Pink", "Gray",
        "Light gray", "Cyan", "Purple", "Blue", "Brown", "Green", "Red", "Black",
    ],
    "ru": [
        "\u0411\u0435\u043b\u044b\u0439", "\u041e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u0439", "\u041f\u0443\u0440\u043f\u0443\u0440\u043d\u044b\u0439", "\u0421\u0432\u0435\u0442\u043b\u043e-\u0433\u043e\u043b\u0443\u0431\u043e\u0439",
        "\u0416\u0435\u043b\u0442\u044b\u0439", "\u041b\u0430\u0439\u043c\u043e\u0432\u044b\u0439", "\u0420\u043e\u0437\u043e\u0432\u044b\u0439", "\u0421\u0435\u0440\u044b\u0439", "\u0421\u0432\u0435\u0442\u043b\u043e-\u0441\u0435\u0440\u044b\u0439",
        "\u0411\u0438\u0440\u044e\u0437\u043e\u0432\u044b\u0439", "\u0424\u0438\u043e\u043b\u0435\u0442\u043e\u0432\u044b\u0439", "\u0421\u0438\u043d\u0438\u0439", "\u041a\u043e\u0440\u0438\u0447\u043d\u0435\u0432\u044b\u0439", "\u0417\u0435\u043b\u0435\u043d\u044b\u0439", "\u041a\u0440\u0430\u0441\u043d\u044b\u0439", "\u0427\u0435\u0440\u043d\u044b\u0439",
    ],
}

TRANSLATIONS = {
    "en": {
        "subtitle": "Visual terminal interface designer",
        "new": "New",
        "open": "Open",
        "save": "Save",
        "undo": "Undo",
        "redo": "Redo",
        "clear": "Clear",
        "copy_lua": "Copy Lua",
        "export_lua": "Export .lua",
        "tools": "TOOLS",
        "tool_brush": "Brush",
        "tool_text": "Text",
        "tool_rectangle": "Rectangle",
        "tool_line": "Line",
        "tool_ellipse": "Ellipse",
        "tool_select": "Select",
        "tool_fill": "Fill",
        "tool_solid": "Solid cell",
        "tool_eraser": "Eraser",
        "tool_picker": "Eyedropper",
        "brush_options": "BRUSH & SHAPES",
        "character": "Character",
        "filled_rectangle": "Filled shapes",
        "solid_shapes": "Color-only shapes",
        "canvas_background": "Use BG as canvas background",
        "swap_colors": "Swap text / background",
        "selection_actions": "SELECTION",
        "copy_cells": "Copy",
        "cut_cells": "Cut",
        "paste_cells": "Paste",
        "delete_cells": "Delete",
        "no_selection": "Select an area first",
        "selection_copied": "Selected area copied",
        "selection_cut": "Selected area cut",
        "selection_pasted": "Area pasted",
        "selection_deleted": "Selected area deleted",
        "palette": "CC PALETTE",
        "change_text": "Text color",
        "change_background": "Background color",
        "canvas": "TERMINAL CANVAS",
        "generated_code": "GENERATED LUA",
        "copy": "Copy",
        "apply_code": "Apply code",
        "code_hint": "Editable live Lua: changes are applied to the canvas automatically. The exporter chooses compact term.blit() rows or paintutils shapes.",
        "code_applied": "Lua changes applied to the canvas",
        "code_error": "Lua preview error: {error}",
        "no_drawing_commands": "No supported drawing commands found",
        "ready": "Ready",
        "foreground_background": "Text: {fg}   |   Background: {bg}",
        "blit_stats": "{calls} draw calls | {chars} Lua characters",
        "position": "Column {x}  Row {y}   |   Tool: {tool}",
        "text_dialog_title": "Insert text",
        "text_dialog_prompt": "Text to place on the canvas:",
        "copied": "Lua code copied to clipboard",
        "export_title": "Export Lua",
        "exported": "Exported: {path}",
        "clear_title": "Clear canvas",
        "clear_prompt": "Remove everything from the canvas?",
        "unsaved_title": "Unsaved changes",
        "unsaved_prompt": "Save the current project before continuing?",
        "new_canvas": "New canvas",
        "new_width": "Terminal width:",
        "new_height": "Terminal height:",
        "device_type": "Screen type",
        "device_computer": "Computer",
        "device_turtle": "Turtle",
        "device_pocket": "Pocket computer / tablet",
        "device_monitor": "External monitor",
        "device_custom": "Custom terminal",
        "monitor_settings": "MONITOR SETTINGS",
        "monitor_blocks_width": "Width in blocks:",
        "monitor_blocks_height": "Height in blocks:",
        "monitor_text_scale": "Text scale:",
        "character_grid": "Character grid",
        "canvas_summary": "{device}  •  {width} × {height} characters",
        "monitor_summary": "{blocks_width} × {blocks_height} blocks  •  scale {scale}",
        "create": "Create",
        "cancel": "Cancel",
        "size_too_large": "The resulting canvas is larger than the editor limit of 200 × 100 characters.",
        "monitor_export_hint": "Lua export will find the first connected monitor and set its text scale automatically.",
        "save_project_title": "Save project",
        "saved": "Saved: {path}",
        "open_project_title": "Open project",
        "opened": "Opened: {path}",
        "error": "Error",
        "open_error": "Could not open the project:\n{error}",
        "invalid_size": "Invalid canvas size",
        "invalid_data_size": "Project data does not match the canvas size",
        "invalid_cell": "Invalid cell data",
        "new_project": "New project",
    },
    "ru": {
        "subtitle": "\u0412\u0438\u0437\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u043e\u0432 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0430",
        "new": "\u041d\u043e\u0432\u044b\u0439", "open": "\u041e\u0442\u043a\u0440\u044b\u0442\u044c", "save": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
        "undo": "\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c", "redo": "\u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u044c", "clear": "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c",
        "copy_lua": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c Lua", "export_lua": "\u042d\u043a\u0441\u043f\u043e\u0440\u0442 .lua",
        "tools": "\u0418\u041d\u0421\u0422\u0420\u0423\u041c\u0415\u041d\u0422\u042b", "tool_brush": "\u041a\u0438\u0441\u0442\u044c", "tool_text": "\u0422\u0435\u043a\u0441\u0442",
        "tool_rectangle": "\u041f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a", "tool_line": "\u041b\u0438\u043d\u0438\u044f", "tool_ellipse": "\u042d\u043b\u043b\u0438\u043f\u0441", "tool_select": "\u0412\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435", "tool_fill": "\u0417\u0430\u043b\u0438\u0432\u043a\u0430", "tool_solid": "\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f \u043a\u043b\u0435\u0442\u043a\u0430", "tool_eraser": "\u041b\u0430\u0441\u0442\u0438\u043a", "tool_picker": "\u041f\u0438\u043f\u0435\u0442\u043a\u0430",
        "brush_options": "\u041a\u0418\u0421\u0422\u042c \u0418 \u0424\u0418\u0413\u0423\u0420\u042b", "character": "\u0421\u0438\u043c\u0432\u043e\u043b", "filled_rectangle": "\u0417\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u044b\u0435 \u0444\u0438\u0433\u0443\u0440\u044b", "solid_shapes": "\u0424\u0438\u0433\u0443\u0440\u044b \u0442\u043e\u043b\u044c\u043a\u043e \u0438\u0437 \u0446\u0432\u0435\u0442\u0430",
        "canvas_background": "\u0421\u0434\u0435\u043b\u0430\u0442\u044c BG \u0444\u043e\u043d\u043e\u043c \u0445\u043e\u043b\u0441\u0442\u0430", "swap_colors": "\u041f\u043e\u043c\u0435\u043d\u044f\u0442\u044c \u0442\u0435\u043a\u0441\u0442 / \u0444\u043e\u043d", "selection_actions": "\u0412\u042b\u0414\u0415\u041b\u0415\u041d\u0418\u0415", "copy_cells": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c", "cut_cells": "\u0412\u044b\u0440\u0435\u0437\u0430\u0442\u044c", "paste_cells": "\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c", "delete_cells": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c", "no_selection": "\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u0432\u044b\u0434\u0435\u043b\u0438\u0442\u0435 \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "selection_copied": "\u0412\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c \u0441\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0430", "selection_cut": "\u0412\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c \u0432\u044b\u0440\u0435\u0437\u0430\u043d\u0430", "selection_pasted": "\u041e\u0431\u043b\u0430\u0441\u0442\u044c \u0432\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0430", "selection_deleted": "\u0412\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c \u0443\u0434\u0430\u043b\u0435\u043d\u0430", "palette": "\u041f\u0410\u041b\u0418\u0422\u0420\u0410 CC", "change_text": "\u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430", "change_background": "\u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430",
        "canvas": "\u0425\u041e\u041b\u0421\u0422 \u0422\u0415\u0420\u041c\u0418\u041d\u0410\u041b\u0410", "generated_code": "\u0413\u041e\u0422\u041e\u0412\u042b\u0419 LUA", "copy": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c", "apply_code": "\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c \u043a\u043e\u0434",
        "code_hint": "\u0416\u0438\u0432\u043e\u0439 Lua-\u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440: \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u0440\u0438\u043c\u0435\u043d\u044f\u044e\u0442\u0441\u044f \u043a \u0445\u043e\u043b\u0441\u0442\u0443. \u042d\u043a\u0441\u043f\u043e\u0440\u0442\u0435\u0440 \u0432\u044b\u0431\u0438\u0440\u0430\u0435\u0442 term.blit() \u0438\u043b\u0438 paintutils.", "code_applied": "\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f Lua \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u044b \u043a \u0445\u043e\u043b\u0441\u0442\u0443", "code_error": "\u041e\u0448\u0438\u0431\u043a\u0430 Lua-\u043f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430: {error}", "no_drawing_commands": "\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u043c\u044b\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u044b \u0440\u0438\u0441\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u044b",
        "ready": "\u0413\u043e\u0442\u043e\u0432\u043e", "foreground_background": "\u0422\u0435\u043a\u0441\u0442: {fg}   |   \u0424\u043e\u043d: {bg}", "blit_stats": "{calls} \u043a\u043e\u043c\u0430\u043d\u0434 \u0440\u0438\u0441\u043e\u0432\u0430\u043d\u0438\u044f | {chars} \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432 Lua",
        "position": "\u0421\u0442\u043e\u043b\u0431\u0435\u0446 {x}  \u0421\u0442\u0440\u043e\u043a\u0430 {y}   |   \u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442: {tool}", "text_dialog_title": "\u0412\u0441\u0442\u0430\u0432\u043a\u0430 \u0442\u0435\u043a\u0441\u0442\u0430", "text_dialog_prompt": "\u0422\u0435\u043a\u0441\u0442 \u0434\u043b\u044f \u0440\u0430\u0437\u043c\u0435\u0449\u0435\u043d\u0438\u044f \u043d\u0430 \u0445\u043e\u043b\u0441\u0442\u0435:",
        "copied": "Lua-\u043a\u043e\u0434 \u0441\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d \u0432 \u0431\u0443\u0444\u0435\u0440 \u043e\u0431\u043c\u0435\u043d\u0430", "export_title": "\u042d\u043a\u0441\u043f\u043e\u0440\u0442 Lua", "exported": "\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043e: {path}",
        "clear_title": "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0445\u043e\u043b\u0441\u0442", "clear_prompt": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u0441\u0435 \u0441 \u0445\u043e\u043b\u0441\u0442\u0430?", "unsaved_title": "\u041d\u0435\u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043d\u044b\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f", "unsaved_prompt": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u043f\u0440\u043e\u0435\u043a\u0442 \u043f\u0435\u0440\u0435\u0434 \u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0435\u043d\u0438\u0435\u043c?",
        "new_canvas": "\u041d\u043e\u0432\u044b\u0439 \u0445\u043e\u043b\u0441\u0442", "new_width": "\u0428\u0438\u0440\u0438\u043d\u0430 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0430:", "new_height": "\u0412\u044b\u0441\u043e\u0442\u0430 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0430:",
        "device_type": "\u0422\u0438\u043f \u044d\u043a\u0440\u0430\u043d\u0430", "device_computer": "\u041a\u043e\u043c\u043f\u044c\u044e\u0442\u0435\u0440", "device_turtle": "\u0427\u0435\u0440\u0435\u043f\u0430\u0448\u043a\u0430", "device_pocket": "\u041a\u0430\u0440\u043c\u0430\u043d\u043d\u044b\u0439 \u043a\u043e\u043c\u043f\u044c\u044e\u0442\u0435\u0440 / \u043f\u043b\u0430\u043d\u0448\u0435\u0442", "device_monitor": "\u0412\u043d\u0435\u0448\u043d\u0438\u0439 \u043c\u043e\u043d\u0438\u0442\u043e\u0440", "device_custom": "\u0414\u0440\u0443\u0433\u043e\u0439 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b",
        "monitor_settings": "\u041d\u0410\u0421\u0422\u0420\u041e\u0419\u041a\u0418 \u041c\u041e\u041d\u0418\u0422\u041e\u0420\u0410", "monitor_blocks_width": "\u0428\u0438\u0440\u0438\u043d\u0430 \u0432 \u0431\u043b\u043e\u043a\u0430\u0445:", "monitor_blocks_height": "\u0412\u044b\u0441\u043e\u0442\u0430 \u0432 \u0431\u043b\u043e\u043a\u0430\u0445:", "monitor_text_scale": "\u041c\u0430\u0441\u0448\u0442\u0430\u0431 \u0442\u0435\u043a\u0441\u0442\u0430:", "character_grid": "\u0421\u0438\u043c\u0432\u043e\u043b\u044c\u043d\u0430\u044f \u0441\u0435\u0442\u043a\u0430", "canvas_summary": "{device}  •  {width} × {height} \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432", "monitor_summary": "{blocks_width} × {blocks_height} \u0431\u043b\u043e\u043a\u043e\u0432  •  \u043c\u0430\u0441\u0448\u0442\u0430\u0431 {scale}", "create": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c", "cancel": "\u041e\u0442\u043c\u0435\u043d\u0430", "size_too_large": "\u041f\u043e\u043b\u0443\u0447\u0435\u043d\u043d\u044b\u0439 \u0445\u043e\u043b\u0441\u0442 \u0431\u043e\u043b\u044c\u0448\u0435 \u043f\u0440\u0435\u0434\u0435\u043b\u0430 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0430 200 × 100 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432.", "monitor_export_hint": "Lua-\u044d\u043a\u0441\u043f\u043e\u0440\u0442 \u0441\u0430\u043c \u043d\u0430\u0439\u0434\u0435\u0442 \u043f\u0435\u0440\u0432\u044b\u0439 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u0439 \u043c\u043e\u043d\u0438\u0442\u043e\u0440 \u0438 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442 \u0435\u0433\u043e \u043c\u0430\u0441\u0448\u0442\u0430\u0431 \u0442\u0435\u043a\u0441\u0442\u0430.",
        "save_project_title": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442", "saved": "\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043e: {path}",
        "open_project_title": "\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442", "opened": "\u041e\u0442\u043a\u0440\u044b\u0442\u043e: {path}", "error": "\u041e\u0448\u0438\u0431\u043a\u0430", "open_error": "\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043e\u0442\u043a\u0440\u044b\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442:\n{error}",
        "invalid_size": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u0440\u0430\u0437\u043c\u0435\u0440 \u0445\u043e\u043b\u0441\u0442\u0430", "invalid_data_size": "\u0414\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u043d\u0435 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u044e\u0442 \u0440\u0430\u0437\u043c\u0435\u0440\u0443 \u0445\u043e\u043b\u0441\u0442\u0430", "invalid_cell": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u043a\u043b\u0435\u0442\u043a\u0438", "new_project": "\u041d\u043e\u0432\u044b\u0439 \u043f\u0440\u043e\u0435\u043a\u0442",
    },
}


def normalize_character(value: str) -> str:
    """Return one byte-safe printable character suitable for term.blit()."""
    if not value:
        return " "
    character = value[0]
    code = ord(character)
    return character if 32 <= code <= 126 else "?"


def lua_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def monitor_terminal_size(block_width: int, block_height: int, text_scale: float):
    """Match CC:Tweaked's ServerMonitor character-grid calculation."""
    width = max(1, math.floor(((block_width - 0.3125) / (text_scale * 0.09375)) + 0.5))
    height = max(1, math.floor(((block_height - 0.3125) / (text_scale * 0.140625)) + 0.5))
    return width, height


def _normalise_device_profile(profile, width: int, height: int):
    if not isinstance(profile, dict):
        profile = {}
    device_type = profile.get("type")
    if device_type in DEVICE_SIZES and DEVICE_SIZES[device_type] == (width, height):
        return {"type": device_type}
    if device_type == "monitor":
        try:
            blocks_width = int(profile["blocks_width"])
            blocks_height = int(profile["blocks_height"])
            text_scale = float(profile["text_scale"])
        except (KeyError, TypeError, ValueError):
            pass
        else:
            if (
                blocks_width >= 1
                and blocks_height >= 1
                and text_scale in MONITOR_TEXT_SCALES
                and monitor_terminal_size(blocks_width, blocks_height, text_scale) == (width, height)
            ):
                return {
                    "type": "monitor",
                    "blocks_width": blocks_width,
                    "blocks_height": blocks_height,
                    "text_scale": text_scale,
                }
    for preset, size in DEVICE_SIZES.items():
        if size == (width, height):
            return {"type": preset}
    return {"type": "custom"}


def _compact_header(default_fg: int, default_bg: int, use_paintutils=False, device_profile=None):
    profile = device_profile or {"type": "computer"}
    if profile.get("type") == "monitor":
        lines = ['local t=assert(peripheral.find("monitor"),"Monitor not found")']
        text_scale = float(profile.get("text_scale", 1.0))
        scale_text = str(int(text_scale)) if text_scale.is_integer() else str(text_scale)
        lines.append(f"t.setTextScale({scale_text})")
        if use_paintutils:
            lines.extend(("local c,p=colors,paintutils", "local old=term.redirect(t)"))
        else:
            lines.append("local c=colors")
    else:
        globals_list = "term.current(),colors,paintutils" if use_paintutils else "term.current(),colors"
        variables = "t,c,p" if use_paintutils else "t,c"
        lines = [f"local {variables}={globals_list}"]
    lines.extend([
        f"t.setBackgroundColor(c.{CC_COLORS[default_bg][0]})",
        f"t.setTextColor(c.{CC_COLORS[default_fg][0]})",
        "t.clear()",
    ])
    return lines


def _row_blit_program(cells, width: int, height: int, default_fg: int, default_bg: int, device_profile=None):
    """Fast general representation: one blit call per visually used row."""
    lines = _compact_header(default_fg, default_bg, device_profile=device_profile)
    commands = []
    hex_digits = "0123456789abcdef"
    for y in range(height):
        row = cells[y]
        used = [x for x, cell in enumerate(row) if not (cell[0] == " " and cell[2] == default_bg)]
        if not used:
            continue
        first, last = used[0], used[-1]
        span = row[first : last + 1]
        characters = "".join(cell[0] for cell in span)
        foreground = "".join(hex_digits[cell[1]] for cell in span)
        background = "".join(hex_digits[cell[2]] for cell in span)
        commands.append(
            (first + 1, y + 1, lua_string(characters), lua_string(foreground), lua_string(background))
        )
    if commands:
        lines.append("local s,b=t.setCursorPos,t.blit")
        for x, y, characters, foreground, background in commands:
            lines.extend((f"s({x},{y})", f"b({characters},{foreground},{background})"))
    return "\n".join(lines) + "\n", len(commands)


def _background_rectangles(cells, width: int, height: int, default_bg: int):
    """Greedily cover every non-default background with solid rectangles."""
    remaining = [[cells[y][x][2] != default_bg for x in range(width)] for y in range(height)]
    rectangles = []
    for y in range(height):
        for x in range(width):
            if not remaining[y][x]:
                continue
            color = cells[y][x][2]
            first_width = 0
            while x + first_width < width and remaining[y][x + first_width] and cells[y][x + first_width][2] == color:
                first_width += 1
            best_width, best_height, best_area = first_width, 1, first_width
            shared_width = first_width
            yy = y + 1
            while yy < height and shared_width:
                row_width = 0
                while (
                    row_width < shared_width
                    and remaining[yy][x + row_width]
                    and cells[yy][x + row_width][2] == color
                ):
                    row_width += 1
                shared_width = min(shared_width, row_width)
                if not shared_width:
                    break
                area = shared_width * (yy - y + 1)
                if area > best_area:
                    best_width, best_height, best_area = shared_width, yy - y + 1, area
                yy += 1
            for fill_y in range(y, y + best_height):
                for fill_x in range(x, x + best_width):
                    remaining[fill_y][fill_x] = False
            rectangles.append((x + 1, y + 1, x + best_width, y + best_height, color))
    return rectangles


def _shape_program(cells, width: int, height: int, default_fg: int, default_bg: int, device_profile=None):
    """Use paintutils for solid areas and blit only for visible characters."""
    rectangles = _background_rectangles(cells, width, height, default_bg)
    text_commands = []
    hex_digits = "0123456789abcdef"
    for y in range(height):
        row = cells[y]
        used = [x for x, cell in enumerate(row) if cell[0] != " "]
        if not used:
            continue
        first, last = used[0], used[-1]
        span = row[first : last + 1]
        text_commands.append(
            (
                first + 1,
                y + 1,
                lua_string("".join(cell[0] for cell in span)),
                lua_string("".join(hex_digits[cell[1]] for cell in span)),
                lua_string("".join(hex_digits[cell[2]] for cell in span)),
            )
        )

    lines = _compact_header(
        default_fg, default_bg, use_paintutils=bool(rectangles), device_profile=device_profile
    )
    if rectangles:
        lines.append("local f=p.drawFilledBox")
        for x1, y1, x2, y2, color in rectangles:
            lines.append(f"f({x1},{y1},{x2},{y2},c.{CC_COLORS[color][0]})")
    if text_commands:
        lines.append("local s,b=t.setCursorPos,t.blit")
        for x, y, characters, foreground, background in text_commands:
            lines.extend((f"s({x},{y})", f"b({characters},{foreground},{background})"))
    if rectangles and (device_profile or {}).get("type") == "monitor":
        lines.append("term.redirect(old)")
    return "\n".join(lines) + "\n", len(rectangles) + len(text_commands)


def generate_lua(cells, width: int, height: int, default_fg: int, default_bg: int, device_profile=None):
    """Generate both representations and return the smallest valid Lua source."""
    row_code, row_calls = _row_blit_program(
        cells, width, height, default_fg, default_bg, device_profile
    )
    shape_code, shape_calls = _shape_program(
        cells, width, height, default_fg, default_bg, device_profile
    )
    if len(shape_code) < len(row_code):
        return shape_code, shape_calls
    return row_code, row_calls


COLOR_INDEX_BY_NAME = {entry[0].lower(): index for index, entry in enumerate(CC_COLORS)}
LUA_QUOTED_STRING = r'"(?:\\.|[^"\\])*"'


def _parse_lua_string(token: str, line_number: int):
    try:
        value = ast.literal_eval(token)
    except (SyntaxError, ValueError) as error:
        raise ValueError(f"line {line_number}: invalid string") from error
    if not isinstance(value, str):
        raise ValueError(f"line {line_number}: string expected")
    return value


def _parse_color(expression: str, line_number: int):
    token = expression.strip()
    name_match = re.fullmatch(r"(?:c|colors)\.([A-Za-z]+)", token)
    if name_match:
        index = COLOR_INDEX_BY_NAME.get(name_match.group(1).lower())
        if index is not None:
            return index
    try:
        value = int(token, 0)
    except ValueError as error:
        raise ValueError(f"line {line_number}: unknown color {token}") from error
    if value > 0 and value & (value - 1) == 0:
        index = value.bit_length() - 1
        if 0 <= index <= 15:
            return index
    raise ValueError(f"line {line_number}: invalid CC color {token}")


def _integer(token: str, line_number: int):
    try:
        return int(float(token.strip()))
    except ValueError as error:
        raise ValueError(f"line {line_number}: integer expected") from error


def _line_points(x1, y1, x2, y2):
    dx, dy = abs(x2 - x1), -abs(y2 - y1)
    step_x = 1 if x1 < x2 else -1
    step_y = 1 if y1 < y2 else -1
    error = dx + dy
    while True:
        yield x1, y1
        if x1 == x2 and y1 == y2:
            return
        doubled = 2 * error
        if doubled >= dy:
            error += dy
            x1 += step_x
        if doubled <= dx:
            error += dx
            y1 += step_y


def parse_lua_design(source: str, width: int, height: int, initial_fg=0, initial_bg=15):
    """Interpret the drawing subset of the CC:Tweaked terminal APIs."""
    foreground, background = initial_fg, initial_bg
    default_fg, default_bg = initial_fg, initial_bg
    cells = [[[" ", foreground, background] for _x in range(width)] for _y in range(height)]
    cursor_x, cursor_y = 1, 1
    visual_commands = 0

    def set_cell(x, y, character=" ", fg=None, bg=None):
        if 1 <= x <= width and 1 <= y <= height:
            cells[y - 1][x - 1] = [
                normalize_character(character),
                foreground if fg is None else fg,
                background if bg is None else bg,
            ]

    for line_number, raw_line in enumerate(source.splitlines(), 1):
        line = raw_line.strip().rstrip(";")
        if not line or line.startswith("--") or line.startswith("local "):
            continue

        match = re.fullmatch(r"(?:t|term)\.setBackgroundColor\((.+)\)", line)
        if match:
            background = _parse_color(match.group(1), line_number)
            continue
        match = re.fullmatch(r"(?:t|term)\.setTextColor\((.+)\)", line)
        if match:
            foreground = _parse_color(match.group(1), line_number)
            continue
        if re.fullmatch(r"(?:t|term)\.clear\(\)", line):
            default_fg, default_bg = foreground, background
            cells = [[[" ", foreground, background] for _x in range(width)] for _y in range(height)]
            cursor_x, cursor_y = 1, 1
            visual_commands += 1
            continue
        if re.fullmatch(r"(?:t|term)\.clearLine\(\)", line):
            for x in range(1, width + 1):
                set_cell(x, cursor_y)
            cursor_x = 1
            visual_commands += 1
            continue

        match = re.fullmatch(r"(?:s|t\.setCursorPos|term\.setCursorPos)\(([^,]+),([^\)]+)\)", line)
        if match:
            cursor_x = _integer(match.group(1), line_number)
            cursor_y = _integer(match.group(2), line_number)
            continue

        match = re.fullmatch(
            rf"(?:b|t\.blit|term\.blit)\s*\(\s*({LUA_QUOTED_STRING})\s*,\s*({LUA_QUOTED_STRING})\s*,\s*({LUA_QUOTED_STRING})\s*\)",
            line,
        )
        if match:
            characters = _parse_lua_string(match.group(1), line_number)
            foreground_hex = _parse_lua_string(match.group(2), line_number)
            background_hex = _parse_lua_string(match.group(3), line_number)
            if not (len(characters) == len(foreground_hex) == len(background_hex)):
                raise ValueError(f"line {line_number}: blit strings must have equal lengths")
            for offset, character in enumerate(characters):
                try:
                    fg = int(foreground_hex[offset], 16)
                    bg = int(background_hex[offset], 16)
                except ValueError as error:
                    raise ValueError(f"line {line_number}: invalid blit color") from error
                set_cell(cursor_x + offset, cursor_y, character, fg, bg)
            cursor_x += len(characters)
            visual_commands += 1
            continue

        match = re.fullmatch(rf"(?:t\.write|term\.write)\s*\(\s*({LUA_QUOTED_STRING})\s*\)", line)
        if match:
            characters = _parse_lua_string(match.group(1), line_number)
            for offset, character in enumerate(characters):
                set_cell(cursor_x + offset, cursor_y, character)
            cursor_x += len(characters)
            visual_commands += 1
            continue

        box_pattern = r"(?:f|p\.drawFilledBox|paintutils\.drawFilledBox)"
        match = re.fullmatch(rf"{box_pattern}\(([^,]+),([^,]+),([^,]+),([^,]+),([^\)]+)\)", line)
        if match:
            x1, y1, x2, y2 = (_integer(match.group(i), line_number) for i in range(1, 5))
            color = _parse_color(match.group(5), line_number)
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    set_cell(x, y, " ", bg=color)
            visual_commands += 1
            continue

        match = re.fullmatch(
            r"(?:p\.drawBox|paintutils\.drawBox)\(([^,]+),([^,]+),([^,]+),([^,]+),([^\)]+)\)", line
        )
        if match:
            x1, y1, x2, y2 = (_integer(match.group(i), line_number) for i in range(1, 5))
            color = _parse_color(match.group(5), line_number)
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            for x in range(x1, x2 + 1):
                set_cell(x, y1, " ", bg=color)
                set_cell(x, y2, " ", bg=color)
            for y in range(y1, y2 + 1):
                set_cell(x1, y, " ", bg=color)
                set_cell(x2, y, " ", bg=color)
            visual_commands += 1
            continue

        match = re.fullmatch(
            r"(?:p\.drawLine|paintutils\.drawLine)\(([^,]+),([^,]+),([^,]+),([^,]+),([^\)]+)\)", line
        )
        if match:
            x1, y1, x2, y2 = (_integer(match.group(i), line_number) for i in range(1, 5))
            color = _parse_color(match.group(5), line_number)
            for x, y in _line_points(x1, y1, x2, y2):
                set_cell(x, y, " ", bg=color)
            visual_commands += 1
            continue

        match = re.fullmatch(r"(?:p\.drawPixel|paintutils\.drawPixel)\(([^,]+),([^,]+),([^\)]+)\)", line)
        if match:
            x = _integer(match.group(1), line_number)
            y = _integer(match.group(2), line_number)
            color = _parse_color(match.group(3), line_number)
            set_cell(x, y, " ", bg=color)
            visual_commands += 1
            continue

        if any(name in line for name in ("blit(", "drawFilledBox(", "drawBox(", "drawLine(", "drawPixel(")):
            raise ValueError(f"line {line_number}: unsupported or malformed drawing command")

    return cells, default_fg, default_bg, visual_commands


class NewCanvasDialog(tk.Toplevel):
    """Device-aware replacement for the old pair of size prompts."""

    def __init__(self, parent, tr, current_width, current_height, current_profile):
        super().__init__(parent)
        self._tr = tr
        self.result = None
        self.configure(bg="#0b1016")
        self.title(tr("new_canvas"))
        self.resizable(False, False)
        self.transient(parent)

        self.profile_labels = {
            code: tr(f"device_{code}")
            for code in ("computer", "turtle", "pocket", "monitor", "custom")
        }
        self.label_profiles = {label: code for code, label in self.profile_labels.items()}
        initial_type = current_profile.get("type", "custom")
        if initial_type not in self.profile_labels:
            initial_type = "custom"

        self.device_var = tk.StringVar(value=self.profile_labels[initial_type])
        self.width_var = tk.IntVar(value=current_width)
        self.height_var = tk.IntVar(value=current_height)
        self.blocks_width_var = tk.IntVar(value=int(current_profile.get("blocks_width", 1)))
        self.blocks_height_var = tk.IntVar(value=int(current_profile.get("blocks_height", 1)))
        self.scale_var = tk.StringVar(value=str(current_profile.get("text_scale", 1.0)))
        self.summary_var = tk.StringVar()
        self.monitor_detail_var = tk.StringVar()
        self.custom_size = (current_width, current_height)
        self.last_type = initial_type
        self._updating_dimensions = False

        body = ttk.Frame(self, style="Card.TFrame", padding=22)
        body.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(body, text=tr("device_type"), style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 7)
        )
        self.device_box = ttk.Combobox(
            body,
            textvariable=self.device_var,
            values=list(self.profile_labels.values()),
            state="readonly",
            width=38,
        )
        self.device_box.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        self.device_box.bind("<<ComboboxSelected>>", self._device_changed)

        ttk.Label(body, text=tr("character_grid"), style="Section.TLabel").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(0, 7)
        )
        ttk.Label(body, text=tr("new_width"), style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Label(body, text=tr("new_height"), style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=4)
        self.width_spin = ttk.Spinbox(body, from_=1, to=200, textvariable=self.width_var, width=12)
        self.height_spin = ttk.Spinbox(body, from_=1, to=100, textvariable=self.height_var, width=12)
        self.width_spin.grid(row=3, column=1, sticky="e", pady=4)
        self.height_spin.grid(row=4, column=1, sticky="e", pady=4)

        ttk.Separator(body).grid(row=5, column=0, columnspan=2, sticky="ew", pady=15)
        ttk.Label(body, text=tr("monitor_settings"), style="Section.TLabel").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(0, 7)
        )
        ttk.Label(body, text=tr("monitor_blocks_width"), style="Card.TLabel").grid(row=7, column=0, sticky="w", pady=4)
        ttk.Label(body, text=tr("monitor_blocks_height"), style="Card.TLabel").grid(row=8, column=0, sticky="w", pady=4)
        ttk.Label(body, text=tr("monitor_text_scale"), style="Card.TLabel").grid(row=9, column=0, sticky="w", pady=4)
        self.blocks_width_spin = ttk.Spinbox(body, from_=1, to=8, textvariable=self.blocks_width_var, width=12)
        self.blocks_height_spin = ttk.Spinbox(body, from_=1, to=6, textvariable=self.blocks_height_var, width=12)
        self.scale_box = ttk.Combobox(
            body,
            textvariable=self.scale_var,
            values=[str(scale) for scale in MONITOR_TEXT_SCALES],
            state="readonly",
            width=10,
        )
        self.blocks_width_spin.grid(row=7, column=1, sticky="e", pady=4)
        self.blocks_height_spin.grid(row=8, column=1, sticky="e", pady=4)
        self.scale_box.grid(row=9, column=1, sticky="e", pady=4)

        summary = tk.Frame(body, bg="#0c141c", highlightthickness=1, highlightbackground="#263647")
        summary.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(16, 8))
        tk.Label(
            summary, textvariable=self.summary_var, bg="#0c141c", fg="#55dfbb",
            font=("Segoe UI Semibold", 11), anchor="w", padx=12, pady=9,
        ).pack(fill="x")
        tk.Label(
            summary, textvariable=self.monitor_detail_var, bg="#0c141c", fg="#8295a8",
            font=("Segoe UI", 9), anchor="w", justify="left", padx=12, pady=4, wraplength=430,
        ).pack(fill="x")

        buttons = ttk.Frame(body, style="Card.TFrame")
        buttons.grid(row=11, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text=tr("cancel"), command=self._cancel).pack(side="left", padx=(0, 7))
        ttk.Button(buttons, text=tr("create"), command=self._accept, style="Accent.TButton").pack(side="left")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        for variable in (
            self.width_var, self.height_var, self.blocks_width_var,
            self.blocks_height_var, self.scale_var,
        ):
            variable.trace_add("write", self._values_changed)

        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.bind("<Escape>", lambda _event: self._cancel())
        self.bind("<Return>", lambda _event: self._accept())
        self._apply_device_type(initial=True)
        self.update_idletasks()
        x = parent.winfo_rootx() + max(0, (parent.winfo_width() - self.winfo_width()) // 2)
        y = parent.winfo_rooty() + max(0, (parent.winfo_height() - self.winfo_height()) // 2)
        self.geometry(f"+{x}+{y}")
        self.grab_set()
        self.device_box.focus_set()

    def _current_type(self):
        return self.label_profiles.get(self.device_var.get(), "custom")

    def _device_changed(self, _event=None):
        if self.last_type == "custom":
            try:
                self.custom_size = (int(self.width_var.get()), int(self.height_var.get()))
            except (tk.TclError, ValueError):
                pass
        self._apply_device_type()

    def _apply_device_type(self, initial=False):
        device_type = self._current_type()
        self.last_type = device_type
        if device_type in DEVICE_SIZES:
            self.width_var.set(DEVICE_SIZES[device_type][0])
            self.height_var.set(DEVICE_SIZES[device_type][1])
        elif device_type == "monitor":
            self._recalculate_monitor_dimensions()
        elif device_type == "custom" and not initial:
            self.width_var.set(self.custom_size[0])
            self.height_var.set(self.custom_size[1])
        self._set_state(self.width_spin, "normal" if device_type == "custom" else "disabled")
        self._set_state(self.height_spin, "normal" if device_type == "custom" else "disabled")
        monitor_state = "normal" if device_type == "monitor" else "disabled"
        self._set_state(self.blocks_width_spin, monitor_state)
        self._set_state(self.blocks_height_spin, monitor_state)
        self.scale_box.configure(state="readonly" if device_type == "monitor" else "disabled")
        self._refresh_summary()

    @staticmethod
    def _set_state(widget, state):
        widget.configure(state=state)

    def _recalculate_monitor_dimensions(self):
        try:
            blocks_width = int(self.blocks_width_var.get())
            blocks_height = int(self.blocks_height_var.get())
            text_scale = float(self.scale_var.get())
        except (tk.TclError, ValueError):
            return False
        if not (1 <= blocks_width <= 8 and 1 <= blocks_height <= 6):
            return False
        if text_scale not in MONITOR_TEXT_SCALES:
            return False
        width, height = monitor_terminal_size(blocks_width, blocks_height, text_scale)
        self._updating_dimensions = True
        try:
            self.width_var.set(width)
            self.height_var.set(height)
        finally:
            self._updating_dimensions = False
        return True

    def _values_changed(self, *_args):
        if self._updating_dimensions:
            return
        if self._current_type() == "monitor":
            self._recalculate_monitor_dimensions()
        self._refresh_summary()

    def _refresh_summary(self):
        try:
            width, height = int(self.width_var.get()), int(self.height_var.get())
        except (tk.TclError, ValueError):
            return
        device_type = self._current_type()
        self.summary_var.set(self._tr(
            "canvas_summary", device=self.profile_labels[device_type], width=width, height=height
        ))
        if device_type == "monitor":
            self.monitor_detail_var.set(
                self._tr(
                    "monitor_summary",
                    blocks_width=self.blocks_width_var.get(),
                    blocks_height=self.blocks_height_var.get(),
                    scale=self.scale_var.get(),
                )
                + "\n"
                + self._tr("monitor_export_hint")
            )
        else:
            self.monitor_detail_var.set("")

    def _accept(self):
        device_type = self._current_type()
        if device_type == "monitor" and not self._recalculate_monitor_dimensions():
            messagebox.showerror(self._tr("error"), self._tr("invalid_size"), parent=self)
            return
        try:
            width, height = int(self.width_var.get()), int(self.height_var.get())
        except (tk.TclError, ValueError):
            messagebox.showerror(self._tr("error"), self._tr("invalid_size"), parent=self)
            return
        if not 1 <= width <= 200 or not 1 <= height <= 100:
            messagebox.showerror(self._tr("error"), self._tr("size_too_large"), parent=self)
            return
        device_type = self._current_type()
        profile = {"type": device_type}
        if device_type == "monitor":
            profile.update({
                "blocks_width": int(self.blocks_width_var.get()),
                "blocks_height": int(self.blocks_height_var.get()),
                "text_scale": float(self.scale_var.get()),
            })
        self.result = (width, height, profile)
        self.grab_release()
        self.destroy()

    def _cancel(self):
        self.result = None
        self.grab_release()
        self.destroy()


class UIEditor:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.width = 51
        self.height = 19
        self.device_profile = {"type": "computer"}
        self.default_fg = 0
        self.default_bg = 15
        self.selected_fg = 0
        self.selected_bg = 15
        self.cells = self._blank_cells(self.width, self.height)
        self.current_file = None
        self.dirty = False
        self.undo_stack = []
        self.redo_stack = []
        self.rect_items = []
        self.text_items = []
        self.drag_start = None
        self.drag_last = None
        self.action_active = False
        self.selection = None
        self.selection_item = None
        self.cell_clipboard = None
        self._updating_code = False
        self._code_apply_after = None
        self._last_applied_code = ""

        self.tool = tk.StringVar(value="brush")
        self.character = tk.StringVar(value="#")
        self.palette_target = tk.StringVar(value="bg")
        self.filled_rectangle = tk.BooleanVar(value=True)
        self.solid_shapes = tk.BooleanVar(value=False)
        self.language = tk.StringVar(value="en")
        self.text_vars = {}
        self.language_buttons = {}
        self.status = tk.StringVar(value=TRANSLATIONS["en"]["ready"])
        self.code_stats = tk.StringVar(value="")

        self._configure_window()
        self._build_ui()
        self._build_canvas_items()
        self._refresh_palette_labels()
        self._refresh_code()

    def _configure_window(self):
        self.root.title(APP_NAME)
        self.root.geometry("1480x860")
        self.root.minsize(1120, 680)
        self.root.configure(bg="#0b1016")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10), background="#0b1016", foreground="#dce7f2")
        style.configure("TFrame", background="#0b1016")
        style.configure("Card.TFrame", background="#111923")
        style.configure("Toolbar.TFrame", background="#0f1720")
        style.configure("TLabel", background="#0b1016", foreground="#cbd7e3")
        style.configure("Card.TLabel", background="#111923", foreground="#cbd7e3")
        style.configure("Section.TLabel", background="#111923", foreground="#6f8194", font=("Segoe UI Semibold", 9))
        style.configure("Title.TLabel", background="#0f1720", foreground="#f4f8fb", font=("Segoe UI Semibold", 18))
        style.configure("Subtitle.TLabel", background="#0f1720", foreground="#73869a", font=("Segoe UI", 9))
        style.configure("TButton", background="#1b2734", foreground="#dce7f2", borderwidth=0, padding=(11, 7))
        style.map("TButton", background=[("active", "#253545"), ("pressed", "#18232e")])
        style.configure("Accent.TButton", background="#3dd6b0", foreground="#07140f", font=("Segoe UI Semibold", 10), padding=(13, 7))
        style.map("Accent.TButton", background=[("active", "#62e2c2"), ("pressed", "#2cb08f")])
        style.configure("Tool.TRadiobutton", background="#111923", foreground="#cbd7e3", padding=(5, 6))
        style.map("Tool.TRadiobutton", background=[("active", "#172330")], foreground=[("selected", "#55dfbb")])
        style.configure("TRadiobutton", background="#111923", foreground="#cbd7e3")
        style.map("TRadiobutton", background=[("active", "#111923")], foreground=[("selected", "#55dfbb")])
        style.configure("TCheckbutton", background="#111923", foreground="#cbd7e3")
        style.map("TCheckbutton", background=[("active", "#111923")], foreground=[("selected", "#55dfbb")])
        style.configure("TEntry", fieldbackground="#0a1017", foreground="#eef5fb", insertcolor="#eef5fb", bordercolor="#263647", padding=6)
        style.configure("Panel.TLabelframe", background="#111923", bordercolor="#202d3b", relief="solid", padding=10)
        style.configure("Panel.TLabelframe.Label", background="#111923", foreground="#6f8194", font=("Segoe UI Semibold", 9))
        style.configure("TScrollbar", background="#202d3b", troughcolor="#0b1016", bordercolor="#0b1016", arrowcolor="#8092a5")

        self.root.bind("<Control-n>", lambda _e: self.new_project())
        self.root.bind("<Control-o>", lambda _e: self.open_project())
        self.root.bind("<Control-s>", lambda _e: self.save_project())
        self.root.bind("<Control-z>", lambda _e: self.undo())
        self.root.bind("<Control-y>", lambda _e: self.redo())
        self.root.bind("<Control-c>", lambda event: self._selection_shortcut(event, "copy"))
        self.root.bind("<Control-x>", lambda event: self._selection_shortcut(event, "cut"))
        self.root.bind("<Control-v>", lambda event: self._selection_shortcut(event, "paste"))
        self.root.bind("<Delete>", lambda event: self._selection_shortcut(event, "delete"))

    def _tr(self, key, **values):
        text = TRANSLATIONS[self.language.get()].get(key, key)
        return text.format(**values) if values else text

    def _v(self, key):
        variable = self.text_vars.get(key)
        if variable is None:
            variable = tk.StringVar(value=self._tr(key))
            self.text_vars[key] = variable
        return variable

    def _set_language(self, language):
        self.language.set(language)
        for key, variable in self.text_vars.items():
            variable.set(self._tr(key))
        for code, button in self.language_buttons.items():
            selected = code == language
            button.configure(
                bg="#3dd6b0" if selected else "#16212c",
                fg="#07140f" if selected else "#8ea0b3",
                activebackground="#55dfbb" if selected else "#21303e",
                activeforeground="#07140f" if selected else "#dce7f2",
            )
        self.status.set(self._tr("ready"))
        self._refresh_palette_labels()
        self._update_size_label()
        self._refresh_code()
        self._update_title()

    def _color_name(self, index):
        return COLOR_NAMES[self.language.get()][index]

    def _build_ui(self):
        header = ttk.Frame(self.root, style="Toolbar.TFrame", padding=(16, 11))
        header.pack(fill="x")
        brand = ttk.Frame(header, style="Toolbar.TFrame")
        brand.pack(side="left")
        tk.Label(
            brand, text="CC:UI", bg="#3dd6b0", fg="#07140f", font=("Consolas", 14, "bold"),
            padx=9, pady=5,
        ).pack(side="left", padx=(0, 10))
        title_box = ttk.Frame(brand, style="Toolbar.TFrame")
        title_box.pack(side="left")
        ttk.Label(title_box, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_box, textvariable=self._v("subtitle"), style="Subtitle.TLabel").pack(anchor="w")

        language_box = tk.Frame(header, bg="#0f1720")
        language_box.pack(side="right")
        for code, caption in (("en", "EN"), ("ru", "RU")):
            button = tk.Button(
                language_box, text=caption, width=4, relief="flat", bd=0, cursor="hand2",
                font=("Segoe UI Semibold", 9), command=lambda lang=code: self._set_language(lang),
            )
            button.pack(side="left", padx=2, pady=3)
            self.language_buttons[code] = button

        toolbar = ttk.Frame(self.root, style="Toolbar.TFrame", padding=(14, 7, 14, 10))
        toolbar.pack(fill="x")
        for key, command, style_name in (
            ("new", self.new_project, "TButton"), ("open", self.open_project, "TButton"),
            ("save", self.save_project, "TButton"), ("undo", self.undo, "TButton"),
            ("redo", self.redo, "TButton"), ("clear", self.clear_canvas, "TButton"),
            ("export_lua", self.export_lua, "TButton"), ("copy_lua", self.copy_lua, "Accent.TButton"),
        ):
            ttk.Button(toolbar, textvariable=self._v(key), command=command, style=style_name).pack(side="left", padx=(0, 5))

        main = ttk.Panedwindow(self.root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        sidebar = ttk.Frame(main, style="Card.TFrame", width=275, padding=12)
        workspace = ttk.Frame(main, style="Card.TFrame", padding=10)
        code_side = ttk.Frame(main, style="Card.TFrame", width=430, padding=12)
        main.add(sidebar, weight=0)
        main.add(workspace, weight=5)
        main.add(code_side, weight=3)

        ttk.Label(sidebar, textvariable=self._v("tools"), style="Section.TLabel").pack(anchor="w", pady=(0, 7))
        tool_grid = ttk.Frame(sidebar, style="Card.TFrame")
        tool_grid.pack(fill="x", pady=(0, 16))
        for index, (key, value) in enumerate((
            ("tool_brush", "brush"), ("tool_text", "text"),
            ("tool_line", "line"), ("tool_rectangle", "rectangle"),
            ("tool_ellipse", "ellipse"), ("tool_fill", "fill"),
            ("tool_solid", "solid"), ("tool_eraser", "eraser"),
            ("tool_picker", "picker"), ("tool_select", "select"),
        )):
            ttk.Radiobutton(
                tool_grid, textvariable=self._v(key), value=value, variable=self.tool, style="Tool.TRadiobutton"
            ).grid(row=index // 2, column=index % 2, sticky="ew", padx=2, pady=2)
        tool_grid.columnconfigure(0, weight=1)
        tool_grid.columnconfigure(1, weight=1)

        ttk.Label(sidebar, textvariable=self._v("brush_options"), style="Section.TLabel").pack(anchor="w", pady=(0, 7))
        character_row = ttk.Frame(sidebar, style="Card.TFrame")
        character_row.pack(fill="x", pady=(0, 8))
        ttk.Label(character_row, textvariable=self._v("character"), style="Card.TLabel").pack(side="left")
        char_entry = ttk.Entry(character_row, textvariable=self.character, width=5, justify="center")
        char_entry.pack(side="right")
        char_entry.bind("<KeyRelease>", self._validate_character_entry)
        ttk.Checkbutton(sidebar, textvariable=self._v("filled_rectangle"), variable=self.filled_rectangle).pack(anchor="w", pady=(0, 7))
        ttk.Checkbutton(sidebar, textvariable=self._v("solid_shapes"), variable=self.solid_shapes).pack(anchor="w", pady=(0, 7))
        ttk.Button(sidebar, textvariable=self._v("swap_colors"), command=self.swap_colors).pack(fill="x", pady=(0, 5))
        ttk.Button(sidebar, textvariable=self._v("canvas_background"), command=self.set_canvas_background).pack(fill="x", pady=(0, 15))

        ttk.Label(sidebar, textvariable=self._v("selection_actions"), style="Section.TLabel").pack(anchor="w", pady=(0, 7))
        selection_buttons = ttk.Frame(sidebar, style="Card.TFrame")
        selection_buttons.pack(fill="x", pady=(0, 15))
        for index, (key, command) in enumerate((
            ("copy_cells", self.copy_selection), ("cut_cells", self.cut_selection),
            ("paste_cells", self.paste_selection), ("delete_cells", self.delete_selection),
        )):
            ttk.Button(selection_buttons, textvariable=self._v(key), command=command).grid(
                row=index // 2, column=index % 2, sticky="ew", padx=2, pady=2
            )
        selection_buttons.columnconfigure(0, weight=1)
        selection_buttons.columnconfigure(1, weight=1)

        ttk.Label(sidebar, textvariable=self._v("palette"), style="Section.TLabel").pack(anchor="w", pady=(0, 7))
        ttk.Radiobutton(sidebar, textvariable=self._v("change_text"), value="fg", variable=self.palette_target).pack(anchor="w")
        ttk.Radiobutton(sidebar, textvariable=self._v("change_background"), value="bg", variable=self.palette_target).pack(anchor="w", pady=(0, 8))
        palette = ttk.Frame(sidebar, style="Card.TFrame")
        palette.pack(fill="x")
        for index, (_lua_name, _localized, color) in enumerate(CC_COLORS):
            button = tk.Button(
                palette, width=3, height=1, bg=color, activebackground=color, relief="flat", bd=0,
                highlightthickness=2, highlightbackground="#111923", cursor="hand2",
                command=lambda i=index: self._select_palette_color(i),
            )
            button.grid(row=index // 8, column=index % 8, padx=2, pady=2, sticky="ew")
            button.bind("<Button-3>", lambda _e, i=index: self._select_palette_color(i, "fg"))
            palette.columnconfigure(index % 8, weight=1)
        self.color_label = ttk.Label(sidebar, text="", style="Card.TLabel", wraplength=245)
        self.color_label.pack(anchor="w", pady=(9, 0))

        canvas_header = ttk.Frame(workspace, style="Card.TFrame")
        canvas_header.pack(fill="x", pady=(0, 8))
        ttk.Label(canvas_header, textvariable=self._v("canvas"), style="Section.TLabel").pack(side="left")
        self.size_label = tk.Label(
            canvas_header, text="51 x 19", bg="#172330", fg="#55dfbb",
            font=("Consolas", 9, "bold"), padx=9, pady=3,
        )
        self.size_label.pack(side="right")

        canvas_frame = ttk.Frame(workspace, style="Card.TFrame")
        canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg="#090d12", highlightthickness=1, highlightbackground="#263647")
        x_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        y_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        self.canvas.bind("<Button-1>", self._canvas_press)
        self.canvas.bind("<B1-Motion>", self._canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._canvas_release)
        self.canvas.bind("<Motion>", self._canvas_motion)

        code_header = ttk.Frame(code_side, style="Card.TFrame")
        code_header.pack(fill="x")
        ttk.Label(code_header, textvariable=self._v("generated_code"), style="Section.TLabel").pack(side="left")
        ttk.Button(code_header, textvariable=self._v("copy"), command=self.copy_lua, style="Accent.TButton").pack(side="right")
        ttk.Button(code_header, textvariable=self._v("apply_code"), command=self.apply_code_from_editor).pack(side="right", padx=(0, 5))
        ttk.Label(code_side, textvariable=self.code_stats, style="Card.TLabel").pack(anchor="w", pady=(5, 8))

        code_frame = ttk.Frame(code_side, style="Card.TFrame")
        code_frame.pack(fill="both", expand=True)
        self.code_text = tk.Text(
            code_frame,
            wrap="none",
            undo=False,
            font=("Consolas", 10),
            bg="#080c11",
            fg="#cfe0ed",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10,
            selectbackground="#285e55",
        )
        code_y = ttk.Scrollbar(code_frame, orient="vertical", command=self.code_text.yview)
        code_x = ttk.Scrollbar(code_frame, orient="horizontal", command=self.code_text.xview)
        self.code_text.configure(yscrollcommand=code_y.set, xscrollcommand=code_x.set)
        self.code_text.bind("<<Modified>>", self._on_code_modified)
        self.code_text.grid(row=0, column=0, sticky="nsew")
        code_y.grid(row=0, column=1, sticky="ns")
        code_x.grid(row=1, column=0, sticky="ew")
        code_frame.rowconfigure(0, weight=1)
        code_frame.columnconfigure(0, weight=1)

        ttk.Label(
            code_side,
            textvariable=self._v("code_hint"),
            wraplength=400,
            style="Card.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        status_bar = tk.Label(
            self.root, textvariable=self.status, bg="#0f1720", fg="#8496a8",
            anchor="w", padx=14, pady=6, font=("Segoe UI", 9),
        )
        status_bar.pack(fill="x")
        self._set_language("en")

    def _blank_cells(self, width, height):
        return [[[" ", self.default_fg, self.default_bg] for _x in range(width)] for _y in range(height)]

    def _build_canvas_items(self):
        self.canvas.delete("all")
        self.selection = None
        self.selection_item = None
        self.rect_items = [[None] * self.width for _ in range(self.height)]
        self.text_items = [[None] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                left, top = x * CELL_WIDTH, y * CELL_HEIGHT
                rect = self.canvas.create_rectangle(
                    left,
                    top,
                    left + CELL_WIDTH,
                    top + CELL_HEIGHT,
                    outline="#343941",
                    width=1,
                )
                text = self.canvas.create_text(
                    left + CELL_WIDTH / 2,
                    top + CELL_HEIGHT / 2,
                    font=("Consolas", 11),
                    anchor="center",
                )
                self.rect_items[y][x] = rect
                self.text_items[y][x] = text
                self._redraw_cell(x, y)
        self.canvas.configure(scrollregion=(0, 0, self.width * CELL_WIDTH, self.height * CELL_HEIGHT))
        self._update_size_label()

    def _update_size_label(self):
        if not hasattr(self, "size_label"):
            return
        device_type = self.device_profile.get("type", "custom")
        device_name = self._tr(f"device_{device_type}")
        if device_type == "monitor":
            blocks_width = self.device_profile.get("blocks_width", 1)
            blocks_height = self.device_profile.get("blocks_height", 1)
            text_scale = self.device_profile.get("text_scale", 1.0)
            device_name = f"{device_name} {blocks_width}×{blocks_height} @ {text_scale:g}"
        self.size_label.configure(text=f"{device_name}  •  {self.width} × {self.height}")

    def _redraw_cell(self, x, y):
        character, foreground, background = self.cells[y][x]
        self.canvas.itemconfigure(self.rect_items[y][x], fill=CC_COLORS[background][2])
        self.canvas.itemconfigure(self.text_items[y][x], text=character, fill=CC_COLORS[foreground][2])

    def _redraw_all(self):
        for y in range(self.height):
            for x in range(self.width):
                self._redraw_cell(x, y)

    def _validate_character_entry(self, _event=None):
        normalized = normalize_character(self.character.get())
        if self.character.get() != normalized:
            self.character.set(normalized)

    def _select_palette_color(self, index, forced_target=None):
        target = forced_target or self.palette_target.get()
        if target == "fg":
            self.selected_fg = index
        else:
            self.selected_bg = index
        self._refresh_palette_labels()

    def swap_colors(self):
        self.selected_fg, self.selected_bg = self.selected_bg, self.selected_fg
        self._refresh_palette_labels()

    def _refresh_palette_labels(self):
        fg = self._color_name(self.selected_fg)
        bg = self._color_name(self.selected_bg)
        self.color_label.configure(text=self._tr("foreground_background", fg=fg, bg=bg))

    def _cell_from_event(self, event):
        x = int(self.canvas.canvasx(event.x) // CELL_WIDTH)
        y = int(self.canvas.canvasy(event.y) // CELL_HEIGHT)
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        return None

    def _canvas_motion(self, event):
        position = self._cell_from_event(event)
        if position:
            x, y = position
            tool_name = self._tr(f"tool_{self.tool.get()}")
            self.status.set(self._tr("position", x=x + 1, y=y + 1, tool=tool_name))

    def _begin_action(self):
        if self.action_active:
            return
        self.undo_stack.append(self._snapshot())
        if len(self.undo_stack) > MAX_HISTORY:
            self.undo_stack.pop(0)
        self.redo_stack.clear()
        self.action_active = True

    def _finish_action(self):
        if not self.action_active:
            return
        self.action_active = False
        self.dirty = True
        self._update_title()
        self._refresh_code()

    def _canvas_press(self, event):
        position = self._cell_from_event(event)
        if not position:
            return
        x, y = position
        self.drag_start = position
        self.drag_last = None
        tool = self.tool.get()

        if tool == "picker":
            _char, self.selected_fg, self.selected_bg = self.cells[y][x]
            self.character.set(self.cells[y][x][0])
            self._refresh_palette_labels()
            return
        if tool == "text":
            value = simpledialog.askstring(
                self._tr("text_dialog_title"), self._tr("text_dialog_prompt"), parent=self.root
            )
            if value:
                self._begin_action()
                for offset, character in enumerate(value):
                    target_x = x + offset
                    if target_x >= self.width:
                        break
                    self.cells[y][target_x] = [normalize_character(character), self.selected_fg, self.selected_bg]
                    self._redraw_cell(target_x, y)
                self._finish_action()
            return
        if tool == "fill":
            self._begin_action()
            self._flood_fill(x, y)
            self._finish_action()
            return
        if tool == "select":
            self.selection = (x, y, x, y)
            self._draw_selection_overlay()
            return

        self._begin_action()
        if tool in ("brush", "solid", "eraser"):
            self._paint_cell(x, y, erase=tool == "eraser", solid=tool == "solid")
            self.drag_last = position

    def _canvas_drag(self, event):
        position = self._cell_from_event(event)
        if not position:
            return
        if self.tool.get() == "select" and self.drag_start:
            x1, y1 = self.drag_start
            self.selection = (min(x1, position[0]), min(y1, position[1]), max(x1, position[0]), max(y1, position[1]))
            self._draw_selection_overlay()
            return
        if not self.action_active or self.tool.get() not in ("brush", "solid", "eraser"):
            return
        if position == self.drag_last:
            return
        x, y = position
        self._paint_cell(
            x, y, erase=self.tool.get() == "eraser", solid=self.tool.get() == "solid"
        )
        self.drag_last = position

    def _canvas_release(self, event):
        if self.tool.get() == "select":
            self.drag_start = None
            self.drag_last = None
            return
        if not self.action_active:
            return
        tool = self.tool.get()
        if tool in ("rectangle", "line", "ellipse") and self.drag_start:
            end = self._cell_from_event(event) or self.drag_start
            if tool == "rectangle":
                self._draw_rectangle(self.drag_start, end)
            elif tool == "line":
                self._draw_line(self.drag_start, end)
            else:
                self._draw_ellipse(self.drag_start, end)
        self.drag_start = None
        self.drag_last = None
        self._finish_action()

    def _paint_cell(self, x, y, erase=False, solid=False):
        if erase:
            self.cells[y][x] = [" ", self.default_fg, self.default_bg]
        elif solid:
            self.cells[y][x] = [" ", self.selected_fg, self.selected_bg]
        else:
            self.cells[y][x] = [normalize_character(self.character.get()), self.selected_fg, self.selected_bg]
        self._redraw_cell(x, y)

    def _shape_character(self):
        return " " if self.solid_shapes.get() else normalize_character(self.character.get())

    def _put_shape_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = [self._shape_character(), self.selected_fg, self.selected_bg]
            self._redraw_cell(x, y)

    def _draw_rectangle(self, start, end):
        x1, x2 = sorted((start[0], end[0]))
        y1, y2 = sorted((start[1], end[1]))
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                border = x in (x1, x2) or y in (y1, y2)
                if self.filled_rectangle.get() or border:
                    self._put_shape_cell(x, y)

    def _draw_line(self, start, end):
        """Integer Bresenham line in terminal-cell coordinates."""
        x1, y1 = start
        x2, y2 = end
        dx, dy = abs(x2 - x1), -abs(y2 - y1)
        step_x = 1 if x1 < x2 else -1
        step_y = 1 if y1 < y2 else -1
        error = dx + dy
        while True:
            self._put_shape_cell(x1, y1)
            if x1 == x2 and y1 == y2:
                break
            doubled = 2 * error
            if doubled >= dy:
                error += dy
                x1 += step_x
            if doubled <= dx:
                error += dx
                y1 += step_y

    def _draw_ellipse(self, start, end):
        x1, x2 = sorted((start[0], end[0]))
        y1, y2 = sorted((start[1], end[1]))
        if x1 == x2 or y1 == y2:
            self._draw_line((x1, y1), (x2, y2))
            return
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        radius_x = (x2 - x1) / 2
        radius_y = (y2 - y1) / 2
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                normalized = ((x - center_x) / radius_x) ** 2 + ((y - center_y) / radius_y) ** 2
                if self.filled_rectangle.get():
                    draw = normalized <= 1.08
                else:
                    tolerance = max(0.16, 1.35 / max(radius_x, radius_y))
                    draw = abs(normalized - 1.0) <= tolerance
                if draw:
                    self._put_shape_cell(x, y)

    def _draw_selection_overlay(self):
        if self.selection_item is not None:
            self.canvas.delete(self.selection_item)
            self.selection_item = None
        if not self.selection:
            return
        x1, y1, x2, y2 = self.selection
        self.selection_item = self.canvas.create_rectangle(
            x1 * CELL_WIDTH + 1,
            y1 * CELL_HEIGHT + 1,
            (x2 + 1) * CELL_WIDTH - 1,
            (y2 + 1) * CELL_HEIGHT - 1,
            outline="#55dfbb",
            width=2,
            dash=(5, 3),
        )
        self.canvas.tag_raise(self.selection_item)

    def _selection_shortcut(self, _event, action):
        focus = self.root.focus_get()
        if isinstance(focus, (tk.Entry, tk.Text, ttk.Entry)):
            return None
        commands = {
            "copy": self.copy_selection,
            "cut": self.cut_selection,
            "paste": self.paste_selection,
            "delete": self.delete_selection,
        }
        commands[action]()
        return "break"

    def copy_selection(self):
        if not self.selection:
            self.status.set(self._tr("no_selection"))
            return False
        x1, y1, x2, y2 = self.selection
        self.cell_clipboard = [
            [self.cells[y][x][:] for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)
        ]
        self.status.set(self._tr("selection_copied"))
        return True

    def cut_selection(self):
        if not self.copy_selection():
            return
        self._begin_action()
        x1, y1, x2, y2 = self.selection
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.cells[y][x] = [" ", self.default_fg, self.default_bg]
                self._redraw_cell(x, y)
        self._finish_action()
        self._draw_selection_overlay()
        self.status.set(self._tr("selection_cut"))

    def paste_selection(self):
        if not self.cell_clipboard:
            self.status.set(self._tr("no_selection"))
            return
        start_x, start_y = (self.selection[0], self.selection[1]) if self.selection else (0, 0)
        self._begin_action()
        pasted_width = 0
        pasted_height = 0
        for offset_y, row in enumerate(self.cell_clipboard):
            y = start_y + offset_y
            if y >= self.height:
                break
            pasted_height += 1
            row_width = 0
            for offset_x, cell in enumerate(row):
                x = start_x + offset_x
                if x >= self.width:
                    break
                self.cells[y][x] = cell[:]
                self._redraw_cell(x, y)
                row_width += 1
            pasted_width = max(pasted_width, row_width)
        self._finish_action()
        if pasted_width and pasted_height:
            self.selection = (
                start_x,
                start_y,
                start_x + pasted_width - 1,
                start_y + pasted_height - 1,
            )
            self._draw_selection_overlay()
        self.status.set(self._tr("selection_pasted"))

    def delete_selection(self):
        if not self.selection:
            self.status.set(self._tr("no_selection"))
            return
        self._begin_action()
        x1, y1, x2, y2 = self.selection
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.cells[y][x] = [" ", self.default_fg, self.default_bg]
                self._redraw_cell(x, y)
        self._finish_action()
        self._draw_selection_overlay()
        self.status.set(self._tr("selection_deleted"))

    def _flood_fill(self, start_x, start_y):
        source = tuple(self.cells[start_y][start_x])
        # A paint bucket changes the complete terminal-cell background. Text is
        # deliberately removed, matching a conventional graphics editor.
        target = (" ", self.selected_fg, self.selected_bg)
        if source == target:
            return
        queue = deque([(start_x, start_y)])
        visited = {(start_x, start_y)}
        while queue:
            x, y = queue.popleft()
            if tuple(self.cells[y][x]) != source:
                continue
            self.cells[y][x] = list(target)
            self._redraw_cell(x, y)
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    def _snapshot(self):
        return {
            "width": self.width,
            "height": self.height,
            "device_profile": dict(self.device_profile),
            "default_fg": self.default_fg,
            "default_bg": self.default_bg,
            "cells": [[cell[:] for cell in row] for row in self.cells],
        }

    def _restore_snapshot(self, snapshot):
        size_changed = self.width != snapshot["width"] or self.height != snapshot["height"]
        self.width = snapshot["width"]
        self.height = snapshot["height"]
        self.device_profile = _normalise_device_profile(
            snapshot.get("device_profile"), self.width, self.height
        )
        self.default_fg = snapshot["default_fg"]
        self.default_bg = snapshot["default_bg"]
        self.cells = [[cell[:] for cell in row] for row in snapshot["cells"]]
        if size_changed:
            self._build_canvas_items()
        else:
            self._redraw_all()
        self.dirty = True
        self._update_title()
        self._refresh_code()

    def undo(self):
        if not self.undo_stack:
            return
        self.redo_stack.append(self._snapshot())
        self._restore_snapshot(self.undo_stack.pop())

    def redo(self):
        if not self.redo_stack:
            return
        self.undo_stack.append(self._snapshot())
        self._restore_snapshot(self.redo_stack.pop())

    def _on_code_modified(self, _event=None):
        if self._updating_code:
            self.code_text.edit_modified(False)
            return
        if not self.code_text.edit_modified():
            return
        self.code_text.edit_modified(False)
        if self._code_apply_after is not None:
            self.root.after_cancel(self._code_apply_after)
        self._code_apply_after = self.root.after(450, self.apply_code_from_editor)

    def apply_code_from_editor(self):
        self._code_apply_after = None
        source = self.code_text.get("1.0", "end-1c")
        if source == self._last_applied_code:
            return
        try:
            cells, default_fg, default_bg, command_count = parse_lua_design(
                source, self.width, self.height, self.default_fg, self.default_bg
            )
        except ValueError as error:
            self.status.set(self._tr("code_error", error=error))
            return
        if command_count == 0:
            self.status.set(self._tr("no_drawing_commands"))
            return

        changed = cells != self.cells or default_fg != self.default_fg or default_bg != self.default_bg
        if changed:
            self.undo_stack.append(self._snapshot())
            if len(self.undo_stack) > MAX_HISTORY:
                self.undo_stack.pop(0)
            self.redo_stack.clear()
            self.cells = cells
            self.default_fg = default_fg
            self.default_bg = default_bg
            self._redraw_all()
            self._draw_selection_overlay()
            self.dirty = True
            self._update_title()
        self._last_applied_code = source
        self.code_stats.set(self._tr("blit_stats", calls=command_count, chars=len(source)))
        self.status.set(self._tr("code_applied"))

    def _refresh_code(self):
        code, blit_count = generate_lua(
            self.cells, self.width, self.height, self.default_fg, self.default_bg,
            self.device_profile,
        )
        if self._code_apply_after is not None:
            self.root.after_cancel(self._code_apply_after)
            self._code_apply_after = None
        self._updating_code = True
        try:
            self.code_text.delete("1.0", "end")
            self.code_text.insert("1.0", code)
            self.code_text.edit_modified(False)
        finally:
            self._updating_code = False
        self._last_applied_code = self.code_text.get("1.0", "end-1c")
        self.code_stats.set(self._tr("blit_stats", calls=blit_count, chars=len(code)))
        return code

    def copy_lua(self):
        code = self._refresh_code()
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.root.update_idletasks()
        self.status.set(self._tr("copied"))

    def export_lua(self):
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title=self._tr("export_title"),
            defaultextension=".lua",
            filetypes=(("Lua", "*.lua"), ("Усі файли", "*.*")),
        )
        if path:
            with open(path, "w", encoding="utf-8", newline="\n") as file:
                file.write(self._refresh_code())
            self.status.set(self._tr("exported", path=path))

    def set_canvas_background(self):
        new_bg = self.selected_bg
        if new_bg == self.default_bg:
            return
        self._begin_action()
        old_bg = self.default_bg
        for row in self.cells:
            for cell in row:
                if cell[0] == " " and cell[2] == old_bg:
                    cell[2] = new_bg
        self.default_bg = new_bg
        self._redraw_all()
        self._finish_action()

    def clear_canvas(self):
        if not messagebox.askyesno(
            self._tr("clear_title"), self._tr("clear_prompt"), parent=self.root
        ):
            return
        self._begin_action()
        self.cells = self._blank_cells(self.width, self.height)
        self._redraw_all()
        self._finish_action()

    def _confirm_discard(self):
        if not self.dirty:
            return True
        answer = messagebox.askyesnocancel(
            self._tr("unsaved_title"),
            self._tr("unsaved_prompt"),
            parent=self.root,
        )
        if answer is None:
            return False
        if answer:
            return self.save_project()
        return True

    def new_project(self):
        if not self._confirm_discard():
            return
        dialog = NewCanvasDialog(
            self.root, self._tr, self.width, self.height, self.device_profile
        )
        self.root.wait_window(dialog)
        if dialog.result is None:
            return
        width, height, device_profile = dialog.result
        self.width, self.height = width, height
        self.device_profile = device_profile
        self.default_fg, self.default_bg = self.selected_fg, self.selected_bg
        self.cells = self._blank_cells(width, height)
        self.current_file = None
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.dirty = False
        self._build_canvas_items()
        self._update_title()
        self._refresh_code()

    def save_project(self):
        path = self.current_file
        if not path:
            path = filedialog.asksaveasfilename(
                parent=self.root,
                title=self._tr("save_project_title"),
                defaultextension=PROJECT_EXTENSION,
                filetypes=(("CC UI project", f"*{PROJECT_EXTENSION}"), ("JSON", "*.json")),
            )
        if not path:
            return False
        data = self._snapshot()
        data["format"] = "cc-tweaked-ui-editor-v1"
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, separators=(",", ":"))
        self.current_file = path
        self.dirty = False
        self._update_title()
        self.status.set(self._tr("saved", path=path))
        return True

    def open_project(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            parent=self.root,
            title=self._tr("open_project_title"),
            filetypes=(("CC UI project", f"*{PROJECT_EXTENSION}"), ("JSON", "*.json"), ("Усі файли", "*.*")),
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            self._validate_project(data)
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                self._tr("error"), self._tr("open_error", error=error), parent=self.root
            )
            return
        self.width = data["width"]
        self.height = data["height"]
        self.device_profile = data["device_profile"]
        self.default_fg = data["default_fg"]
        self.default_bg = data["default_bg"]
        self.cells = data["cells"]
        self.current_file = path
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.dirty = False
        self._build_canvas_items()
        self._update_title()
        self._refresh_code()
        self.status.set(self._tr("opened", path=path))

    def _validate_project(self, data):
        width = int(data["width"])
        height = int(data["height"])
        if not 1 <= width <= 200 or not 1 <= height <= 100:
            raise ValueError(self._tr("invalid_size"))
        if len(data["cells"]) != height or any(len(row) != width for row in data["cells"]):
            raise ValueError(self._tr("invalid_data_size"))
        for row in data["cells"]:
            for cell in row:
                if len(cell) != 3 or not 0 <= int(cell[1]) <= 15 or not 0 <= int(cell[2]) <= 15:
                    raise ValueError(self._tr("invalid_cell"))
                cell[0] = normalize_character(str(cell[0]))
                cell[1] = int(cell[1])
                cell[2] = int(cell[2])
        data["width"], data["height"] = width, height
        data["device_profile"] = _normalise_device_profile(
            data.get("device_profile"), width, height
        )
        data["default_fg"] = int(data["default_fg"])
        data["default_bg"] = int(data["default_bg"])

    def _update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else self._tr("new_project")
        marker = " *" if self.dirty else ""
        self.root.title(f"{name}{marker} — {APP_NAME}")

    def _on_close(self):
        if self._confirm_discard():
            self.root.destroy()


def main():
    root = tk.Tk()
    UIEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
