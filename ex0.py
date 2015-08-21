from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text,func,select

engine = create_engine('sqlite:///:memory:',echo=True)

def run_sql(sql):
    return engine.execute(sql)

def main():

if __name__ == "__main__":
    main()

