import unittest
from core.models import MemorySegment
from core.algorithms import select_first_fit, select_best_fit, select_worst_fit

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        # Setup matching the doc's examples (H1=250, H2=150, H3=324)
        self.segments = [
            MemorySegment(start=0, size=100, process_id="P1"),
            MemorySegment(start=100, size=250, process_id=None),   # index 1 (H1)
            MemorySegment(start=350, size=100, process_id="P3"),
            MemorySegment(start=450, size=150, process_id=None),   # index 3 (H2)
            MemorySegment(start=600, size=100, process_id="P5"),
            MemorySegment(start=700, size=324, process_id=None)    # index 5 (H3)
        ]

    def test_first_fit(self):
        # Needs 140 -> Should pick H1 (index 1)
        idx = select_first_fit(self.segments, 140)
        self.assertEqual(idx, 1)

    def test_first_fit_too_large(self):
        # Needs 400 -> Should return None
        self.assertIsNone(select_first_fit(self.segments, 400))

    def test_best_fit(self):
        # Needs 140 -> Smallest fitting is H2 (150) -> index 3
        idx = select_best_fit(self.segments, 140)
        self.assertEqual(idx, 3)

    def test_worst_fit(self):
        # Needs 140 -> Largest fitting is H3 (324) -> index 5
        idx = select_worst_fit(self.segments, 140)
        self.assertEqual(idx, 5)
        
    def test_best_fit_tie_break(self):
        # Tie break lowest address
        segments = [
            MemorySegment(start=0, size=100, process_id=None),
            MemorySegment(start=100, size=50, process_id="P1"),
            MemorySegment(start=150, size=100, process_id=None)
        ]
        idx = select_best_fit(segments, 90)
        self.assertEqual(idx, 0)
        
    def test_worst_fit_tie_break(self):
        # Tie break lowest address
        segments = [
            MemorySegment(start=0, size=200, process_id=None),
            MemorySegment(start=200, size=50, process_id="P1"),
            MemorySegment(start=250, size=200, process_id=None)
        ]
        idx = select_worst_fit(segments, 90)
        self.assertEqual(idx, 0)
        
    def test_exact_size_fit(self):
        idx = select_best_fit(self.segments, 150)
        self.assertEqual(idx, 3) # H2 exactly

if __name__ == '__main__':
    unittest.main()
