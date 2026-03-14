import logging
from typing import List, Optional
from pathlib import Path

from core.models import DataEntry, DataEntryType, AppConfigModel, RulesetVersion

# Note: AppLanguage import was missing from the check above, but assuming core.models has it (it did)
try:
    from core.models import AppLanguage
except ImportError:
    pass

from data.loader import DataLoader

logger = logging.getLogger(__name__)

# Map RulesetVersion to directory prefix
RULESET_DIR_MAP = {
    RulesetVersion.DND50E: "dnd-50",
    RulesetVersion.DND50E_SDR: "dnd-50-sdr51",
    RulesetVersion.DND55E: "dnd-55",
    RulesetVersion.DND55E_SDR: "dnd-55-sdr" # Optional assumption
}

class SearchEngine:
    """
    In-memory data search engine for D&D data.
    Loads data directly from the active ruleset directory using DataLoader.
    """
    
    def __init__(self, data_root_path: str = None):
        # Default to the `data/` directory relative to THIS file's actual location on disk.
        # This ensures it works regardless of the process working directory.
        if data_root_path is None:
            self.data_root = Path(__file__).parent.resolve()
        else:
            self.data_root = Path(data_root_path).resolve()
        self._entries: List[DataEntry] = []
        self._loaded_ruleset_key: Optional[str] = None
        
    def load_active_ruleset(self, config: AppConfigModel):
        """
        Clears existing data and loads data from the directory specified by current config.
        """
        ruleset_prefix = RULESET_DIR_MAP.get(config.active_ruleset, "dnd-50")
        
        # Determine language suffix (assume EN if no lang or error)
        lang_suffix = "en"
        if hasattr(config, 'language') and config.language:
            lang_suffix = config.language.value.lower()
            
        ruleset_key = f"{ruleset_prefix}-{lang_suffix}"
        
        # Avoid reloading if same ruleset is already loaded
        if self._loaded_ruleset_key == ruleset_key and self._entries:
            logger.debug(f"Ruleset {ruleset_key} already loaded, skipping reload.")
            return

        self._entries.clear()
        dir_name = ruleset_key
        target_dir = self.data_root / dir_name
        
        # Fallback to English if localized dir doesn't exist
        if not target_dir.exists():
            logger.warning(f"Localized ruleset {target_dir} not found. Falling back to English.")
            target_dir = self.data_root / f"{ruleset_prefix}-en"
            
        # Support user's directory naming schema `dnd-50-eng` vs `-en`
        if not target_dir.exists():
            target_dir = self.data_root / f"{ruleset_prefix}-eng"
        
        if not target_dir.exists():
            logger.error(f"Ruleset directory not found: {target_dir}")
            self._loaded_ruleset_key = None
            return

        logger.info(f"Loading ruleset data from: {target_dir}")
        start_time = 0
        try:
            import time
            start_time = time.time()
        except: pass

        self._entries = DataLoader.load_directory(target_dir)
        self._loaded_ruleset_key = ruleset_key
        
        duration_msg = ""
        if start_time:
            duration = (time.time() - start_time) * 1000
            duration_msg = f" in {duration:.2f}ms"
            
        logger.info(f"Loaded {len(self._entries)} data entries{duration_msg}.")
        
    def search(self, query: str = "", entry_types: Optional[List[DataEntryType]] = None) -> List[DataEntry]:
        """
        Fast in-memory case-insensitive search by substring matching name or content.
        Filtered by DataEntryType if provided.
        Returns alphabetically sorted results.
        """
        if not self._entries:
            return []
            
        query_lower = query.lower() if query else ""
        results = []
        
        for entry in self._entries:
            # Filter by type
            if entry_types and entry.type not in entry_types:
                continue
                
            # Filter by query
            if query_lower:
                if query_lower in entry.name.lower():
                    results.append(entry)
                    continue
                    
                # Search in content if not found in name
                if query_lower in entry.content_markdown.lower():
                    results.append(entry)
            else:
                # If query is empty, but type matched (or no type filter), include
                results.append(entry)
                    
        # Sort alphabetically by name
        results.sort(key=lambda x: x.name)
        return results

    def get_entry_by_id(self, entry_id: str) -> Optional[DataEntry]:
        """Fetch a specific entry by its ID."""
        for entry in self._entries:
            if entry.id == entry_id:
                return entry
        return None
