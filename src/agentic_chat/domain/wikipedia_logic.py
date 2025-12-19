"""Wikipedia domain logic for content retrieval."""
import wikipediaapi


wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='im2203-wiki-tool/1.0 (educational-project)'
)


class WikipediaLogic:
    """Domain logic for Wikipedia content retrieval."""
    
    def search_content(self, query: str) -> str:
        """
        Search Wikipedia for information about a topic.
        
        Args:
            query: The topic to search for
            
        Returns:
            String containing the summary of the Wikipedia page
            
        Raises:
            RuntimeError: If the page is not found
            Exception: For other Wikipedia API errors
        """
        try:
            page = wiki.page(query)
            if page.exists():
                # Get the summary (first paragraph) or full text if summary is short
                summary = page.summary
                if len(summary) < 100:
                    return page.text[:1000] + "..." if len(page.text) > 1000 else page.text
                return summary
            else:
                raise RuntimeError(f"Page '{query}' not found on Wikipedia")
        except RuntimeError:
            raise  # Re-raise our custom error
        except Exception as e:
            raise Exception(f"Error searching Wikipedia: {str(e)}")