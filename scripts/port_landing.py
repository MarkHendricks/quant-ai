#!/usr/bin/env python3
"""Port the reviewed author-book landing; preserve the shell's local H1."""
import ast
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT.parent / 'ai-models/models/M5_generative_scenarios/book'
source = (BOOK / 'index.md').read_text()
tree = ast.parse((BOOK / 'port_to_canonical.py').read_text())
renames = next(ast.literal_eval(node.value) for node in tree.body
               if isinstance(node, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == 'DISC_RENAMES' for t in node.targets))
for old, new in renames.items():
    source = source.replace(quote(old, safe='-_.,()'), quote(new, safe='-_.,()'))
# raw-HTML tile hrefs end in .html, so the full-name pass above misses them;
# rewrite the URL-encoded stems too (encoded stems occur only inside hrefs)
for old, new in renames.items():
    old_stem, new_stem = old.rsplit('.', 1)[0], new.rsplit('.', 1)[0]
    source = source.replace(quote(old_stem, safe='-_.,()'), quote(new_stem, safe='-_.,()'))
source = source.replace('discussions/', 'discussions/quant_ai/')
destination = ROOT / 'docs/index.md'
heading = '# Quant AI'
frontmatter = '---\ntitle: "Quant AI"\nauthor: "Mark Hendricks"\n---\n\n' 
destination.write_text(frontmatter + heading + '\n' + source.split('\n', 1)[1])
print('Ported authoritative landing to docs/index.md')
