

# # ---------------------------------------------------------
# # backend/app/graphs/analysis_graph.py (LANGGRAPH)
# # ---------------------------------------------------------
# from langgraph.graph import StateGraph
# from app.agents.structure_agent import structure_agent
# from app.agents.api_agent import api_agent
# from app.agents.pm_agent import pm_agent




# def build_analysis_graph():
#     graph = StateGraph(dict)


#     graph.add_node("structure", structure_agent)
#     graph.add_node("api", api_agent)
#     graph.add_node("pm", pm_agent)


#     graph.set_entry_point("structure")
#     graph.add_edge("structure", "api")
#     graph.add_edge("api", "pm")


#     return graph.compile()


from langgraph.graph import StateGraph

from app.agents.structure_agent import structure_agent
from app.agents.api_agent import api_agent
from app.agents.db_agent import db_agent
from app.agents.pm_agent import pm_agent
from app.agents.web_search_agent import web_search_agent

def build_analysis_graph():
    graph = StateGraph(dict)

    graph.add_node("structure", structure_agent)
    graph.add_node("api", api_agent)
    graph.add_node("db", db_agent)
    graph.add_node("web", web_search_agent)
    graph.add_node("pm", pm_agent)

    graph.set_entry_point("structure")
    graph.add_edge("structure", "api")
    graph.add_edge("api", "db")
    graph.add_edge("db", "web")
    graph.add_edge("web", "pm")

    return graph.compile()
