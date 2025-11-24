from sqlalchemy import create_engine, MetaData, Integer, String, Table, Column

DB_PATH = 'job_data/job.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
metadata = MetaData()

jobs_table = Table(
    'jobs', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('input', Integer),
    Column('status', String)
)

def init_db():
    metadata.create_all(engine)

def log_to_db(table, record):
    with engine.begin() as conn:
        stmt = table.insert().values(record)
        conn.execute(stmt)

