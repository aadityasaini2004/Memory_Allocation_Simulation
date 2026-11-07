import copy
from typing import List, Dict, Optional
from core.models import MemorySegment, Process, AllocationAlgorithm
from core.exceptions import (
    InvalidMemoryRequestError,
    DuplicateProcessError,
    ProcessNotFoundError,
    InsufficientMemoryError,
    ExternalFragmentationError,
    MemoryIntegrityError
)
from core.algorithms import select_first_fit, select_best_fit, select_worst_fit

class MemoryAllocator:
    def __init__(self, total_memory_kb: int):
        if not isinstance(total_memory_kb, int) or total_memory_kb <= 0:
            raise InvalidMemoryRequestError("Total memory must be a positive integer.")
        self._total_memory = total_memory_kb
        self.reset(total_memory_kb)

    def reset(self, total_memory_kb: Optional[int] = None):
        if total_memory_kb is not None:
            if not isinstance(total_memory_kb, int) or total_memory_kb <= 0:
                raise InvalidMemoryRequestError("Total memory must be a positive integer.")
            self._total_memory = total_memory_kb
        
        self._segments: List[MemorySegment] = [
            MemorySegment(start=0, size=self._total_memory, process_id=None)
        ]
        self._processes: Dict[str, Process] = {}
        self._check_invariants()

    def get_segments(self) -> List[MemorySegment]:
        # Return a safe snapshot so GUI cannot mutate core state
        return copy.deepcopy(self._segments)

    def get_processes(self) -> List[Process]:
        return copy.deepcopy(list(self._processes.values()))
        
    def _normalize_pid(self, pid: str) -> str:
        if not isinstance(pid, str) or not pid.strip():
            raise InvalidMemoryRequestError("Process ID must be a non-empty string.")
        return pid.strip().upper()

    def allocate(self, process_id: str, size_kb: int, algorithm: AllocationAlgorithm):
        pid = self._normalize_pid(process_id)
        if pid in self._processes:
            raise DuplicateProcessError(f"Process '{pid}' is already active.")
            
        if not isinstance(size_kb, int) or size_kb <= 0:
            raise InvalidMemoryRequestError("Requested size must be a positive integer.")
            
        if size_kb > self._total_memory:
            raise InsufficientMemoryError("Requested size is larger than total memory.")

        # Backup snapshot to guarantee atomicity
        backup_segments = copy.deepcopy(self._segments)
        backup_processes = copy.deepcopy(self._processes)

        try:
            total_free = sum(s.size for s in self._segments if s.is_free)
            if total_free < size_kb:
                raise InsufficientMemoryError(f"Allocation failed: {size_kb} KB requested, {total_free} KB free in total.")

            idx = None
            if algorithm == AllocationAlgorithm.FIRST_FIT:
                idx = select_first_fit(self._segments, size_kb)
            elif algorithm == AllocationAlgorithm.BEST_FIT:
                idx = select_best_fit(self._segments, size_kb)
            elif algorithm == AllocationAlgorithm.WORST_FIT:
                idx = select_worst_fit(self._segments, size_kb)
            else:
                raise ValueError("Unknown allocation algorithm.")

            if idx is None:
                largest_hole = max((s.size for s in self._segments if s.is_free), default=0)
                raise ExternalFragmentationError(
                    f"Allocation failed: {size_kb} KB requested, {total_free} KB free in total, "
                    f"but the largest free block is {largest_hole} KB."
                )

            # Mutate
            hole = self._segments[idx]
            allocated_segment = MemorySegment(start=hole.start, size=size_kb, process_id=pid)
            
            new_segments = self._segments[:idx] + [allocated_segment]
            
            # Split segment and add remainder if the hole was larger than requested
            if hole.size > size_kb:
                remainder = MemorySegment(start=hole.start + size_kb, size=hole.size - size_kb, process_id=None)
                new_segments.append(remainder)
                
            new_segments.extend(self._segments[idx+1:])
            self._segments = new_segments
            
            self._processes[pid] = Process(process_id=pid, start=allocated_segment.start, size=size_kb)

            self._check_invariants()
        except Exception as e:
            # Revert to backup on failure
            self._segments = backup_segments
            self._processes = backup_processes
            raise e

    def deallocate(self, process_id: str):
        pid = self._normalize_pid(process_id)
        if pid not in self._processes:
            raise ProcessNotFoundError(f"Process '{pid}' not found.")

        backup_segments = copy.deepcopy(self._segments)
        backup_processes = copy.deepcopy(self._processes)

        try:
            for i, seg in enumerate(self._segments):
                if seg.process_id == pid:
                    self._segments[i] = MemorySegment(start=seg.start, size=seg.size, process_id=None)
                    break

            del self._processes[pid]
            self._coalesce()
            self._check_invariants()
        except Exception as e:
            self._segments = backup_segments
            self._processes = backup_processes
            raise e

    def _coalesce(self):
        merged = []
        for seg in self._segments:
            if not merged:
                merged.append(seg)
            else:
                last = merged[-1]
                if last.is_free and seg.is_free:
                    merged[-1] = MemorySegment(start=last.start, size=last.size + seg.size, process_id=None)
                else:
                    merged.append(seg)
        self._segments = merged

    def _check_invariants(self):
        if not isinstance(self._total_memory, int) or self._total_memory <= 0:
            raise MemoryIntegrityError("Total memory must be a positive integer.")
            
        if not self._segments:
            raise MemoryIntegrityError("At least one segment must exist.")
            
        if self._segments[0].start != 0:
            raise MemoryIntegrityError("First segment must start at 0.")

        total_size = 0
        expected_start = 0
        allocated_ids = set()
        
        for i, seg in enumerate(self._segments):
            if not isinstance(seg.size, int) or seg.size <= 0:
                raise MemoryIntegrityError(f"Segment {i} has invalid size: {seg.size}")
                
            if seg.start != expected_start:
                raise MemoryIntegrityError(f"Segment {i} start {seg.start} does not match expected {expected_start}")
                
            total_size += seg.size
            expected_start = seg.end
            
            if not seg.is_free:
                if seg.process_id in allocated_ids:
                    raise MemoryIntegrityError(f"Duplicate allocation for process {seg.process_id}")
                allocated_ids.add(seg.process_id)
                if seg.process_id not in self._processes:
                    raise MemoryIntegrityError(f"Segment allocated to unknown process {seg.process_id}")
                
                p = self._processes[seg.process_id]
                if p.start != seg.start or p.size != seg.size:
                    raise MemoryIntegrityError(f"Process {p.process_id} bounds mismatch segment bounds.")
            
            if i > 0:
                if self._segments[i-1].is_free and seg.is_free:
                    raise MemoryIntegrityError("Adjacent free segments were not merged.")

        if total_size != self._total_memory:
            raise MemoryIntegrityError(f"Sum of segment sizes {total_size} != total memory {self._total_memory}")
            
        for pid in self._processes:
            if pid not in allocated_ids:
                raise MemoryIntegrityError(f"Process {pid} is registered but has no allocated segment.")