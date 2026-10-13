import os
import time

import run_nowcast as rn


def test_second_run_is_locked_out_and_stale_lock_reclaimed(tmp_path):
    lock = tmp_path / "run.lock"
    assert rn.acquire_lock(lock)
    assert not rn.acquire_lock(lock)          # concurrent run refused
    old = time.time() - rn.LOCK_STALE_S - 60
    os.utime(lock, (old, old))
    assert rn.acquire_lock(lock)              # crashed run's lock reclaimed
