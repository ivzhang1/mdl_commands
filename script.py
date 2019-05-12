import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    polygons = []
    edges = []

    for command in commands:
        if command['op'] == 'push':
            stack.append(stack[-1][:])

        elif command['op'] == 'pop':
            stack.pop()

        elif command['op'] == 'move':
            t = make_translate(command['args'][0],command['args'][1],command['args'][2])
            matrix_mult(stack[-1], t)
            stack[-1] = t

        elif command['op'] == 'scale':
            t = make_scale(command['args'][0],command['args'][1],command['args'][2])
            matrix_mult(stack[-1], t)
            stack[-1] = t

        elif command['op'] == 'rotate':
            t = new_matrix()
            if(command['args'][0] == 'x'):
                t = make_rotX(command['args'][1])

            elif(command['args'][0] == 'y'):
                t = make_rotY(command['args'][1])

            elif(command['args'][0] == 'z'):
                t = make_rotZ(command['args'][1])

            else:
                print("Input axis for rotate is incorrect")

            matrix_mult(stack[-1], t)
            stack[-1] = t

        elif command['op'] in 'sphere box torus':
            if command['op'] == 'sphere':
                add_sphere(polygons, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]), float(command['args'][3]), step_3d)
            elif command['op'] == 'box':
                add_box(polygons, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]), float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            elif command['op'] == 'torus':
                add_torus(polygons, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]), float(command['args'][3]), float(command['args'][4]), step_3d)

            matrix_mult( stack[-1], polygons )
            if(command['constants']):
                try:
                    draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
                except KeyError:
                    draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif command['op'] == 'line':
            add_edge(edges, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]), float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            matrix_mult( stack[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []
