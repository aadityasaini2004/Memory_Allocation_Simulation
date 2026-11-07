from typing import List, Dict, Any, Tuple, Callable
from core.models import AllocationAlgorithm, MemorySegment
from core.allocator import MemoryAllocator
from core.memory_metrics import calculate_metrics

def run_comparison(total_memory: int, setup_func: Callable[[MemoryAllocator], None], operations: List[Tuple[str, int]]) -> Dict[AllocationAlgorithm, Dict[str, Any]]:
    """
    Runs an isolated comparison for all three algorithms given a setup function and subsequent operations.
    """
    results = {}
    for algo in [AllocationAlgorithm.FIRST_FIT, AllocationAlgorithm.BEST_FIT, AllocationAlgorithm.WORST_FIT]:
        allocator = MemoryAllocator(total_memory)
        if setup_func:
            setup_func(allocator)
        
        # Execute comparison operations under this specific algorithm
        for pid, size in operations:
            try:
                allocator.allocate(pid, size, algo)
            except Exception:
                # In comparison runs, if an allocation fails we just continue to show final state
                pass
        
        metrics = calculate_metrics(total_memory, allocator.get_segments(), allocator.get_processes())
        free_holes = [s.size for s in allocator.get_segments() if s.is_free]
        
        results[algo] = {
            "metrics": metrics,
            "segments": allocator.get_segments(),
            "free_holes": free_holes
        }
    return results