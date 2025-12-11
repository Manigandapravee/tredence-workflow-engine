
# Tredence AI Engineering Internship - Workflow Engine Assignment

This project is my submission for the Tredence AI Engineering Internship case study.  
The assignment was to build a minimal workflow/graph engine using Python and FastAPI.

The engine supports:
- Nodes (Python functions)
- Shared state passed between nodes
- Branching
- Looping
- Execution logs
- FastAPI endpoints for running workflows

Three sample workflows were implemented exactly as mentioned in the assignment:

1. Code Review Mini Agent
   - Extract functions
   - Check complexity
   - Detect issues
   - Suggest improvements
   - Loop until a quality threshold is reached

2. Summarization and Refinement
   - Split text into chunks
   - Summarize chunks
   - Merge summaries
   - Refine summary
   - Loop until the summary length is under a limit

3. Data Quality Pipeline
   - Profile data
   - Identify anomalies
   - Generate rules
   - Apply rules
   - Loop until anomaly count becomes small

------------------------------------------------------------

## Project Structure

app/
  graph_engine.py      -> Core workflow execution engine  
  nodes.py             -> All node functions  
  workflows.py         -> Workflow definitions  
  main.py              -> FastAPI application  

requirements.txt  
README.md  

------------------------------------------------------------

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Start the FastAPI server:
   uvicorn main:app --reload

3. Open the API documentation:
   http://127.0.0.1:8000/docs

------------------------------------------------------------

## API Endpoints

POST /graph/create  
POST /graph/run  
GET /graph/state/{run_id}  

------------------------------------------------------------

## Example

1. Create a workflow:
   {
     "workflow": "code_review"
   }

2. Run the workflow:
   {
     "graph_id": "your_graph_id_here",
     "initial_state": {
       "code": "def foo():\n    pass",
       "quality_threshold": 6
     }
   }

------------------------------------------------------------

## Notes

This project focuses on:
- Clean Python code
- Clear workflow logic
- Basic async support
- Simple rule-based node logic

No machine learning models are used, as instructed.

This repository demonstrates understanding of backend development, workflow execution, and API design as required for the Tredence AI Engineering role.
