import sys
from pprint import pprint

from langchain_core.tools import tool

from src.tool import get_tavily_tool


# Tool 데코레이터로 사용자 정의 도구 선언
@tool
def search_web(query: str) -> str:
    """Searches the internet for information that does not exist in the database or for the latest information."""

    web_search = get_tavily_tool()
    docs = web_search.invoke(query)

    formatted_docs = "\n---\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in docs
        ]
    )

    if len(formatted_docs) > 0:
        return formatted_docs

    return "관련 정보를 찾을 수 없습니다."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "❌ 쿼리를 인자로 전달해주세요.\n예: python src/chain.py '오늘 날씨 어때?'"
        )
    else:
        query = sys.argv[1]
        try:
            print("자료형: ")
            print(type(search_web))
            print("-" * 100)

            print("name: ")
            print(search_web.name)
            print("-" * 100)

            print("description: ")
            pprint(search_web.description)
            print("-" * 100)

            print("schema: ")
            pprint(search_web.args_schema.schema())
            print("-" * 100)

            search_result = search_web.invoke(query)
            pprint(search_result)
        except Exception as e:
            print(e)
