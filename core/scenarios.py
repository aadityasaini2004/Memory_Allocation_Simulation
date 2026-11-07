from core.allocator import MemoryAllocator
from core.models import AllocationAlgorithm

def setup_demo_scenario(allocator: MemoryAllocator):
    """
    Sets up the fixed workload to show distinct outcomes across First Fit, Best Fit, and Worst Fit.
    Initial capacity must be 1024 KB.
    """
    allocator.reset(1024)
    # Setup sequence
    allocator.allocate("P1", 100, AllocationAlgorithm.FIRST_FIT)
    allocator.allocate("P2", 250, AllocationAlgorithm.FIRST_FIT)
    allocator.allocate("P3", 100, AllocationAlgorithm.FIRST_FIT)
    allocator.allocate("P4", 150, AllocationAlgorithm.FIRST_FIT)
    allocator.allocate("P5", 100, AllocationAlgorithm.FIRST_FIT)
    allocator.deallocate("P2")
    allocator.deallocate("P4")