try:
    from fabric.colors import blue,green,cyan,magenta,red
except ImportError:
    _color = lambda txt,arg=None: txt
    blue,green,cyan,magenta,red = _color,_color,_color,_color,_color

def display_error():
    print red("ERROR!!",True)
    print red('An ACTION must be supplied, see usage below.\n\n',True)
    display_usage()

def display_usage():
    import sys
    print green('''{0}\n\tA command line task manager\n\n\nUSAGE:\n{0} [ACTION [arg [arg ...]]]

    Actions:
      {0} list [PROJECT_NAME]\t\t\t\t\t\t\tList PROJECT_NAME or all projects

      {0} create PROJECT_NAME\t\t\t\t\t\t\tCreate new collection of tasks under PROJECT_NAME

      {0} add PROJECT_NAME <[TASK_NAME]> <[DESCRIPTION]> <[DUE [Y,M,D]]>\t\tAdd new task TASK_NAME to PROJECT_NAME

      {0} complete [TASK_ID]\t\t\t\t\t\t\tComplete Task_id or list all completed tasks

      {0} remove PROJECT_NAME\t\t\t\t\t\t\tRemove PROJECT_NAME

    '''.format(sys.argv[0]),True)
    sys.exit(0)

def run_argv(funcs):
    import sys
    ACTIONS = [
        'list',
        'create',
        'add',
        'complete',
        'remove',
    ]
    if any(filter(lambda x: x in sys.argv,['-h','--help'])):
        display_usage()
    if len(sys.argv) <= 1 or sys.argv[1] not in ACTIONS:
        display_error()
    dict(zip(ACTIONS,funcs))[sys.argv[1]](*sys.argv[2:])
