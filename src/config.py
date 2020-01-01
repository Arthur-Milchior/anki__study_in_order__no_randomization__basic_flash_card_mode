from collections import OrderedDict
from pprint import pprint as pp

from anki.hooks import addHook

from aqt import mw
from aqt.qt import *
from aqt.utils import (
    showInfo,
    tooltip
)

from .checkdialog import CheckDialog
from .forms import configdialog
from .texts import t


def gc(arg, fail=False):
    return mw.addonManager.getConfig(__name__).get(arg, fail)


def wc(arg, val):
    config = mw.addonManager.getConfig(__name__)
    config[arg] = val
    mw.addonManager.writeConfig(__name__, config)


def installtime():
    addon = mw.addonManager.addonFromModule(__name__)
    meta = mw.addonManager.addonMeta(addon)
    return meta["mod"]


setting_to_override = {
    "rev": gc("rev_overrides"),
    "revorder": gc("revorder_overrides"),
    "new": gc("new_overrides"),
    "nofuzz": gc("nofuzz_overrides"),
}


def apply_setting(setting, carddid):
    ubi = True  # use-built-in
    if gc(setting):
        ubi ^= True
    if carddid in setting_to_override[setting]:
        ubi ^= True
    if not ubi:
        return True


def get_did_even_if_in_filtered(card):
    if hasattr(card, "odid") and card.odid:
        did = card.odid
    else:
        did = card.did
    return did


class MyConfigWindow(QDialog):
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = configdialog.Ui_Dialog()
        self.dialog.setupUi(self)
        self.setWindowTitle(t.config_windowtitle)
        self.applylabels()
        self.setbuttons()
        self.loadstate()

    def applylabels(self):
        # rich text didn't work in checkbox
        self.dialog.l_new.setText(t.config_new_cb_label)
        self.dialog.pb_new.setText(t.config_new_pb_label)
        self.dialog.l_rev.setText(t.config_rev_cb_label)
        self.dialog.pb_rev.setText(t.config_rev_pb_label)
        self.dialog.l_revorder.setText(t.config_revorder_cb_label)
        self.dialog.pb_revorder.setText(t.config_revorder_pb_label)
        self.dialog.l_fuzz.setText(t.config_fuzz_cb_label)
        self.dialog.pb_fuzz.setText(t.config_fuzz_pb_label)
        self.dialog.l_new.setWordWrap(True)
        self.dialog.l_rev.setWordWrap(True)
        self.dialog.l_revorder.setWordWrap(True)
        self.dialog.l_fuzz.setWordWrap(True)
        # TODO: update help texts
        self.dialog.pb_new_help.hide()
        self.dialog.pb_rev_help.hide()
        self.dialog.pb_revorder_help.hide()
        self.dialog.pb_fuzz_help.hide()
                
    def loadstate(self):
        self.dialog.cb_new.setChecked(gc("new"))
        self.dialog.cb_rev.setChecked(gc("rev"))
        self.dialog.cb_revorder.setChecked(gc("revorder"))
        self.dialog.cb_fuzz.setChecked(gc("nofuzz"))
        self.new_overrides = gc("new_overrides")
        self.nofuzz_overrides = gc("nofuzz_overrides")
        self.rev_overrides = gc("rev_overrides")
        self.revorder_overrides = gc("revorder_overrides")

    def setbuttons(self):
        # don't hide third option so that I can still set Deck overrides
        # self.dialog.cb_rev.stateChanged.connect(self.onCbRevChange)
        # if not gc("rev"):
        #     self.dialog.widget.setVisible(False)
        self.dialog.pb_new.clicked.connect(lambda: self.set_deck_overrides(self.new_overrides))
        self.dialog.pb_rev.clicked.connect(lambda: self.set_deck_overrides(self.rev_overrides))
        self.dialog.pb_revorder.clicked.connect(lambda: self.set_deck_overrides(self.revorder_overrides))
        self.dialog.pb_fuzz.clicked.connect(lambda: self.set_deck_overrides(self.nofuzz_overrides))
        self.dialog.pb_new_help.clicked.connect(lambda: showInfo(t.config_new_help))
        self.dialog.pb_rev_help.clicked.connect(lambda: showInfo(t.config_rev_help))
        self.dialog.pb_revorder_help.clicked.connect(lambda: showInfo(t.config_revorder_help))
        self.dialog.pb_fuzz_help.clicked.connect(lambda: showInfo(t.config_fuzz_help))  

    # def onCbRevChange(self):
    #     if self.dialog.cb_rev.isChecked():
    #         # self.dialog.cb_revorder.setDisabled(False) # hardly noticeable
    #         self.dialog.widget.setVisible(True)
    #     else:
    #         # self.dialog.cb_revorder.setDisabled(True)
    #         self.dialog.widget.setVisible(False)

    def set_deck_overrides(self, list_):
        decks_and_their_state = OrderedDict()
        for n in sorted(mw.col.decks.allNames(dyn=False)):
            did = mw.col.decks.byName(n)["id"]
            decks_and_their_state[n] = True if did in list_ else False
        d = CheckDialog(parent=None,
                        valuedict=decks_and_their_state,
                        windowtitle=t.deck_selector_window_title,
                        text=t.deck_selector_text)
        if d.exec():
            for name, val in d.valuedict.items():
                if val:
                    list_.append(mw.col.decks.byName(name)["id"])

    def accept(self):
        self.config = {
            "new": self.dialog.cb_new.isChecked(),
            "new_overrides": self.new_overrides,
            "nofuzz": self.dialog.cb_fuzz.isChecked(),
            "nofuzz_overrides": self.nofuzz_overrides,
            "rev": self.dialog.cb_rev.isChecked(),
            "rev_overrides": self.rev_overrides,
            "revorder": self.dialog.cb_revorder.isChecked(),
            "revorder_overrides": self.revorder_overrides,
        }
        QDialog.accept(self)


fuzz_incompatible_addons = {
    "175851166": "Agent Orange Pseudo-Fuzz Defoliator",
    "2092706270": "DeFuzz Quick Effective Trimming",
    "1334482773": "No Fuzz Whatsoever",
    "1417170896": "load balancer",
    "208879074": "Load Balanced Scheduler",
}


def check_for_nofuzz_incompatible_addons(conflictmessage, simplemessage):
    aa = mw.addonManager.allAddons()
    install_conflict = []
    if gc("nofuzz") or len(gc("nofuzz_overrides")):
        for e in aa:
            known = gc("known_conflicting_addons")[:]
            if e in fuzz_incompatible_addons and e not in known:
                install_conflict.append(e)
                known.append(e)
            wc("known_conflicting_addons", known)
        if len(install_conflict):
            names = [fuzz_incompatible_addons[i] for i in install_conflict]
            if len(names) > 1:
                namestr = "       " + ",\n       ".join(names[:-1]) + names[-1]
            else:
                namestr = "       " + names[0]
            showInfo(conflictmessage % namestr)
        elif simplemessage:
            showInfo(simplemessage)
check_for_nofuzz_incompatible_addons(t.warn_about_fuzz_conflict_at_startup, False)


def onMySettings():
    dialog = MyConfigWindow(mw, mw.addonManager.getConfig(__name__))
    if dialog.exec_():
        mw.addonManager.writeConfig(__name__, dialog.config)
        mw.col.reset()
        if dialog.config["nofuzz"] or len(dialog.config["nofuzz_overrides"]):
            # warn about possible incompatitiblites with other add-ons
            check_for_nofuzz_incompatible_addons(t.warn_about_fuzz_conflict, t.warn_about_fuzz_general)
mw.addonManager.setConfigAction(__name__, onMySettings)
