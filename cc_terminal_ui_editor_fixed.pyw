"""Finished launcher for the CC:Tweaked UI Editor.

This module keeps the original editor implementation intact and applies the
remaining device/monitor fixes plus the finished application theme before
starting the editor.
"""

from __future__ import annotations

import importlib.util
import os
import tkinter as tk
from importlib.machinery import SourceFileLoader
from tkinter import messagebox, ttk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_PATH = os.path.join(BASE_DIR, "cc_terminal_ui_editor.pyw")

loader = SourceFileLoader("cc_terminal_ui_editor_core", CORE_PATH)
spec = importlib.util.spec_from_loader(loader.name, loader)
if spec is None:
    raise RuntimeError("Could not load CC:Tweaked UI Editor core")
core = importlib.util.module_from_spec(spec)
loader.exec_module(core)


# ---------------------------------------------------------------------------
# Finished dark UI theme
# ---------------------------------------------------------------------------

def _apply_finished_theme(root: tk.Tk):
    """Apply one coherent dark theme to every ttk control used by the editor."""
    colors = {
        "window": "#0b1016",
        "panel": "#111923",
        "toolbar": "#0f1720",
        "field": "#0a1017",
        "field_disabled": "#101821",
        "hover": "#253545",
        "pressed": "#18232e",
        "border": "#263647",
        "border_soft": "#202d3b",
        "text": "#dce7f2",
        "text_bright": "#eef5fb",
        "muted": "#8092a5",
        "accent": "#3dd6b0",
        "accent_hover": "#62e2c2",
        "accent_pressed": "#2cb08f",
        "accent_dark": "#07140f",
        "selection": "#285e55",
        "scroll_thumb": "#26384a",
        "scroll_hover": "#3b5268",
        "trough": "#090d12",
    }

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    # Native Tk popup parts used by ttk.Combobox are not controlled by ttk
    # styles, so finish them through the option database as well.
    root.option_add("*TCombobox*Listbox.background", colors["field"])
    root.option_add("*TCombobox*Listbox.foreground", colors["text"])
    root.option_add("*TCombobox*Listbox.selectBackground", colors["selection"])
    root.option_add("*TCombobox*Listbox.selectForeground", colors["text_bright"])
    root.option_add("*TCombobox*Listbox.borderWidth", 0)
    root.option_add("*TCombobox*Listbox.relief", "flat")
    root.option_add("*Menu.background", colors["panel"])
    root.option_add("*Menu.foreground", colors["text"])
    root.option_add("*Menu.activeBackground", colors["hover"])
    root.option_add("*Menu.activeForeground", colors["text_bright"])
    root.option_add("*Menu.borderWidth", 0)
    root.option_add("*selectBackground", colors["selection"])
    root.option_add("*selectForeground", colors["text_bright"])

    style.configure(
        ".",
        font=("Segoe UI", 10),
        background=colors["window"],
        foreground=colors["text"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        focuscolor=colors["accent"],
    )

    # Frames, labels and separators.
    style.configure("TFrame", background=colors["window"])
    style.configure("Card.TFrame", background=colors["panel"])
    style.configure("Toolbar.TFrame", background=colors["toolbar"])
    style.configure("TLabel", background=colors["window"], foreground=colors["text"])
    style.configure("Card.TLabel", background=colors["panel"], foreground=colors["text"])
    style.configure(
        "Section.TLabel",
        background=colors["panel"],
        foreground="#74879a",
        font=("Segoe UI Semibold", 9),
    )
    style.configure(
        "Title.TLabel",
        background=colors["toolbar"],
        foreground="#f4f8fb",
        font=("Segoe UI Semibold", 18),
    )
    style.configure(
        "Subtitle.TLabel",
        background=colors["toolbar"],
        foreground="#73869a",
        font=("Segoe UI", 9),
    )
    style.configure("TSeparator", background=colors["border_soft"])

    # Buttons.
    style.configure(
        "TButton",
        background="#1b2734",
        foreground=colors["text"],
        borderwidth=0,
        relief="flat",
        padding=(11, 7),
        focusthickness=1,
        focuscolor=colors["accent"],
    )
    style.map(
        "TButton",
        background=[
            ("disabled", "#131c25"),
            ("pressed", colors["pressed"]),
            ("active", colors["hover"]),
        ],
        foreground=[("disabled", "#526274"), ("!disabled", colors["text"])],
    )
    style.configure(
        "Accent.TButton",
        background=colors["accent"],
        foreground=colors["accent_dark"],
        borderwidth=0,
        relief="flat",
        font=("Segoe UI Semibold", 10),
        padding=(13, 7),
        focusthickness=1,
        focuscolor=colors["accent_hover"],
    )
    style.map(
        "Accent.TButton",
        background=[
            ("disabled", "#285448"),
            ("pressed", colors["accent_pressed"]),
            ("active", colors["accent_hover"]),
        ],
        foreground=[("disabled", "#78938b"), ("!disabled", colors["accent_dark"])],
    )

    # Entries.
    style.configure(
        "TEntry",
        fieldbackground=colors["field"],
        background=colors["field"],
        foreground=colors["text_bright"],
        insertcolor=colors["text_bright"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        relief="flat",
        borderwidth=1,
        padding=7,
    )
    style.map(
        "TEntry",
        fieldbackground=[("disabled", colors["field_disabled"]), ("!disabled", colors["field"])],
        foreground=[("disabled", "#5f7082"), ("!disabled", colors["text_bright"])],
        bordercolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        lightcolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        darkcolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
    )

    # Comboboxes, including the arrow and readonly/disabled states.
    style.configure(
        "TCombobox",
        fieldbackground=colors["field"],
        background="#182431",
        foreground=colors["text_bright"],
        arrowcolor=colors["muted"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        relief="flat",
        borderwidth=1,
        padding=6,
        arrowsize=14,
    )
    style.map(
        "TCombobox",
        fieldbackground=[
            ("disabled", colors["field_disabled"]),
            ("readonly", colors["field"]),
            ("!disabled", colors["field"]),
        ],
        background=[
            ("disabled", "#131c25"),
            ("pressed", colors["pressed"]),
            ("active", colors["hover"]),
            ("readonly", "#182431"),
        ],
        foreground=[("disabled", "#5f7082"), ("!disabled", colors["text_bright"])],
        arrowcolor=[
            ("disabled", "#4e5e6f"),
            ("active", colors["accent"]),
            ("!disabled", colors["muted"]),
        ],
        bordercolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        lightcolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        darkcolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        selectbackground=[("readonly", colors["field"])],
        selectforeground=[("readonly", colors["text_bright"])],
    )

    # Spinboxes and their up/down arrow buttons.
    style.configure(
        "TSpinbox",
        fieldbackground=colors["field"],
        background="#182431",
        foreground=colors["text_bright"],
        arrowcolor=colors["muted"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        relief="flat",
        borderwidth=1,
        padding=6,
        arrowsize=12,
    )
    style.map(
        "TSpinbox",
        fieldbackground=[("disabled", colors["field_disabled"]), ("!disabled", colors["field"])],
        background=[
            ("disabled", "#131c25"),
            ("pressed", colors["pressed"]),
            ("active", colors["hover"]),
            ("!disabled", "#182431"),
        ],
        foreground=[("disabled", "#5f7082"), ("!disabled", colors["text_bright"])],
        arrowcolor=[
            ("disabled", "#4e5e6f"),
            ("active", colors["accent"]),
            ("!disabled", colors["muted"]),
        ],
        bordercolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        lightcolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
        darkcolor=[("focus", colors["accent"]), ("!focus", colors["border"])],
    )

    # Checkboxes and radio buttons.
    style.configure(
        "TCheckbutton",
        background=colors["panel"],
        foreground=colors["text"],
        indicatorbackground=colors["field"],
        indicatorforeground=colors["accent"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        padding=(2, 3),
    )
    style.map(
        "TCheckbutton",
        background=[("active", "#172330")],
        foreground=[("disabled", "#5f7082"), ("selected", colors["accent"])],
        indicatorbackground=[
            ("disabled", "#151e27"),
            ("selected", colors["accent"]),
            ("!selected", colors["field"]),
        ],
        indicatorforeground=[("selected", colors["accent_dark"])],
    )
    style.configure(
        "TRadiobutton",
        background=colors["panel"],
        foreground=colors["text"],
        indicatorbackground=colors["field"],
        indicatorforeground=colors["accent"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        padding=(2, 3),
    )
    style.map(
        "TRadiobutton",
        background=[("active", "#172330")],
        foreground=[("disabled", "#5f7082"), ("selected", colors["accent"])],
        indicatorbackground=[
            ("disabled", "#151e27"),
            ("selected", colors["accent"]),
            ("!selected", colors["field"]),
        ],
    )
    style.configure(
        "Tool.TRadiobutton",
        background=colors["panel"],
        foreground=colors["text"],
        indicatorbackground=colors["field"],
        indicatorforeground=colors["accent"],
        bordercolor=colors["border"],
        padding=(7, 7),
    )
    style.map(
        "Tool.TRadiobutton",
        background=[("active", "#172330"), ("selected", "#142a2a")],
        foreground=[("disabled", "#5f7082"), ("selected", colors["accent"])],
        indicatorbackground=[
            ("selected", colors["accent"]),
            ("!selected", colors["field"]),
        ],
    )

    # Scrollbars: custom trough, thumb, hover and pressed states. These are the
    # most visible previously-unfinished slider-like controls in the editor.
    for scrollbar_style in ("Vertical.TScrollbar", "Horizontal.TScrollbar", "TScrollbar"):
        style.configure(
            scrollbar_style,
            background=colors["scroll_thumb"],
            troughcolor=colors["trough"],
            bordercolor=colors["trough"],
            lightcolor=colors["scroll_thumb"],
            darkcolor=colors["scroll_thumb"],
            arrowcolor=colors["muted"],
            relief="flat",
            borderwidth=0,
            arrowsize=12,
            width=14,
        )
        style.map(
            scrollbar_style,
            background=[
                ("disabled", "#17202a"),
                ("pressed", colors["accent_pressed"]),
                ("active", colors["scroll_hover"]),
            ],
            arrowcolor=[
                ("disabled", "#3d4a58"),
                ("active", colors["accent"]),
                ("!disabled", colors["muted"]),
            ],
            lightcolor=[
                ("pressed", colors["accent_pressed"]),
                ("active", colors["scroll_hover"]),
            ],
            darkcolor=[
                ("pressed", colors["accent_pressed"]),
                ("active", colors["scroll_hover"]),
            ],
        )

    # Scale widgets are not currently prominent in the UI, but style both
    # orientations so every present/future slider follows the same theme.
    for scale_style in ("Horizontal.TScale", "Vertical.TScale", "TScale"):
        style.configure(
            scale_style,
            background=colors["panel"],
            troughcolor="#172330",
            bordercolor=colors["border"],
            lightcolor=colors["accent"],
            darkcolor=colors["accent"],
            sliderrelief="flat",
        )
        style.map(
            scale_style,
            background=[
                ("disabled", "#26313b"),
                ("pressed", colors["accent_pressed"]),
                ("active", colors["accent_hover"]),
                ("!disabled", colors["accent"]),
            ],
        )

    # Paned-window sashes, notebook tabs, progress bars, tree views and menu
    # buttons are also themed so no ttk control falls back to the OS defaults.
    style.configure(
        "TPanedwindow",
        background=colors["window"],
        sashwidth=8,
        sashrelief="flat",
    )
    style.configure("Sash", background=colors["border_soft"], relief="flat")
    style.map("Sash", background=[("active", colors["accent_pressed"])])

    style.configure("TNotebook", background=colors["window"], borderwidth=0, tabmargins=(0, 0, 0, 0))
    style.configure(
        "TNotebook.Tab",
        background="#16212c",
        foreground=colors["muted"],
        padding=(12, 7),
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", "#1c2a36"), ("active", colors["hover"])],
        foreground=[("selected", colors["accent"]), ("active", colors["text_bright"])],
    )

    style.configure(
        "TProgressbar",
        background=colors["accent"],
        troughcolor=colors["trough"],
        bordercolor=colors["trough"],
        lightcolor=colors["accent"],
        darkcolor=colors["accent"],
        borderwidth=0,
    )
    style.configure(
        "Treeview",
        background=colors["field"],
        fieldbackground=colors["field"],
        foreground=colors["text"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        rowheight=25,
        borderwidth=1,
    )
    style.map(
        "Treeview",
        background=[("selected", colors["selection"])],
        foreground=[("selected", colors["text_bright"])],
    )
    style.configure(
        "Treeview.Heading",
        background="#182431",
        foreground=colors["text"],
        bordercolor=colors["border"],
        relief="flat",
        padding=(8, 6),
        font=("Segoe UI Semibold", 9),
    )
    style.map("Treeview.Heading", background=[("active", colors["hover"])])

    style.configure(
        "TMenubutton",
        background="#1b2734",
        foreground=colors["text"],
        arrowcolor=colors["muted"],
        borderwidth=0,
        relief="flat",
        padding=(10, 6),
    )
    style.map(
        "TMenubutton",
        background=[("pressed", colors["pressed"]), ("active", colors["hover"])],
        arrowcolor=[("active", colors["accent"])],
    )
    style.configure("TSizegrip", background=colors["window"])

    style.configure(
        "Panel.TLabelframe",
        background=colors["panel"],
        bordercolor=colors["border_soft"],
        lightcolor=colors["border_soft"],
        darkcolor=colors["border_soft"],
        relief="solid",
        padding=10,
    )
    style.configure(
        "Panel.TLabelframe.Label",
        background=colors["panel"],
        foreground="#74879a",
        font=("Segoe UI Semibold", 9),
    )


_original_configure_window = core.UIEditor._configure_window


def _configure_window(self):
    _original_configure_window(self)
    _apply_finished_theme(self.root)


core.UIEditor._configure_window = _configure_window


# ---------------------------------------------------------------------------
# Monitor export and New Canvas fixes
# ---------------------------------------------------------------------------

# Preserve the compact exporter for normal computer/turtle/pocket terminals,
# but force monitor exports to use explicit monitor.blit calls. paintutils
# draws through term.current(), so the original compact shape exporter could
# accidentally draw rectangles on the computer terminal instead of the
# selected external monitor.
_original_generate_lua = core.generate_lua


def _generate_lua(cells, width, height, default_fg, default_bg, device_profile=None):
    profile = device_profile or {"type": "computer"}
    if profile.get("type") == "monitor":
        return core._row_blit_program(
            cells, width, height, default_fg, default_bg, profile
        )
    return _original_generate_lua(
        cells, width, height, default_fg, default_bg, profile
    )


core.generate_lua = _generate_lua


# Finish the New Canvas monitor integration. The original implementation had
# the correct CC:Tweaked monitor-size formula, but did not recalculate the
# character grid immediately when switching to External monitor and allowed a
# stale width/height to be accepted.
def _recalculate_monitor_dimensions(self):
    try:
        blocks_width = int(self.blocks_width_var.get())
        blocks_height = int(self.blocks_height_var.get())
        text_scale = float(self.scale_var.get())
    except (tk.TclError, ValueError):
        return False

    if not 1 <= blocks_width <= 8 or not 1 <= blocks_height <= 6:
        return False
    if text_scale not in core.MONITOR_TEXT_SCALES:
        return False

    width, height = core.monitor_terminal_size(
        blocks_width, blocks_height, text_scale
    )
    self._updating_dimensions = True
    try:
        self.width_var.set(width)
        self.height_var.set(height)
    finally:
        self._updating_dimensions = False
    return True


_original_apply_device_type = core.NewCanvasDialog._apply_device_type
_original_accept = core.NewCanvasDialog._accept


def _apply_device_type(self, initial=False):
    _original_apply_device_type(self, initial)
    if self._current_type() == "monitor":
        _recalculate_monitor_dimensions(self)
        self._refresh_summary()


def _values_changed(self, *_args):
    if self._updating_dimensions:
        return
    if self._current_type() == "monitor":
        _recalculate_monitor_dimensions(self)
    self._refresh_summary()


def _accept(self):
    if self._current_type() == "monitor" and not _recalculate_monitor_dimensions(self):
        messagebox.showerror(
            self._tr("error"), self._tr("invalid_size"), parent=self
        )
        return
    _original_accept(self)


core.NewCanvasDialog._recalculate_monitor_dimensions = _recalculate_monitor_dimensions
core.NewCanvasDialog._apply_device_type = _apply_device_type
core.NewCanvasDialog._values_changed = _values_changed
core.NewCanvasDialog._accept = _accept


if __name__ == "__main__":
    core.main()
