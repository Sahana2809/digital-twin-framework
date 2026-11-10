with open("wmn_lab_report_sahana_extended.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the accidental \n macro which LaTeX hates
content = content.replace('\\n\\newpage', '\\newpage')

with open("wmn_lab_report_sahana_extended.md", "w", encoding="utf-8") as f:
    f.write(content)
