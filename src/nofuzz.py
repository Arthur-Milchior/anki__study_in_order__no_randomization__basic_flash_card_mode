from heapq import *
import random
import time

from anki.hooks import wrap
from anki.sched import Scheduler as schedv1
from anki.schedv2 import Scheduler as schedv2
from anki.utils import intTime

from .config import (
    gc,
    get_did_even_if_in_filtered,
    apply_setting,
)

# this just comments out the line   delay *= random.uniform(1, 1.25)   
# which removes randomness/fuzz for lrn
def _myAnswerLrnCard(self, card, ease):
    # ease 1=no, 2=yes, 3=remove
    conf = self._lrnConf(card)
    if card.odid and not card.wasNew:
        type = 3
    elif card.type == 2:
        type = 2
    else:
        type = 0
    leaving = False
    # lrnCount was decremented once when card was fetched
    lastLeft = card.left
    # immediate graduate?
    if ease == 3:
        self._rescheduleAsRev(card, conf, True)
        leaving = True
    # graduation time?
    elif ease == 2 and (card.left%1000)-1 <= 0:
        self._rescheduleAsRev(card, conf, False)
        leaving = True
    else:
        # one step towards graduation
        if ease == 2:
            # decrement real left count and recalculate left today
            left = (card.left % 1000) - 1
            card.left = self._leftToday(conf['delays'], left)*1000 + left
        # failed
        else:
            card.left = self._startingLeft(card)
            resched = self._resched(card)
            if 'mult' in conf and resched:
                # review that's lapsed
                card.ivl = max(1, conf['minInt'], card.ivl*conf['mult'])
            else:
                # new card; no ivl adjustment
                pass
            if resched and card.odid:
                card.odue = self.today + 1
        delay = self._delayForGrade(conf, card.left)
        if card.due < time.time():
            # not collapsed; add some randomness
            delay *= random.uniform(1, 1)  # (1, 1.25)
        card.due = int(time.time() + delay)
        # due today?
        if card.due < self.dayCutoff:
            self.lrnCount += card.left // 1000
            # if the queue is not empty and there's nothing else to do, make
            # sure we don't put it at the head of the queue and end up showing
            # it twice in a row
            card.queue = 1
            if self._lrnQueue and not self.revCount and not self.newCount:
                smallestDue = self._lrnQueue[0][0]
                card.due = max(card.due, smallestDue+1)
            heappush(self._lrnQueue, (card.due, card.id))
        else:
            # the card is due in one or more days, so we need to use the
            # day learn queue
            ahead = ((card.due - self.dayCutoff) // 86400) + 1
            card.due = self.today + ahead
            card.queue = 3
    self._logLrn(card, ease, conf, leaving, type, lastLeft)


def LrnCardHelper(self, card, ease):
    did = get_did_even_if_in_filtered(card)
    if apply_setting("nofuzz", did):
        return _myAnswerLrnCard(self, card, ease)
    else:
        return self._oldAnswerLrnCard(card, ease)
schedv1._oldAnswerLrnCard = schedv1._answerLrnCard
schedv1._answerLrnCard = LrnCardHelper


## V2 - one line changed; _rescheduleLrnCard version from 2019-11-30 (5411cf0)
def _rescheduleLrnCard(self, card, conf, delay=None):
    # normal delay for the current step?
    if delay is None:
        delay = self._delayForGrade(conf, card.left)

    card.due = int(time.time() + delay)
    # due today?
    if card.due < self.dayCutoff:
        # add some randomness, up to 5 minutes or 25%
        maxExtra = min(300, int(delay*0.25))
        fuzz = 0  # random.randrange(0, maxExtra)
        card.due = min(self.dayCutoff-1, card.due + fuzz)
        card.queue = 1
        if card.due < (intTime() + self.col.conf['collapseTime']):
            self.lrnCount += 1
            # if the queue is not empty and there's nothing else to do, make
            # sure we don't put it at the head of the queue and end up showing
            # it twice in a row
            if self._lrnQueue and not self.revCount and not self.newCount:
                smallestDue = self._lrnQueue[0][0]
                card.due = max(card.due, smallestDue+1)
            heappush(self._lrnQueue, (card.due, card.id))
    else:
        # the card is due in one or more days, so we need to use the
        # day learn queue
        ahead = ((card.due - self.dayCutoff) // 86400) + 1
        card.due = self.today + ahead
        card.queue = 3
    return delay


def rescheduleLrnHelper(self, card, conf, delay=None):
    did = get_did_even_if_in_filtered(card)
    if apply_setting("nofuzz", did):
        return _rescheduleLrnCard(self, card, conf, delay=None)
    else:
        return self._oldRescheduleLrnCard(card, conf, delay=None)
schedv2._oldRescheduleLrnCard = schedv2._rescheduleLrnCard
schedv2._rescheduleLrnCard = rescheduleLrnHelper


# _adjRevIvl is only overwritten by Load Balancer in 2019-12
def _adjRevIvl(self, card, idealIvl):
    did = get_did_even_if_in_filtered(card)
    if self._spreadRev and not apply_setting("nofuzz", did):
        idealIvl = self._fuzzedIvl(idealIvl)
    return idealIvl
schedv1._adjRevIvl = _adjRevIvl


def _myGraduatingIvl(self, card, conf, early, fuzz=True, _old=None):
    did = get_did_even_if_in_filtered(card)
    if apply_setting("nofuzz", did):
        fuzz=False
    return _old(self, card, conf, early, fuzz)
schedv2._graduatingIvl = wrap(schedv2._graduatingIvl, _myGraduatingIvl, "around")


def _nextRevIvl(self, card, ease, fuzz, _old):
    "Next review interval for CARD, given EASE."
    delay = self._daysLate(card)
    conf = self._revConf(card)
    fct = card.factor / 1000
    hardFactor = conf.get("hardFactor", 1.2)
    if hardFactor > 1:
        hardMin = card.ivl
    else:
        hardMin = 0
    #### mod start
    did = get_did_even_if_in_filtered(card)
    if apply_setting("nofuzz", did):
        fuzz = False
    #### end mod
    ivl2 = self._constrainedIvl(card.ivl * hardFactor, conf, hardMin, fuzz)
    if ease == 2:
        return ivl2

    ivl3 = self._constrainedIvl((card.ivl + delay // 2) * fct, conf, ivl2, fuzz)
    if ease == 3:
        return ivl3

    ivl4 = self._constrainedIvl(
        (card.ivl + delay) * fct * conf['ease4'], conf, ivl3, fuzz)
    return ivl4
schedv2._nextRevIvl = wrap(schedv2._nextRevIvl, _nextRevIvl, "around")
