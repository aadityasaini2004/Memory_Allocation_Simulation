import unittest
from core.allocator import MemoryAllocator
from core.scenarios import setup_demo_scenario

class TestScenarios(unittest.TestCase):
    def test_setup_demo_scenario(self):
        allocator = MemoryAllocator(1024)
        setup_demo_scenario(allocator)
        
        segments = allocator.get_segments()
        
        # Verify sizes and state matching section 10.3
        expected = [
            (100, False), # P1
            (250, True),  # Free
            (100, False), # P3
            (150, True),  # Free
            (100, False), # P5
            (324, True)   # Free
        ]
        
        self.assertEqual(len(segments), len(expected))
        for i, (size, is_free) in enumerate(expected):
            self.assertEqual(segments[i].size, size)
            self.assertEqual(segments[i].is_free, is_free)