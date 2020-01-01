from anki.hooks import wrap
from anki.sched import Scheduler as schedv1
from anki.schedv2 import Scheduler as schedv2

from .config import (
    gc,
    get_did_even_if_in_filtered,
    apply_setting,
)

# this function means that the siblings will be in increasing order but not necessarily right
# after each other
'''
def _myGetRevCard(self, _old):
    card = _old(self)
    if not mw.col.conf['268644742_intraday_spacing_global_override']:
        return card
    if card:
        sql = """select id, ord from cards where nid=? and queue=2 and due<=?"""
        due_siblings_nested_list = list(self.col.db.execute(sql, card.nid, self.today))  # list, you can't sort a cursor
        due_siblings_nested_list.sort(key=lambda x: x[1])
        due_siblings_list = [int(x[0]) for x in due_siblings_nested_list]
        for cid in due_siblings_list[1:]:
            self._revQueue = [x for x in self._revQueue if x is not cid]
        newcard = self.col.getCard(due_siblings_list[0])
        return newcard
'''


# This approach checks and modifies each due review card once it's fetched from the revQueue.
# It's probably inefficient in comparison to modifying the queue building which usually only happens
# every 50 cards.
# But on my machine that's a few years old with a SATA-SSD I don't notice a slowdown. 
# Advantage: Since I don't overwrite queue building methods it should work more or less with 
# HoochieMama or similar add-ons. The add-ons kind of interfere but should cooperate reasonably 
# well: 
# HoochieMama rebuilds the queue according to certain criteria. A queue in Anki by default consists
# of 50 cards and the function below mainly modifies the queue. So if you have like 500 due cards
# you should still notice the general effect of HoochieMama ??
def _myGetRevCard(self, _old):
    card = _old(self)
    if card:
        did = get_did_even_if_in_filtered(card)
        if not apply_setting("rev", did):
            return card
        if (
                apply_setting("revorder", did) and
                len(self._revQueue) > 0 and  # maybe _old returned/removed the last card
                not self.still_processing_due_review_siblings
           ):
            lowest_cid = min(self._revQueue)
            lowest_card = self.col.getCard(lowest_cid)
            nid = lowest_card.nid
            # this means card is removed from the _revQueue but once the queue is rebuilt the card will be back in 
            # so it shouldn't be a problem to not readd card in this function.
        else:  # start with card that the database returns as the first. 
            nid = card.nid
        sql = """select id, ord from cards where nid=? and queue=2 and due<=?"""
        due_siblings_nested_list = list(self.col.db.execute(sql, nid, self.today))

        if len(due_siblings_nested_list) > 1:
            self.still_processing_due_review_siblings = True
        else:
            self.still_processing_due_review_siblings = False
        due_siblings_nested_list.sort(key=lambda x: x[1], reverse = True)
        due_siblings_list = [int(x[0]) for x in due_siblings_nested_list]
        for cid in due_siblings_list:
            while cid in self._revQueue:
                self._revQueue.remove(cid)
            self._revQueue.append(cid)
        newcard = self.col.getCard(self._revQueue.pop())
        return newcard


schedv1.still_processing_due_review_siblings = False
schedv2.still_processing_due_review_siblings = False
schedv1._getRevCard = wrap(schedv1._getRevCard, _myGetRevCard, 'around')
schedv2._getRevCard = wrap(schedv2._getRevCard, _myGetRevCard, 'around')
