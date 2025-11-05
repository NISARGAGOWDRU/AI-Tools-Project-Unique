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
    
    async def assess_compliance(self, document_summary: str) -> Dict[str, Any]:
        """
        Run all subpart agents in parallel to assess compliance
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
        
        logger.info(f"🔄 Starting compliance assessment with {len(self.subpart_agents)} specialized agents sequentially")
        logger.info(f"� Available agents: {list(self.subpart_agents.keys())}")
        logger.info(f"📄 Document summary length: {len(document_summary)} characters")
        
        # Run agents sequentially with comprehensive error handling
        results = []
        logger.info(f"🔄 EXECUTION START: Processing {len(self.subpart_agents)} agents sequentially")
        
        # Send progress update
        await status_updater.send_update(
            "conducting_compliance", 
            f"Analyzing compliance across {len(self.subpart_agents)} CFR 21 subparts...", 
            "update"
        )
        
        for i, (agent_name, agent) in enumerate(self.subpart_agents.items(), 1):
            logger.info(f"📋 AGENT {i}/{len(self.subpart_agents)} START: {agent_name}")
            logger.info(f"🔍 Agent type: {type(agent)}")
            
            # Send progress update for each agent
            await status_updater.send_update(
                "conducting_compliance",
                f"Analyzing {agent_name} compliance ({i}/{len(self.subpart_agents)})...",
                "update"
            )
            
            try:
                logger.info(f"🚀 Calling compare_compliance for {agent_name}")
                result = await asyncio.wait_for(agent.compare_compliance(document_summary), timeout=180.0)
                
                if result:
                    results.append(result)
                    status = result.get('status', 'unknown')
                    score = result.get('compliance_score', 'N/A')
                    score_display = f"{score}/100" if isinstance(score, int) else score
                    logger.info(f"✅ AGENT {agent_name} SUCCESS: status={status}, score={score_display}")
                    logger.info(f"📊 {agent_name} output: {str(result)[:300]}...")
                    
                    # Send progress update
                    await status_updater.send_update(
                        "conducting_compliance",
                        f"✅ {agent_name} analysis complete (Score: {score_display})",
                        "update"
                    )
                else:
                    logger.error(f"❌ AGENT {agent_name} returned None/empty result")
                    results.append({
                        "subpart": agent_name,
                        "error": "Empty result returned",
                        "compliance_score": 0,
                        "status": "failed"
                    })
                
            except asyncio.TimeoutError:
                logger.error(f"⏰ AGENT {agent_name} TIMEOUT after 60 seconds")
                results.append({
                    "subpart": agent_name,
                    "error": "Timeout after 60 seconds",
                    "compliance_score": 0,
                    "status": "failed"
                })
            except Exception as e:
                logger.error(f"❌ AGENT {agent_name} EXCEPTION: {type(e).__name__}: {e}")
                import traceback
                logger.error(f"❌ {agent_name} traceback: {traceback.format_exc()}")
                results.append({
                    "subpart": agent_name,
                    "error": str(e),
                    "compliance_score": 0,
                    "status": "failed"
                })
            
            logger.info(f"✅ AGENT {i}/{len(self.subpart_agents)} COMPLETE: {agent_name}")
            
            # Send overall progress update
            completed_count = i
            total_count = len(self.subpart_agents)
            await status_updater.send_update(
                "conducting_compliance",
                f"Progress: {completed_count}/{total_count} subpart assessments completed",
                "update"
            )
        
        try:
            # Process results
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
            # Create empty coordinator to avoid crashes
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