import logging
from abc import ABC, abstractmethod

logger = logging.getLogger("agriguard.services.llm")


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, context: str, query: str) -> dict:
        pass


class DemoProvider(LLMProvider):
    def generate(self, context: str, query: str) -> dict:
        """A local deterministic mock provider.

        Synthesizes provided evidence without inventing facts.
        """
        if not context.strip():
            return {
                "recommendation": "Insufficient authoritative advisory evidence was retrieved. Please consult a qualified agricultural expert before applying chemical or cultural treatments.",
                "provider": "local-demo",
            }

        recommendation = (
            f"Advisory grounded in retrieved evidence:\n\n{context.strip()[:350]}\n\n"
            "Action Plan: Monitor fields closely, ensure adequate drainage during wet periods, "
            "and consult a local agricultural extension officer for field validation."
        )

        return {"recommendation": recommendation, "provider": "local-demo"}


class GraniteProvider(LLMProvider):
    def __init__(self, api_key: str, project_id: str, url: str, model_id: str):
        self.api_key = api_key
        self.project_id = project_id
        self.url = url
        self.model_id = model_id
        self._model = None

        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference

            creds = Credentials(url=self.url, api_key=self.api_key)
            self._model = ModelInference(
                model_id=self.model_id,
                credentials=creds,
                project_id=self.project_id,
            )
            logger.info(f"Initialized IBM WatsonX Granite model: {self.model_id}")
        except Exception as e:
            logger.warning(f"Could not initialize IBM WatsonX client ({str(e)}). Will fall back to DemoProvider.")
            self._model = None

    def generate(self, context: str, query: str) -> dict:
        if not context.strip():
            return {
                "recommendation": "Insufficient authoritative advisory evidence was retrieved. Please consult a qualified agricultural expert.",
                "provider": "ibm-granite",
            }

        if self._model is None:
            # Safe fallback if credentials or initialization failed
            demo = DemoProvider()
            res = demo.generate(context, query)
            res["provider"] = "ibm-granite (local fallback)"
            return res

        prompt = (
            f"System: You are an expert agricultural advisor for smallholder farmers. "
            f"Synthesize the following retrieved evidence to answer the farmer query. "
            f"Do not invent facts not present in the evidence.\n\n"
            f"Retrieved Evidence:\n{context}\n\n"
            f"Farmer Query: {query}\n\n"
            f"Grounded Advisory:"
        )

        try:
            params = {"max_new_tokens": 300, "temperature": 0.2}
            output = self._model.generate_text(prompt=prompt, params=params)
            return {
                "recommendation": output.strip(),
                "provider": "ibm-granite",
            }
        except Exception as e:
            logger.error(f"Error calling IBM Granite API: {str(e)}")
            demo = DemoProvider()
            res = demo.generate(context, query)
            res["provider"] = "ibm-granite (error fallback)"
            return res


def get_llm_provider() -> LLMProvider:
    from app.core.config import settings

    if settings.watsonx_api_key and settings.watsonx_project_id:
        return GraniteProvider(
            api_key=settings.watsonx_api_key,
            project_id=settings.watsonx_project_id,
            url=settings.watsonx_url,
            model_id=settings.granite_model_id or "ibm/granite-13b-instruct-v2",
        )
    return DemoProvider()
