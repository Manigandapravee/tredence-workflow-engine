from nodes import (
    a_extract_functions, a_check_complexity, a_detect_issues, a_suggest_improvements,
    b_split_text, b_summarize_chunk, b_merge_summaries, b_refine_summary,
    c_profile_data, c_identify_anomalies, c_generate_rules, c_apply_rules
)

def code_review_workflow():
    nodes = {
        "extract": a_extract_functions,
        "complexity": a_check_complexity,
        "issues": a_detect_issues,
        "improve": a_suggest_improvements
    }
    edges = {
        "extract": "complexity",
        "complexity": "issues",
        "issues": "improve",
        "improve": lambda s: None if s.get("stop") else "extract"
    }
    return nodes, edges


def summarization_workflow():
    nodes = {
        "split": b_split_text,
        "summarize": b_summarize_chunk,
        "merge": b_merge_summaries,
        "refine": b_refine_summary
    }
    edges = {
        "split": "summarize",
        "summarize": "merge",
        "merge": "refine",
        "refine": lambda s: None if s.get("stop") else "merge"
    }
    return nodes, edges


def data_quality_workflow():
    nodes = {
        "profile": c_profile_data,
        "anomalies": c_identify_anomalies,
        "rules": c_generate_rules,
        "apply": c_apply_rules
    }
    edges = {
        "profile": "anomalies",
        "anomalies": "rules",
        "rules": "apply",
        "apply": lambda s: None if s.get("anomaly_count", 0) == 0 else "profile"
    }
    return nodes, edges
