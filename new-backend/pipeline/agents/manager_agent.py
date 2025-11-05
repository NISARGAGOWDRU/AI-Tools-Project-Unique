from typing import Any, Dict
from langchain_core.runnables import Runnable
from langgraph.prebuilt import create_react_agent
import re
import json

from services.llm import make_llm
from mcp_clients.client import get_tools
import logging

logger = logging.getLogger(__name__)

async def make_manager_agent() -> Runnable:
    """
    Manager agent: orchestrates tool use by reasoning via the OSS LLM.
    Returns a LangChain Runnable that can be plugged into a LangGraph StateGraph.
    """
    llm = make_llm()
    
    # Get tools from MCP (will return empty list if MCP unavailable)
    tools = await get_tools()
    
    if not tools:
        logger.warning("No MCP tools available. Agent will run without tools.")
    else:
        logger.info(f"Loaded {len(tools)} tools from MCP server")
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        debug=True
    )

    return agent

class ManagerAgent:
    """Manager agent for CFR 21 compliance summarization"""
    
    def __init__(self, agent: Runnable):
        self.agent = agent
    
    def _extract_summary_data(self, agent_result: Any) -> Dict[str, Any]:
        """Extract structured summary from agent result"""
        try:
            if hasattr(agent_result, 'content'):
                text = agent_result.content
            elif isinstance(agent_result, dict) and 'messages' in agent_result:
                messages = agent_result['messages']
                for message in reversed(messages):
                    if hasattr(message, 'content'):
                        text = message.content
                        break
                else:
                    text = str(agent_result)
            else:
                text = str(agent_result)
            
            score_match = re.search(r'overall[\s_]*compliance[\s_]*score[:\s]*([0-9]+)', text, re.IGNORECASE)
            overall_score = int(score_match.group(1)) if score_match else 0
            
            if overall_score >= 80:
                status = "Fully Compliant"
            elif overall_score >= 60:
                status = "Partially Compliant"
            else:
                status = "Non-Compliant"
            
            satisfied_match = re.search(r'satisfied[\s_]*requirements[:\s]*([^\n]*(?:\n[^\n]*)*?)(?=missing|recommendations|overall|$)', text, re.IGNORECASE | re.DOTALL)
            satisfied = satisfied_match.group(1).strip() if satisfied_match else "Analysis not available"
            
            missing_match = re.search(r'missing[\s_]*requirements[:\s]*([^\n]*(?:\n[^\n]*)*?)(?=satisfied|recommendations|overall|$)', text, re.IGNORECASE | re.DOTALL)
            missing = missing_match.group(1).strip() if missing_match else "Analysis not available"
            
            rec_match = re.search(r'recommendations[:\s]*([^\n]*(?:\n[^\n]*)*?)(?=satisfied|missing|overall|$)', text, re.IGNORECASE | re.DOTALL)
            recommendations = rec_match.group(1).strip() if rec_match else "No specific recommendations provided"
            
            return {
                "overall_compliance_score": overall_score,
                "cfr21_status": status,
                "satisfied_requirements": satisfied,
                "missing_requirements": missing,
                "recommendations": recommendations,
                "detailed_analysis": text[:1500]  # 🚀 NEW: Limit to 1500 chars
            }
            
        except Exception as e:
            logger.error(f"Error extracting summary data: {e}")
            return {
                "overall_compliance_score": 0,
                "cfr21_status": "Analysis Failed",
                "satisfied_requirements": "Error in analysis",
                "missing_requirements": "Error in analysis",
                "recommendations": "Please retry analysis",
                "detailed_analysis": f"Error occurred: {str(e)}"
            }
    
    async def summarize_compliance(self, compliance_results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize all subpart compliance results - CONCISE VERSION"""
        logger.info("🔍 Manager Agent: Starting CFR 21 compliance summarization")
        
        individual_assessments = compliance_results.get('individual_assessments', {})
        subpart_scores = {}
        
        # 🚀 NEW: Extract only scores and key points (no full explanations)
        concise_summaries = []
        
        for subpart_name, result in individual_assessments.items():
            score = result.get('compliance_score', 0)
            subpart_scores[subpart_name] = score
            
            # Extract just the key points (first 200 chars of explanation)
            explanation = result.get('compliance_explanation', '')[:200]
            concise_summaries.append(f"{subpart_name}: {score}/100 - {explanation}")
        
        # Combine concise summaries
        combined_text = "\n".join(concise_summaries)
        
        # Calculate average score upfront
        avg_score = sum(subpart_scores.values()) // len(subpart_scores) if subpart_scores else 0
        
        # 🚀 NEW: Single LLM call with strict output limits
        final_prompt = f"""
CFR 21 Compliance Summary - BE EXTREMELY CONCISE (MAX 300 WORDS TOTAL)

SUBPART SCORES:
{json.dumps(subpart_scores, indent=2)}

BRIEF DETAILS:
{combined_text[:2000]}

Provide:

SATISFIED REQUIREMENTS: (max 80 words)
[Top 5 requirements met]

MISSING REQUIREMENTS: (max 80 words)
[Top 5 critical gaps]

RECOMMENDATIONS: (max 80 words)
[Top 5 priority actions]

OVERALL COMPLIANCE SCORE: {avg_score}/100

Keep TOTAL response under 300 words. Be concise.
"""
        
        try:
            logger.info("🚀 Manager Agent: Generating concise final summary")
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": final_prompt}]})
            
            # Extract structured data
            summary_data = self._extract_summary_data(result)
            summary_data["subpart_scores"] = subpart_scores
            summary_data["overall_compliance_score"] = avg_score  # Use pre-calculated score
            
            logger.info(f"✅ Manager Agent: Overall CFR 21 score: {summary_data['overall_compliance_score']}/100")
            logger.info(f"📊 Manager Agent: Status: {summary_data['cfr21_status']}")
            
            return summary_data
            
        except Exception as e:
            logger.error(f"❌ Manager Agent: Summarization failed - {e}")
            return {
                "overall_compliance_score": avg_score,
                "cfr21_status": "Analysis Failed",
                "satisfied_requirements": "Error in analysis",
                "missing_requirements": "Error in analysis",
                "subpart_scores": subpart_scores,
                "recommendations": "Please retry analysis",
                "detailed_analysis": f"Error: {str(e)}"
            }

async def create_manager_agent() -> ManagerAgent:
    """Create manager agent for compliance summarization"""
    logger.info("🔧 Creating Manager Agent for CFR 21 summarization")
    
    try:
        agent = await make_manager_agent()
        manager = ManagerAgent(agent)
        logger.info("✅ Manager Agent created successfully")
        return manager
    except Exception as e:
        logger.error(f"❌ Failed to create Manager Agent: {e}")
        raise