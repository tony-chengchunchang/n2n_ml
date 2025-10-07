from database import log_to_db, jobs_table, engine
from sqlalchemy import text
import time

def run_job(input):
    time.sleep(10)  # Simulate a long-running job


while True:
    with engine.begin() as conn:
        res = conn.execute(text("SELECT * FROM jobs where status = 'queued' order by id asc limit 1")).first()
        if res:
            job_id = res[0]
            conn.execute(text(f"update jobs set status='processing' where id={job_id}"))
        else:
            time.sleep(1)
            continue
    try:
        run_job(res[1])
        with engine.begin() as conn:
            conn.execute(text(f"update jobs set status='success' where id={job_id}"))
        print(f"Job {job_id} completed successfully")
    except Exception as e:
        with engine.begin() as conn:
            conn.execute(text(f"update jobs set status='failed' where id={job_id}"))
        print(f"Job {job_id} failed: {e}")