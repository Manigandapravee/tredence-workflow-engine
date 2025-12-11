# ---------------------------
# Workflow A - Code Review Agent
# ---------------------------

def a_extract_functions(state, tools):
    code = state.get("code", "")
    funcs = [line.strip() for line in code.splitlines() if line.strip().startswith("def ")]
    return {"functions": funcs, "quality_score": state.get("quality_score", 1)}

def a_check_complexity(state, tools):
    funcs = state.get("functions", [])
    avg_len = sum(len(f) for f in funcs)/len(funcs) if funcs else 0
    score = state.get("quality_score", 0) + len(funcs) + int(avg_len/20)
    return {"quality_score": score}

def a_detect_issues(state, tools):
    funcs = state.get("functions", [])
    issues = sum(1 for f in funcs if "pass" in f or "TODO" in f)
    return {"issues": issues, "quality_score": state.get("quality_score", 0) - issues}

def a_suggest_improvements(state, tools):
    qs = state.get("quality_score", 0)
    threshold = state.get("quality_threshold", 6)
    if qs >= threshold:
        return {"stop": True, "suggestion": "Quality good"}
    return {"quality_score": qs + 1, "suggestion": "Refactor"}


# ---------------------------
# Workflow B - Text Summarization
# ---------------------------

def b_split_text(state, tools):
    text = state.get("text", "")
    chunk = state.get("chunk_size", 200)
    return {"chunks": [text[i:i+chunk] for i in range(0, len(text), chunk)]}

def b_summarize_chunk(state, tools):
    return {"summaries": [c[:100].strip() for c in state.get("chunks", [])]}

def b_merge_summaries(state, tools):
    return {"merged_summary": "\n".join(state.get("summaries", []))}

def b_refine_summary(state, tools):
    merged = state.get("merged_summary", "")
    refined = " ".join(merged.split())
    limit = state.get("summary_limit", 300)
    if len(refined) <= limit:
        return {"final_summary": refined, "stop": True}
    return {"merged_summary": refined[:limit]}


# ---------------------------
# Workflow C - Data Quality Pipeline
# ---------------------------

def c_profile_data(state, tools):
    data = state.get("data", [])
    return {
        "count": len(data),
        "nan_count": sum(1 for x in data if x is None),
        "distinct": len(set(x for x in data if x is not None))
    }

def c_identify_anomalies(state, tools):
    data = state.get("data", [])
    anomalies = [i for i, v in enumerate(data) if v is None or (isinstance(v, (int,float)) and (v < 0 or abs(v) > 1e6))]
    return {"anomalies": anomalies, "anomaly_count": len(anomalies)}

def c_generate_rules(state, tools):
    rules = []
    if state.get("nan_count", 0) > 0:
        rules.append({"action": "impute", "value": 0})
    if state.get("anomaly_count", 0) > 0:
        rules.append({"action": "remove_negative"})
    return {"rules": rules}

def c_apply_rules(state, tools):
    data = state.get("data", [])
    new = data.copy()
    for r in state.get("rules", []):
        if r["action"] == "impute":
            new = [0 if x is None else x for x in new]
        if r["action"] == "remove_negative":
            new = [x for x in new if not (isinstance(x,(int,float)) and x < 0)]
    return {"data": new, "anomaly_count": 0}
