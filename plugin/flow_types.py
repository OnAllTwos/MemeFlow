from typing_extensions import TypedDict, NotRequired

class JsonRPCAction(TypedDict):
    method: str
    parameters: list[str]

class QueryResponse(TypedDict):
    title: str
    subTitle: NotRequired[str]
    icoPath: NotRequired[str]
    jsonRPCAction: NotRequired[JsonRPCAction]
    score: NotRequired[int]

class QueryComponents(TypedDict):
    template: str
    arguments: list[str]