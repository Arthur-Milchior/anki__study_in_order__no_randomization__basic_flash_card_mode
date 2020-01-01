from anki.hooks import addHook, wrap
from anki.lang import getLang
from anki.sched import Scheduler as schedv1
from anki.schedv2 import Scheduler as schedv2
from anki.utils import ids2str, intTime


import aqt
from aqt import mw
from aqt.utils import showInfo, tooltip
from aqt.qt import *


from .config import gc, onMySettings
from .texts import t



def add_same_day_spacing_to_menu():
    # must be loaded after load_global_setting
    menu = None
    for a in mw.form.menubar.actions():
        if t.menu == a.text():
            menu=a.menu()
            menu.addSeparator()
            break
    if not menu:
        menu=mw.form.menubar.addMenu(t.menu)
    a = menu.addAction(t.menu_entry)
    a.triggered.connect(onMySettings)
addHook('profileLoaded', add_same_day_spacing_to_menu)
