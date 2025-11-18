import time
from typing import Tuple

from langchain_core.language_models import BaseChatModel

from rag.prompts.prompt import PromptTemplate
from rag.retrieval.base import BaseRetriever

class QARetriever:
    """High-level QA pipeline built on a retriever."""
    
    def __init__(self, retriever: BaseRetriever, llm: BaseChatModel, prompt_template: PromptTemplate):
        self.retriever = retriever
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, query: str, verbose: bool = False) -> Tuple[str, list]:
        start_time = time.time()

        docs = self.retriever.retrieve(query)
        for i, d in enumerate(docs):
            print(f"Doc {i+1} type: {type(d)}, value: {repr(d)}")

        context = "\n\n---\n\n".join([d.page_content for d in docs])
        prompt = self.prompt_template.format(query=query, context=context)

        response = self.llm.invoke(prompt)
        response_text = getattr(response, "content", str(response)).strip()

        elapsed = time.time() - start_time
        if verbose:
            print(f"[QA] Retrieved {len(docs)} docs, generated in {elapsed:.2f}s")

        return response_text, docs
