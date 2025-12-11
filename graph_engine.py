import uuid
import asyncio
from typing import Callable, Dict, Any, Optional, Tuple, List

class GraphEngine:
    def __init__(self):
        self.graphs: Dict[str, Dict[str, Any]] = {}
        self.runs: Dict[str, Dict[str, Any]] = {}
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, fn: Callable):
        self.tools[name] = fn

    def create_graph(self, nodes: Dict[str, Callable], edges: Dict[str, Optional[str]]):
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = {"nodes": nodes, "edges": edges}
        return graph_id

    async def _execute_node(self, node_fn: Callable, state: Dict[str, Any]) -> Dict[str, Any]:
        if asyncio.iscoroutinefunction(node_fn):
            out = await node_fn(state, self.tools)
        else:
            out = node_fn(state, self.tools)
        if out is None:
            out = {}
        if not isinstance(out, dict):
            raise ValueError("Node must return dict")
        return out

    async def run_graph_async(self, graph_id: str, initial_state: Dict[str, Any], max_iterations: int = 50):
        if graph_id not in self.graphs:
            raise KeyError("Graph not found")

        run_id = str(uuid.uuid4())
        graph = self.graphs[graph_id]
        nodes = graph["nodes"]
        edges = graph["edges"]
        state = dict(initial_state) if initial_state else {}
        log = []
        visited = 0

        current = list(nodes.keys())[0]

        while current:
            visited += 1
            if visited > max_iterations:
                log.append("Stopped: max_iterations reached")
                break

            func = nodes[current]
            log.append(f"Running node: {current}")
            out = await self._execute_node(func, state)
            state.update(out)
            log.append(f"Output: {out}")

            if state.get("stop", False):
                log.append("Stop flag detected")
                break

            nxt = edges.get(current)
            if callable(nxt):
                current = nxt(state)
            else:
                current = nxt

        self.runs[run_id] = {"state": state, "log": log}
        return run_id, state, log

    def run_graph(self, graph_id, initial_state, max_iterations=50):
        return asyncio.get_event_loop().run_until_complete(
            self.run_graph_async(graph_id, initial_state, max_iterations)
        )

    def get_state(self, run_id: str):
        return self.runs.get(run_id, {"error": "run_id not found"})
