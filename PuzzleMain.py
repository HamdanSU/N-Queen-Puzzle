"""
This the main driver file. It will be responsible for handling user input and displaying the current PuzzleState object.
"""

import pygame as p
import sys
import pygame_gui as p_gui

from PuzzleEngine import PuzzleState

p.init()
width = height = 512
screen_width = width + 300
screen_height = height + 200

p.display.set_caption('N-Queen Puzzle')
screen = p.display.set_mode((screen_width, screen_height))
manager = p_gui.UIManager((screen_width, screen_height))
clock = p.time.Clock()

dark_blue = (33, 40, 45)
white = (255, 255, 255)

max_fpx = 15  # For queen movement

gui_components = {}

main_font = p.font.SysFont(None, 90, bold=True)
font_sub = p.font.SysFont(None, 70, bold=True)
font_opt = p.font.SysFont(None, 40, bold=True)

puzzle_variable = {'dimensions': 8, 'Algorithm': 'A*', 'crossover': 'Single point', 'crossover_rate': 0.9,
                   'mutation_rate': 0.1, "recombination": 'With elitism',
                   'population_size': 100, 'n_generations': 250}


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


"""
Responsible for managing the main menu UI elements and its controls.
"""


def main_menu():
    draw_main_menu_ui()
    running = True
    ps = PuzzleState(puzzle_variable)
    ps.initialize_generation()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
                running = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    p.quit()
                    sys.exit()
                    running = False

            manager.process_events(e)
            if e.type == p.USEREVENT:
                if e.user_type == p_gui.UI_BUTTON_PRESSED:
                    if e.ui_element == gui_components['start_button']:
                        puzzle_screen()
                    elif e.ui_element == gui_components['settings']:
                        settings_menu()

        manager.update(max_fpx)
        manager.draw_ui(screen)
        clock.tick(max_fpx)
        p.display.update()


"""
Responsible for managing the settings menu UI elements, User inputs and algorithms' parameters.
"""


def settings_menu():
    running = True
    manager.clear_and_reset()
    draw_settings_ui()
    if puzzle_variable['Algorithm'] == 'Genetic':
        genetic_parameters_ui()

    while running:
        screen.fill(dark_blue)
        draw_settings_text()
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
                running = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    manager.clear_and_reset()
                    draw_main_menu_ui()
                    running = False
            manager.process_events(e)
            if e.type == p.USEREVENT:
                if e.user_type == p_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if e.ui_element == gui_components['algorithm']:
                        puzzle_variable['Algorithm'] = gui_components['algorithm'].selected_option
                        if puzzle_variable['Algorithm'] == 'Genetic':
                            genetic_parameters_ui()
                        else:
                            manager.clear_and_reset()
                            draw_settings_ui()
                    elif e.ui_element == gui_components['board_size']:
                        puzzle_variable['dimensions'] = int(gui_components['board_size'].selected_option)
                    elif e.ui_element == gui_components['crossover']:
                        puzzle_variable['crossover'] = gui_components['crossover'].selected_option
                    elif e.ui_element == gui_components['recombination']:
                        puzzle_variable['recombination'] = gui_components['recombination'].selected_option
                    elif e.ui_element == gui_components['crossover_rate']:
                        puzzle_variable['crossover_rate'] = float(gui_components['crossover_rate'].selected_option)
                    elif e.ui_element == gui_components['mutation_rate']:
                        puzzle_variable['mutation_rate'] = float(gui_components['mutation_rate'].selected_option)
                elif e.user_type == p_gui.UI_BUTTON_PRESSED:
                    if e.ui_element == gui_components['save_button']:
                        try:
                            if puzzle_variable['Algorithm'] == 'Genetic':
                                puzzle_variable['population_size'] = int(gui_components['population_size'].text)
                                puzzle_variable['n_generations'] = int(gui_components['n_generations'].text)
                            running = False
                            manager.clear_and_reset()
                            draw_main_menu_ui()
                        except:
                            manager.clear_and_reset()
                            draw_settings_ui()
                    elif e.ui_element == gui_components['reset_button']:
                        manager.clear_and_reset()
                        init_vars = {'dimensions': 8, 'Algorithm': 'A*', 'crossover': 'Single point',
                                     'crossover_rate': 0.9,
                                     'mutation_rate': 0.1, "recombination": 'With elitism',
                                     'population_size': 100, 'n_generations': 250}
                        for var in init_vars:
                            puzzle_variable[var] = init_vars[var]
                        draw_settings_ui()

        manager.update(max_fpx)
        manager.draw_ui(screen)
        clock.tick(max_fpx)
        p.display.update()


"""
Responsible for displaying the puzzle board, queens, number of steps, and elapsed time.
"""


def puzzle_screen():
    speed = 10
    p.display.set_mode((width + 300, height + 100))
    ps = PuzzleState(puzzle_variable)
    running = True
    paused = True
    solved = False
    manager.clear_and_reset()

    draw_board()
    draw_puzzle_ui()
    number_of_steps = 0

    cur_gen = 0
    start_time = 0
    counting_time = 0

    while running:
        if not paused and not solved:
            if puzzle_variable['Algorithm'] == 'A*':
                solved = paused = ps.astar_algorithm()
                number_of_steps += 1
            else:
                solved, n_gen = ps.genetic_algorithm()
                number_of_steps += puzzle_variable['dimensions']
                paused = solved
                cur_gen = n_gen
        elif solved:
            gui_components['toggle_button'].disable()
            gui_components['return_button'].enable()

        screen.fill(dark_blue)
        draw_text('Step:', font_opt, white, screen, 550, 50)
        draw_text(str(number_of_steps), font_opt, white, screen, 650, 50)

        minutes = int(counting_time / 60000)
        seconds = int((counting_time % 60000) / 1000)
        m_seconds = int(counting_time % 1000)
        shown_1 = str(seconds)
        shown_2 = str(m_seconds)
        letter = 's'
        if minutes > 0:
            letter = ' min'

            shown_1 = '{:02}'.format(minutes)
            shown_2 = '{:02}'.format(seconds)
        draw_text('Time:', font_opt, white, screen, 550, 150)
        draw_text(shown_1 + '.' + shown_2 + letter,
                  font_opt, white, screen, 650, 150)

        if puzzle_variable['Algorithm'] == 'Genetic':
            draw_text('Gen:', font_opt, white, screen, 550, 250)
            draw_text(str(cur_gen), font_opt, white, screen, 650, 250)

        draw_board()
        draw_queens(ps)
        if not paused:
            counting_time = p.time.get_ticks() - start_time

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
                running = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    if paused:
                        p.display.set_mode((screen_width, screen_height))
                        manager.clear_and_reset()
                        draw_main_menu_ui()
                        running = False
            manager.process_events(e)
            if e.type == p.USEREVENT:
                if e.user_type == p_gui.UI_BUTTON_PRESSED:
                    if e.ui_element == gui_components['toggle_button']:
                        if gui_components['toggle_button'].text == "Run":
                            paused = False
                            start_time = p.time.get_ticks()
                            gui_components['toggle_button'].set_text('Stop')
                            gui_components['return_button'].disable()
                        else:
                            paused = True
                            gui_components['toggle_button'].set_text('Run')
                            gui_components['return_button'].enable()
                    elif e.ui_element == gui_components['return_button']:
                        p.display.set_mode((screen_width, screen_height))
                        running = False
                        manager.clear_and_reset()
                        draw_main_menu_ui()
                elif e.user_type == p_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    speed = gui_components['speed_slide'].current_value

        manager.update(max_fpx)
        manager.draw_ui(screen)
        clock.tick(speed)
        p.display.update()


"""
Responsible for drawing main menu UI elements.
"""


def draw_main_menu_ui():
    screen.fill(dark_blue)
    q_image = p.transform.scale(p.image.load('images/wQ.png'), (100, 100))
    screen.blit(q_image,
                p.Rect(350, 50, 300, 300))

    draw_text('N-Queen Puzzle', main_font, white, screen, 130, 160)

    gui_components['start_button'] = p_gui.elements.UIButton(
        text='Start',
        relative_rect=p.Rect((200, 300), (400, 50)),
        manager=manager)

    gui_components['settings'] = p_gui.elements.UIButton(
        text='Settings',
        relative_rect=p.Rect((200, 400), (400, 50)),
        manager=manager)


"""
Responsible for drawing settings menu UI elements.
"""


def draw_settings_ui():
    x_label = 50
    label_width = 200
    label_height = 50

    x_drop = 250
    drop_width = 350
    drop_height = 40

    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 100), (label_width, label_height)),
                           text='Algorithm:',
                           manager=manager)
    gui_components['algorithm'] = p_gui.elements.UIDropDownMenu(options_list=['A*', 'Genetic'],
                                                                starting_option=puzzle_variable['Algorithm'],
                                                                relative_rect=p.Rect((x_drop, 110),
                                                                                     (drop_width, drop_height)),
                                                                manager=manager)

    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 170), (label_width, label_height)),
                           text='N:',
                           manager=manager)

    options_list = []
    for i in range(4, 21):
        options_list.append(str(i))

    gui_components['board_size'] = p_gui.elements.UIDropDownMenu(
        options_list=options_list,
        starting_option=str(puzzle_variable['dimensions']),
        relative_rect=p.Rect((x_drop, 180), (drop_width, drop_height)),
        manager=manager
    )

    gui_components['save_button'] = p_gui.elements.UIButton(
        text='Save',
        relative_rect=p.Rect((650, 600), (150, 40)),
        manager=manager
    )
    gui_components['reset_button'] = p_gui.elements.UIButton(
        text='Reset',
        relative_rect=p.Rect((650, 650), (150, 40)),
        manager=manager
    )


"""
Responsible for drawing genetic algorithm parameters when its selected.
"""


def genetic_parameters_ui():
    x_label = 50
    label_width = 200
    label_height = 50

    x_entries = 250
    entries_width = 350
    entries_height = 40
    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 240), (label_width, label_height)),
                           text='Population size:',
                           manager=manager,
                           )
    gui_components['population_size'] = p_gui.elements.UITextEntryLine(
        relative_rect=p.Rect((x_entries, 250), (entries_width, entries_height)),
        manager=manager,

    )
    gui_components['population_size'].set_text(str(puzzle_variable['population_size']))

    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 310), (label_width, label_height)),
                           text='Number of generations:',
                           manager=manager,
                           )

    gui_components['n_generations'] = p_gui.elements.UITextEntryLine(
        relative_rect=p.Rect((x_entries, 320), (entries_width, entries_height)),
        manager=manager,
    )
    gui_components['n_generations'].set_text(str(puzzle_variable['n_generations']))
    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 380), (label_width, label_height)),
                           text='Crossover:',
                           manager=manager,
                           )
    gui_components['crossover'] = p_gui.elements.UIDropDownMenu(
        options_list=['Single point', 'Multi-point'],
        starting_option=puzzle_variable['crossover'],
        relative_rect=p.Rect((x_entries, 390), (entries_width, entries_height)),
        manager=manager
    )

    rates_list = []
    for i in range(1, 10):
        rates_list.append('0.' + str(i))
    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 450), (label_width, label_height)),
                           text='Crossover rate:',
                           manager=manager,
                           )

    gui_components['crossover_rate'] = p_gui.elements.UIDropDownMenu(
        options_list=rates_list,
        starting_option=str(puzzle_variable['crossover_rate']),
        relative_rect=p.Rect((x_entries, 460), (entries_width, entries_height)),
        manager=manager
    )
    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 520), (label_width, label_height)),
                           text='Mutation rate:',
                           manager=manager,
                           )

    gui_components['mutation_rate'] = p_gui.elements.UIDropDownMenu(
        options_list=rates_list,
        starting_option=str(puzzle_variable['mutation_rate']),
        relative_rect=p.Rect((x_entries, 530), (entries_width, entries_height)),
        manager=manager
    )
    p_gui.elements.UILabel(relative_rect=p.Rect((x_label, 580), (label_width, label_height)),
                           text='Recombination:',
                           manager=manager,
                           )
    gui_components['recombination'] = p_gui.elements.UIDropDownMenu(
        options_list=['With elitism', 'Without elitism'],
        starting_option=puzzle_variable['recombination'],
        relative_rect=p.Rect((x_entries, 590), (entries_width, entries_height)),
        manager=manager
    )


"""
Responsible for drawing settings menu decorations.
"""


def draw_settings_text():
    draw_text('Settings', font_sub, white, screen, 290, 30)

    q_image = p.transform.scale(p.image.load('images/wQ.png'), (100, 100))
    screen.blit(q_image,
                p.Rect(0, 0, 300, 300))

    screen.blit(q_image,
                p.Rect(712, 0, 300, 300))


"""
Responsible for drawing of the board's squares
"""


def draw_board():
    dimensions = puzzle_variable['dimensions']
    sq_size = (height // dimensions)  # Size of each square

    colors = [p.Color('gray'), dark_blue]
    for row in range(dimensions):
        for column in range(dimensions):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color,
                        p.Rect(row * sq_size, column * sq_size, sq_size, sq_size))


"""
Responsible for the drawing of the queens on the board using the PuzzleState.board variable
"""


def draw_queens(ps):
    dimensions = puzzle_variable['dimensions']
    sq_size = height // dimensions  # Size of each square
    q_image = p.transform.scale(p.image.load('images/wQ.png'), (sq_size, sq_size))  # Queen image

    for column in range(dimensions):
        screen.blit(q_image,
                    p.Rect(column * sq_size, ps.board[column] * sq_size, sq_size, sq_size))


"""
Responsible for drawing the puzzle screen controls.
"""


def draw_puzzle_ui():
    x_button = 600
    button_width = 200
    button_height = 40
    gui_components['toggle_button'] = p_gui.elements.UIButton(
        text='Run',
        relative_rect=p.Rect((x_button, 500), (button_width, button_height)),
        manager=manager
    )
    gui_components['return_button'] = p_gui.elements.UIButton(
        text='Return',
        relative_rect=p.Rect((x_button, 550), (button_width, button_height)),
        manager=manager
    )

    gui_components['speed_slide'] = p_gui.elements.UIHorizontalSlider(
        relative_rect=p.Rect((x_button, 425), (button_width, button_height)),
        manager=manager,
        start_value=10,
        value_range=[10, 100]
    )


if __name__ == '__main__':
    main_menu()
