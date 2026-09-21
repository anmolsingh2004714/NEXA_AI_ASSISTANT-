import ast
import importlib
import os
import sys

STD_LIBS = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()

LOCAL_MODULES = {"memory", "thinking", "youtube", "automation", "agent",
                  "main", "iron", "x", "flipkart", "ip_address",
                  "keyboard_mouse_CTRL", "object_detection", "file_search",
                  "image_generate", "image_to_pdf", "memory_interceptor",
                  "diagnose_api"}

missing = set()
checked = set()

for root, dirs, files in os.walk("."):
    if ".venv" in root or "__pycache__" in root or ".git" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    tree = ast.parse(f.read(), filename=path)
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        mod = alias.name.split(".")[0]
                        checked.add(mod)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        mod = node.module.split(".")[0]
                        checked.add(mod)

for mod in sorted(checked):
    if mod in STD_LIBS or mod in LOCAL_MODULES:
        continue
    try:
        importlib.import_module(mod)
    except Exception:
        missing.add(mod)

print("\n=== MISSING MODULES ===")
if missing:
    for m in sorted(missing):
        print(m)
    print("\nInstall command:")
    print("pip install " + " ".join(sorted(missing)))
else:
    print("Koi missing module nahi mila! ✅")