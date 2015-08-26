import datetime

def seed_data(meta,add_proj,add_task):
    meta.drop_all()
    meta.create_all()

    add_proj('testing')
    add_proj('my_next_test')

    task = {'name':'taskA','description':'my first task','due_date':datetime.datetime(2017,8,13)}
    task2 = {'name':'taskG','description':'my next task'}
    task3 = {'name':'taskY','description':'another task','due_date':datetime.datetime(2017,8,15)}

    add_task('testing',task)
    add_task('testing',task2)
    add_task('testing',task3)

    task = {'name':'CtaskA','description':'my B task','due_date':datetime.datetime(2017,8,13)}
    task2 = {'name':'BtaskG','description':'my Xtask'}
    add_task('my_next_test',task)
    add_task('my_next_test',task2)
