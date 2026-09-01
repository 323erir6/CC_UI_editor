# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['cc_terminal_ui_editor_fixed.pyw'],
    pathex=[],
    binaries=[],
    datas=[('cc_terminal_ui_editor.pyw', '.')],
    hiddenimports=[
        'ast',
        'json',
        'math',
        're',
        'collections',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CC_Terminal_UI_Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
