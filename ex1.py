from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text,func,select

engine = create_engine('sqlite:///:memory:',echo=True)

def run_sql(sql):
    return engine.execute(sql)

def main():
    sql = text('SELECT CURRENT_TIMESTAMP as now_1')
    print run_sql(sql).fetchall()
    sql = select([func.now()])
    print run_sql(sql).fetchall()

if __name__ == "__main__":
    main()

