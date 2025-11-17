from core.openai_client import client

class SearchTool:
    def search(self, query):
        result = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Search the internet and summarize: {query}"
        )
        return result.output_text
