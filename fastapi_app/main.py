import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, RootModel, Field
from typing import List
import pandas as pd
import mlflow
from database import init_db, log_to_db, jobs_table, engine
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = FastAPI()
tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(tracking_uri)
mlflow.autolog()
MODEL_URI = "models:/N2N/1"
model = mlflow.pyfunc.load_model(MODEL_URI)
init_db()

# Example request model
class PredInputs(RootModel[dict]):
    pass

class JobSubmission(BaseModel):
    iterations: int = Field(ge=1, le=3)
    input:int = Field(ge=1, le=100)

@app.get("/training")
def train():
    try:
        mlflow.set_experiment('n2n')
        X, y = load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        with mlflow.start_run() as run:
            clf = RandomForestClassifier()
            clf.fit(X_train, y_train)
            
            y_pred = clf.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            print(f"Test Accuracy: {acc}")

        mlflow.register_model(f"runs:/{run.info.run_id}/model", "N2N")
        return {"run_id": run.info.run_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(records: List[PredInputs]):
    data = pd.DataFrame([r.root for r in records])
    
    # Make predictions
    preds = model.predict(data)
    
    # Return as list/dict
    return {'predictions': preds.tolist()}

@app.post('/submit_jobs')
def submit_jobs(submission: JobSubmission):
    data = submission.model_dump()
    job_ids = []
    for i in range(data['iterations']):
        with engine.begin() as conn:
            stmt = jobs_table.insert().values({'input':data['input'], 'status':'queued'})
            conn.execute(stmt)

            stmt = jobs_table.select().order_by(jobs_table.c.id.desc()).limit(1)
            res = conn.execute(stmt).first()
            job_ids.append(res[0])

    return {'job_ids': job_ids}

@app.get('/job_status/{job_id}')
def check_job_status(job_id: int):
    with engine.begin() as conn:
        stmt = jobs_table.select().where(jobs_table.c.id == job_id)
        res = conn.execute(stmt).first()
        if res:
            return {'job_id': res[0], 'input': res[1], 'status': res[2]}
        else:
            raise HTTPException(status_code=404, detail="Job not found")