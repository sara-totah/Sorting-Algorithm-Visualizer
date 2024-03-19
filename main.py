import pygame
import random
import math

pygame.init()

class SortVisualizer:
    BLACK = 0, 0, 0
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = (255, 255, 255)
    BLOCK_COLORS = [(102, 173, 228), (81, 162, 224), (59, 150, 221)]
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 50)
    SIDE_PAD = 100
    TOP_PAD = 150
    
    def __init__(self, width, height, lst) -> None:
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)
 
    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 70))
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort ", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 120))
    draw_list(draw_info)
    pygame.display.update()
    
    
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.block_height
        color = draw_info.BLOCK_COLORS[i % 3]
        if i in color_positions:
            color = color_positions[i] 
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()
           
def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1 - i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)):
        min_index = i
        for j in range(i+1, len(lst)):
            if (ascending and lst[j] < lst[min_index]) or (not ascending and lst[j] > lst[min_index]):
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
        yield True
        

def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    sorting = False
    ascending = True
    sort_algorithm = bubble_sort
    sort_algorithm_name = "Bubble Sort"
    sort_algorithm_generator = None
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = SortVisualizer(1200, 700, lst)
    while run:
        clock.tick(30) #this can be adjusted for a faster or slower sorting
        draw(draw_info, sort_algorithm_name, ascending)
        if sorting:
            try:
                next(sort_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sort_algorithm_name, ascending)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sort_algorithm_generator = sort_algorithm(draw_info, ascending)
            elif (event.key == pygame.K_a and not sorting):
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sort_algorithm = insertion_sort
                sort_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sort_algorithm = bubble_sort
                sort_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sort_algorithm = selection_sort
                sort_algorithm_name = "Selection Sort"
    pygame.quit()

if __name__ == "__main__":
	main()