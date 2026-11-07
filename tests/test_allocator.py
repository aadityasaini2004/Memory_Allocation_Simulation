import unittest
from core.models import AllocationAlgorithm, MemorySegment
from core.allocator import MemoryAllocator
from core.exceptions import (
    InvalidMemoryRequestError,
    DuplicateProcessError,
    InsufficientMemoryError,
    ExternalFragmentationError,
    MemoryIntegrityError
)

class TestMemoryAllocator(unittest.TestCase):
    def setUp(self):
        self.allocator = MemoryAllocator(1024)

    def test_initial_state(self):
        segments = self.allocator.get_segments()
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].size, 1024)
        self.assertTrue(segments[0].is_free)

    def test_allocate_exact_fit(self):
        self.allocator.allocate("P1", 1024, AllocationAlgorithm.FIRST_FIT)
        segments = self.allocator.get_segments()
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].process_id, "P1")

    def test_allocate_splitting(self):
        self.allocator.allocate("P1", 200, AllocationAlgorithm.FIRST_FIT)
        segments = self.allocator.get_segments()
        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0].size, 200)
        self.assertEqual(segments[0].process_id, "P1")
        self.assertEqual(segments[1].size, 824)
        self.assertTrue(segments[1].is_free)

    def test_duplicate_process_rejected(self):
        self.allocator.allocate("P1", 100, AllocationAlgorithm.FIRST_FIT)
        with self.assertRaises(DuplicateProcessError):
            self.allocator.allocate("P1", 100, AllocationAlgorithm.FIRST_FIT)
        
        # Test case-insensitive normalization
        with self.assertRaises(DuplicateProcessError):
            self.allocator.allocate("p1", 100, AllocationAlgorithm.FIRST_FIT)

    def test_insufficient_memory(self):
        with self.assertRaises(InsufficientMemoryError):
            self.allocator.allocate("P1", 2048, AllocationAlgorithm.FIRST_FIT)

    def test_external_fragmentation(self):
        # Create holes
        self.allocator.allocate("P1", 400, AllocationAlgorithm.FIRST_FIT)
        self.allocator.allocate("P2", 200, AllocationAlgorithm.FIRST_FIT)
        self.allocator.allocate("P3", 424, AllocationAlgorithm.FIRST_FIT)
        
        self.allocator.deallocate("P1") # 400 free
        self.allocator.deallocate("P3") # 424 free
        
        # Total free = 824, but largest block is 424. Requesting 500 should fail due to fragmentation.
        with self.assertRaises(ExternalFragmentationError):
            self.allocator.allocate("P4", 500, AllocationAlgorithm.FIRST_FIT)

    def test_atomicity_on_failure(self):
        self.allocator.allocate("P1", 100, AllocationAlgorithm.FIRST_FIT)
        backup = self.allocator.get_segments()
        
        try:
            self.allocator.allocate("P2", 2000, AllocationAlgorithm.FIRST_FIT)
        except InsufficientMemoryError:
            pass
            
        # State must remain exactly the same
        self.assertEqual(self.allocator.get_segments(), backup)

    def test_integrity_failure_catches_bad_state(self):
        # Manually corrupt state to test the invariant checker
        self.allocator._segments.append(MemorySegment(start=1024, size=100, process_id=None))
        with self.assertRaises(MemoryIntegrityError):
            self.allocator._check_invariants()

if __name__ == '__main__':
    unittest.main()