import re

with open("services/ai_vision.py", "r") as f:
    code = f.read()

import_statement = "import json\nimport base64\nimport re"

if "import re" not in code:
    code = code.replace("import json\nimport base64", import_statement)

old_logic = """            if "```" in svg_code:
                svg_code = svg_code.split("```")[1].replace("svg", "", 1).strip()"""

new_logic = """            # Robustly handle markdown wrappers to prevent malformed SVGs
            if "```" in svg_code:
                match = re.search(r"<svg.*?</svg>", svg_code, re.IGNORECASE | re.DOTALL)
                if match:
                    svg_code = match.group(0).strip()
                else:
                    # Fallback string stripping
                    svg_code = svg_code.split("```")[1].strip()
                    for prefix in ["xml", "svg", "html"]:
                        if svg_code.lower().startswith(prefix):
                            svg_code = svg_code[len(prefix):].strip()
                            break"""

code = code.replace(old_logic, new_logic)

with open("services/ai_vision.py", "w") as f:
    f.write(code)

print("SVG parsing robustly fixed.")
