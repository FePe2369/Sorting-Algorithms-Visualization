# Sorting Algorithm Visualizer

An interactive tool that runs five sorting algorithms side by side, animating comparisons and swaps in real time with live statistics. Built with Python and Pygame.

## Features

- Compares Bubble, Insertion, Selection, Quick and Merge sort simultaneously
- Live stats per algorithm: comparisons, swaps and execution time
- Adjustable array size (10–100) and animation speed
- State-based bar coloring: comparing (yellow), swapping (red), sorted (green)
- Controls: generate array (G), start/pause (Space), reset (R)

## Algorithm comparison

| Algorithm | Best       | Average    | Worst      | Space    | Stable |
| --------- | ---------- | ---------- | ---------- | -------- | ------ |
| Bubble    | O(n)       | O(n²)      | O(n²)      | O(1)     | Yes    |
| Insertion | O(n)       | O(n²)      | O(n²)      | O(1)     | Yes    |
| Selection | O(n²)      | O(n²)      | O(n²)      | O(1)     | No     |
| Quick     | O(n log n) | O(n log n) | O(n²)      | O(log n) | No     |
| Merge     | O(n log n) | O(n log n) | O(n log n) | O(n)     | Yes    |

## Architecture

Each algorithm extends a `SortingAlgorithm` base class and implements `sort_step()`, which runs one logical step per call. That makes it possible to animate every algorithm at the same pace and compare them fairly:

```
SortingAlgorithm (base)
├── BubbleSort
├── InsertionSort
├── SelectionSort
├── QuickSort
└── MergeSort

SortingVisualizer   # controller: state, rendering, input, animation
```

Adding a new algorithm means subclassing `SortingAlgorithm` and implementing `sort_step()`.

## Install and run

```bash
pip install pygame
python main.py
```

## Notes

- Quick Sort can look faster because it triggers fewer visual updates
- Speeds above ~90 may drop frames on slower machines
