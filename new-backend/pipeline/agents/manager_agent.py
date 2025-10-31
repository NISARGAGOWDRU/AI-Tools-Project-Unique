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
        tools=tools,  # Can be empty list
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
                "detailed_analysis": text
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
        """Summarize all subpart compliance results into overall CFR 21 assessment"""
        logger.info("🔍 Manager Agent: Starting CFR 21 compliance summarization")
        
        individual_assessments = compliance_results.get('individual_assessments', {})
        subpart_scores = {}
        all_explanations = []
        
        for subpart_name, result in individual_assessments.items():
            score = result.get('compliance_score', 0)
            explanation = result.get('compliance_explanation', '')
            subpart_scores[subpart_name] = score
            if explanation:
                all_explanations.append(f"**{subpart_name}**: {explanation}")
        
        prompt = f"""
        You are a CFR 21 compliance expert. Analyze the individual subpart compliance results and provide an overall CFR 21 compliance assessment.
        
        INDIVIDUAL SUBPART RESULTS:
        {json.dumps(subpart_scores, indent=2)}
        
        DETAILED EXPLANATIONS:
        {chr(10).join(all_explanations)}
        
        Provide a comprehensive CFR 21 compliance summary with:
        
        1. Calculate an overall compliance score (0-100) based on all subpart scores
        2. Identify what requirements were satisfied across all subparts
        3. Identify what requirements are missing across all subparts
        4. Provide specific recommendations for improvement
        
        Format your response as:
        
        **OVERALL CFR 21 COMPLIANCE ANALYSIS**
        
        **SATISFIED REQUIREMENTS:**
        [List all requirements that were met across subparts]
        
        **MISSING REQUIREMENTS:**
        [List all requirements that are missing or insufficient]
        
        **RECOMMENDATIONS:**
        [Specific actionable recommendations to improve compliance]
        
        **OVERALL COMPLIANCE SCORE: [NUMBER]/100**
        
        Provide detailed analysis explaining why this score was assigned and what it means for CFR 21 compliance.
        """
        
        try:
            logger.info("🚀 Manager Agent: Invoking compliance summarization")
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
            
            # Extract structured data
            summary_data = self._extract_summary_data(result)
            summary_data["subpart_scores"] = subpart_scores
            
            logger.info(f"✅ Manager Agent: Overall CFR 21 score: {summary_data['overall_compliance_score']}/100")
            logger.info(f"📊 Manager Agent: Status: {summary_data['cfr21_status']}")
            
            return summary_data
            
        except Exception as e:
            logger.error(f"❌ Manager Agent: Summarization failed - {e}")
            return {
                "overall_compliance_score": 0,
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