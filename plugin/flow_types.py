from typing import TypedDict

class JsonRPCAction(TypedDict):
    method: str
    parameters: list[str]

class QueryResponse(TypedDict):
    title: str
    subTitle: str
    icoPath: str
    jsonRPCAction: JsonRPCAction
    score: int

class QueryComponents(TypedDict):
    template: str
    arguments: list[str]