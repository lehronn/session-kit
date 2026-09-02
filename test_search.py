import sys
import os
import time

sys.path.insert(0, os.path.abspath("."))

from core.models import AppConfigModel, RulesetVersion, AppLanguage
from data.search import SearchEngine

config = AppConfigModel(language=AppLanguage.EN, active_ruleset=RulesetVersion.DND50E_SDR)

engine = SearchEngine()
start = time.time()
engine.load_active_ruleset(config)
print(f"Loaded ruleset data in {(time.time() - start)*1000:.2f}ms")

start = time.time()
res = engine.search("Fireball")
print(f"Searched 'Fireball' in {(time.time() - start)*1000:.2f}ms. Found {len(res)} results.")
if res:
    print(f"First result: {res[0].name} ({res[0].type})")
