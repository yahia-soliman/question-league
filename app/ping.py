#!/usr/bin/python3
"""SSE implementation"""

import queue
from typing import List

print("yes bro they imported me again")


subs: List[queue.Queue] = []


def puplish(msg="pong"):
    """pulish a pong, or message"""
    for i in reversed(range(len(subs))):
        if subs[i].full():
            del subs[i]
            continue
        subs[i].put(msg)


def subscribe():
    """subscribe to get pongs when there are any"""
    q = queue.Queue(maxsize=5)
    subs.append(q)
    while True:
        msg = q.get(block=True, timeout=None)
        yield msg
