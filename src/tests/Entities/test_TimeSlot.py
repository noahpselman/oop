import pytest
from unittest.mock import Mock
from datetime import time
from src.Entities.TimeSlot import TimeSlot


def test_no_overlap_true():
    t0 = TimeSlot(start_time=time(0), end_time=time(2), days=['M'])
    t1 = TimeSlot(start_time=time(2), end_time=time(4), days=['M'])
    assert t0.no_overlap(t1)


def test_no_overlap_false():
    t0 = TimeSlot(start_time=time(0), end_time=time(2), days=['M'])
    t1 = TimeSlot(start_time=time(0), end_time=time(2), days=['M'])
    assert not t0.no_overlap(t1)
