import re

with open("wmn_lab_report_sahana_extended.md", "r", encoding="utf-8") as f:
    content = f.read()

# Images mapping
images = {
    1: ["exp1.png", "exp1(1).png", "exp1(2).png", "figure1exp1.png", "figure2exp1.png", "figure3exp1.png", "figure5exp1.png"],
    2: ["experiment2.png"],
    3: ["exp3.png", "experiment3.png"],
    4: ["exp4.png"],
    5: ["exp5.png", "exp5(1).png"],
    6: ["exp6.png"],
    7: ["exp7.png", "exp7(1).png"],
    8: ["exp8.png"],
    9: ["exp9.png"],
    10: []
}

# Split content by Experiment to accurately inject images
experiments = re.split(r'(?=# Experiment \d+:)', content)

for i in range(1, 11):
    # Find the chunk for experiment i
    chunk_index = -1
    for j, chunk in enumerate(experiments):
        if chunk.startswith(f"# Experiment {i}:"):
            chunk_index = j
            break
            
    if chunk_index != -1:
        # Remove all existing placeholders in this chunk
        experiments[chunk_index] = re.sub(r'\*\[Paste Figure.*?\]\*', '', experiments[chunk_index])
        
        # Build the image markdown string
        img_md = "\n\n"
        for img in images.get(i, []):
            img_md += f"![Experiment {i} Figure]({img})\n\n"
            
        # Insert images before the conclusion or at the end of results
        # We can append it before '## X.8 Conclusion' or similar
        conclusion_pattern = re.compile(r'(## \d+\.\d+ Conclusion)')
        match = conclusion_pattern.search(experiments[chunk_index])
        if match:
            experiments[chunk_index] = experiments[chunk_index][:match.start()] + img_md + experiments[chunk_index][match.start():]
        else:
            experiments[chunk_index] += img_md

# Rejoin and save
with open("wmn_lab_report_sahana_extended.md", "w", encoding="utf-8") as f:
    f.write("".join(experiments))

