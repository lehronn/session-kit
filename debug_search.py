import sys
import os
import logging

sys.path.insert(0, os.path.abspath("."))
logging.basicConfig(level=logging.DEBUG)

from core.config import config_manager
from core.models import AppConfigModel, RulesetVersion, AppLanguage
from data.search import SearchEngine
from data.loader import DataLoader
from pathlib import Path

print(f"Current Config Ruleset: {config_manager.config.active_ruleset}")
print(f"Current Config Lang: {config_manager.config.language}")

engine = SearchEngine()
# Let's see what load_active_ruleset does
engine.load_active_ruleset(config_manager.config)

print(f"Engine entries length: {len(engine._entries)}")

# Test loader directly to a known path
p = Path("data/dnd-50-sdr51-eng")
print(f"Testing direct load of {p} (exists? {p.exists()})")
res = DataLoader.load_directory(p)
print(f"DataLoader returned {len(res)} items from {p}")

