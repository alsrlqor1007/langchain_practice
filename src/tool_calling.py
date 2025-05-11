from pprint import pprint

from langchain_openai import ChatOpenAI

from src.tool import get_tavily_tool


def llm_bind_tools(tool):
    """
    LLM 모델에 도구 바인딩해서 반환
    """
    # ChatOpenAI 모델 초기화
    llm = ChatOpenAI(model="gpt-4o-mini")
    print("2️⃣  ChatOpenAI 모델 initialize 및 Tool binding")

    # 웹 검색 도구 LLM에 바인딩
    llm_with_tools = llm.bind_tools(tools=[tool])
    return llm_with_tools


def call_tools(query: str):
    # Tavily 웹 검색 도구 호출
    web_search = get_tavily_tool()
    llm_with_tools = llm_bind_tools(web_search)

    # LLM tool calling
    ai_msg = llm_with_tools.invoke(query)

    # Tool calling 결과 출력
    print("Tool calling result")
    pprint(ai_msg)

    # 메시지 content 속성 출력
    print("Tool calling content text")
    pprint(ai_msg.content)

    # LLM이 호출한 도구 정보 출력
    print("Tool information")
    pprint(ai_msg.tool_calls)

    return ai_msg
