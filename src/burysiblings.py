from anki.utils import ids2str, intTime
from anki.sched import Scheduler as schedv1
from anki.schedv2 import Scheduler as schedv2
from aqt import mw

from .config import (
    gc,
    get_did_even_if_in_filtered,
    apply_setting,
)


def siblings_in_order(queue, card):
    did = get_did_even_if_in_filtered(card)
    if apply_setting("new", did):
        return True


def my_burySiblings(self, card):
    toBury = []
    nconf = self._newConf(card)
    buryNew = nconf.get("bury", True)
    rconf = self._revConf(card)
    buryRev = rconf.get("bury", True)
    # loop through and remove from queues
    for cid, queue in self.col.db.execute("""
select id, queue from cards where nid=? and id!=?
and (queue=0 or (queue=2 and due<=?))""",
            card.nid, card.id, self.today):
        if queue == 2:  # review
            if buryRev:
                toBury.append(cid)
            # if bury disabled, we maybe discard to give same-day spacing
            if not siblings_in_order(queue, card):
                try:
                    self._revQueue.remove(cid)
                except ValueError:
                    pass
        else:
            if buryNew:
                toBury.append(cid)
            # if bury disabled, we maybe discard to give same-day spacing
            if not siblings_in_order(queue, card):
                try:
                    self._newQueue.remove(cid)
                except ValueError:
                    pass
    # then bury
    if toBury:
        if self.col.schedVer() != 1:
            self.buryCards(toBury, manual=False)
        else:
            self.col.db.execute(
                "update cards set queue=-2,mod=?,usn=? where id in "+ids2str(toBury),
                intTime(), self.col.usn())
            self.col.log(toBury)
schedv1._burySiblings = my_burySiblings
schedv2._burySiblings = my_burySiblings
