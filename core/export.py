import logging
from typing import List
from pathlib import Path
from core.models import DataEntry

logger = logging.getLogger(__name__)

def export_entries_to_markdown(entries: List[DataEntry], filepath: str) -> bool:
    """
    Exports a list of DataEntry objects into a single cohesive Markdown file.
    """
    try:
        path = Path(filepath)
        
        markdown_blocks = []
        markdown_blocks.append("# Session Kit Export\n")
        markdown_blocks.append(f"*Generated {len(entries)} items*\n")
        markdown_blocks.append("---\n")
        
        for entry in entries:
            # entry.content_markdown already includes "# {name}" and basic fields
            markdown_blocks.append(entry.content_markdown)
            markdown_blocks.append("\n---\n")
            
        final_content = "\n".join(markdown_blocks)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        logger.info(f"Successfully exported {len(entries)} items to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to export entries to markdown: {e}")
        return False
