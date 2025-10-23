from typing import List

from langchain.schema import Document


class PromptConstructor:
    """Constructs prompts by merging user query with retrieved context"""
    def __init__(self, template: str = None):
        self.template = template or """
You are an AI assistant implementing pure RAG (Retrieval-Augmented Generation) for questions about the EU AI Act.

IMPORTANT INSTRUCTIONS:
1. ONLY answer based on the document context provided with each question
2. If the information needed to answer the question is NOT found in the provided context, respond with \"I don't know. The necessary information is not found in the provided context.\"
3. DO NOT use prior knowledge about the EU AI Act outside of the provided context
4. DO NOT make up or infer information that isn't explicitly stated in the context
5. ALWAYS cite your sources by referring to document numbers [1], [2], or [3] for each piece of information
6. When possible, refer to specific Articles, Chapters, or Sections as mentioned in the reference information
7. Format citations like: \"According to Document [1], Article 28 states that...\"
8. Focus only on the current question and context, not on previous exchanges

Your answers must be fully grounded in the retrieved document context with explicit citations.

Context:
{context}

Question: {query}

Answer:"""
    
    def build_prompt(self, query: str, retrieved_docs: List[Document]) -> str:
        """Merge query and retrieved documents into a prompt"""
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        return self.template.format(context=context, query=query)
