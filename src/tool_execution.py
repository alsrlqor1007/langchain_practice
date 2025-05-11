import sys
from pprint import pprint

from langchain_core.messages import ToolMessage

from src.tool import get_tavily_tool
from src.tool_calling import call_tools


def execute_tool(query: str):
    # 검색할 쿼리 설정
    query = "스테이크와 어울리는 와인을 추천해주세요." if query is None else query
    ai_msg = call_tools(query)
    tool_call = ai_msg.tool_calls[0]

    web_search = get_tavily_tool()

    # 직접 도구 호출하는 바법
    # tool_output = web_search.invoke(tool_call["args"])
    # print(f"{tool_call['name']} 호출 결과")
    # print(tool_output)

    # ToolMessage 객체 생성해서 호출하는 방법
    # tool_message = ToolMessage(
    #     content=tool_output,
    #     tool_call_id=tool_call["id"],
    #     name=tool_call["name"]
    # )
    # print(tool_message)

    # 도구 직접 호출해서 ToolMessage 객체 생성하는 방법
    tool_message = web_search.invoke(tool_call)
    print(tool_message)

    pprint(tool_message.tool_call_id)

    pprint(tool_message.name)
    pprint(tool_message.content)

    print("호출된 모든 도구 조회")
    print(ai_msg.tool_calls)

    # 도구 호출이 여러 개인 경우 batch 처리
    tool_messages = web_search.batch(ai_msg.tool_calls)

    print(tool_messages)
    pprint(tool_messages[0].content)

    return tool_messages


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "❌ 쿼리를 인자로 전달해주세요.\n예: python src/chain.py '오늘 날씨 어때?'"
        )
    else:
        execute_tool(sys.argv[1])
