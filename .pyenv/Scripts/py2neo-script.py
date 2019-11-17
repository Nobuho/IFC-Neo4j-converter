#!c:\_python\191111_ifcandneo4j\.pyenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'py2neo==4.3.0','console_scripts','py2neo'
__requires__ = 'py2neo==4.3.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('py2neo==4.3.0', 'console_scripts', 'py2neo')()
    )
