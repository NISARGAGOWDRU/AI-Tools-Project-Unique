from enum import Enum


class PipelineStatus(str, Enum):
    STARTED = "started"
    SUMMARIZING_PAGES = "summarizing_pages"
    PAGES_SUMMARIZED = "pages_summarized"
    DOCUMENT_SUMMARY_GENERATED = "document_summary_generated"
    CONDUCTING_COMPLIANCE = "conducting_compliance"
    SUMMARIZING_COMPLIANCE = "summarizing_compliance"
    COMPLETED = "completed"
    ERROR = "error"


PROCESS_MESSAGES = {
    PipelineStatus.STARTED: "Initializing document processing...",
    PipelineStatus.PAGES_SUMMARIZED: "Summarizing document pages...",
    PipelineStatus.DOCUMENT_SUMMARY_GENERATED: "Generating document summary...",
    PipelineStatus.CONDUCTING_COMPLIANCE: "Analyzing Subparts compliance...",
    PipelineStatus.SUMMARIZING_COMPLIANCE: "Generating final compliance summary...",
    PipelineStatus.COMPLETED: "Finalizing document analysis...",
}

def get_compliance_message(subpart: str, current: int, total: int) -> str:
    return f"Analyzing Subpart_{subpart} compliance ({current}/{total})..."

SUCCESS_MESSAGES = {
    PipelineStatus.PAGES_SUMMARIZED: "Pages summarized",
    PipelineStatus.DOCUMENT_SUMMARY_GENERATED: "Document summary generated",
    PipelineStatus.CONDUCTING_COMPLIANCE: "Analysis complete",
    PipelineStatus.SUMMARIZING_COMPLIANCE: "Analysis complete",
    PipelineStatus.COMPLETED: "Document analysis complete",
}
