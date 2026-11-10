import re

with open("wmn_lab_report_sahana_extended.md", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the YAML frontmatter block at the top
content = re.sub(r'^---.*?---\n+', '', content, flags=re.DOTALL)

# 2. Fix the typo "ewpage" to "\newpage"
content = content.replace('\newpage', '\\newpage')
content = content.replace('ewpage', '\\newpage') # Just in case

# 3. Add the manual INDEX page right after the first \newpage
manual_index = """
# INDEX

**1.** Apply different propagation models and plot the graph for signal strength
**2.** Capture and analyze wireless traffic to understand beacon transmission, spectrum usage, and network telemetry metrics
**3.** Performance Analysis of Active and Passive Wireless Network Scanning
**4.** Simulation and Analysis of Handover Between Wireless Access Points
**5.** Install Open5GS and configure a standalone (SA) 5G Core
**6.** Integrate a software-based gNB with Open5GS and verify NG interface signaling
**7.** Register a UE and establish a PDU session through Open5GS
**8.** Create Multiple S-NSSAI Profiles and Configure Slice-Based Routing
**9.** Deploy a Simple Edge Application Near the UPF and Compare Latency
**10.** Demonstrate Full End-to-End Communication from UE to Internet

\\newpage
"""

# Replace the first \newpage with \newpage + manual_index
content = content.replace('\\newpage', '\\newpage\n' + manual_index, 1)

with open("wmn_lab_report_sahana_extended.md", "w", encoding="utf-8") as f:
    f.write(content)

