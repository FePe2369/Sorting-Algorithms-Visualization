import pygame
import random
import time
from enum import Enum
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Colors
class Colors:
    BACKGROUND = (15, 15, 25)
    CARD_BG = (25, 25, 40)
    TEXT_PRIMARY = (220, 220, 240)
    TEXT_SECONDARY = (140, 140, 160)
    ACCENT_1 = (88, 166, 255)  # Blue
    ACCENT_2 = (255, 107, 107)  # Red
    ACCENT_3 = (106, 255, 193)  # Green
    ACCENT_4 = (255, 193, 106)  # Orange
    ACCENT_5 = (187, 107, 255)  # Purple
    BAR_DEFAULT = (70, 70, 100)
    BAR_COMPARING = (255, 200, 0)
    BAR_SWAPPING = (255, 100, 100)
    BAR_SORTED = (100, 255, 150)
    BORDER = (60, 60, 80)

class SortState(Enum):
    IDLE = 1
    RUNNING = 2
    PAUSED = 3
    COMPLETED = 4

class SortingAlgorithm:
    """Base class for sorting algorithms"""
    
    def __init__(self, name: str, color: Tuple[int, int, int]):
        self.name = name
        self.color = color
        self.array = []
        self.comparisons = 0
        self.swaps = 0
        self.state = SortState.IDLE
        self.start_time = 0
        self.end_time = 0
        self.current_indices = []  # Indices being compared/swapped
        self.sorted_indices = set()  # Indices that are in final position
        
    def reset(self, array: List[int]):
        """Reset algorithm state with new array"""
        self.array = array.copy()
        self.comparisons = 0
        self.swaps = 0
        self.state = SortState.IDLE
        self.start_time = 0
        self.end_time = 0
        self.current_indices = []
        self.sorted_indices = set()
        
    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        if self.state == SortState.COMPLETED:
            return self.end_time - self.start_time
        elif self.state == SortState.RUNNING:
            return time.time() - self.start_time
        return 0
    
    def sort_step(self) -> bool:
        """Execute one step of sorting. Returns True if more steps needed."""
        raise NotImplementedError

class BubbleSort(SortingAlgorithm):
    def __init__(self):
        super().__init__("Bubble Sort", Colors.ACCENT_1)
        self.i = 0
        self.j = 0
        
    def reset(self, array: List[int]):
        super().reset(array)
        self.i = 0
        self.j = 0
        
    def sort_step(self) -> bool:
        if self.j < len(self.array) - self.i - 1:
            self.current_indices = [self.j, self.j + 1]
            self.comparisons += 1
            
            if self.array[self.j] > self.array[self.j + 1]:
                self.array[self.j], self.array[self.j + 1] = self.array[self.j + 1], self.array[self.j]
                self.swaps += 1
                
            self.j += 1
            return True
        else:
            self.sorted_indices.add(len(self.array) - self.i - 1)
            self.j = 0
            self.i += 1
            
            if self.i < len(self.array) - 1:
                return True
            else:
                self.sorted_indices = set(range(len(self.array)))
                return False

class InsertionSort(SortingAlgorithm):
    def __init__(self):
        super().__init__("Insertion Sort", Colors.ACCENT_2)
        self.step = 1
        self.j = 0
        self.key = 0
        self.inserting = False
        
    def reset(self, array: List[int]):
        super().reset(array)
        self.step = 1
        self.j = 0
        self.key = 0
        self.inserting = False
        
    def sort_step(self) -> bool:
        if self.step < len(self.array):
            if not self.inserting:
                self.key = self.array[self.step]
                self.j = self.step - 1
                self.inserting = True
                self.current_indices = [self.step]
                return True
                
            if self.j >= 0:
                self.current_indices = [self.j, self.j + 1]
                self.comparisons += 1
                
                if self.key < self.array[self.j]:
                    self.array[self.j + 1] = self.array[self.j]
                    self.swaps += 1
                    self.j -= 1
                    return True
                    
            self.array[self.j + 1] = self.key
            self.sorted_indices = set(range(self.step + 1))
            self.step += 1
            self.inserting = False
            return True
        else:
            self.sorted_indices = set(range(len(self.array)))
            return False

class SelectionSort(SortingAlgorithm):
    def __init__(self):
        super().__init__("Selection Sort", Colors.ACCENT_3)
        self.step = 0
        self.i = 0
        self.min_idx = 0
        self.finding_min = True
        
    def reset(self, array: List[int]):
        super().reset(array)
        self.step = 0
        self.i = 0
        self.min_idx = 0
        self.finding_min = True
        
    def sort_step(self) -> bool:
        if self.step < len(self.array):
            if self.finding_min:
                if self.i == self.step:
                    self.min_idx = self.step
                    self.i = self.step + 1
                    
                if self.i < len(self.array):
                    self.current_indices = [self.min_idx, self.i]
                    self.comparisons += 1
                    
                    if self.array[self.i] < self.array[self.min_idx]:
                        self.min_idx = self.i
                    
                    self.i += 1
                    return True
                else:
                    self.finding_min = False
                    
            if not self.finding_min:
                if self.min_idx != self.step:
                    self.array[self.step], self.array[self.min_idx] = self.array[self.min_idx], self.array[self.step]
                    self.swaps += 1
                    
                self.sorted_indices.add(self.step)
                self.step += 1
                self.i = self.step
                self.finding_min = True
                return True
        else:
            self.sorted_indices = set(range(len(self.array)))
            return False

class QuickSort(SortingAlgorithm):
    def __init__(self):
        super().__init__("Quick Sort", Colors.ACCENT_4)
        self.stack = []
        self.partition_step = None
        
    def reset(self, array: List[int]):
        super().reset(array)
        self.stack = [(0, len(array) - 1)]
        self.partition_step = None
        
    def sort_step(self) -> bool:
        if not self.stack and self.partition_step is None:
            self.sorted_indices = set(range(len(self.array)))
            return False
            
        if self.partition_step is None:
            # Keep popping until we find a valid segment or run out
            while self.stack:
                low, high = self.stack.pop()
                if low < high:
                    self.partition_step = {'low': low, 'high': high, 'i': low - 1, 'j': low}
                    return True
            # No valid segments left
            self.sorted_indices = set(range(len(self.array)))
            return False
            
        ps = self.partition_step
        pivot = self.array[ps['high']]
        
        if ps['j'] < ps['high']:
            self.current_indices = [ps['j'], ps['high']]
            self.comparisons += 1
            
            if self.array[ps['j']] < pivot:
                ps['i'] += 1
                self.array[ps['i']], self.array[ps['j']] = self.array[ps['j']], self.array[ps['i']]
                self.swaps += 1
                
            ps['j'] += 1
            return True
        else:
            self.array[ps['i'] + 1], self.array[ps['high']] = self.array[ps['high']], self.array[ps['i'] + 1]
            self.swaps += 1
            pivot_idx = ps['i'] + 1
            
            self.stack.append((ps['low'], pivot_idx - 1))
            self.stack.append((pivot_idx + 1, ps['high']))
            self.partition_step = None
            return True

class MergeSort(SortingAlgorithm):
    def __init__(self):
        super().__init__("Merge Sort", Colors.ACCENT_5)
        self.merge_steps = []
        self.current_merge = None
        
    def reset(self, array: List[int]):
        super().reset(array)
        self.merge_steps = self._generate_merge_steps(0, len(array) - 1)
        self.current_merge = None
        
    def _generate_merge_steps(self, left: int, right: int) -> List:
        steps = []
        if left < right:
            mid = (left + right) // 2
            steps.extend(self._generate_merge_steps(left, mid))
            steps.extend(self._generate_merge_steps(mid + 1, right))
            steps.append(('merge', left, mid, right))
        return steps
        
    def sort_step(self) -> bool:
        if not self.merge_steps and self.current_merge is None:
            self.sorted_indices = set(range(len(self.array)))
            return False
            
        if self.current_merge is None:
            if not self.merge_steps:
                return False
            _, left, mid, right = self.merge_steps.pop(0)
            left_arr = self.array[left:mid + 1].copy()
            right_arr = self.array[mid + 1:right + 1].copy()
            self.current_merge = {
                'left': left, 'mid': mid, 'right': right,
                'left_arr': left_arr, 'right_arr': right_arr,
                'i': 0, 'j': 0, 'k': left
            }
            
        cm = self.current_merge
        self.comparisons += 1
        
        if cm['i'] < len(cm['left_arr']) and cm['j'] < len(cm['right_arr']):
            self.current_indices = [cm['k']]
            if cm['left_arr'][cm['i']] <= cm['right_arr'][cm['j']]:
                self.array[cm['k']] = cm['left_arr'][cm['i']]
                cm['i'] += 1
            else:
                self.array[cm['k']] = cm['right_arr'][cm['j']]
                cm['j'] += 1
            self.swaps += 1
            cm['k'] += 1
            return True
        elif cm['i'] < len(cm['left_arr']):
            self.array[cm['k']] = cm['left_arr'][cm['i']]
            cm['i'] += 1
            cm['k'] += 1
            self.swaps += 1
            return True
        elif cm['j'] < len(cm['right_arr']):
            self.array[cm['k']] = cm['right_arr'][cm['j']]
            cm['j'] += 1
            cm['k'] += 1
            self.swaps += 1
            return True
        else:
            self.current_merge = None
            return True

class SortingVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        # Algorithms
        self.algorithms = [
            BubbleSort(),
            InsertionSort(),
            SelectionSort(),
            QuickSort(),
            MergeSort()
        ]
        
        # Settings
        self.array_size = 50
        self.speed = 50  # 1-100
        self.master_array = []
        self.generate_array()
        
        # UI State
        self.running = True
        self.sorting = False
        self.paused = False
        
        # UI Elements
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI button positions"""
        self.buttons = {
            'generate': pygame.Rect(50, SCREEN_HEIGHT - 70, 150, 40),
            'start': pygame.Rect(220, SCREEN_HEIGHT - 70, 150, 40),
            'pause': pygame.Rect(390, SCREEN_HEIGHT - 70, 150, 40),
            'reset': pygame.Rect(560, SCREEN_HEIGHT - 70, 150, 40),
        }
        
        self.sliders = {
            'size': {'rect': pygame.Rect(900, SCREEN_HEIGHT - 60, 200, 10), 'value': self.array_size, 'min': 10, 'max': 100},
            'speed': {'rect': pygame.Rect(1150, SCREEN_HEIGHT - 60, 200, 10), 'value': self.speed, 'min': 1, 'max': 100},
        }
        
    def generate_array(self):
        """Generate random array"""
        self.master_array = [random.randint(10, 400) for _ in range(self.array_size)]
        for algo in self.algorithms:
            algo.reset(self.master_array)
            
    def start_sorting(self):
        """Start all algorithms"""
        self.sorting = True
        self.paused = False
        for algo in self.algorithms:
            algo.state = SortState.RUNNING
            algo.start_time = time.time()
            
    def pause_sorting(self):
        """Toggle pause"""
        self.paused = not self.paused
        for algo in self.algorithms:
            if algo.state == SortState.RUNNING:
                algo.state = SortState.PAUSED
            elif algo.state == SortState.PAUSED:
                algo.state = SortState.RUNNING
                
    def reset_sorting(self):
        """Reset all algorithms"""
        self.sorting = False
        self.paused = False
        for algo in self.algorithms:
            algo.reset(self.master_array)
            
    def update(self):
        """Update sorting algorithms"""
        if self.sorting and not self.paused:
            all_done = True
            for algo in self.algorithms:
                if algo.state == SortState.RUNNING:
                    # Execute multiple steps based on speed
                    steps = max(1, self.speed // 10)
                    for _ in range(steps):
                        if not algo.sort_step():
                            algo.state = SortState.COMPLETED
                            algo.end_time = time.time()
                            break
                    if algo.state == SortState.RUNNING:
                        all_done = False
                        
            if all_done:
                self.sorting = False
                
    def draw_array(self, algo: SortingAlgorithm, x: int, y: int, width: int, height: int):
        """Draw algorithm visualization"""
        # Background card
        pygame.draw.rect(self.screen, Colors.CARD_BG, (x, y, width, height))
        pygame.draw.rect(self.screen, Colors.BORDER, (x, y, width, height), 2)
        
        # Title
        title = self.font_medium.render(algo.name, True, algo.color)
        self.screen.blit(title, (x + 15, y + 15))
        
        # Stats
        stats_y = y + 50
        stats = [
            f"Comparisons: {algo.comparisons}",
            f"Swaps: {algo.swaps}",
            f"Time: {algo.get_elapsed_time():.3f}s"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_small.render(stat, True, Colors.TEXT_SECONDARY)
            self.screen.blit(text, (x + 15, stats_y + i * 22))
            
        # Array visualization
        array_y = y + 150
        array_height = height - 170
        bar_width = (width - 40) / len(algo.array)
        max_val = max(algo.array) if algo.array else 1
        
        for i, val in enumerate(algo.array):
            bar_height = (val / max_val) * (array_height - 20)
            bar_x = x + 20 + i * bar_width
            bar_y = y + height - 20 - bar_height
            
            # Determine color
            if i in algo.sorted_indices:
                color = Colors.BAR_SORTED
            elif i in algo.current_indices:
                color = Colors.BAR_COMPARING if len(algo.current_indices) > 1 else Colors.BAR_SWAPPING
            else:
                color = algo.color
                
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, bar_width - 2, bar_height))
            
    def draw_button(self, name: str, rect: pygame.Rect, text: str):
        """Draw a button"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        
        color = Colors.ACCENT_1 if is_hover else Colors.BORDER
        pygame.draw.rect(self.screen, color, rect, 0, 5)
        pygame.draw.rect(self.screen, Colors.ACCENT_1, rect, 2, 5)
        
        text_surf = self.font_medium.render(text, True, Colors.TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        
    def draw_slider(self, name: str, slider: dict, label: str):
        """Draw a slider"""
        # Label
        text = self.font_small.render(f"{label}: {slider['value']}", True, Colors.TEXT_PRIMARY)
        self.screen.blit(text, (slider['rect'].x, slider['rect'].y - 25))
        
        # Track
        pygame.draw.rect(self.screen, Colors.BORDER, slider['rect'], 0, 5)
        
        # Fill
        progress = (slider['value'] - slider['min']) / (slider['max'] - slider['min'])
        fill_rect = slider['rect'].copy()
        fill_rect.width = int(slider['rect'].width * progress)
        pygame.draw.rect(self.screen, Colors.ACCENT_1, fill_rect, 0, 5)
        
        # Handle
        handle_x = slider['rect'].x + fill_rect.width
        handle_rect = pygame.Rect(handle_x - 8, slider['rect'].y - 5, 16, 20)
        pygame.draw.rect(self.screen, Colors.ACCENT_1, handle_rect, 0, 3)
        
    def handle_slider_drag(self, name: str, slider: dict, mouse_pos):
        """Handle slider dragging"""
        relative_x = mouse_pos[0] - slider['rect'].x
        relative_x = max(0, min(relative_x, slider['rect'].width))
        progress = relative_x / slider['rect'].width
        new_value = int(slider['min'] + progress * (slider['max'] - slider['min']))
        slider['value'] = new_value
        
        if name == 'size':
            self.array_size = new_value
        elif name == 'speed':
            self.speed = new_value
            
    def draw(self):
        """Main draw function"""
        self.screen.fill(Colors.BACKGROUND)
        
        # Title
        title = self.font_large.render("Sorting Algorithm Visualizer", True, Colors.TEXT_PRIMARY)
        self.screen.blit(title, (50, 30))
        
        # Draw algorithms in 2 rows
        algo_width = (SCREEN_WIDTH - 120) // 3
        algo_height = (SCREEN_HEIGHT - 280) // 2
        
        for i, algo in enumerate(self.algorithms):
            row = i // 3
            col = i % 3
            x = 50 + col * (algo_width + 20)
            y = 80 + row * (algo_height + 20)
            self.draw_array(algo, x, y, algo_width, algo_height)
            
        # Draw controls
        self.draw_button('generate', self.buttons['generate'], "Generate")
        self.draw_button('start', self.buttons['start'], "Start All")
        
        pause_text = "Resume" if self.paused else "Pause"
        self.draw_button('pause', self.buttons['pause'], pause_text)
        self.draw_button('reset', self.buttons['reset'], "Reset")
        
        self.draw_slider('size', self.sliders['size'], "Array Size")
        self.draw_slider('speed', self.sliders['speed'], "Speed")
        
        pygame.display.flip()
        
    def handle_events(self):
        """Handle pygame events"""
        dragging_slider = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check buttons
                if self.buttons['generate'].collidepoint(mouse_pos):
                    self.generate_array()
                    self.reset_sorting()
                elif self.buttons['start'].collidepoint(mouse_pos) and not self.sorting:
                    self.start_sorting()
                elif self.buttons['pause'].collidepoint(mouse_pos) and self.sorting:
                    self.pause_sorting()
                elif self.buttons['reset'].collidepoint(mouse_pos):
                    self.reset_sorting()
                    
                # Check sliders
                for name, slider in self.sliders.items():
                    handle_x = slider['rect'].x + int((slider['value'] - slider['min']) / (slider['max'] - slider['min']) * slider['rect'].width)
                    handle_rect = pygame.Rect(handle_x - 8, slider['rect'].y - 5, 16, 20)
                    if handle_rect.collidepoint(mouse_pos) or slider['rect'].collidepoint(mouse_pos):
                        dragging_slider = name
                        self.handle_slider_drag(name, slider, mouse_pos)
                        
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if dragging_slider:
                    self.handle_slider_drag(dragging_slider, self.sliders[dragging_slider], pygame.mouse.get_pos())
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.sorting:
                        self.start_sorting()
                    else:
                        self.pause_sorting()
                elif event.key == pygame.K_r:
                    self.reset_sorting()
                elif event.key == pygame.K_g:
                    self.generate_array()
                    self.reset_sorting()
                    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    visualizer = SortingVisualizer()
    visualizer.run()