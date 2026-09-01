"""Finished launcher for the CC:Tweaked UI Editor.

This module keeps the original editor implementation intact and applies the
remaining device/monitor fixes before starting the application.
"""

from __future__ import annotations

import importlib.util
import os
import tkinter as tk
from importlib.machinery import SourceFileLoader
from tkinter import messagebox


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_PATH = os.path.join(BASE_DIR, "cc_terminal_ui_editor.pyw")

loader = SourceFileLoader("cc_terminal_ui_editor_core", CORE_PATH)
spec = importlib.util.spec_from_loader(loader.name, loader)
if spec is None:
    raise RuntimeError("Could not load CC:Tweaked UI Editor core")
core = importlib.util.module_from_spec(spec)
loader.exec_module(core)


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
