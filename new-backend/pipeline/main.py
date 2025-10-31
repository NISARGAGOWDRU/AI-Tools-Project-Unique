from langgraph.checkpoint.memory import MemorySaver
from pipeline.state import PipelineState
from pipeline.agents.manager_agent import make_manager_agent, create_manager_agent
from pipeline.agents.compliance_coordinator import create_compliance_coordinator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from mcp_clients.client import get_resources
import logging

logger = logging.getLogger(__name__)

async def build_pipeline():
    graph = StateGraph(PipelineState)

    try:
        agent = await make_manager_agent()   
        manager_agent = await create_manager_agent()  
        logger.info("Manager agent created successfully")
    except Exception as e:
        logger.error(f"Failed to create manager agent: {e}")
        raise

    try:
        resources = await get_resources()
        subpart_summary_uris = []
        logger.info(f"Processing {len(resources)} total resources")
        for r in resources:
            uri = str(getattr(r, 'metadata', {}).get('uri', ''))
            logger.info(f"Found resource URI: {uri}")
            if 'subpart' in uri and uri.endswith('_summary.json'):
                subpart_summary_uris.append(uri)
                logger.info(f"✅ Added subpart URI: {uri}")
        logger.info(f"Fetched {len(subpart_summary_uris)} subpart summary URIs: {subpart_summary_uris}")
    except Exception as e:
        logger.warning(f"Could not fetch subpart summary URIs: {e}")
        subpart_summary_uris = []
    
    compliance_coordinator = None
    if subpart_summary_uris:
        try:
            logger.info(f"🚀 PIPELINE: Creating compliance coordinator with {len(subpart_summary_uris)} URIs")
            compliance_coordinator = await create_compliance_coordinator(subpart_summary_uris)
            if compliance_coordinator and hasattr(compliance_coordinator, 'subpart_agents'):
                agent_count = len(compliance_coordinator.subpart_agents)
                logger.info(f"✅ PIPELINE: Compliance coordinator created with {agent_count} agents")
                logger.info(f"📊 PIPELINE: Available agents: {list(compliance_coordinator.subpart_agents.keys())}")
            else:
                logger.warning("⚠️ PIPELINE: Compliance coordinator created but has no agents")
        except Exception as e:
            logger.error(f"❌ PIPELINE: Failed to create compliance coordinator: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"❌ PIPELINE: Full traceback: {traceback.format_exc()}")
    else:
        logger.warning("⚠️ PIPELINE: No subpart URIs found - compliance coordinator not created")

    async def manager_node(state: PipelineState) -> PipelineState:
        logger.info("💼 MANAGER NODE STARTED")
        prompt = state.get("user_input", "")
        document_summary = state.get("document_summary")
        compliance_results = state.get("compliance_results")
        
        logger.info(f"💼 Manager input: '{prompt}'")
        logger.info(f"📄 Document summary in manager: {bool(document_summary)}")
        logger.info(f"📈 Compliance results in manager: {bool(compliance_results)}")
        
        if compliance_results and compliance_results.get('status') == 'completed':
            try:
                logger.info("🔍 Generating CFR 21 compliance summary")
                final_summary = await manager_agent.summarize_compliance(compliance_results)
                state["final_compliance_summary"] = final_summary
                logger.info(f"✅ CFR 21 Summary: {final_summary['overall_compliance_score']}/100 - {final_summary['cfr21_status']}")
            except Exception as e:
                logger.error(f"❌ CFR 21 summarization failed: {e}")
                state["final_compliance_summary"] = {
                    "overall_compliance_score": 0,
                    "cfr21_status": "Analysis Failed",
                    "error": str(e)
                }
        
        if compliance_results:
            logger.info(f"📈 Compliance status: {compliance_results.get('status')}")
            if compliance_results.get('summary'):
                completed = compliance_results['summary'].get('completed_assessments', 0)
                total = compliance_results['summary'].get('total_subparts', 0)
                logger.info(f"📈 Compliance summary: {completed}/{total} assessments completed")

        state["subpart_summary_uris"] = subpart_summary_uris
        logger.info(f"📊 Available subpart summary URIs: {len(subpart_summary_uris)}")

        try:
            result = await agent.ainvoke({"messages": [HumanMessage(content=prompt)]})
            messages = result.get("messages", [])
            last_ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
            output = last_ai_message.content if last_ai_message else ""
            if output is not None:
                state["last_tool_result"] = output
            state["status"] = "done"
            logger.info("✅ MANAGER NODE COMPLETED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"❌ MANAGER NODE ERROR: {type(e).__name__}: {e}")
            state["last_tool_result"] = f"Error processing query: {str(e)}"
            state["status"] = "error"

        return state

    async def compliance_node(state: PipelineState) -> PipelineState:
        """Node for running compliance assessment with specialized agents"""
        logger.info("🚀 COMPLIANCE NODE STARTED")
        document_summary = state.get("document_summary")
        
        if not document_summary:
            logger.error("❌ COMPLIANCE NODE: No document summary available")
            state["compliance_results"] = {
                "error": "No document summary available",
                "status": "skipped"
            }
            return state
        
        if not compliance_coordinator:
            logger.error("❌ COMPLIANCE NODE: No compliance coordinator available")
            state["compliance_results"] = {
                "error": "No compliance coordinator available",
                "status": "skipped"
            }
            return state
        
        try:
            logger.info("🔄 COMPLIANCE NODE: Starting assessment with ComplianceCoordinator")
            logger.info(f"📄 Document summary length: {len(document_summary)} characters")
            logger.info(f"🤖 Using coordinator with {len(compliance_coordinator.subpart_agents)} agents")
            
            compliance_results = await compliance_coordinator.assess_compliance(document_summary)
            
            state["compliance_results"] = compliance_results
            logger.info(f"✅ COMPLIANCE NODE COMPLETED: {compliance_results.get('status')}")
            logger.info(f"📈 Results: {compliance_results.get('summary', {}).get('completed_assessments', 0)}/{compliance_results.get('summary', {}).get('total_subparts', 0)} assessments completed")
            
        except Exception as e:
            logger.error(f"❌ COMPLIANCE NODE ERROR: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            state["compliance_results"] = {
                "error": f"Compliance assessment failed: {str(e)}",
                "status": "failed"
            }
        
        logger.info("🏁 COMPLIANCE NODE FINISHED")
        return state

    def should_run_compliance(state: PipelineState) -> str:
        """Conditional edge to determine if compliance assessment should run"""
        document_summary = state.get("document_summary")
        logger.info(f"🔍 COMPLIANCE CHECK: document_summary={bool(document_summary)}, coordinator={bool(compliance_coordinator)}")
        
        if document_summary:
            logger.info(f"📄 DOCUMENT SUMMARY FOUND: {len(document_summary)} characters")
            logger.info(f"📄 Summary preview: {document_summary[:200]}...")
        else:
            logger.info("❌ NO DOCUMENT SUMMARY FOUND")
            
        if compliance_coordinator:
            agent_count = len(compliance_coordinator.subpart_agents) if hasattr(compliance_coordinator, 'subpart_agents') else 0
            logger.info(f"🤖 COMPLIANCE COORDINATOR AVAILABLE with {agent_count} agents")
            if agent_count > 0:
                logger.info(f"📊 Available agents: {list(compliance_coordinator.subpart_agents.keys())}")
        else:
            logger.info("❌ NO COMPLIANCE COORDINATOR AVAILABLE")
        
        if document_summary and compliance_coordinator:
            logger.info("✅ TRIGGERING COMPLIANCE ASSESSMENT")
            return "compliance"
        
        logger.info("⏭️ SKIPPING COMPLIANCE - going directly to manager")
        return "manager"

    async def document_summary_node(state: PipelineState) -> PipelineState:
        """Node that triggers when document_summary is available"""
        logger.info(f"📄 DOCUMENT SUMMARY CHECK - Current state keys: {list(state.keys())}")
        document_summary = state.get('document_summary')
        if document_summary:
            logger.info(f"✅ DOCUMENT SUMMARY AVAILABLE: {len(document_summary)} characters")
            logger.info(f"📄 Summary preview: {document_summary[:200]}...")
        else:
            logger.info("❌ NO DOCUMENT SUMMARY IN STATE")
        return state

    graph.add_node("document_summary_check", document_summary_node)
    graph.add_node("manager", manager_node)
    graph.add_node("compliance", compliance_node)
    graph.set_entry_point("document_summary_check")
    graph.add_conditional_edges(
        "document_summary_check",
        should_run_compliance,
        {
            "compliance": "compliance",
            "manager": "manager"
        }
    )
    graph.add_edge("compliance", "manager")
    graph.add_edge("manager", END)
    
    return graph.compile(checkpointer=MemorySaver())