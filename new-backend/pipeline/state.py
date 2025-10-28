
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