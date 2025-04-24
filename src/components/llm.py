from openai import OpenAI


class LLM:
    def __init__(self):
        self.llm = OpenAI()

    def generate_response(self, query: str, content: str):
        return self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a part of a rag system, you will be provided content from documents and you will be able to answer questions based on the content.",
                },
                {
                    "role": "system",
                    "content": content,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )
