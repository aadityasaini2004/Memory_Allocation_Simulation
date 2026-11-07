import unittest
from core.models import AllocationAlgorithm
from core.allocator import MemoryAllocator
from core.exceptions import ProcessNotFoundError

class TestDeallocation(unittest.TestCase):
    def setUp(self):
        self.allocator = MemoryAllocator(1000)
        self.allocator.allocate("P1", 200, AllocationAlgorithm.FIRST_FIT)
        self.allocator.allocate("P2", 200, AllocationAlgorithm.FIRST_FIT)
        self.allocator.allocate("P3", 200, AllocationAlgorithm.FIRST_FIT)
        self.allocator.allocate("P4", 200, AllocationAlgorithm.FIRST_FIT)
        self.allocator.allocate("P5", 200, AllocationAlgorithm.FIRST_FIT)
        # Segments map: [P1:200][P2:200][P3:200][P4:200][P5:200]

    def test_deallocate_active_process(self):
        self.allocator.deallocate("P1")
        segments = self.allocator.get_segments()
        self.assertTrue(segments[0].is_free)
        self.assertEqual(segments[0].size, 200)

    def test_unknown_process(self):
        with self.assertRaises(ProcessNotFoundError):
            self.allocator.deallocate("P99")

    def test_merge_right(self):
        self.allocator.deallocate("P5") # End of memory, becomes free
        self.allocator.deallocate("P4") # P4 and P5 should merge
        segments = self.allocator.get_segments()
        self.assertEqual(len(segments), 4) # P1, P2, P3, FREE(400)
        self.assertEqual(segments[-1].size, 400)
        self.assertTrue(segments[-1].is_free)

    def test_merge_left(self):
        self.allocator.deallocate("P1")
        self.allocator.deallocate("P2") # P1 and P2 should merge
        segments = self.allocator.get_segments()
        self.assertEqual(len(segments), 4) # FREE(400), P3, P4, P5
        self.assertEqual(segments[0].size, 400)
        self.assertTrue(segments[0].is_free)

    def test_merge_both_sides(self):
        self.allocator.deallocate("P2")
        self.allocator.deallocate("P4")
        self.allocator.deallocate("P3") # P3 merges with P2(left) and P4(right)
        
        segments = self.allocator.get_segments()
        self.assertEqual(len(segments), 3) # P1, FREE(600), P5
        self.assertEqual(segments[1].size, 600)
        self.assertTrue(segments[1].is_free)
        
    def test_reuse_process_id(self):
        self.allocator.deallocate("P1")
        self.allocator.allocate("P1", 100, AllocationAlgorithm.FIRST_FIT)
        segments = self.allocator.get_segments()
        self.assertEqual(segments[0].process_id, "P1")
        self.assertEqual(segments[0].size, 100)

if __name__ == '__main__':
    unittest.main()