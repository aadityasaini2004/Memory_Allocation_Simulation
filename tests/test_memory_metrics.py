import unittest
from core.models import MemorySegment, Process
from core.memory_metrics import calculate_metrics

class TestMemoryMetrics(unittest.TestCase):
    def test_metrics_no_free_memory(self):
        segments = [MemorySegment(start=0, size=100, process_id="P1")]
        processes = [Process("P1", 0, 100)]
        metrics = calculate_metrics(100, segments, processes)
        
        self.assertEqual(metrics["free_memory"], 0)
        self.assertEqual(metrics["external_fragmentation"], "N/A")
        self.assertEqual(metrics["utilization"], 100.0)

    def test_metrics_one_hole(self):
        segments = [
            MemorySegment(start=0, size=50, process_id="P1"),
            MemorySegment(start=50, size=50, process_id=None)
        ]
        processes = [Process("P1", 0, 50)]
        metrics = calculate_metrics(100, segments, processes)
        
        self.assertEqual(metrics["free_memory"], 50)
        self.assertEqual(metrics["external_fragmentation"], 0.0)
        
    def test_metrics_multiple_holes(self):
        segments = [
            MemorySegment(start=0, size=50, process_id="P1"),
            MemorySegment(start=50, size=20, process_id=None),
            MemorySegment(start=70, size=10, process_id="P2"),
            MemorySegment(start=80, size=20, process_id=None)
        ]
        processes = [Process("P1", 0, 50), Process("P2", 70, 10)]
        metrics = calculate_metrics(100, segments, processes)
        
        self.assertEqual(metrics["free_memory"], 40)
        self.assertEqual(metrics["largest_free_block"], 20)
        self.assertEqual(metrics["free_hole_count"], 2)
        self.assertEqual(metrics["external_fragmentation"], (1 - (20/40)) * 100.0) # 50%