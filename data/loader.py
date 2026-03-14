import csv
import logging
from typing import List, Optional
from pathlib import Path

from core.models import DataEntry, DataEntryType

logger = logging.getLogger(__name__)

# Map CSV file stems to DataEntryType. If a filename is not listed, it will be skipped or need special handling.
FILE_TYPE_MAP = {
    "spells": DataEntryType.SPELL,
    "monsters": DataEntryType.MONSTER,
    "items": DataEntryType.ITEM,
    "classes": DataEntryType.CLASS,
    "classfeatures": DataEntryType.FEATURE,
    "backgrounds": DataEntryType.BACKGROUND,
    "species": DataEntryType.RACE,
    "feats": DataEntryType.FEATURE,
    "optionalfeatures": DataEntryType.FEATURE,
    "subclassfeatures": DataEntryType.FEATURE,
}

class DataLoader:
    """
    Responsible for reading data files from the data/ directories and parsing them into DataEntry models.
    """
    
    @staticmethod
    def load_directory(directory_path: Path) -> List[DataEntry]:
        """
        Scans a directory for known CSV files and parses them.
        """
        entries = []
        if not directory_path.exists() or not directory_path.is_dir():
            logger.warning(f"Data directory {directory_path} not found.")
            return entries

        # We specifically read CSV files based on our mapping to bypass macOS Sandbox terminal restrictions correctly
        for file_path in directory_path.glob("*.csv"):
            file_stem = file_path.stem.lower()
            if file_stem in FILE_TYPE_MAP:
                entry_type = FILE_TYPE_MAP[file_stem]
                entries.extend(DataLoader._parse_csv(file_path, entry_type))
            else:
                logger.debug(f"Skipping unknown CSV file: {file_path.name}")
                
        return entries

    @staticmethod
    def _parse_csv(file_path: Path, entry_type: DataEntryType) -> List[DataEntry]:
        """
        Parses a single CSV file and converts each row into a DataEntry.
        Formats the contents generically into Markdown.
        """
        import time
        start_time = time.time()
        file_size = file_path.stat().st_size
        entries = []
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entry = DataLoader._row_to_entry(row, entry_type)
                    if entry:
                        entries.append(entry)
            duration = (time.time() - start_time) * 1000
            logger.debug(f"Parsed {file_path.name} ({file_size/1024:.1f} KB) in {duration:.2f}ms. Found {len(entries)} entries.")
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            
        return entries

    @staticmethod
    def _row_to_entry(row: dict, entry_type: DataEntryType) -> Optional[DataEntry]:
        """
        Converts a CSV row string dictionary into a structured DataEntry.
        """
        name = row.get("Name", "Unknown")
        source = row.get("Source", "Unknown")
        
        # Skip empty rows that somehow got parsed
        if name == "Unknown" and source == "Unknown":
            return None

        # Generate a unique slug ID
        entry_id = f"{entry_type.value.lower()}-{name.lower().replace(' ', '-')}-{source.lower()}"
        
        markdown_lines = []
        # Add Title and Metadata
        markdown_lines.append(f"# {name}")
        markdown_lines.append(f"**Type:** {entry_type.value} | **Source:** {source}")
        markdown_lines.append("---")
        
        # Generically populate remaining existing fields into Markdown
        for key, value in row.items():
            if not key or not value:
                continue
            if key in ("Name", "Source", "id"):
                continue
                
            formatted_val = DataLoader._format_value(value)
            markdown_lines.append(f"**{key}:** {formatted_val}\n")

        content_markdown = "\n".join(markdown_lines)

        return DataEntry(
            id=entry_id,
            name=name,
            type=entry_type,
            source=source,
            content_markdown=content_markdown
        )

    @staticmethod
    def _format_value(value: any) -> str:
        """
        Recursively formats values, handling JSON-like strings and 5etools tags.
        """
        if not value:
            return ""

        import json
        
        # Basic cleanup of 5etools' tags
        def clean_tags(s: str) -> str:
            if not isinstance(s, str): return str(s)
            import re
            # Matches {@tag content|pipe|more} or {@tag content}
            # Simplifies to **content**
            s = re.sub(r'\{@[\w]+ ([^|}]+)[^}]*\}', r'**\1**', s)
            return s

        if isinstance(value, str):
            value_trimmed = value.strip()
            # Try to parse as JSON if it looks like it
            if (value_trimmed.startswith('[') and value_trimmed.endswith(']')) or \
               (value_trimmed.startswith('{') and value_trimmed.endswith('}')):
                try:
                    data = json.loads(value_trimmed)
                    return DataLoader._format_complex_data(data)
                except:
                    pass
            return clean_tags(value)
        
        return str(value)

    @staticmethod
    def _format_complex_data(data: any) -> str:
        """
        Processes lists and dicts from JSON into readable strings.
        """
        if isinstance(data, list):
            items = [DataLoader._format_complex_data(i) for i in data]
            return ", ".join(items) if len(items) < 5 else "\n" + "\n".join([f"- {i}" for i in items])
        
        if isinstance(data, dict):
            # Special D&D data patterns
            # 1. Action/Time: {"number": 1, "unit": "action"}
            if "number" in data and "unit" in data:
                return f"{data['number']} {data['unit']}"
            
            # 2. Range: {"type": "point", "distance": {"type": "feet", "amount": 60}}
            if "distance" in data:
                dist = data["distance"]
                if isinstance(dist, dict) and "amount" in dist:
                    return f"{dist.get('amount', '')} {dist.get('type', '')}"
                return str(dist)

            # 3. Entries/Content: {"type": "entries", "name": "Title", "entries": [...]}
            if "entries" in data:
                header = f"### {data.get('name', '')}\n" if "name" in data else ""
                content = DataLoader._format_complex_data(data["entries"])
                return f"{header}{content}"

            # Generic dict fallback
            parts = []
            for k, v in data.items():
                if k in ("type", "name") and len(data) > 1: continue
                parts.append(f"{k}: {DataLoader._format_complex_data(v)}")
            return "; ".join(parts)

        return str(data)
