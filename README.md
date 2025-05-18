# 🧠 LangChain Tool Calling 실습: Tavily 검색 도구 연동

이 프로젝트는 LangChain에서 OpenAI LLM과 웹 검색 도구(Tavily)를 연동하여,
사용자의 질문에 따라 **LLM이 스스로 판단하여 도구를 호출하고**, **도구 실행 결과를 반영해 최종 응답을 생성하는 전체 흐름** 실습

---

## 📌 프로젝트 목적

- LangChain의 **tool calling 메커니즘** 이해
- LLM이 **도구 실행 명세(tool_calls)**를 반환하고,
  개발자가 직접 도구를 실행하여 결과를 다시 LLM에 넘기는 구조 체험
- Tavily 검색 도구를 사용해 웹 기반 정보 응답 자동화 체험

---

## ⚙️ 사용 기술

- Python 3.12
- [LangChain](https://github.com/langchain-ai/langchain)
- [Tavily Search API](https://docs.tavily.com/)
- [OpenAI API](https://platform.openai.com/)
- `poetry`, `dotenv`

---

## 🗂️ 디렉토리 구조

```
langchain-tool-calling/
├── src/
│ ├── chain.py          # 전체 실행 흐름 컨트롤
│ ├── tool.py           # Tavily 도구 초기화 및 속성 출력
│ ├── tool_calling.py   # LLM 초기화 및 도구 바인딩
│ ├── tool_decorator.py # 사용자 정의 도구 선언 방식
│ └── tool_execution.py # Tavily 도구 호출 단일 실행
├── .env                # API 키 설정
├── pyproject.toml
└── README.md
```
---

## 🧠 LangChain Tool Calling 개념 정리

### 📌 Tool Calling이란?

- LLM이 **외부 기능이나 데이터**에 접근할 수 있게 해주는 메커니즘
- 단순 응답 생성 외에, **실시간 정보 조회**, **정확성 향상**, **특수 기능 실행**을 위해 필수 요소
- LangChain은 다양한 외부 도구와의 연동을 손쉽게 구현할 수 있도록 지원

### 🧱 Tool 구성 요소

| 요소 | 설명 |
|------|------|
| `name` | 도구의 이름 (LLM이 식별할 때 사용) |
| `description` | 도구의 기능 설명 (LLM의 이해에 직접적 영향) |
| `JSON Schema` | 도구의 입력 파라미터 구조 (LLM이 어떤 인자를 넣어야 하는지 이해함) |
| `function` | 실제 실행할 Python 함수 (동기 또는 비동기 가능) |

> 🧠 **`name`과 `description`은 프롬프트에 포함되며, LLM이 도구의 쓰임을 판단하는 핵심이다.**  
> `JSON Schema`는 LLM이 인자 구조를 인식하고 자동 완성하는데 필요하다.

---

### 🔍 Tavily Search 도구

- AI 기반 **웹 검색 API** 서비스
- LangChain에 공식 도구로 통합되어 사용 가능
- **월 1,000회 무료 사용** 가능
- LLM이 검색 키워드를 생성 → Tavily가 검색 실행 → 결과를 기반으로 응답 생성

### 🧪 검색 흐름

> LLM은 사용자의 질문을 그대로 검색하는 것이 아니라, **적절한 검색어로 변환하는 작업도 수행**한다.

---

### 🔁 Tool Calling 실행 흐름 요약

1. ✅ **LLM 모델 초기화**
2. 🔗 **도구 바인딩 (bind_tools)**
3. 🗣️ **사용자 쿼리 입력 + invoke 실행**
4. 📦 **LLM이 도구 호출 명세(`tool_calls`)를 생성**
5. 🛠️ **실제 도구를 명세에 따라 실행**
6. 🔁 **도구 결과를 LLM에 다시 전달**
7. 🧾 **LLM이 최종 응답 생성**

---

### 🧭 LLM + Tool 체인 구성 흐름

1. 📅 **오늘 날짜 설정** → 시점 기준 정보 판단에 활용
2. 🧩 **프롬프트 템플릿 구성** → system + user 메시지 조합
3. 🔗 **프롬프트와 바인딩된 LLM 체인 생성**
4. 🧵 **@chain 데코레이터로 실행 체인 구성**
5. 💬 **사용자 쿼리 수신 후 tool call 판단**
6. 🧾 **도구 실행 결과(ToolMessage) 수신**
7. 🤖 **LLM이 최종 응답 생성 후 반환**

---

## ✅ 실행 방법

### 1. `.env` 파일에 API 키 설정
```dotenv
OPENAI_API_KEY=...
TAVILY_API_KEY=...
```

### 2. Poetry 환경 설치

```bash
poetry install
```

### 3. 실행(example)
```bash
poetry run python src/chain.py "오늘 날씨는 어때?"
```

---

## 🔁 실행 흐름 요약

### 전체 흐름

```
[사용자 쿼리 입력]
        │
        ▼
[1️⃣ llm_chain.invoke(input_)]
        │
        │  → LLM이 도구 사용 필요 판단
        │  → 도구 호출 명세(tool_calls)를 포함한 ai_msg 생성
        ▼
[2️⃣ ai_msg.tool_calls]
        │
        │  → 예: [{'name': 'tavily_search_results_json', 'args': {'query': '오늘 날씨'}}]
        ▼
[3️⃣ 도구 실행: web_search.batch(tool_calls)]
        │
        │  → 실제 도구 실행 결과 ToolMessage 리스트(tool_msgs) 생성
        ▼
[4️⃣ llm_chain.invoke(messages=[ai_msg, *tool_msgs])]
        │
        │  → 도구 실행 결과를 바탕으로 LLM이 최종 응답 생성
        ▼
[✅ 최종 응답 출력]
```
---
## 🔎 주요 개념 정리

| 항목        | 설명                                                                 |
|-------------|----------------------------------------------------------------------|
| `ai_msg`     | LLM이 사용자 질문에 응답한 메시지로, 도구 호출 명세(`tool_calls`) 포함 |
| `tool_calls` | LLM이 호출하라고 판단한 도구의 이름과 인자 정보                     |
| `tool_msgs`  | 실제 도구를 실행한 결과로 생성된 메시지. LLM에게 전달되어 응답 생성에 사용 |

---
## 🧪 LLM Chain 실행에 따른 print문 출력 순서
```bash
1️⃣  TavilySearch 웹 검색 도구 initialize
2️⃣  ChatOpenAI 모델 initialize 및 Tool binding
3️⃣  프롬프트와 Tool 바인딩된 LLM으로 체인 생성
4️⃣  LLM 체인으로 Tool 호출
5️⃣  tool_calls 명세 기반으로 실제 도구 실행 및 응답 생성
6️⃣  도구 응답을 포함해 LLM에게 최종 응답 요청
✅  final response
```

---

## 🛠️ 단독 도구 호출(`tool_execution.py`)

이 스크립트는 LangChain에서 LLM의 응답 결과로 생성된 `tool_calls` 명세를 기반으로, **도구만 직접 실행**해보고 `ToolMessage` 객체를 생성하는 방법 실습

### 주요 흐름

1. 사용자 쿼리 → `call_tools()`를 통해 LLM 응답(`tool_calls`) 추출
2. LLM이 판단한 도구 호출 명세(`tool_call`) 확인
3. 해당 도구(`TavilySearchResults`)를 직접 호출하여 결과 확인
4. 결과를 `ToolMessage`로 감싸는 방법, 또는 `batch()` 호출을 통한 다중 실행

### 실행 예시

```bash
python src/tool_execution.py "2025년 전국 장마 예상 기간을 알려줘."
```

이 스크립트는 LLM 없이도 도구 호출 흐름을 독립적으로 테스트하거나, LangChain 내부 `tool_call` 처리 구조를 확인할 때 사용
