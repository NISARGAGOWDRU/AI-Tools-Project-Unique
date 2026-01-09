from typing import TypedDict, List, Optional, Union, Dict, Any

class PipelineState(TypedDict, total=False):
  """
  Defines the shared state for the LangGraph pipeline.
  Keep this minimal: only small pointers/flags, not whole documents.
  """

  user_input: str
  document: Optional[Dict[str, Any]]
  document_id: Optional[str]
  tool_calls: List[str]
  last_tool_result: Optional[Union[str, List[Union[str, Dict[str, Any]]]]]
  status: str
  upload_completed: str
  page_urls: Optional[Dict[str, Any]]
  summarized_page_uris: Optional[List[str]]
  document_summary: Optional[str]
  subpart_summary_uris: List[str]
  compliance_results: Optional[Dict[str, Any]]
  final_compliance_summary: Optional[Dict[str, Any]]
  detailed_check_page: Optional[Union[int, List[int]]]
  detailed_check_subpart: Optional[str]
  detailed_check_result: Optional[Dict[str, Any]]