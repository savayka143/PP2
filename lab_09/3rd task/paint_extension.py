import pygame, sys, math

# Инициализируем pygame
pygame.init()

# Определяем цвета
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
PURPLE  = (128, 0, 128)
ORANGE  = (255, 165, 0)
GRAY    = (200, 200, 200)

# Размеры окна и высота панели инструментов
WIDTH = 1500
HEIGHT = 1000
TOOLBAR_HEIGHT = 60

# Создаем главное окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")
clock = pygame.time.Clock()

# Создаем отдельную поверхность для рисования (canvas) под панелью инструментов
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Режимы рисования
MODE_FREE   = 'free'
MODE_RECT   = 'rectangle'
MODE_SQUARE = 'square'
MODE_CIRCLE = 'circle'
MODE_RIGHT_TRIANGLE = 'right_triangle'
MODE_EQUILATERAL_TRIANGLE = 'equilateral_triangle'
MODE_RHOMBUS = 'rhombus'
MODE_ERASER = 'eraser'
draw_mode = MODE_FREE    # по умолчанию свободное рисование

current_color = BLACK    # цвет рисования по умолчанию
brush_size = 5           # толщина кисти

# Устанавливаем шрифт для кнопок панели
button_font = pygame.font.SysFont(None, 24)

# Задаем размеры кнопок и отступы
button_width = 80  # уменьшили ширину, чтобы вместить все кнопки
button_height = 40
padding = 10
start_x = padding
start_y = (TOOLBAR_HEIGHT - button_height) // 2

# Создаем кнопки для инструментов
# Добавлены новые инструменты: квадрат, прямоугольный треугольник, равносторонний треугольник, ромб
tools = [
    {'label': 'Free',      'mode': MODE_FREE},
    {'label': 'Rect',      'mode': MODE_RECT},
    {'label': 'Square',    'mode': MODE_SQUARE},
    {'label': 'Circle',    'mode': MODE_CIRCLE},
    {'label': 'RightTri',  'mode': MODE_RIGHT_TRIANGLE},
    {'label': 'EquiTri',   'mode': MODE_EQUILATERAL_TRIANGLE},
    {'label': 'Rhombus',   'mode': MODE_RHOMBUS},
    {'label': 'Eraser',    'mode': MODE_ERASER}
]
tool_buttons = []
for tool in tools:
    btn_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    tool_buttons.append({'label': tool['label'], 'mode': tool['mode'], 'rect': btn_rect})
    start_x += button_width + padding

# Создаем кнопки выбора цвета
colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
color_buttons = []
for col in colors:
    btn_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    color_buttons.append({'color': col, 'rect': btn_rect})
    start_x += button_width + padding

# Переменные для отслеживания состояния рисования
drawing = False    # флаг, когда пользователь рисует
start_pos = None   # начальная позиция для рисования фигур

# Главный цикл программы
running = True
while running:
    clock.tick(60)  # ограничиваем 60 кадрами в секунду
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Если клик в области панели инструментов
            if pos[1] < TOOLBAR_HEIGHT:
                # Проверяем, нажата ли кнопка инструмента
                for btn in tool_buttons:
                    if btn['rect'].collidepoint(pos):
                        draw_mode = btn['mode']
                # Проверяем, нажата ли кнопка выбора цвета
                for btn in color_buttons:
                    if btn['rect'].collidepoint(pos):
                        current_color = btn['color']
                        # Если в режиме ластика, меняем режим на свободное рисование при выборе цвета
                        if draw_mode == MODE_ERASER:
                            draw_mode = MODE_FREE
            else:
                # Если клик вне панели – в области рисования (canvas)
                canvas_pos = (pos[0], pos[1] - TOOLBAR_HEIGHT)
                drawing = True
                start_pos = canvas_pos
                # Для свободного рисования и ластика сразу рисуем точку
                if draw_mode in [MODE_FREE, MODE_ERASER]:
                    color_to_use = WHITE if draw_mode == MODE_ERASER else current_color
                    pygame.draw.circle(canvas, color_to_use, canvas_pos, brush_size)
        
        # Обработка движения мыши при удерживании кнопки
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = pygame.mouse.get_pos()
                canvas_pos = (pos[0], pos[1] - TOOLBAR_HEIGHT)
                if draw_mode in [MODE_FREE, MODE_ERASER]:
                    color_to_use = WHITE if draw_mode == MODE_ERASER else current_color
                    # Рисуем линию от предыдущей позиции к текущей
                    pygame.draw.line(canvas, color_to_use, start_pos, canvas_pos, brush_size * 2)
                    start_pos = canvas_pos
        
        # Обработка отпускания кнопки мыши для завершения рисования фигуры
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                pos = pygame.mouse.get_pos()
                end_pos = (pos[0], pos[1] - TOOLBAR_HEIGHT)
                
                if draw_mode == MODE_RECT:
                    # Рисуем прямоугольник: вычисляем координаты и размеры
                    rect_x = min(start_pos[0], end_pos[0])
                    rect_y = min(start_pos[1], end_pos[1])
                    rect_width = abs(end_pos[0] - start_pos[0])
                    rect_height = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(canvas, current_color, (rect_x, rect_y, rect_width, rect_height), brush_size)
                
                elif draw_mode == MODE_SQUARE:
                    # Рисуем квадрат: выбираем сторону как максимум из разниц по x и y
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    side = max(abs(dx), abs(dy))
                    # Определяем координаты в зависимости от направления рисования
                    if dx < 0:
                        rect_x = start_pos[0] - side
                    else:
                        rect_x = start_pos[0]
                    if dy < 0:
                        rect_y = start_pos[1] - side
                    else:
                        rect_y = start_pos[1]
                    pygame.draw.rect(canvas, current_color, (rect_x, rect_y, side, side), brush_size)
                
                elif draw_mode == MODE_CIRCLE:
                    # Рисуем окружность: вычисляем радиус по Евклидову расстоянию
                    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                
                elif draw_mode == MODE_RIGHT_TRIANGLE:
                    # Рисуем прямоугольный треугольник с прямым углом в start_pos
                    vertex1 = start_pos
                    vertex2 = (end_pos[0], start_pos[1])
                    vertex3 = (start_pos[0], end_pos[1])
                    pygame.draw.polygon(canvas, current_color, [vertex1, vertex2, vertex3], brush_size)
                
                elif draw_mode == MODE_EQUILATERAL_TRIANGLE:
                    # Рисуем равносторонний треугольник, где базой является отрезок от start_pos до end_pos
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    # Находим середину базы
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    dx = x2 - x1
                    dy = y2 - y1
                    base_length = math.hypot(dx, dy)
                    # Вычисляем высоту равностороннего треугольника
                    height = (math.sqrt(3) / 2) * base_length
                    # Определяем вектор, перпендикулярный базе (-dy, dx)
                    if base_length != 0:
                        perp_dx = -dy / base_length
                        perp_dy = dx / base_length
                    else:
                        perp_dx, perp_dy = 0, 0
                    third_vertex = (mid_x + perp_dx * height, mid_y + perp_dy * height)
                    pygame.draw.polygon(canvas, current_color, [start_pos, end_pos, third_vertex], brush_size)
                
                elif draw_mode == MODE_RHOMBUS:
                    # Рисуем ромб, используя нарисованную диагональ от start_pos до end_pos
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    # Находим центр диагонали
                    center = ((x1 + x2) / 2, (y1 + y2) / 2)
                    # Вычисляем смещение для второй диагонали (перпендикулярно к нарисованной)
                    factor = 0.5  # коэффициент, определяющий длину второй диагонали
                    offset = (-(y2 - y1) * factor, (x2 - x1) * factor)
                    # Определяем оставшиеся две вершины ромба
                    vertex2 = (center[0] + offset[0], center[1] + offset[1])
                    vertex4 = (center[0] - offset[0], center[1] - offset[1])
                    # Задаем порядок вершин для корректного отрисовывания
                    pygame.draw.polygon(canvas, current_color, [start_pos, vertex2, end_pos, vertex4], brush_size)
                
                # Завершаем процесс рисования
                drawing = False
                start_pos = None

    # --- Рисуем интерфейс ---
    
    # Рисуем фон панели инструментов
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    
    # Отрисовываем кнопки инструментов
    for btn in tool_buttons:
        pygame.draw.rect(screen, WHITE, btn['rect'])
        text = button_font.render(btn['label'], True, BLACK)
        text_rect = text.get_rect(center=btn['rect'].center)
        screen.blit(text, text_rect)
    
    # Отрисовываем кнопки выбора цвета
    for btn in color_buttons:
        pygame.draw.rect(screen, btn['color'], btn['rect'])
        # Рисуем рамку вокруг кнопок выбора цвета
        pygame.draw.rect(screen, BLACK, btn['rect'], 2)
    
    # Накладываем область для рисования (canvas) на главное окно
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
