from typing import List, Dict, Any
from core.models import MemorySegment, Process

def calculate_metrics(total_memory: int, segments: List[MemorySegment], processes: List[Process]) -> Dict[str, Any]:
    used_memory = sum(s.size for s in segments if not s.is_free)
    free_segments = [s for s in segments if s.is_free]
    free_memory = sum(s.size for s in free_segments)
    utilization = (used_memory / total_memory) * 100 if total_memory > 0 else 0.0
    
    largest_free_block = max((s.size for s in free_segments), default=0)
    free_hole_count = len(free_segments)
    active_process_count = len(processes)
    
    if free_memory == 0:
        external_fragmentation = "N/A"
    elif free_hole_count <= 1:
        external_fragmentation = 0.0
    else:
        external_fragmentation = (1 - (largest_free_block / free_memory)) * 100.0

    return {
        "total_memory": total_memory,
        "used_memory": used_memory,
        "free_memory": free_memory,
        "utilization": utilization,
        "largest_free_block": largest_free_block,
        "free_hole_count": free_hole_count,
        "active_process_count": active_process_count,
        "external_fragmentation": external_fragmentation
    }