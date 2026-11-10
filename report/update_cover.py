import re

with open("wmn_lab_report_sahana_extended.md", "r", encoding="utf-8") as f:
    content = f.read()

# Replace HTML img with markdown img for better pandoc compatibility
content = content.replace('<img src="logo.jpg" alt="KLE Logo" width="250"/>', '![KLE Logo](logo.jpg){width=2.5in}')

with open("wmn_lab_report_sahana_extended.md", "w", encoding="utf-8") as f:
    f.write(content)
