from typing import Dict, Any, List
from pipeline.agents.subpart_agent import create_all_subpart_agents, SubpartAgent
from pipeline.update import status_updater
import asyncio
import logging

logger = logging.getLogger(__name__)

class ComplianceCoordinator:
    """Coordinates all subpart agents for comprehensive compliance assessment"""
    
    def __init__(self, subpart_agents: Dict[str, SubpartAgent]):
        self.subpart_agents = subpart_agents
    
    async def assess_single_subpart(self, subpart_name: str, page_content: str) -> Dict[str, Any]:
        """
        Run a single subpart agent for targeted compliance check
        Returns single subpart compliance result
        """
        if not page_content:
            logger.error("❌ No page content provided")
            return {"error": "No page content provided", "status": "failed"}
        
        if subpart_name not in self.subpart_agents:
            logger.error(f"❌ Subpart agent '{subpart_name}' not found")
            return {"error": f"Subpart '{subpart_name}' not found", "status": "failed"}
        
        agent = self.subpart_agents[subpart_name]
        logger.info(f"🎯 Running targeted check: {subpart_name}")
        
        try:
            result = await asyncio.wait_for(
                agent.compare_compliance(page_content),
                timeout=300.0
            )
            logger.info(f"✅ Targeted check complete: {subpart_name} - Score: {result.get('compliance_score', 'N/A')}")
            return result
        except Exception as e:
            logger.error(f"❌ Targeted check failed for {subpart_name}: {e}")
            return {
                "subpart": subpart_name,
                "error": str(e),
                "compliance_score": 0,
                "status": "failed"
            }
    
    async def assess_compliance(self, document_summary: str) -> Dict[str, Any]:
        """
        Run all subpart agents in PARALLEL with staggered start to assess compliance
        Returns comprehensive compliance results
        """
        if not document_summary:
            logger.error("❌ No document summary provided to assess_compliance")
            return {
                "error": "No document summary provided",
                "status": "failed"
            }
        
        if not self.subpart_agents:
            logger.error("❌ No subpart agents available for compliance assessment")
            return {
                "error": "No subpart agents available",
                "status": "failed"
            }
        
        logger.info(f"🔄 Starting PARALLEL compliance assessment with {len(self.subpart_agents)} specialized agents")
        logger.info(f"📊 Available agents: {list(self.subpart_agents.keys())}")
        logger.info(f"📄 Document summary length: {len(document_summary)} characters")
        
        # 🚀 Truncate document summary to reduce token usage
        max_summary_length = 1000
        truncated_summary = document_summary[:max_summary_length]
        if len(document_summary) > max_summary_length:
            logger.info(f"✂️ Truncated document summary from {len(document_summary)} to {max_summary_length} chars")
        
        # 🚀 NEW: Create tasks with staggered start (1 second delay between each)
        async def run_single_agent_with_delay(agent_name: str, agent: SubpartAgent, delay: float, index: int) -> Dict[str, Any]:
            """Run a single agent with initial delay and error handling"""
            # 🚀 Stagger agent starts to avoid overwhelming local LLM
            await asyncio.sleep(delay)
            logger.info(f"🚀 PARALLEL START (after {delay}s delay): {agent_name}")
            
            # Send progress update for each agent
            await status_updater.send_update(
                "conducting_compliance",
                f"Analyzing {agent_name} compliance ({index}/{len(self.subpart_agents)})...",
                "update"
            )
            
            try:
                result = await asyncio.wait_for(
                    agent.compare_compliance(truncated_summary), 
                    timeout=300.0  
                )
                
                if result:
                    status = result.get('status', 'unknown')
                    score = result.get('compliance_score', 'N/A')
                    score_display = f"{score}/100" if isinstance(score, int) else score
                    logger.info(f"✅ PARALLEL SUCCESS: {agent_name} - status={status}, score={score_display}")
                    return result
                else:
                    logger.error(f"❌ PARALLEL FAIL: {agent_name} returned None/empty result")
                    return {
                        "subpart": agent_name,
                        "error": "Empty result returned",
                        "compliance_score": 0,
                        "status": "failed"
                    }
            
            except asyncio.TimeoutError:
                logger.error(f"⏰ PARALLEL TIMEOUT: {agent_name} after 300 seconds")
                return {
                    "subpart": agent_name,
                    "error": "Timeout after 300 seconds",
                    "compliance_score": 0,
                    "status": "failed"
                }
            except Exception as e:
                logger.error(f"❌ PARALLEL EXCEPTION: {agent_name} - {type(e).__name__}: {e}")
                import traceback
                logger.error(f"❌ {agent_name} traceback: {traceback.format_exc()}")
                return {
                    "subpart": agent_name,
                    "error": str(e),
                    "compliance_score": 0,
                    "status": "failed"
                }
        
        # 🚀 Create tasks with 1-second delays between each agent
        logger.info(f"🔄 PARALLEL EXECUTION START: Processing {len(self.subpart_agents)} agents with staggered starts")
        
        tasks = []
        delay = 0
        for i, (agent_name, agent) in enumerate(self.subpart_agents.items(), 1):
            task = run_single_agent_with_delay(agent_name, agent, delay, i)
            tasks.append(task)
            delay += 1.0  
            logger.info(f"📋 Scheduled {agent_name} to start after {delay}s")
        
        # Execute all tasks concurrently (they start with delays but run in parallel)
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        logger.info(f"✅ PARALLEL EXECUTION COMPLETE: All {len(results)} agents finished")
        
        # Process results
        try:
            compliance_results = {
                "individual_assessments": {},
                "summary": {
                    "total_subparts": len(self.subpart_agents),
                    "completed_assessments": 0,
                    "failed_assessments": 0
                },
                "status": "completed"
            }
            
            for result in results:
                if isinstance(result, Exception):
                    compliance_results["summary"]["failed_assessments"] += 1
                    logger.error(f"❌ Exception result found: {result}")
                else:
                    subpart_name = result.get("subpart", "Unknown_Agent")
                    compliance_results["individual_assessments"][subpart_name] = result
                    logger.info(f"📄 Processing result for {subpart_name}: status={result.get('status')}")
                    
                    if result.get("status") == "completed":
                        compliance_results["summary"]["completed_assessments"] += 1
                    else:
                        compliance_results["summary"]["failed_assessments"] += 1
            
            logger.info(f"🎉 ALL AGENTS PROCESSED! Compliance assessment completed: {compliance_results['summary']['completed_assessments']}/{compliance_results['summary']['total_subparts']} successful")
            logger.info(f"📈 FINAL COMPLIANCE SUMMARY: {compliance_results['summary']}")
            logger.info(f"📋 INDIVIDUAL RESULTS: {list(compliance_results['individual_assessments'].keys())}")
            
            # Force log the complete results
            for agent_name, result in compliance_results['individual_assessments'].items():
                score = result.get('compliance_score', 'N/A')
                score_display = f"{score}/100" if isinstance(score, int) else score
                logger.info(f"📊 {agent_name}: Score={score_display}, Status={result.get('status')}")
            
            return compliance_results
            
        except Exception as e:
            logger.error(f"Error during compliance assessment: {e}")
            return {
                "error": f"Compliance assessment failed: {str(e)}",
                "status": "failed"
            }

async def create_compliance_coordinator(subpart_uris: List[str]) -> ComplianceCoordinator:
    """Create compliance coordinator with all subpart agents"""
    logger.info(f"🚀 COORDINATOR CREATION START: {len(subpart_uris)} subpart URIs provided")
    logger.info(f"📋 URIs to process: {subpart_uris}")
    
    try:
        subpart_agents = await create_all_subpart_agents(subpart_uris)
        logger.info(f"✅ AGENT CREATION COMPLETE: {len(subpart_agents)} agents created successfully")
        logger.info(f"📊 Created agents: {list(subpart_agents.keys())}")
        
        if not subpart_agents:
            logger.error("❌ CRITICAL: No subpart agents were created successfully")
            return ComplianceCoordinator({})
        
        if len(subpart_agents) < len(subpart_uris):
            logger.warning(f"⚠️ WARNING: Only {len(subpart_agents)}/{len(subpart_uris)} agents created successfully")
            missing = len(subpart_uris) - len(subpart_agents)
            logger.warning(f"⚠️ {missing} agents failed to create")
        
        return ComplianceCoordinator(subpart_agents)
        
    except Exception as e:
        logger.error(f"❌ COORDINATOR CREATION FAILED: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return ComplianceCoordinator({})