from dataclasses import dataclass
from typing import Optional
from enum import Enum

class AllocationAlgorithm(Enum):
    FIRST_FIT = "First Fit"
    BEST_FIT = "Best Fit"
    WORST_FIT = "Worst Fit"

@dataclass
class MemorySegment:
    start: int
    size: int
    process_id: Optional[str] = None
    
    @property
    def end(self) -> int:
        return self.start + self.size
        
    @property
    def is_free(self) -> bool:
        return self.process_id is None

@dataclass
class Process:
    process_id: str
    start: int
    size: int
    
    @property
    def end(self) -> int:
        return self.start + self.size
