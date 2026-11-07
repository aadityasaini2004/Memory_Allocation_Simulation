from typing import List, Optional
from core.models import MemorySegment, AllocationAlgorithm

def select_first_fit(segments: List[MemorySegment], requested_size: int) -> Optional[int]:
    """Returns the index of the first free segment large enough to satisfy the request."""
    for i, segment in enumerate(segments):
        if segment.is_free and segment.size >= requested_size:
            return i
    return None

def select_best_fit(segments: List[MemorySegment], requested_size: int) -> Optional[int]:
    """Returns the index of the smallest free segment large enough to satisfy the request.
    Ties are broken by lowest start address (which naturally corresponds to the lowest index since segments are ordered).
    """
    best_idx = None
    min_size = float('inf')
    
    for i, segment in enumerate(segments):
        if segment.is_free and segment.size >= requested_size:
            if segment.size < min_size:
                min_size = segment.size
                best_idx = i
    return best_idx

def select_worst_fit(segments: List[MemorySegment], requested_size: int) -> Optional[int]:
    """Returns the index of the largest free segment that can satisfy the request.
    Ties are broken by lowest start address.
    """
    worst_idx = None
    max_size = -1
    
    for i, segment in enumerate(segments):
        if segment.is_free and segment.size >= requested_size:
            if segment.size > max_size:
                max_size = segment.size
                worst_idx = i
    return worst_idx
