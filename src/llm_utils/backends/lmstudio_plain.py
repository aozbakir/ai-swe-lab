# llm_utils/backends/lmstudio_plain.py
import lmstudio as lms
from llm_utils.interfaces.base import BaseLLM

class LMStudioPlain(BaseLLM):
    def __init__(self,  model_name):
        self._model = lms.llm(model_name)

    def name(self) -> str:
        return f"lmstudio-plain:{self._model.model_name}"

    def metadata(self) -> dict:
        return {"backend": "lmstudio", "capabilities": ["chat"]}

    def generate(self, prompt: str) -> str:
        response = self._model.complete(prompt)
        return response.content
