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
    
    async def _process_chunk(self, chunk_explanations: list, chunk_num: int) -> str:
        """Process a single chunk of explanations"""
        chunk_text = "\n\n".join(chunk_explanations)
        
        prompt = f"""
        Analyze these CFR 21 subpart compliance results (Chunk {chunk_num}):
        
        {chunk_text}
        
        Extract and preserve all key compliance information:
        1. All requirements that were satisfied
        2. All requirements that are missing
        3. All recommendations provided
        
        Maintain all details - do not summarize or truncate.
        """
        
        try:
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
            if hasattr(result, 'content'):
                return result.content
            elif isinstance(result, dict) and 'messages' in result:
                messages = result['messages']
                for message in reversed(messages):
                    if hasattr(message, 'content'):
                        return message.content
            return f"Chunk {chunk_num}: No content extracted"
        except Exception as e:
            logger.warning(f"Failed to process chunk {chunk_num}: {e}")
            return f"Chunk {chunk_num}: Processing failed - {str(e)}"

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
        
        try:
            logger.info("🚀 Manager Agent: Processing explanations in chunks")
            
            # Process in chunks of 2 to stay within token limits
            chunk_size = 2
            processed_chunks = []
            
            for i in range(0, len(all_explanations), chunk_size):
                chunk = all_explanations[i:i + chunk_size]
                chunk_num = i // chunk_size + 1
                logger.info(f"Processing chunk {chunk_num}/{(len(all_explanations) + chunk_size - 1) // chunk_size}")
                
                chunk_result = await self._process_chunk(chunk, chunk_num)
                processed_chunks.append(chunk_result)
            
            # Combine all processed chunks
            all_processed_content = "\n\n=== CHUNK SEPARATOR ===\n\n".join(processed_chunks)
            
            # Create final summary using only scores and brief processed content
            final_prompt = f"""
            CFR 21 Compliance Expert: Create overall assessment from processed chunks.
            
            SUBPART SCORES:
            {json.dumps(subpart_scores, indent=2)}
            
            Based on the scores, provide:
            
            **OVERALL CFR 21 COMPLIANCE ANALYSIS**
            
            **SATISFIED REQUIREMENTS:**
            [Key requirements met across subparts]
            
            **MISSING REQUIREMENTS:**
            [Critical gaps identified]
            
            **RECOMMENDATIONS:**
            [Top actionable improvements]
            
            **OVERALL COMPLIANCE SCORE: [Calculate average of subpart scores]/100**
            """
            
            logger.info("🚀 Manager Agent: Creating final compliance summary")
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": final_prompt}]})
            
            # Extract structured data
            summary_data = self._extract_summary_data(result)
            summary_data["subpart_scores"] = subpart_scores
            summary_data["detailed_analysis"] = all_processed_content  # Include all chunk details
            
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