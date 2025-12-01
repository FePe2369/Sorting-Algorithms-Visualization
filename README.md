# 🎨 Sorting Algorithm Visualizer

A modern, interactive visualization tool for comparing popular sorting algorithms side-by-side. Watch algorithms compete in real-time with detailed statistics and smooth animations.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

## ✨ Features

### 🔄 Multiple Algorithms

Compare 5 sorting algorithms simultaneously:

- **Bubble Sort** - Simple comparison-based algorithm
- **Insertion Sort** - Efficient for small datasets
- **Selection Sort** - Minimizes swaps
- **Quick Sort** - Divide and conquer approach
- **Merge Sort** - Guaranteed O(n log n) performance

### 📊 Real-Time Statistics

Track performance metrics for each algorithm:

- Number of comparisons
- Number of swaps/moves
- Execution time (in seconds)

### 🎮 Interactive Controls

- **Generate**: Create new random array
- **Start All**: Begin sorting all algorithms
- **Pause/Resume**: Control execution flow
- **Reset**: Return to initial state
- **Array Size Slider**: Adjust from 10 to 100 elements
- **Speed Slider**: Control animation speed (1-100)

### ⌨️ Keyboard Shortcuts

- **Space**: Start/Pause sorting
- **R**: Reset algorithms
- **G**: Generate new array

### 🎨 Visual Design

- Color-coded algorithms for easy distinction
- State-based bar coloring:
  - **Default**: Algorithm's signature color
  - **Comparing**: Yellow (elements being compared)
  - **Swapping**: Red (elements being swapped)
  - **Sorted**: Green (elements in final position)
- Smooth animations with adjustable speed
- Modern UI with clean cards and controls

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
Pygame 2.0+
```

### Installation

1. Install Pygame:

```bash
pip install pygame
```

2. Run the visualizer:

```bash
python sorting_visualizer.py
```

## 📖 How to Use

1. **Launch** the program
2. **Adjust settings**:
   - Use the Array Size slider to change number of elements
   - Use the Speed slider to control animation speed
3. **Generate** a random array (or press G)
4. **Start** sorting (or press Space)
5. **Watch** algorithms compete in real-time!
6. **Compare** statistics to see which performs best

## 🎯 Algorithm Comparison

| Algorithm      | Best Case  | Average Case | Worst Case | Space    | Stable |
| -------------- | ---------- | ------------ | ---------- | -------- | ------ |
| Bubble Sort    | O(n)       | O(n²)        | O(n²)      | O(1)     | Yes    |
| Insertion Sort | O(n)       | O(n²)        | O(n²)      | O(1)     | Yes    |
| Selection Sort | O(n²)      | O(n²)        | O(n²)      | O(1)     | No     |
| Quick Sort     | O(n log n) | O(n log n)   | O(n²)      | O(log n) | No     |
| Merge Sort     | O(n log n) | O(n log n)   | O(n log n) | O(n)     | Yes    |

## 🏗️ Architecture

### Object-Oriented Design

```
SortingAlgorithm (Base Class)
├── BubbleSort
├── InsertionSort
├── SelectionSort
├── QuickSort
└── MergeSort

SortingVisualizer (Main Controller)
├── Algorithm Management
├── UI Rendering
├── Event Handling
└── Animation Control
```

### Key Features

**Step-by-Step Execution**
Each algorithm implements `sort_step()` which executes one logical step of the sorting process, allowing for smooth visualization and comparison.

**State Management**

- `IDLE`: Not started
- `RUNNING`: Currently sorting
- `PAUSED`: Temporarily stopped
- `COMPLETED`: Finished sorting

**Modular Design**
Easy to add new algorithms by extending the `SortingAlgorithm` base class.

## 🎨 Customization

### Adding a New Algorithm

```python
class YourSort(SortingAlgorithm):
    def __init__(self):
        super().__init__("Your Sort", Colors.ACCENT_6)
        # Initialize your variables

    def reset(self, array: List[int]):
        super().reset(array)
        # Reset your variables

    def sort_step(self) -> bool:
        # Implement one step of your algorithm
        # Return True if more steps needed, False if done
        pass
```

### Changing Colors

Edit the `Colors` class:

```python
class Colors:
    BACKGROUND = (15, 15, 25)  # Dark blue-gray
    ACCENT_1 = (88, 166, 255)  # Blue for Bubble Sort
    # ... customize other colors
```

### Adjusting Window Size

```python
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
```

## 🔬 Technical Details

### Performance Optimization

- **Variable Speed**: Executes multiple steps per frame based on speed slider
- **Efficient Rendering**: Only updates changed elements
- **60 FPS Cap**: Smooth animations without excessive CPU usage

### Visualization Technique

- Arrays are copied independently for each algorithm
- Each algorithm maintains its own state and statistics
- Synchronous step execution ensures fair comparison

## 🐛 Known Limitations

- Quick Sort may appear faster due to fewer visual updates
- Very high speeds (>90) may cause frame drops on slower systems
- Array sizes >100 may reduce bar visibility

## 💡 Educational Value

Perfect for:

- **Students**: Understanding algorithm behavior and complexity
- **Teachers**: Demonstrating sorting concepts visually
- **Developers**: Comparing algorithm performance
- **Interview Prep**: Visualizing common sorting algorithms

## 🤝 Contributing

Ideas for contributions:

- Add more algorithms (Heap Sort, Radix Sort, Shell Sort)
- Implement algorithm complexity graphs
- Add sound effects for comparisons/swaps
- Create presets for different data patterns (reversed, nearly sorted, etc.)
- Add "race mode" with scoring system

## 📝 Code Quality

- **Clean Architecture**: Separation of concerns with classes
- **Type Hints**: Full type annotations for clarity
- **Documentation**: Comprehensive docstrings
- **No Code Duplication**: DRY principle applied
- **Modular**: Easy to extend and maintain

## 🎓 Learning Outcomes

After using this visualizer, you'll understand:

- How different sorting algorithms work step-by-step
- Why some algorithms are faster than others
- The concept of time/space complexity
- When to use which algorithm
- The importance of algorithm analysis

## 📚 Resources

- [Sorting Algorithm Animations](https://www.toptal.com/developers/sorting-algorithms)
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Pygame Documentation](https://www.pygame.org/docs/)

## 🙏 Acknowledgments

- Inspired by classic sorting visualizers
- Built with Python and Pygame
- Designed for educational purposes

---

**Made with 💙 and lots of comparisons**

_"In theory, theory and practice are the same. In practice, they are not." - Albert Einstein_

## 📧 Questions?

Feel free to experiment, modify, and learn!

**Happy Sorting! 🔢**
