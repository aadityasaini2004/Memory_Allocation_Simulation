import unittest
from core.models import AllocationAlgorithm
from core.comparison import run_comparison
from core.scenarios import setup_demo_scenario

class TestComparison(unittest.TestCase):
    def test_demo_comparison_oracle(self):
        # Comparison run matching section 10.3 exactly
        operations = [("P6", 140), ("P7", 180)]
        results = run_comparison(1024, setup_demo_scenario, operations)
        
        # FIRST FIT EXPECTATIONS
        ff = results[AllocationAlgorithm.FIRST_FIT]
        self.assertEqual(ff["free_holes"], [110, 150, 144])
        self.assertEqual(ff["metrics"]["total_memory"], 1024)
        self.assertEqual(ff["metrics"]["used_memory"], 620)
        self.assertEqual(ff["metrics"]["free_memory"], 404)
        self.assertEqual(ff["metrics"]["largest_free_block"], 150)
        self.assertEqual(ff["metrics"]["free_hole_count"], 3)
        self.assertAlmostEqual(ff["metrics"]["utilization"], 60.55, places=2)
        self.assertAlmostEqual(ff["metrics"]["external_fragmentation"], 62.87, places=2)

        # BEST FIT EXPECTATIONS
        bf = results[AllocationAlgorithm.BEST_FIT]
        self.assertEqual(bf["free_holes"], [70, 10, 324])
        self.assertEqual(bf["metrics"]["free_memory"], 404)
        self.assertEqual(bf["metrics"]["largest_free_block"], 324)
        self.assertEqual(bf["metrics"]["free_hole_count"], 3)
        self.assertAlmostEqual(bf["metrics"]["utilization"], 60.55, places=2)
        self.assertAlmostEqual(bf["metrics"]["external_fragmentation"], 19.80, places=2)

        # WORST FIT EXPECTATIONS
        wf = results[AllocationAlgorithm.WORST_FIT]
        self.assertEqual(wf["free_holes"], [70, 150, 184])
        self.assertEqual(wf["metrics"]["free_memory"], 404)
        self.assertEqual(wf["metrics"]["largest_free_block"], 184)
        self.assertEqual(wf["metrics"]["free_hole_count"], 3)
        self.assertAlmostEqual(wf["metrics"]["utilization"], 60.55, places=2)
        self.assertAlmostEqual(wf["metrics"]["external_fragmentation"], 54.46, places=2)