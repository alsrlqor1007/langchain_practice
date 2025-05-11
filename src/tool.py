from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults

load_dotenv()


def get_tavily_tool(search_max_results: int = 2) -> TavilySearchResults:
    """
    Tavily Search Tool 반환
    """
    # Tavily 검색 도구 초기화
    web_search = TavilySearchResults(max_results=search_max_results)
    print("1️⃣  TavilySearch 웹 검색 도구 initialize")
    inspect_tool_info(web_search)
    return web_search


def inspect_tool_info(tool):
    print("Tavily 도구 속성 조회")
    print("자료형: ", type(tool))
    print("name: ", tool.name)
    print("description: ", tool.description)
    print("schema: ", tool.args_schema.schema())
