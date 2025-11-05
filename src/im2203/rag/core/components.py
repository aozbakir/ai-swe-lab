from im2203.rag.schemas.rag_config import RAGConfig

class BaseComponent:
    def __init__(self, rag_config: RAGConfig, section: str):
        self.config = rag_config
        self.section = section

    def get_strategy_config(self):
        section_cfg = getattr(self.config, self.section, None)
        if not section_cfg:
            raise ValueError(f"Config missing section '{self.section}'")
        
        strategy = getattr(section_cfg, "default", None)
        if not strategy:
            raise ValueError(f"Config section '{self.section}' missing 'default' strategy")
        
        # Use dict() to access the strategy kwargs
        strategy_kwargs = section_cfg.dict().get(strategy, {}) or {}
        return strategy, strategy_kwargs
