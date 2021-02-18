import subprocess
from pathlib import Path
import platform

base_batch_script = r"""
@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "{dest}\{command}.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "{command}" >> %SCRIPT%
echo oLink.Arguments = "{args}" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%
"""


def create_shortcut(dest: Path, command: str, args: str = ''):
    """
    A minimal function that creates a shortcut at the given destination

    :supports: Windows

    :param dest: shortcut destination directory
    :param command: shortcut command, maybe a file or callable command
    :param args: commandline arguments
    :return: None
    """
    if platform.system() == 'Windows':
        script = base_batch_script.format(dest=str(dest), command=command, args=args)

        # create temp bat file
        script_file = Path.home() / '.qrshare_shortcut_script.bat'
        with script_file.open('w') as f:
            f.write(script)

        subprocess.run(str(script_file), stdout=subprocess.PIPE)

        # delete temp batch file
        script_file.unlink()
    else:
        raise Exception(f'{platform.system()} is not supported')
