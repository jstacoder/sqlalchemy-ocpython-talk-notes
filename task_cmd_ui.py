
def _print_project(name,data):
    HEAD_LIST = ['id','name','description','due_date','complete']
    _proj = data
    print 'Project: {}'.format(name)
    FMT = '|{:^15}|{:<15}|{:<25}|{:<15}|{:<15}|'
    HEAD_FMT = '|{:^15}|{:^15}|{:^25}|{:^15}|{:^15}|'
    head = HEAD_FMT.format(*HEAD_LIST)
    print head
    print '-'*len(head)
    print '\n'.join(map(str,map(lambda x: FMT.format(*map(str,x)),_proj)))
    print '\n\n'

