import sys
from datetime import datetime
from pprint import pprint

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, chain

from src.tool import get_tavily_tool
from src.tool_calling import llm_bind_tools

# 오늘 날짜 설정
today = datetime.today().strftime("%Y-%m-%d")

# 프롬프트 템플릿
prompt = ChatPromptTemplate(
    [
        ("system", f"You are a helpful AI assistant. Today's date is {today}."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)


# 도구 실행 체인 정의
@chain
def web_search_chain(user_input: str, config: RunnableConfig):
    input_ = {"user_input": user_input}
    print("4️⃣  사용자 쿼리 기반으로 LLM tool calls 생성")
    ai_msg = llm_chain.invoke(input_, config=config)
    print("ai_msg(=Tool Calling이 필요한지 판단한 결과) \n", ai_msg)
    print("5️⃣  tool calling 결과 명세 기반으로 실제 도구 실행 및 응답 생성")
    tool_msgs = web_search.batch(ai_msg.tool_calls, config=config)
    print("tool_msgs(=실제 도구를 실행한 결과) \n", tool_msgs)
    print("6️⃣  도구 응답을 포함해 LLM에게 최종 응답 요청")
    return llm_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]}, config=config)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "❌ 쿼리를 인자로 전달해주세요.\n예: python src/chain.py '오늘 날씨 어때?'"
        )
    else:
        query = sys.argv[1]
        try:
            # Tavily 웹 검색 도구 호출
            web_search = get_tavily_tool()

            # LLM에 도구를 바인딩
            llm_with_tools = llm_bind_tools(web_search)

            # LLM 체인 생성
            llm_chain = prompt | llm_with_tools
            print("3️⃣  프롬프트와 Tool 바인딩된 LLM으로 체인 생성")

            response = web_search_chain.invoke(query)
            # 응답 출력
            print("✅  final response")
            pprint(response.content)
        except Exception as e:
            print(e)
