from typing import Any, Dict
from langchain_core.runnables import Runnable
from langgraph.prebuilt import create_react_agent
from services.llm import make_llm
from mcp_clients.client import get_tools
import logging
import asyncio
import re
from langchain_core.messages import AIMessage

logger = logging.getLogger(__name__)

class SubpartAgent:
    """Specialized agent for comparing document summary with a specific subpart summary"""
    
    def __init__(self, subpart_uri: str, agent: Runnable):
        logger.info(f"🎯 Initializing SubpartAgent for {subpart_uri}")
        self.subpart_uri = subpart_uri
        self.agent = agent
        self.subpart_name = self._extract_subpart_name(subpart_uri)
        logger.info(f"✅ SubpartAgent initialized: {self.subpart_name}")
    
    def _extract_subpart_name(self, uri: str) -> str:
        """Extract subpart name from URI (e.g., 'Subpart_A' from the URI)"""
        try:
            parts = uri.split('/')
            for part in parts:
                if part.startswith('Subpart_'):
                    logger.info(f"🏷️ Extracted subpart name: {part} from {uri}")
                    return part
            
            filename = uri.split('/')[-1] if '/' in uri else uri
            if 'Subpart_' in filename:
                subpart = filename.split('Subpart_')[1].split('.')[0]
                name = f"Subpart_{subpart}"
                logger.info(f"🏷️ Extracted from filename: {name}")
                return name
            
            logger.warning(f"⚠️ Could not extract subpart name from {uri}, using Unknown_Subpart")
            return "Unknown_Subpart"
        except Exception as e:
            logger.error(f"❌ Error extracting subpart name from {uri}: {e}")
            return "Unknown_Subpart"
    
    def _extract_compliance_score(self, agent_result: Any) -> int:
        """Extract compliance score from agent result"""
        try:
            if isinstance(agent_result, dict) and 'messages' in agent_result:
                messages = agent_result['messages']
                for message in reversed(messages):
                    if isinstance(message, AIMessage) or (isinstance(message, dict) and message.get('type') == 'ai'):
                        content = message.content if hasattr(message, 'content') else message.get('content', '')
                        score = self._parse_score_from_text(content)
                        if score is not None:
                            return score
            
            text_content = str(agent_result)
            score = self._parse_score_from_text(text_content)
            return score if score is not None else 0
            
        except Exception as e:
            logger.error(f"❌ {self.subpart_name}: Error extracting score: {e}")
            return 0
    
    def _extract_compliance_explanation(self, agent_result: Any) -> str:
        """Extract detailed explanation from agent result"""
        try:
            if isinstance(agent_result, dict) and 'messages' in agent_result:
                messages = agent_result['messages']
                for message in reversed(messages):
                    if isinstance(message, AIMessage) or (isinstance(message, dict) and message.get('type') == 'ai'):
                        content = message.content if hasattr(message, 'content') else message.get('content', '')
                        return self._parse_explanation_from_text(content)
            
            text_content = str(agent_result)
            return self._parse_explanation_from_text(text_content)
            
        except Exception as e:
            logger.error(f"❌ {self.subpart_name}: Error extracting explanation: {e}")
            return "No explanation available due to processing error."
    
    def _parse_explanation_from_text(self, text: str) -> str:
        """Parse detailed explanation from text"""
        if not text:
            return "No explanation provided."
        
        lines = text.split('\n')
        explanation_lines = []
        
        for line in lines:
            if re.search(r'final\s+compliance\s+score', line, re.IGNORECASE):
                break
            explanation_lines.append(line)
        
        explanation = '\n'.join(explanation_lines).strip()
        
        if len(explanation) < 50:
            cleaned_text = re.sub(r'final\s+compliance\s+score[:\s]*[0-9]+/100', '', text, flags=re.IGNORECASE)
            explanation = cleaned_text.strip()
        
        return explanation if explanation else "Compliance assessment completed but no detailed explanation was provided."
    
    def _parse_score_from_text(self, text: str) -> int:
        """Parse compliance score from text using regex patterns"""
        if not text:
            return None
        
        patterns = [
            r'(?:compliance\s*)?score[:\s]*([0-9]+)(?:/100|%)?',
            r'([0-9]+)(?:/100|%)\s*(?:compliance|score)',
            r'(?:rating|assessment)[:\s]*([0-9]+)(?:/100|%)?',
            r'([0-9]+)\s*(?:out\s*of\s*100|/100)',
            r'(?:final|overall)\s*(?:score|rating)[:\s]*([0-9]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    score = int(matches[-1])  
                    if 0 <= score <= 100:
                        logger.info(f"📊 {self.subpart_name}: Extracted score {score} using pattern: {pattern}")
                        return score
                except ValueError:
                    continue
        
        logger.warning(f"⚠️ {self.subpart_name}: Could not extract score from text: {text[:200]}...")
        return None
    
    async def compare_compliance(self, document_summary: str) -> Dict[str, Any]:
        """
        Compare document summary with subpart summary using search_similarity tool
        Returns compliance assessment
        """
        logger.info(f"🔍 {self.subpart_name}: Starting compliance comparison")
        
        prompt = f"""
        You are a specialized compliance agent for {self.subpart_name}.
        
        Your task:
        1. First, use the read_file tool to load the subpart summary content from {self.subpart_uri}
        2. Then use the similarity_search tool to compare the document summary with the loaded subpart content
        3. Provide a detailed compliance assessment including:
           - What specific requirements were met or not met
           - What data was missing or insufficient that affected the score
           - Why the score is high/medium/low based on the evidence
           - Key gaps or strengths identified
        
        Provide your analysis in this structure:
        
        **COMPLIANCE ANALYSIS:**
        - Requirements Met: [List specific requirements that were satisfied]
        - Requirements Not Met: [List specific requirements that were missing or insufficient]
        - Missing Data: [Identify what critical information was absent]
        - Score Justification: [Explain why this specific score was assigned]
        
        **RECOMMENDATIONS:**
        [Suggest what needs to be added or improved to increase compliance]
        
        IMPORTANT: End your response with:
        "Final Compliance Score: [NUMBER]/100"
        
        Document Summary to analyze:
        {document_summary}
        
        Start by reading the subpart file, then perform similarity comparison, and provide the detailed assessment.
        """
        
        try:
            logger.info(f"🚀 {self.subpart_name}: Invoking agent with prompt")
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
            
            logger.info(f"✅ {self.subpart_name}: Agent completed successfully")
            logger.info(f"📊 {self.subpart_name}: Result type: {type(result)}")
            
            compliance_score = self._extract_compliance_score(result)
            compliance_explanation = self._extract_compliance_explanation(result)
            logger.info(f"📊 {self.subpart_name}: Extracted compliance score: {compliance_score}")
            logger.info(f"📝 {self.subpart_name}: Compliance explanation: {compliance_explanation[:200]}..." if len(compliance_explanation) > 200 else f"📝 {self.subpart_name}: Compliance explanation: {compliance_explanation}")
            
            return {
                "subpart": self.subpart_name,
                "subpart_uri": self.subpart_uri,
                "result": result,
                "compliance_score": compliance_score,
                "compliance_explanation": compliance_explanation,
                "status": "completed"
            }
        except Exception as e:
            logger.error(f"❌ {self.subpart_name}: Agent failed - {type(e).__name__}: {e}")
            import traceback
            logger.error(f"❌ {self.subpart_name}: Full traceback: {traceback.format_exc()}")
            return {
                "subpart": self.subpart_name,
                "subpart_uri": self.subpart_uri,
                "result": f"Error: {str(e)}",
                "compliance_score": 0,
                "compliance_explanation": f"Error occurred during compliance assessment: {str(e)}",
                "status": "error"
            }

async def create_subpart_agent(subpart_uri: str) -> SubpartAgent:
    """Create a specialized agent for a specific subpart"""
    logger.info(f"🔧 Creating individual agent for: {subpart_uri}")
    
    try:
        logger.info(f"🤖 Creating LLM for {subpart_uri}")
        llm = make_llm()
        if not llm:
            raise ValueError("Failed to create LLM")
        
        logger.info(f"🔧 Getting MCP tools for {subpart_uri}")
        tools = await get_tools()
        if not tools:
            logger.warning(f"No MCP tools available for {subpart_uri} agent - continuing anyway")
            tools = []  
        
        agent = create_react_agent(
            model=llm,
            tools=tools,
            debug=True
        )
        
        if not agent:
            raise ValueError("create_react_agent returned None")
        
        subpart_agent = SubpartAgent(subpart_uri, agent)
        
        logger.info(f"✅ Successfully created agent: {subpart_agent.subpart_name}")
        return subpart_agent
        
    except Exception as e:
        logger.error(f"❌ Failed to create agent for {subpart_uri}: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"❌ Detailed traceback: {traceback.format_exc()}")
        raise  

async def create_all_subpart_agents(subpart_uris: list) -> Dict[str, SubpartAgent]:
    """Create all 7 specialized subpart agents"""
    logger.info(f"🏢 AGENT CREATION START: {len(subpart_uris)} URIs provided")
    logger.info(f"📋 URIs to process: {subpart_uris}")
    
    if not subpart_uris:
        logger.error("❌ CRITICAL: No subpart URIs provided to create_all_subpart_agents")
        return {}
    
    agents = {}
    successful_count = 0
    failed_count = 0
    
    for i, uri in enumerate(subpart_uris, 1):
        logger.info(f"🚀 CREATING AGENT {i}/{len(subpart_uris)}: {uri}")
        
        try:
            if not uri or not isinstance(uri, str):
                raise ValueError(f"Invalid URI: {uri}")
            
            logger.info(f"🔧 Calling create_subpart_agent for {uri}")
            agent = await create_subpart_agent(uri)
            
            if not agent:
                raise ValueError(f"create_subpart_agent returned None for {uri}")
            
            if not hasattr(agent, 'subpart_name') or not agent.subpart_name:
                raise ValueError(f"Agent missing subpart_name for {uri}")
            
            agents[agent.subpart_name] = agent
            successful_count += 1
            logger.info(f"✅ AGENT {i} SUCCESS: {agent.subpart_name} created successfully")
            
        except Exception as e:
            failed_count += 1
            logger.error(f"❌ AGENT {i} FAILED: {uri} - {type(e).__name__}: {e}")
            import traceback
            logger.error(f"❌ Full traceback for {uri}: {traceback.format_exc()}")
            
            continue
    
    logger.info(f"🎯 AGENT CREATION COMPLETE: {successful_count} successful, {failed_count} failed")
    logger.info(f"📊 Created agents: {list(agents.keys())}")
    
    if not agents:
        logger.error("❌ CRITICAL: No agents were successfully created!")
    elif len(agents) < len(subpart_uris):
        logger.warning(f"⚠️ WARNING: Only {len(agents)}/{len(subpart_uris)} agents created")
    else:
        logger.info(f"✅ SUCCESS: All {len(agents)} agents created successfully")
    
    return agents