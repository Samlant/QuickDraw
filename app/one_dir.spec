# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
PyInstaller.config.CONF['distpath'] = "../../pkging/dist"

block_cipher = None
python_module_dirs = [
        '..\\..\\..\\..\\virtualenvs\\QuickDraw\\Lib\\site-packages', 
        '.\\model',
        '.\\model\\api',
        '.\\model\\api\\ms_graph',
        '.\\model\\api\\ms_graph\\utils',
        '.\\model\\api\\ms_graph\\workbooks_and_charts',
        '.\\model\\dir_handler',
        '.\\model\\email',
        '.\\model\\base_model.py',
        '.\\presenter',
        '.\\view',
        '.',
    ]

a = Analysis(
    ['app.py'],
    pathex=python_module_dirs,
    binaries=[],
    datas=[
        ('.\\resources\\img\\app.ico', '.\\resources\\img'),
        ('.\\resources\\img\\sys_tray.ico', '.\\resources\\img'),
        ],
    hiddenimports=[],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += Tree('..\\docs\\site', prefix='.\\resources\\docs')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QuickDraw',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\img\\app.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QuickDraw',
)