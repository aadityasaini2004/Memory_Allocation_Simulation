# Memory Allocation Simulator

A Python-based desktop educational application that demonstrates **variable-sized contiguous memory allocation** in an operating-system-style memory space.

The simulator models how an operating system assigns memory segments to processes, dynamically handles segment splitting and coalescing, and manages external fragmentation using standard placement algorithms.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Tests](https://img.shields.io/badge/tests-26%2F26%20passing-brightgreen)
![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey)

---

## Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#️-tech-stack)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Demo Scenario](#-demo-scenario)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Scope Limitations](#️-scope-limitations)

---

## 🌟 Features

- **Variable-Sized Contiguous Allocation:** Processes receive exactly the size they request, so there is no internal fragmentation.
- **Three Placement Algorithms:** First Fit, Best Fit, and Worst Fit, with deterministic tie-breaking.
- **Dynamic Coalescing:** Adjacent free blocks merge automatically when a process is deallocated.
- **Granular Error Handling:** Clearly distinguishes between:
  - `InsufficientMemoryError`: total free memory is too low.
  - `ExternalFragmentationError`: total free memory is enough, but no single contiguous hole is large enough.
- **Live Telemetry & Metrics:** Real-time used/free memory, utilization percentage, active process count, and an educational external fragmentation metric.
- **Isolated Algorithm Comparison:** Runs the same workload across all three algorithms in isolation, without touching the active simulation state.
- **Learning Center:** Built-in explanations of core memory management concepts.

---

## 📸 Screenshots

| Main Simulator | Algorithm Comparison |
|:---:|:---:|
| ![Main Simulator](assets/screenshots/simulator_main.png) | ![Algorithm Comparison](assets/screenshots/algorithm_comparison.png) |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| GUI Framework | Tkinter & ttk (standard library) |
| Testing | `unittest` (standard library) |
| Dependencies | **None.** No third-party packages required |

---

## 🚀 Quick Start

1. **Clone or extract the repository**, then move into the root directory:

   ```bash
   cd memory-allocation-simulator
   ```

2. **Launch the application:**

   ```bash
   python main.py
   ```

> **Note:** Linux users may need to install Tkinter separately if it isn't bundled with their Python distribution:
>
> ```bash
> sudo apt install python3-tk
> ```

---

## 📖 Usage Guide

1. On launch, memory initializes as a single **1024 KB** free block.
2. In the **Process Control** panel, enter a **Process ID** (e.g., `P1`), a **Size in KB** (e.g., `200`), choose an algorithm, and click **Allocate**.
3. Allocate a few more processes and watch the memory map split into smaller segments.
4. Enter `P1` in the deallocate box and click **Deallocate**. The block becomes a free hole and automatically coalesces with adjacent free space.

---

## 🎬 Demo Scenario

To see fragmentation in action:

1. Click **Load Demo Scenario** in the header.
2. The memory resets, allocates `P1`–`P5`, then frees `P2` and `P4`. This leaves a fragmented memory state with free holes of **250 KB, 150 KB, and 324 KB**.
3. Open the **Algorithm Comparison** tab and click **Run Demo Comparison**.
4. The app independently attempts to allocate `P6` (140 KB) and `P7` (180 KB) under each algorithm, showing how **First Fit, Best Fit, and Worst Fit** lead to noticeably different final fragmentation percentages.

---

## 🧪 Testing

The core engine is fully decoupled from the GUI and covered by an automated test suite that verifies pure logic, atomicity, and 12 strict memory invariants.

Run the tests from the project root:

```bash
python -m unittest discover -s tests -v
```

**Expected result:** 26/26 tests passing.

---

## 📂 Project Structure

```plaintext
memory-allocation-simulator/
│
├── core/                     # Pure domain logic (no GUI dependencies)
│   ├── algorithms.py         # First, Best, and Worst Fit selection logic
│   ├── allocator.py          # Atomic state mutation and coalescing
│   ├── comparison.py         # Isolated comparison engine
│   ├── exceptions.py         # Domain-specific errors
│   ├── memory_metrics.py     # Pure statistics calculations
│   ├── models.py             # MemorySegment and Process dataclasses
│   └── scenarios.py          # Fixed workload generators
│
├── gui/                      # Tkinter presentation layer
│   ├── activity_log.py       # Chronological event tracking
│   ├── app.py                # Main Tk application and notebook
│   ├── comparison_view.py    # Side-by-side algorithm comparison UI
│   ├── dashboard.py          # Live metrics display
│   ├── learning_view.py      # Educational content
│   ├── memory_visualizer.py  # Proportional Canvas rendering
│   ├── process_panel.py      # Input controls and validation
│   ├── process_table.py      # Active process Treeview
│   └── styles.py             # Custom dark theme configuration
│
├── tests/                    # Core test suite
├── docs/                     # Markdown deliverables and Viva guide
├── assets/screenshots/       # Visual evidence
├── main.py                   # Application entry point
├── README.md
└── TEAM_GUIDE.md
```

---

## ⚠️ Scope Limitations

This is a **user-space educational simulator**. It does not allocate actual host OS RAM.

**Out of scope for v1:** paging, fixed partitions, virtual memory, TLB translation, and memory compaction (relocating active processes to eliminate external fragmentation).
