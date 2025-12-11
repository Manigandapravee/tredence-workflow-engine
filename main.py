from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph_engine import GraphEngine
from workflows import code_review_workflow, summarization_workflow, data_quality_workflow

app = FastAPI(title="Workflow Engine - Tredence Assignment")

engine = GraphEngine()

nodes_a, edges_a = code_review_workflow()
gid_a = engine.create_graph(nodes_a, edges_a)

nodes_b, edges_b = summarization_workflow()
gid_b = engine.create_graph(nodes_b, edges_b)

nodes_c, edges_c = data_quality_workflow()
gid_c = engine.create_graph(nodes_c, edges_c)

WORKFLOWS = {
    "code_review": gid_a,
    "summarization": gid_b,
    "data_quality": gid_c
}

class CreateGraphRequest(BaseModel):
    workflow: str

class RunGraphRequest(BaseModel):
    graph_id: str
    initial_state: dict = {}

@app.post("/graph/create")
def create_graph(req: CreateGraphRequest):
    gid = WORKFLOWS.get(req.workflow)
    if not gid:
        raise HTTPException(404, "workflow not found")
    return {"graph_id": gid}

@app.post("/graph/run")
def run_graph(req: RunGraphRequest):
    run_id, state, log = engine.run_graph(req.graph_id, req.initial_state)
    return {"run_id": run_id, "final_state": state, "log": log}

@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    return engine.get_state(run_id)
