import re

with open("wmn_lab_report_sahana_extended.md", "r", encoding="utf-8") as f:
    content = f.read()

# The new Experiment 1 text based on Assignment1-VishalNaik.pdf
exp1_new = """# Experiment 1: Apply different propagation models and plot the graph for signal strength

## 1.1 Aim
To understand why propagation models are required for wireless communication, apply different propagation models (Friis, Log-Distance, Log-Normal Shadowing, ITU, and Two-Ray Ground) in Mininet-WiFi, and plot the graph for signal strength perceived by a station.

## 1.2 Objectives
* To create a network topology using the Mininet-WiFi emulator with at least one Access Point and two or more stations.
* To apply the 5 standard propagation models to the topology.
* To measure and record the signal strength for each model.
* To plot a graph comparing the recorded signal strengths.

## 1.3 Introduction and Theoretical Background
### Why are Propagation Models Required?
In a virtual emulator like Mininet-WiFi, physical space does not actually exist; nodes are simply software interfaces assigned to virtual X,Y coordinates. A **Propagation Model** acts as the "physics engine" of the simulation.

It provides the mathematical formulas required to calculate how much a wireless signal degrades (attenuates) over a specific virtual distance due to factors like free space, obstacles, and ground reflection. Without a propagation model, a station 1,000 meters away would unrealistically receive the exact same perfect signal as a station 1 meter away, making realistic network simulation impossible.

### The 5 Standard Propagation Models
* **Friis Propagation Loss Model:** Simulates an ideal, obstacle-free environment with a perfect line-of-sight.
* **Log-Distance Propagation Loss Model (Default):** A generalized model that uses a "path loss exponent" to simulate denser environments (like urban areas or offices) where the signal drops faster than in free space.
* **Log-Normal Shadowing Propagation Loss Model:** Builds on the Log-Distance model by adding a random Gaussian variable. This simulates random, unpredictable obstacles (like people moving or foliage).
* **ITU Propagation Loss Model:** An International Telecommunication Union standard specifically formulated for indoor environments and multi-floor building penetration.
* **Two-Ray Ground Propagation Loss Model:** Accounts for two paths: the direct line-of-sight signal and the signal reflecting off the ground. Highly accurate for longer distances.

## 1.4 Creating the Topology
### Designing the Network Topology
**Step 1:** Launch the Mininet-WiFi GUI builder (MiniEdit) from your terminal:
`sudo python3 mininet-wifi/examples/miniedit.py`

**Step 2:** From the left toolbar, drag and drop the following components onto the canvas:
* 1x Controller (`c0`)
* 1x Access Point (`ap1`)
* 4x Stations (`sta1`, `sta2`, `sta3`, `sta4`) - Place them at varying distances from the AP.

**Step 3:** Use the NetLink (Blue Line) tool to create a wired connection between the Controller (`c0`) and the Access Point (`ap1`).

*[Paste Figure: Mininet-WiFi GUI Canvas here]*

## 1.5 Data Collection: Testing the 5 Official Models
We will now apply the 5 official models to the exported topology script (`demo.py`), run it, and record the signal strength at the Mininet prompt using `sta1 iw dev sta1-wlan0 link`.

**Test 1: Friis Model**
Add the following line right above `net.build()`:
`net.setPropagationModel(model="friis", sL=1)`
*Recorded Signal Strength:* -64 dBm

**Test 2: Log-Distance Model**
Change the line to match the official Log-Distance model:
`net.setPropagationModel(model="logDistance", sL=1, exp=3)`
*Recorded Signal Strength:* -75 dBm

**Test 3: Log-Normal Shadowing Model**
Change the line to the official Log-Normal model:
`net.setPropagationModel(model="logNormalShadowing", sL=1, exp=3, variance=2)`
*Recorded Signal Strength:* -78 dBm

**Test 4: ITU Model**
Change the line to the ITU model:
`net.setPropagationModel(model="ITU")`
*Recorded Signal Strength:* -72 dBm

**Test 5: Two-Ray Ground Model**
Change the line to the Two-Ray model:
`net.setPropagationModel(model="twoRayGround")`
*Recorded Signal Strength:* -68 dBm

## 1.6 Results and Analysis
### Plotting the Graph

| Propagation Model | Recorded Signal Strength (dBm) |
| :--- | :--- |
| Friis | -64 |
| Log-Distance | -75 |
| Log-Normal Shadowing | -78 |
| ITU | -72 |
| Two-Ray Ground | -68 |

*[Paste Figure: Propagation Model Comparison Bar Chart here]*

### Key Observations
* **Friis Model:** Displayed the strongest signal (-64 dBm) as it assumes a perfect, obstacle-free environment.
* **Two-Ray Ground:** Showed a slightly lower signal (-68 dBm) as it accounts for ground reflection interference.
* **ITU Model:** Recorded -72 dBm, representing an indoor environment attenuation.
* **Log-Distance & Log-Normal Shadowing:** Displayed the weakest signals (-75 dBm and -78 dBm respectively), accurately reflecting denser environments with higher path loss exponents and unpredictable obstacles.

## 1.7 Conclusion
The experiment successfully demonstrated the application of different propagation models in Mininet-WiFi. By observing the varying signal strengths at a fixed distance across the five models, we validated that propagation models are essential to accurately simulate real-world physical signal attenuation caused by distance, obstacles, and ground reflections.

\newpage
"""

# Replace the content from # Experiment 1 to # Experiment 2
pattern = re.compile(r'# Experiment 1:.*?(?=# Experiment 2:)', re.DOTALL)
new_content = pattern.sub(exp1_new, content)

with open("wmn_lab_report_sahana_extended.md", "w", encoding="utf-8") as f:
    f.write(new_content)
