# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\zsz\\ML\\code\\database\\PycharmProjects\\oracle\\unload_dbf\\ui_unload.py'],
             pathex=['C:\\zsz\\ML\\code\\database\\PycharmProjects\\oracle\\unload_dbf'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui_unload',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
