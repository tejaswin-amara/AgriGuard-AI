class LLMProvider:
    def generate(self, context: str, query: str) -> dict:
        raise NotImplementedError


class DemoProvider(LLMProvider):
    def generate(self, context: str, query: str) -> dict:
        """
        A local, deterministic mock provider.
        Does not invent advice; only synthesizes the provided context.
        """
        if not context.strip():
            return {
                "recommendation": "Insufficient authoritative advisory evidence was retrieved. Please consult a qualified agricultural expert.",
                "provider": "local-demo",
            }

        # Mock synthesis
        recommendation = f"Based on the guidelines: {context[:100]}... Please refer to the specific sources below for complete details."

        return {"recommendation": recommendation, "provider": "local-demo"}


class GraniteProvider(LLMProvider):
    def __init__(self, api_key: str, project_id: str, url: str, model_id: str):
        self.api_key = api_key
        self.project_id = project_id
        self.url = url
        self.model_id = model_id

        # Initialize ibm_watsonx_ai client here when credentials are provided
        # e.g., self.model = Model(...)

    def generate(self, context: str, query: str) -> dict:
        if not context.strip():
            return {
                "recommendation": "Insufficient authoritative advisory evidence was retrieved. Please consult a qualified agricultural expert.",
                "provider": "ibm-granite",
            }

        # This would call the actual IBM Granite API
        # For safety, if credentials fail or it's just a placeholder, we could fall back,
        # but here we'll assume it's correctly configured if this class is used.
        return {
            "recommendation": f"[IBM Granite Simulated Response] Grounded on: {context[:50]}...",
            "provider": "ibm-granite",
        }


def get_llm_provider() -> LLMProvider:
    from app.core.config import settings

    if settings.watsonx_api_key and settings.watsonx_project_id:
        return GraniteProvider(
            api_key=settings.watsonx_api_key,
            project_id=settings.watsonx_project_id,
            url=settings.watsonx_url,
            model_id=settings.granite_model_id,
        )
    return DemoProvider()
