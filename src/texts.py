from types import SimpleNamespace

from anki.lang import getLang


if getLang().startswith("de"):
    LANG = "de"
else:
    LANG = "en"

at = {}
at["menu"] = {
    "en": "&Study",
    "de": "&Lernen",
}

at["menu_entry"] = {
    "en": 'adjust card order add-on',
    "de": 'Kartenreihenfolgen-Add-on anpassen',
}

at["startup_reminder"] = {
    "en": 'Info: the add-on "modify sibling spacing and review order" is globally enabled',
    "de": ('Zur Erinnerung: Die Erweiterung "modify sibling spacing and review order" ist '
           'als Voreinstellung aktiviert'),
}

at["menu_toggle"] = {
    "en": ("Option has been activated! Sibling Cards (= cards belonging to the same note) "
        "will now always be asked right after each other<br><br>"
        "To put the review of specific "
        'cards off until tomorrow press the "-"-key when you are asked about them. '
        "This makes sense in situations where you've just been asked: \"What does 'Kuchen' "
        "mean in Englisch?\" And the next question is: \"What does 'cake' mean in "
        "German?\"<br><br>"
        "More information about this option can be found on the page "
        "<a href=\"https://ankiweb.net/shared/info/268644742\">"
        "of the corresponding Anki-Add-On</a>."),
    "de": ("Option aktiviert! Karten, die zu derselben Notiz gehören, werden "
        "jetzt immer unmittelbar nacheinander abgefragt...<br><br>"
        "Um bestimmte einzelne Karten erst morgen abfragen zu lassen, kannst du, "
        "wenn du danach gefragt wirst, einfach die \"-\"-Taste (Bindestrich-Taste) "
        "auf deiner Tastatur drücken. Das ist z.B. sinnvoll, wenn du gerade gefragt "
        "wurdest: \"Was heißt 'Kuchen' auf Englisch?\" Und dann direkt danach: \"Was "
        "bedeutet 'cake' auf Deutsch?\"<br><br>Weitere Infos zu dieser Funktion findest "
        "du auf der Seite <a href=\"https://ankiweb.net/shared/info/268644742\">des "
        "dazugehörigen Anki-Addons</a>."),
}

at["config_windowtitle"] = {
    "en": "Anki Add-on config",
    "de": "Anki Erweiterung Konfiguration",
}


at["config_new_cb_label"] = {
    "en": "show <b>new</b> sibling cards in order <i>by default</i>",
    "de": ("Fällige, verwandte <b>neue</b> Karten <i>standardmäßig</i> in aufsteigender ",
          "Reihenfolge anzeigen"),
}
at["config_new_pb_label"] = {
    "en": "Exceptions for certain decks",
    "de": "Ausnahmen für einzelne Decks festlegen",
}
at["config_new_help"] = {
    "en": "the next version will contain a help text in this place.",
    "de": "Hilfstext - neue",
}


at["config_rev_cb_label"] = {
    "en": ("show due <b>review</b> sibling cards in order <i>by default</i>"
          ),
    "de": ("Fällige, verwandte <b>Wiederholungs</b>-Karten <i>standardmäßig</i> "
           "in aufsteigender Reihenfolge anzeigen"
           ),
}
at["config_rev_pb_label"] = {
    "en": "Exceptions for certain decks",
    "de": "Ausnahmen für einzelne Decks festlegen",
}
at["config_rev_help"] = {
    "en": "the next version will contain a help text in this place.",
    "de": "Hilfstext - rev",
}


at["config_revorder_cb_label"] = {
    "en": ("order due <b>review</b> cards by creation time by <i>default</i>"
           "<br>This setting only has an effect if the prior setting "
           "\"show due review sibling cards in order\" is also enabled"),
    "de": ("Fällige <b>Wiederholungs</b>-Karten <i>standardmäßig</i> sortieren: alte "
           "zuerst anzeigen<br>Diese Einstellung entfaltet nur dann Wirkung, wenn auch die ",
           "vorherige Einstellung \"Fällige, verwandte Wiederholungs-Karten "
           "in aufsteigender Reihenfolge anzeigen\" aktiiert ist."),
}
at["config_revorder_pb_label"] = {
    "en": "Exceptions for certain decks",
    "de": "Ausnahmen für einzelne Decks festlegen",
}
at["config_revorder_help"] = {
    "en": "the next version will contain a help text in this place.",
    "de": "Hilfstext - revorder",
}


at["config_fuzz_cb_label"] = {
    "en": "After rating a card <b>don't</b> add fuzz/randomization to the intervals",
    "de": ("Nach einer Wertung nächstes Intervall <b>nicht</b> etwas randomisieren, "
          "d.h. fixe Intervalle nutzen"),
}
at["config_fuzz_pb_label"] = {
    "en": "Exceptions for certain decks",
    "de": "Ausnahmen für einzelne Decks festlegen"
}
at["config_fuzz_help"] = {
    "en": "the next version will contain a help text in this place.",
    "de": "Hilfstext - fuzz",
}


at["deck_selector_window_title"] = {
    "en": "override default setting for Decks",
    "de": "Voreinstellungen für einzelne Decks außer Kraft setzen"
}

at["deck_selector_text"] = {
    "en": "the next version will contain a help text in this place.",
    "de": "Hilfstext - deck selector"
}


at["warn_about_fuzz_general"] = {
    "en": ("In the add-on 'siblings spacing' you have disabled for at least one deck the "
           "fuzzing of the next interval. "
           "This setting is applied by modifying functions from Anki that several other "
           "add-ons also overwrite like the add-on 'Load Balancer'. "
           "If you ever install such an add-on you should disable all fuzz-related settings"
           "in this add-on or you will run into problems. For a list of add-ons that are "
           "known to not work with the nofuzz option check the description of this add-on "
           "on Ankiweb at ..." ),
}


at["warn_about_fuzz_conflict"] = {
    "en": ("In the add-on 'siblings spacing' you have disabled for at least one deck the "
           "fuzzing of the next interval."
           "\n\nThis setting is applied by modifying functions from Anki that several other "
           "add-ons also overwrite like the add-on 'load balancer'."
           "In fact you have installed these incompatible add-ons:\n%s\n\n"
           "You should disable all fuzz-related settings in this add-on or disable the other "
           "addons or you will run into problems."
           "\n\nFor a list of add-ons that are "
           "known to not work with the nofuzz option check the description of this add-on "
           "on Ankiweb at ..." ),
}

at["warn_about_fuzz_conflict_at_startup"] = {
    "en": ("In the add-on 'siblings spacing' you have disabled for at least one deck the "
           "fuzzing of the next interval."
           "\n\nThis setting is applied by modifying functions from Anki that several other "
           "add-ons also overwrite like the add-on 'load balancer'."
           "In fact you have installed these incompatible add-ons:\n%s\n\n"
           "You should disable all fuzz-related settings in this add-on or disable the other "
           "addons or you will run into problems. "
           "This warning message will only be shown once."
           "\n\nFor a list of add-ons that are "
           "known to not work with the nofuzz option check the description of this add-on "
           "on Ankiweb at ..." ),
}



# localized = {k: v[LANG] for k, v in at.items()}
localized = {}
for k, v in at.items():
    if LANG in v:
        localized[k] = v[LANG]
    elif "en" in v:
        localized[k] = v["en"]
    else:
        print('missing text, value: {}'.format(k))
t = SimpleNamespace(**localized)
