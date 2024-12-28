from langgraph.graph import (
    StateGraph,
    END
)
from nodes.nodes import (
    generate_context,
    generate_summary,
    analyse_law_content,
    route_legal_action,
    suggest_legal_actions,
    evaluate_legal_actions,
    decide_legal_action,
    re_implement_law_actions,
    take_decision
)
from schemas.schemas import GraphState

workflow = StateGraph(GraphState)

workflow.add_node("generate_context", generate_context)
workflow.add_node("generate_summary", generate_summary)
workflow.add_node("analyse_law_content", analyse_law_content)
workflow.add_node("suggest_legal_actions", suggest_legal_actions)
workflow.add_node("evaluate_legal_actions", evaluate_legal_actions)
workflow.add_node("decide_legal_action", decide_legal_action)
workflow.add_node("re_implement_law_actions", re_implement_law_actions)
workflow.add_node("take_decision", take_decision)

workflow.set_entry_point("generate_context")
workflow.add_edge("generate_context", "generate_summary")
workflow.add_edge("generate_summary", "analyse_law_content")
workflow.add_edge("analyse_law_content", "suggest_legal_actions")
workflow.add_edge("suggest_legal_actions", "evaluate_legal_actions")
workflow.add_edge("evaluate_legal_actions", "decide_legal_action")

# Conditional Routing Using add_conditional_edges
workflow.add_conditional_edges(
    "decide_legal_action",
    route_legal_action,  # Your custom routing function
    {
        "re_implement_law_actions": "re_implement_law_actions",
        "take_decision": "take_decision"
    }
)

# Re-implementation Loop
workflow.add_edge("re_implement_law_actions", "take_decision")

workflow.add_edge('take_decision', END)

app = workflow.compile()