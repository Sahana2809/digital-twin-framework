![](media/image1.jpeg){width="6.268055555555556in"
height="1.0118055555555556in"}

**SCHOOL OF COMPUTER SCIENCE AND**

**                          ENGINEERING**

**                                                  Wireless and Mobile
Networks(25ECSC311)**

**Assignment report**

**             ** submitted in partial fulfillment of the requirements
for the award of the degree of

**                                                          Bachelor of 
Engineering**

**                                                                     
       IN**

**                                      Computer Science and
Engineering**

*                                                                  *

*Submitted by*

***                                                  **Chinmayi P Hosur 
  01FE23BCS262*

                                                     

   Under the Guidance of 

                                                             Prof. Vidya
S H

                                       School of Computer Science and
Engineering

                                          KLE Technological University,
Hubballi

                                                                 2025 --
2026

**Assignment 1 : Wireless Network Simulation Using Different Propagation
Models**

**Aim**

To configure a wireless network simulation using different propagation
models such as Free Space, Two-Ray Ground, and Log-Distance, and analyze
their impact on interference levels, mobility behavior, and link
aggregation performance.

**Objective**

- To study the characteristics of various wireless propagation models.

- To compare signal propagation under different environmental
  conditions.

- To observe the effect of propagation models on network interference.

- To analyze mobility model performance under varying propagation
  conditions.

- To evaluate link aggregation performance in wireless networks.

**Introduction**

Wireless communication systems rely on radio wave propagation to
establish communication between network devices. The propagation model
defines how signals travel through the wireless medium and how signal
strength decreases with distance. Different propagation models represent
different real-world environments and significantly affect network
performance.

In wireless network simulations, propagation models are used to estimate
signal attenuation, coverage area, interference, and communication
reliability. Understanding these models is essential for designing
efficient wireless networks and optimizing network resources.

This experiment investigates three commonly used propagation models:

**1. Free Space Propagation Model**

The Free Space model assumes a clear line-of-sight path between the
transmitter and receiver with no obstacles, reflections, or
interference. It is suitable for ideal communication environments and
generally provides the highest received signal strength.

**2. Two-Ray Ground Propagation Model**

The Two-Ray Ground model considers both the direct path and the
ground-reflected path of the transmitted signal. It provides more
realistic results for outdoor environments and is widely used in
wireless network simulations.

**3. Log-Distance Propagation Model**

The Log-Distance model estimates signal attenuation using a path-loss
exponent that varies according to the environment. It is commonly used
to model urban, suburban, and indoor communication scenarios where
obstacles cause signal degradation.

**Software Requirements**

- Ubuntu Linux

- Mininet-WiFi

- Python

- Open vSwitch

- Matplotlib (optional for visualization)

**Procedure**

**Step 1: Create Wireless Nodes**

Configure multiple wireless stations and an access point within the
simulation environment.

**Step 2: Apply Different Propagation Models**

Execute the simulation using:

- Free Space Model

- Two-Ray Ground Model

- Log-Distance Model

**Step 3: Configure Mobility**

Implement node mobility using a suitable mobility model such as Random
Waypoint.

**Step 4: Generate Traffic**

Establish communication between stations and generate network traffic
using tools such as iperf.

**Step 5: Observe Network Parameters**

Monitor:

- Signal strength

- Throughput

- Packet loss

- Delay

- Interference effects

**Step 6: Evaluate Link Aggregation**

Analyze bandwidth utilization and communication efficiency when multiple
links are aggregated.

**Observations**

  --------------------------------
  **Propagation   **Interference
  Model**         Level**
  --------------- ----------------
  Free Space      Low

  Two-Ray Ground  Moderate

  Log-Distance    High
  --------------------------------

The Free Space model exhibits minimal interference due to ideal
line-of-sight communication. Two-Ray Ground introduces additional signal
reflections, while Log-Distance experiences greater attenuation and
interference due to environmental effects.

**Impact on Mobility Behavior**

  ----------------------------------
  **Propagation   **Mobility
  Model**         Performance**
  --------------- ------------------
  Free Space      Stable
                  connectivity

  Two-Ray Ground  Moderate
                  fluctuations

  Log-Distance    Frequent signal
                  variations
  ----------------------------------

Node movement affects communication quality differently across
propagation models. Log-Distance shows significant signal variation as
nodes move farther from the access point.

**Impact on Link Aggregation Performance**

  ---------------------------------
  **Propagation   **Aggregation
  Model**         Efficiency**
  --------------- -----------------
  Free Space      Highest

  Two-Ray Ground  Moderate

  Log-Distance    Lowest
  ---------------------------------

Free Space propagation provides the best throughput and bandwidth
utilization due to lower signal loss. Log-Distance propagation reduces
aggregation efficiency because of increased attenuation and packet
retransmissions.

**Results**

The simulation successfully demonstrated the influence of different
propagation models on wireless network performance. Free Space
propagation achieved the best overall performance with minimal
interference and maximum throughput. Two-Ray Ground provided more
realistic outdoor behavior, while Log-Distance represented practical
environments with greater signal attenuation and reduced network
efficiency.

![](media/image2.png){width="4.855575240594925in"
height="2.6166666666666667in"}

**Figure 1: Signal Strength Comparison for Different Wireless
Propagation Models**

**Conclusion**

The experiment demonstrated that propagation models play a crucial role
in determining wireless network performance. Free Space propagation
offers ideal communication conditions, whereas Two-Ray Ground and
Log-Distance models provide more realistic representations of real-world
environments. The results show that increased signal attenuation and
environmental effects lead to higher interference levels, reduced
mobility performance, and lower link aggregation efficiency. Therefore,
selecting an appropriate propagation model is essential for accurate
wireless network design and performance evaluation.

**Assignment 2 : Wireless Traffic Analysis for Beacon Transmission,
Spectrum Usage, and Network Telemetry**

**Aim**

To capture and analyze wireless network traffic in order to study beacon
transmissions, evaluate spectrum utilization, and monitor network
telemetry metrics.

**Objective**

- To understand the role of beacon frames in wireless communication.

- To analyze wireless spectrum usage and channel occupancy.

- To monitor network telemetry metrics such as throughput, latency,
  packet loss, and signal strength.

- To gain practical experience in wireless packet capture and analysis.

**Introduction**

Wireless networks continuously exchange management, control, and data
frames to maintain communication between devices. Monitoring and
analyzing these transmissions is essential for understanding network
behavior, diagnosing performance issues, and optimizing wireless
communication.

Beacon frames are periodically transmitted by access points to announce
the presence of a wireless network. They contain important information
such as the Service Set Identifier (SSID), supported data rates, channel
information, and timing synchronization data.

Spectrum analysis helps identify channel utilization, interference, and
congestion within the wireless environment. Network telemetry provides
valuable performance metrics that enable administrators to monitor
network health and efficiency.

This experiment focuses on capturing wireless traffic and analyzing
beacon transmissions, spectrum usage patterns, and network telemetry
parameters.

**Software Requirements**

- Ubuntu Linux

- Wireshark

- Mininet-WiFi

- Python

- Wireless Network Interface Card (Monitor Mode Support)

**Theory**

**Beacon Frames**

Beacon frames are management frames periodically transmitted by wireless
access points. They provide:

- Network identification (SSID)

- Supported transmission rates

- Channel information

- Security capabilities

- Synchronization information

Beacon frames enable wireless devices to discover and connect to
available networks.

**Spectrum Usage Analysis**

Spectrum usage analysis involves monitoring wireless channels to
determine:

- Channel occupancy

- Signal strength distribution

- Interference levels

- Frequency utilization

Efficient spectrum management improves network performance and reduces
communication delays.

**Procedure**

**Step 1: Configure Wireless Network**

Create a wireless network topology consisting of stations and an access
point.

**Step 2: Enable Traffic Capture**

Launch Wireshark and configure the wireless interface in monitor mode.

**Step 3: Capture Wireless Frames**

Start packet capture and generate wireless traffic between stations.

**Step 4: Analyze Beacon Frames**

Filter captured packets using:

wlan.fc.type_subtype == 8

Observe:

- SSID

- Channel Number

- Beacon Interval

- Supported Rates

**Step 5: Analyze Spectrum Usage**

Monitor channel utilization and signal activity across different
frequencies.

**Step 6: Collect Telemetry Metrics**

Record:

- Throughput

- Delay

- Packet Loss

- Signal Strength

- Channel Occupancy

**Step 7: Document Observations**

Compare network behavior under varying traffic loads and channel
conditions.

**Observations**

**Beacon Transmission Analysis**

  --------------------------------------
  **Parameter**   **Observation**
  --------------- ----------------------
  Beacon Interval Periodic transmission
                  observed

  SSID Broadcast  Successfully detected

  Channel         Available in beacon
  Information     frames

  Network         Successful
  Discovery       
  --------------------------------------

Beacon frames were transmitted at regular intervals, allowing stations
to discover and synchronize with the wireless network.

**Spectrum Usage Analysis**

  ---------------------------------
  **Metric**      **Observation**
  --------------- -----------------
  Channel         Moderate
  Occupancy       

  Signal Activity Continuous

  Interference    Low to Moderate

  Frequency       Efficient
  Utilization     
  ---------------------------------

Spectrum monitoring revealed active channel utilization with occasional
interference from neighboring transmissions.

**Network Telemetry Analysis**

  ---------------------------------
  **Metric**      **Observation**
  --------------- -----------------
  Throughput      Stable

  Latency         Low

  Packet Loss     Minimal

  Signal Strength Consistent

  Channel         Moderate
  Utilization     
  ---------------------------------

Telemetry metrics indicated stable network performance under normal
operating conditions.

**Results**

Wireless traffic was successfully captured and analyzed. Beacon frame
transmissions were observed periodically, enabling network discovery and
synchronization. Spectrum analysis revealed channel utilization patterns
and interference levels, while telemetry metrics provided insights into
network performance and reliability.

![](media/image3.png){width="6.493784995625547in"
height="3.6523632983377077in"}

**Figure 2: *Wireless traffic analysis dashboard in Mininet-WiFi
illustrating beacon transmissions, RSSI trends, throughput, latency,
spectrum utilization, and wireless frame distribution.***

**Conclusion**

The experiment successfully demonstrated wireless traffic analysis
techniques for beacon transmission, spectrum usage, and network
telemetry monitoring. Beacon frames played a crucial role in network
discovery and synchronization. Spectrum analysis provided valuable
information regarding channel occupancy and interference, while
telemetry metrics helped evaluate network performance. These analyses
are essential for efficient wireless network management and
optimization.

**Assignment 3 : Performance Analysis of Active and Passive Wireless
Network Scanning**

**Aim**

To configure a wireless client device for Active Scanning and Passive
Scanning and compare their performance in terms of discovery time, power
consumption, and network response.

**Objective**

- To understand the working principles of active and passive wireless
  scanning.

- To configure a wireless client for both scanning techniques.

- To measure network discovery time under different scanning methods.

- To analyze power consumption during the scanning process.

- To evaluate network response and efficiency.

**Introduction**

Wireless devices must discover available networks before establishing
communication. This discovery process is performed using scanning
mechanisms. The IEEE 802.11 standard defines two primary methods of
network discovery: Active Scanning and Passive Scanning.

In Active Scanning, the client device actively broadcasts Probe Request
frames and waits for Probe Responses from nearby access points. This
method provides faster network discovery but consumes more power.

In Passive Scanning, the client device listens for periodic Beacon
frames transmitted by access points without transmitting any requests.
This approach reduces power consumption but generally results in longer
discovery times.

Understanding the trade-offs between these scanning techniques is
essential for optimizing wireless network performance, particularly in
mobile and battery-powered devices.

**Procedure**

**Step 1: Configure Wireless Topology**

Create a wireless network consisting of:

- One Access Point

- One Wireless Client Station

**Step 2: Configure Active Scanning**

Enable active scanning on the client device and capture:

- Probe Requests

- Probe Responses

- Discovery time

**Step 3: Configure Passive Scanning**

Enable passive scanning and monitor:

- Beacon Frames

- Discovery delay

- Network information collection

**Step 4: Capture Traffic**

Use Wireshark to analyze:

- Probe Requests

- Probe Responses

- Beacon Frames

**Step 5: Measure Performance**

Record:

- Discovery Time

- Power Consumption

- Network Response Time

**Step 6: Compare Results**

Analyze the performance differences between both scanning techniques.

**Observations**

**Discovery Time Comparison**

  ---------------------------
  **Scanning    **Discovery
  Method**      Time**
  ------------- -------------
  Active        Low
  Scanning      

  Passive       High
  Scanning      
  ---------------------------

Active scanning discovers available networks more quickly because the
client actively requests network information.

**Power Consumption Comparison**

  -----------------------------
  **Scanning    **Power
  Method**      Consumption**
  ------------- ---------------
  Active        High
  Scanning      

  Passive       Low
  Scanning      
  -----------------------------

Active scanning consumes more power due to frequent transmission of
probe requests.

**Network Response Comparison**

  ----------------------------
  **Scanning    **Network
  Method**      Response**
  ------------- --------------
  Active        Immediate
  Scanning      

  Passive       Delayed
  Scanning      
  ----------------------------

Active scanning receives direct responses from access points, resulting
in faster network identification.

**Results**

The wireless client successfully performed both active and passive
scanning operations. Active scanning achieved faster network discovery
and quicker access point responses, while passive scanning demonstrated
lower power consumption and reduced network overhead.
![](media/image4.png){width="6.268055555555556in"
height="3.2597222222222224in"}

**Figure 3: *Comparative analysis of Active and Passive scanning
mechanisms in a wireless network. Metrics evaluated include discovery
time, power consumption, and network response time. Active scanning
demonstrates superior responsiveness at the cost of increased energy
usage, whereas passive scanning provides improved power efficiency with
higher discovery latency.***

**Conclusion**

The experiment successfully demonstrated the operation of active and
passive wireless scanning techniques. Active scanning provided faster
discovery and immediate network responses at the expense of higher power
consumption. Passive scanning reduced energy usage and channel traffic
but required longer network discovery times. The choice between the two
methods depends on application requirements, device mobility, and power
constraints.

**Assignment 4 : Simulation and Analysis of Handover Between Wireless
Access Points**

**Aim**

To simulate a mobile node moving between two access points (APs) or base
stations and observe the handover process in a wireless network.

**Objective**

- To understand the concept of wireless handover.

- To simulate mobility between two wireless coverage areas.

- To observe connectivity changes during movement.

- To analyze packet transmission before, during, and after handover.

- To evaluate the impact of handover on network performance.

**Introduction**

In wireless communication networks, mobile devices frequently move
between different coverage areas. To maintain uninterrupted
connectivity, the network performs a process known as handover (or
handoff), where the connection is transferred from one access point or
base station to another.

Handover is a critical feature in Wi-Fi, cellular, and 5G networks,
enabling seamless communication for mobile users. During handover, the
device disconnects from the current access point and establishes a
connection with a stronger or more suitable access point.

This experiment demonstrates the handover process by simulating a mobile
node moving from the coverage area of one access point to another and
observing the associated network behavior.

**Procedure**

**Step 1: Create Network Topology**

Configure:

- Two Access Points (AP1 and AP2)

- One Mobile Station (STA1)

**Step 2: Configure Coverage Areas**

Assign different positions and transmission ranges to AP1 and AP2.

**Step 3: Enable Mobility**

Configure STA1 to move from AP1 coverage toward AP2 coverage.

**Step 4: Start Communication**

Generate continuous traffic using:

- Ping

- Iperf

**Step 5: Monitor Connectivity**

Observe:

- Association status

- Signal strength

- Packet transmission

**Step 6: Capture Handover Events**

Record:

- AP disassociation

- AP reassociation

- Packet delay

- Temporary packet loss

**Step 7: Analyze Results**

Compare connectivity before, during, and after handover.

**Observations**

**Mobile Node Behavior**

  --------------------------
  **Stage**    **Connected
               AP**
  ------------ -------------
  Initial      AP1
  Position     

  Transition   AP1/AP2
  Zone         

  Final        AP2
  Position     
  --------------------------

The mobile station initially communicates through AP1 and later
associates with AP2 as it moves into the second coverage area.

**Signal Strength Analysis**

  ---------------------------
  **Location**   **Signal
                 Strength**
  -------------- ------------
  Near AP1       Strong

  Midpoint       Moderate

  Near AP2       Strong
  ---------------------------

Signal strength gradually decreases from AP1 and increases as the node
approaches AP2.

**Network Performance During Handover**

  ---------------------------------
  **Parameter**   **Observation**
  --------------- -----------------
  Connectivity    Maintained

  Packet Loss     Minimal

  Delay           Slight Increase

  Throughput      Temporary
                  Reduction
  ---------------------------------

A brief performance degradation was observed during the handover process
due to reassociation overhead.

**Handover Analysis**

**Before Handover**

- Strong connection with AP1.

- Stable throughput.

- Low latency.

**During Handover**

- Signal from AP1 weakens.

- Device scans for alternative AP.

- Reassociation occurs.

- Temporary increase in delay.

**After Handover**

- Successful connection to AP2.

- Throughput stabilizes.

- Communication continues normally.

**Results**

The mobile node successfully transitioned from AP1 to AP2 while
maintaining network connectivity. The handover process resulted in a
brief increase in latency and a small reduction in throughput, but
communication resumed normally after reassociation with the new access
point.

**Observations from Figure 4 below**

- **RSSI: AP1 signal strength decreases from −35 dBm to −88 dBm, while
  AP2 increases from −90 dBm to −35 dBm, indicating successful
  handover.**

- **Throughput: Drops from approximately 52 Mbps to 30 Mbps during
  handover and recovers to 50 Mbps after reassociation.**

- **Latency: Increases from 2 ms to 12 ms during handover due to
  scanning and reassociation procedures.**

- **Packet Loss: Remains very low before and after handover but
  temporarily rises to 3.5% during the transition.**

- **Connectivity: The mobile station maintains connectivity throughout
  the movement, demonstrating a successful horizontal handover between
  AP1 and AP2.**

![](media/image5.png){width="6.425062335958005in"
height="4.186994750656168in"}

**Fig 4:** ***Handover analysis in Mininet-WiFi showing RSSI variation,
throughput, latency, and packet loss before, during, and after the
transition from AP1 to AP2.***

**Conclusion**

The experiment successfully demonstrated the wireless handover process
between two access points. As the mobile node moved between coverage
areas, the network performed a seamless transfer of connectivity from
AP1 to AP2. The results show that handover mechanisms are essential for
maintaining uninterrupted communication in mobile wireless networks and
play a crucial role in Wi-Fi and modern cellular systems such as 4G and
5G.

**Assignment 5 :Installation and Configuration of Open5GS Standalone
(SA) 5G Core Network**

**Aim**

To install Open5GS and configure a Standalone (SA) 5G Core Network, and
verify the successful operation of key network functions such as the
Access and Mobility Management Function (AMF), Session Management
Function (SMF), and User Plane Function (UPF).

**Objective**

- To understand the architecture of a 5G Standalone Core Network.

- To install and configure Open5GS.

- To deploy and verify core network functions.

- To analyze the role of AMF, SMF, and UPF in 5G communication.

- To validate successful operation of the 5G Core.

**Introduction**

Fifth Generation (5G) mobile networks introduce a cloud-native core
architecture designed to support enhanced mobile broadband,
ultra-reliable low-latency communication, and massive machine-type
communication. Unlike Non-Standalone (NSA) deployments that depend on
LTE infrastructure, Standalone (SA) 5G networks operate independently
using a dedicated 5G Core (5GC).

Open5GS is an open-source implementation of the 5G Core Network. It
provides all major network functions required for a standalone
deployment, enabling researchers and students to experiment with
real-world 5G technologies.

In this experiment, Open5GS was installed and configured to establish a
standalone 5G Core Network. The functionality of critical network
functions including AMF, SMF, and UPF was verified.

**Theory**

**5G Core Architecture**

The 5G Core consists of multiple service-based network functions that
communicate through standardized interfaces.

**Access and Mobility Management Function (AMF)**

The AMF is responsible for:

- UE registration

- Mobility management

- Authentication procedures

- Connection management

**Session Management Function (SMF)**

The SMF manages:

- PDU session establishment

- IP address allocation

- Session control policies

- UPF selection

**User Plane Function (UPF)**

The UPF handles:

- User data forwarding

- Packet routing

- Traffic enforcement

- Internet connectivity

Together, these functions provide complete control and user plane
services for the 5G network.

**Software Requirements**

- Ubuntu Linux

- Docker

- Kubernetes (K8s)

- Open5GS

- UERANSIM

- MongoDB

- kubectl

**Procedure**

**Step 1: Install Prerequisites**

Install:

- Docker

- Kubernetes

- MongoDB

- Open5GS components

**Step 2: Deploy Open5GS**

Deploy Open5GS network functions using Kubernetes manifests.

**Step 3: Verify Pod Creation**

Execute:

kubectl get pods -n open5gs

Verify that all network function pods are running.

**Step 4: Check AMF Status**

Execute:

kubectl logs \<amf-pod-name\> -n open5gs

Confirm successful AMF initialization.

**Step 5: Check SMF Status**

Execute:

kubectl logs \<smf-pod-name\> -n open5gs

Verify successful session management service startup.

**Step 6: Check UPF Status**

Execute:

kubectl logs \<upf-pod-name\> -n open5gs

Ensure the UPF is operational and ready to process user traffic.

**Step 7: Verify Core Services**

Execute:

kubectl get pods -n open5gs

**Step 8: Validate Connectivity**

Attach a UE using UERANSIM and verify successful registration with the
5G Core.

**Observations**

The Open5GS Standalone (SA) 5G Core Network was successfully deployed
and all required network functions started without errors. Verification
using Kubernetes commands confirmed that the AMF, SMF, UPF, and
supporting functions such as NRF, AUSF, UDM, UDR, NSSF, and PCF were in
the running state.

The Access and Mobility Management Function (AMF) was able to initialize
correctly and was ready to handle user equipment (UE) registration and
mobility management procedures. The Session Management Function (SMF)
successfully managed session establishment and allocation of network
resources for connected users.

The User Plane Function (UPF) was operational and capable of forwarding
user traffic between the radio access network and external data
networks. Log analysis showed successful communication between core
network components, indicating proper service-based architecture
operation.

Overall, the successful deployment and verification of the AMF, SMF, and
UPF confirmed that the Open5GS Standalone 5G Core was functioning
correctly and was ready to support UE registration, session
establishment, and data communication.

**Results**

Open5GS was successfully installed and configured as a Standalone 5G
Core Network. All major network functions, including AMF, SMF, and UPF,
were deployed successfully and operated without errors. The system was
able to support UE registration and session establishment.

![](media/image6.png){width="6.268055555555556in"
height="2.5303029308836393in"}

**Figure 5:** *Kubernetes pod status of the Open5GS 5G Core deployment
showing all core network functions and UE/RAN simulator components
running successfully in the open5gs namespace.*

**Conclusion**

The experiment successfully demonstrated the deployment and verification
of an Open5GS Standalone 5G Core Network. Core network functions such as
AMF, SMF, and UPF were configured and validated successfully. The
results confirm that Open5GS provides a practical platform for
implementing and studying modern 5G Core Network architectures.

**Assignment 6 : Integration of UERANSIM gNB with Open5GS and
Verification of NG Interface Signaling**

**Aim**

To integrate a software-based gNB (UERANSIM) with the Open5GS Standalone
5G Core Network and verify NG interface signaling between the Radio
Access Network (RAN) and the Core Network.

**Objective**

- To understand the role of a gNB in a 5G network.

- To configure and deploy a software-based gNB using UERANSIM.

- To establish communication between the gNB and Open5GS.

- To verify NG interface signaling using NGAP messages.

- To observe successful UE registration through the integrated network.

**Introduction**

The Next Generation NodeB (gNB) is the base station used in 5G networks
that provides radio connectivity between User Equipment (UE) and the 5G
Core Network (5GC). In a Standalone (SA) 5G deployment, the gNB
communicates directly with the core network through the NG interface.

UERANSIM is an open-source software that emulates both the gNB and UE
components of a 5G network. It is widely used for testing and research
purposes because it enables the simulation of a complete 5G environment
without requiring physical radio hardware.

In this experiment, a software-based gNB was configured using UERANSIM
and integrated with the Open5GS Standalone 5G Core Network. The NG
interface was verified by observing signaling messages exchanged between
the gNB and the Access and Mobility Management Function (AMF).

**Theory**

**gNB (Next Generation NodeB)**

The gNB serves as the radio access node in a 5G network. Its primary
functions include:

- Radio resource management

- UE connectivity management

- Data transmission and reception

- Communication with the 5G Core

**NG Interface**

The NG interface connects the gNB with the 5G Core Network. It consists
of:

**NG-C (Control Plane)**

Used for signaling communication between the gNB and AMF through NGAP
(NG Application Protocol).

**NG-U (User Plane)**

Used for user data transfer between the gNB and UPF through GTP-U
tunnels.

**Procedure**

**Step 1: Start Open5GS Core Network**

Deploy and verify all Open5GS network functions.

kubectl get pods -n open5gs

Ensure that AMF, SMF, UPF, and other services are running.

**Step 2: Configure UERANSIM gNB**

Edit the gNB configuration file:

nano open5gs-gnb.yaml

Configure:

- MCC

- MNC

- TAC

- AMF Address

- gNB ID

**Step 3: Start the gNB**

Execute:

./nr-gnb -c open5gs-gnb.yaml

The gNB attempts to establish communication with the AMF through the NG
interface.

**Step 4: Verify NG Setup**

Observe the gNB logs and confirm:

- NG Setup Request Sent

- NG Setup Response Received

**Step 5: Configure the UE**

Edit the UE configuration file:

nano open5gs-ue.yaml

Configure:

- IMSI

- MCC

- MNC

- Authentication Credentials

**Step 6: Start the UE**

Execute:

./nr-ue -c open5gs-ue.yaml

**Step 7: Observe Registration**

Verify that the UE successfully registers with the Open5GS Core through
the gNB.

**Step 8: Analyze Signaling Messages**

Check logs from:

- UERANSIM gNB

- UERANSIM UE

- Open5GS AMF

Observe:

- NG Setup Procedure

- Registration Request

- Registration Accept

- PDU Session Establishment

**Observations**

The UERANSIM gNB was successfully configured and connected to the
Open5GS Standalone 5G Core Network. After startup, the gNB initiated
communication with the AMF and completed the NG Setup procedure
successfully. The exchange of NG Setup Request and NG Setup Response
messages confirmed the establishment of the NG interface.

The configured UE connected to the gNB and initiated the registration
procedure. During this process, NGAP signaling messages were exchanged
between the gNB and the AMF. The logs indicated successful transmission
of registration-related messages and authentication procedures.

The AMF successfully processed the registration request and accepted the
UE into the network. Subsequent signaling messages confirmed that the UE
had established communication with the core network through the gNB.

The successful exchange of NGAP messages demonstrated proper operation
of the control plane between the Radio Access Network and the 5G Core.
The integration validated that the gNB, UE, and Open5GS core components
were functioning together as a complete Standalone 5G network.

**Results**

The software-based UERANSIM gNB was successfully integrated with the
Open5GS Standalone 5G Core Network. The NG interface was established
successfully, and NGAP signaling messages were exchanged between the gNB
and AMF. The UE completed registration through the gNB, confirming
successful communication between the Radio Access Network and the Core
Network.

![](media/image6.png){width="6.268055555555556in"
height="4.0055555555555555in"}

**Figure 6:** *Verification of the Open5GS 5G Core deployment using the
kubectl get pods -n open5gs command. The output confirms that all core
network functions, including AMF, AUSF, NRF, NSSF, PCF, SCP, SMF, UDM,
UDR, UPF, and WebUI, are in the **Running** state with no restarts.
Additionally, the simulated gNB and UE pods are operational, indicating
successful deployment and healthy operation of the containerized 5G
network environment.*

**Conclusion**

The experiment successfully demonstrated the integration of a
software-based gNB with the Open5GS 5G Core Network. The NG interface
was established successfully, and the exchange of NGAP signaling
messages verified proper communication between the gNB and AMF. The
successful registration of the UE confirmed the correct operation of the
integrated Standalone 5G network and highlighted the importance of NG
interface signaling in 5G communication.

**Assignment 7 :UE Registration and PDU Session Establishment Using
Open5GS**

**Aim**

To register a User Equipment (UE) with the Open5GS Standalone 5G Core
Network and establish a PDU session for data communication.

**Objective**

- To understand the UE registration procedure in a 5G network.

- To configure a UE using UERANSIM.

- To perform successful UE registration with the Open5GS Core.

- To establish a PDU session through the 5G Core Network.

- To verify IP address allocation and user-plane connectivity.

**Introduction**

In a 5G Standalone (SA) network, a User Equipment (UE) must first
register with the 5G Core before accessing network services. During the
registration process, the network authenticates the UE, verifies
subscription information, and establishes a secure connection.

After successful registration, the UE requests a Protocol Data Unit
(PDU) session. A PDU session provides connectivity between the UE and
external data networks, enabling services such as internet access and
application communication. The Session Management Function (SMF) manages
session establishment, while the User Plane Function (UPF) forwards user
data packets.

In this experiment, a UE was registered with the Open5GS 5G Core
Network, and a PDU session was established to enable data communication.

**Procedure**

**Step 1: Verify Open5GS Core Network**

Ensure all core network functions are running:

kubectl get pods -n open5gs

**Step 2: Add Subscriber Information**

Configure subscriber details in Open5GS:

- IMSI

- Authentication Key

- OPC

- DNN/APN

**Step 3: Configure UE**

Edit the UE configuration file:

nano open5gs-ue.yaml

Configure:

- IMSI

- MCC

- MNC

- Authentication credentials

**Step 4: Start the gNB**

Launch the UERANSIM gNB:

./nr-gnb -c open5gs-gnb.yaml

**Step 5: Start the UE**

Launch the UE:

./nr-ue -c open5gs-ue.yaml

**Step 6: Observe Registration**

Monitor logs for:

- Registration Request

- Authentication

- Registration Accept

**Step 7: Establish PDU Session**

Observe:

- PDU Session Establishment Request

- PDU Session Establishment Accept

**Step 8: Verify IP Address Allocation**

Check whether the UE receives an IP address from the Open5GS network.

**Step 9: Verify Connectivity**

Test communication using:

ping 8.8.8.8

or

curl google.com

**Observations**

The Open5GS core network was running successfully, and the subscriber
information was configured correctly in the database. After starting the
gNB and UE, the UE initiated the registration procedure with the 5G Core
Network.

The AMF processed the registration request and successfully
authenticated the UE using the subscriber credentials. Registration
acceptance messages were observed in both the UE and AMF logs,
confirming successful attachment to the network.

Following registration, the UE requested the establishment of a PDU
session. The SMF processed the request and coordinated with the UPF to
create the user-plane connection. A PDU Session Establishment Accept
message was received, indicating successful session creation.

The UE was assigned an IP address by the network, confirming successful
session establishment. Connectivity tests showed that user traffic was
routed through the UPF, demonstrating proper operation of the control
plane and user plane functions.

Overall, the successful UE registration and PDU session establishment
verified that the Open5GS Standalone 5G Core Network was functioning
correctly and capable of supporting user communication services.

**Results**

The UE successfully registered with the Open5GS Standalone 5G Core
Network and established a PDU session. The network authenticated the UE,
assigned an IP address, and enabled user-plane communication through the
UPF, confirming successful end-to-end connectivity.

![](media/image7.png){width="6.268055555555556in"
height="3.6458333333333335in"}

***Figure 7: Open5GS Subscriber Profile Showing IMSI and Authentication
Parameters***

![](media/image8.png){width="6.268055555555556in" height="3.85in"}

***Figure 8: ICMP Ping Test to 8.8.8.8 Demonstrating Successful UE
Registration and PDU Session Connectivity Through the Open5GS 5G Core
Network***

**Conclusion**

The experiment successfully demonstrated the UE registration procedure
and PDU session establishment in a Standalone 5G network using Open5GS.
The AMF handled registration and authentication, while the SMF and UPF
established and managed the user data session. The successful allocation
of an IP address and verification of connectivity confirmed the proper
operation of the 5G Core Network.

**Assignment 8 : Creation of Multiple S-NSSAI Profiles and Configuration
of Slice-Based Routing in Open5GS**

**Aim**

To create multiple S-NSSAI profiles in Open5GS and configure slice-based
routing to provide isolated network services for different user
equipments (UEs).

**Objective**

- To understand the concept of Network Slicing in 5G networks.

- To create multiple network slices using different S-NSSAI profiles.

- To configure subscribers for different slices.

- To establish slice-specific routing using dedicated UPFs.

- To verify traffic isolation between network slices.

**Introduction**

Network Slicing is one of the most important features introduced in 5G
networks. It enables a single physical network infrastructure to be
divided into multiple logical networks called slices. Each slice is
designed to support specific service requirements such as enhanced
Mobile Broadband (eMBB), Ultra-Reliable Low-Latency Communication
(URLLC), and Massive Machine-Type Communication (mMTC).

A Network Slice Selection Assistance Information (S-NSSAI) uniquely
identifies a slice using two parameters:

- Slice/Service Type (SST)

- Slice Differentiator (SD)

In this experiment, two different slices were configured:

- Slice 1: Internet Service

- Slice 2: Video Streaming Service

Separate subscribers were assigned to each slice, and slice-based
routing was implemented to ensure that traffic from each UE was directed
through the appropriate User Plane Function (UPF).

**Theory**

**Network Slicing**

Network slicing allows operators to create multiple virtual networks
over a common physical infrastructure. Each slice can have its own:

- Quality of Service (QoS)

- Routing policies

- Security policies

- Network resources

**S-NSSAI**

S-NSSAI uniquely identifies a network slice.

**SST (Slice/Service Type)**

Defines the type of service offered by the slice.

**SD (Slice Differentiator)**

Distinguishes slices having the same SST.

**Slice-Based Routing**

Slice-based routing ensures that traffic belonging to a particular slice
is routed through its designated UPF. This provides logical isolation
between services and improves resource management.

**Procedure**

**Step 1: Access Open5GS WebUI**

Open the Open5GS dashboard and log in using administrator credentials.

**Step 2: Create Subscriber for Slice 1**

Configure:

- IMSI: 001010000000001

- SST: 1

- SD: 000001

- DNN: internet

Save the subscriber profile.

**Step 3: Create Subscriber for Slice 2**

Configure:

- IMSI: 001010000000002

- SST: 2

- SD: 000002

- DNN: streaming

Save the subscriber profile.

**Step 4: Restart UEs**

Delete and recreate the UE pods to apply the new subscriber
configurations.

**Step 5: Verify UE Registration**

Check that both UEs successfully register with the Open5GS Core Network.

**Step 6: Configure Slice-Based Routing**

Associate:

- Slice 1 → UPF1

- Slice 2 → UPF2

**Step 7: Capture Traffic on UPF2**

Use tcpdump to monitor traffic on the UPF associated with Slice 2.

**Step 8: Generate Traffic**

Initiate traffic from UE2 by performing a ping test to an external
network.

**Step 9: Verify Traffic Isolation**

Observe packet flow through UPF2 and confirm that UE2 traffic is routed
through the correct slice.

**Observations**

Two subscriber profiles were successfully created using different
S-NSSAI values. The first subscriber was assigned to Slice 1 with SST 1
and SD 000000 for internet services, while the second subscriber was
assigned to Slice 2 with SST 2 and SD 000001 for streaming services.

Both UEs successfully registered with the Open5GS Core Network after
restarting the UERANSIM instances. The registration process confirmed
that the network recognized the slice information configured for each
subscriber.

Traffic monitoring on the UPF associated with Slice 2 showed packet
transmission when UE2 generated network traffic. The captured packets
confirmed that traffic from UE2 was routed through the dedicated UPF
configured for Slice 2.

The observed packet flow demonstrated successful traffic isolation
between slices. Each subscriber accessed network resources through its
designated slice without interfering with traffic belonging to other
slices.

The experiment verified that Open5GS successfully supports multiple
S-NSSAI profiles and slice-based routing, enabling differentiated
services within the same 5G infrastructure.

**Results**

Multiple S-NSSAI profiles were successfully created and configured in
Open5GS. Two separate network slices were established, and traffic from
each subscriber was routed through the designated UPF. The successful
packet capture on UPF2 confirmed proper slice-based routing and traffic
isolation.

![](media/image9.png){width="5.6052285651793525in"
height="2.3114391951006126in"}

***Fig. 9. Open5GS WebUI with two subscriber records added to the
database, enabling multiple UEs to register and establish PDU sessions
through the 5G core network.***

**Conclusion**

The experiment successfully demonstrated the implementation of network
slicing using Open5GS. Multiple S-NSSAI profiles were created and
assigned to different subscribers, enabling the formation of separate
logical networks. Traffic generated by each UE was routed through the
appropriate UPF, confirming successful slice-based routing and service
isolation. The results highlight the flexibility of 5G network slicing
in supporting diverse applications and service requirements.

**Assignment 9 : Deployment of an Edge Application Near the UPF and
Latency Comparison with Cloud-Based Hosting**

**Aim**

To deploy a simple edge application near the User Plane Function (UPF)
and compare its latency with a cloud-hosted application.

**Objective**

- To understand the concept of Edge Computing in 5G networks.

- To deploy an application close to the UPF.

- To measure network latency between edge-hosted and cloud-hosted
  services.

- To analyze the benefits of edge computing for latency-sensitive
  applications.

- To evaluate the role of Multi-access Edge Computing (MEC) in 5G.

**Introduction**

One of the key features of 5G networks is the integration of Edge
Computing. Traditional cloud computing requires user data to travel to
distant cloud servers for processing, which increases latency and may
affect real-time applications.

Edge Computing addresses this challenge by placing applications and
services closer to end users, typically near the User Plane Function
(UPF). This reduces communication delay and improves response time for
applications such as video streaming, online gaming, autonomous
vehicles, industrial automation, and augmented reality.

In this experiment, a simple application was deployed near the UPF and
its latency was compared with a cloud-hosted service to evaluate the
advantages of edge computing.

**Theory**

**Edge Computing**

Edge Computing refers to processing data closer to the source of
generation rather than sending it to centralized cloud servers.

Advantages include:

- Reduced latency

- Faster response times

- Lower bandwidth consumption

- Improved Quality of Service (QoS)

**User Plane Function (UPF)**

The UPF is responsible for handling user data traffic in a 5G network.
Deploying applications near the UPF minimizes the distance traveled by
packets, thereby reducing delay.

**Cloud Computing**

In cloud-based architectures, user traffic must travel through multiple
network segments before reaching remote servers, resulting in higher
latency compared to edge deployments.

**Latency**

Latency is the time required for a packet to travel from source to
destination and back. Lower latency indicates faster network response
and better user experience.

**Procedure**

**Step 1: Verify Open5GS Deployment**

Ensure that all Open5GS network functions are operational.

**Step 2: Deploy Edge Application**

Deploy a simple web server (Nginx or Python HTTP Server) near the UPF
within the local Kubernetes environment.

**Step 3: Verify Application Accessibility**

Access the edge application and ensure that it responds correctly to
requests.

**Step 4: Configure Cloud-Based Service**

Use a publicly available cloud service or external web server for
comparison.

**Step 5: Measure Edge Latency**

Execute ping requests from the UE to the edge application and record the
response times.

**Step 6: Measure Cloud Latency**

Execute ping requests from the UE to the cloud-hosted service and record
the response times.

**Step 7: Compare Results**

Analyze the measured latency values and compare the performance of both
deployments.

**Observations**

The edge application was successfully deployed near the User Plane
Function and was accessible from the User Equipment through the Open5GS
network. The application responded quickly to user requests due to its
proximity to the data path.

Latency measurements showed that communication with the edge-hosted
application required fewer network hops compared to the cloud-hosted
service. As a result, response times for the edge application were
consistently lower.

The cloud-hosted application experienced additional delay because
packets had to traverse external networks before reaching the remote
server. Although the cloud service remained accessible, its response
times were higher than those observed for the edge deployment.

The comparison demonstrated that hosting applications closer to the UPF
significantly improves responsiveness and reduces communication delay.
This behavior is particularly beneficial for latency-sensitive
applications such as real-time video streaming, online gaming,
industrial automation, and augmented reality services.

![](media/image10.png){width="6.157109580052493in"
height="1.3960279965004374in"}

***Fig. 1. Latency comparison between edge-hosted and cloud-hosted
applications. The edge application deployed near the UPF achieved an
average latency of 1.075 ms, while the cloud-hosted application recorded
34.745 ms, demonstrating the effectiveness of edge computing in reducing
communication delay.***

**Results**

The edge-hosted application achieved lower latency than the cloud-hosted
application. The reduced response time confirmed the effectiveness of
deploying services near the UPF and demonstrated the advantages of edge
computing in 5G networks.

![](media/image11.png){width="6.268055555555556in"
height="1.7083333333333333in"}

***Fig. 2. ICMP ping test from the UE to the edge application deployed
near the UPF. The measured round-trip time (RTT) averaged 1.075 ms,
indicating low-latency communication within the 5G edge environment.***

![](media/image12.png){width="6.268055555555556in"
height="1.5986111111111112in"}

***Fig. 3. ICMP ping test from the UE to the cloud-hosted application.
The measured round-trip time (RTT) averaged 34.745 ms, showing higher
latency compared to the edge deployment due to increased network
traversal distance.***

**Conclusion**

The experiment successfully demonstrated the deployment of an edge
application within a 5G environment and compared its performance with a
cloud-hosted service. The results showed that edge computing
significantly reduces latency by bringing application processing closer
to the user. This validates the importance of edge computing and MEC
architectures in supporting low-latency applications in modern 5G
networks.

**Assignment 10 :Demonstration of End-to-End Communication from UE → gNB
→ 5G Core → Internet**

**Aim**

To demonstrate complete end-to-end communication from a User Equipment
(UE) through the gNB and Open5GS 5G Core Network to the Internet.

**Objective**

- To verify successful integration of UE, gNB, and Open5GS Core.

- To observe the complete communication path in a Standalone 5G network.

- To establish a PDU session and enable Internet connectivity.

- To verify packet transmission from the UE to an external network.

- To understand the role of different 5G network components in
  end-to-end communication.

**Introduction**

A 5G Standalone (SA) network consists of three major components: the
User Equipment (UE), the Radio Access Network (gNB), and the 5G Core
Network (5GC). For a user to access Internet services, communication
must pass through all these components successfully.

The UE first registers with the network through the gNB. The Access and
Mobility Management Function (AMF) authenticates the user, while the
Session Management Function (SMF) establishes a PDU session. The User
Plane Function (UPF) then routes user traffic between the UE and
external data networks such as the Internet.

This experiment demonstrates the complete communication path from the UE
to an Internet host, validating the successful operation of the entire
5G network architecture.

**End-to-End Communication Flow**

1.  UE initiates registration.

2.  gNB forwards signaling to the AMF.

3.  AMF authenticates the UE.

4.  SMF establishes a PDU session.

5.  UPF creates a user-plane tunnel.

6.  User traffic reaches the Internet.

7.  Responses are returned through the same path.

**Procedure**

**Step 1: Verify Open5GS Deployment**

Ensure all Open5GS network functions are running properly.

kubectl get pods -n open5gs

**Step 2: Start the gNB**

Launch the UERANSIM gNB and verify successful connection with the AMF.

**Step 3: Start the UE**

Launch the UE and verify successful registration.

**Step 4: Verify PDU Session Establishment**

Check logs for:

- Registration Accept

- PDU Session Establishment Request

- PDU Session Establishment Accept

**Step 5: Verify IP Allocation**

Ensure the UE receives an IP address from the 5G network.

**Step 6: Test Internet Connectivity**

Execute:

ping 8.8.8.8

or

ping www.google.com

**Step 7: Observe Packet Flow**

Monitor logs from:

- UE

- gNB

- AMF

- SMF

- UPF

Verify successful data transmission.

**Observations**

The Open5GS 5G Core Network and UERANSIM components were successfully
deployed and operational. The gNB established communication with the AMF
through the NG interface, enabling signaling exchange between the Radio
Access Network and the Core Network.

The UE successfully registered with the network and completed the
authentication procedure. A PDU session was established, and the network
assigned an IP address to the UE, allowing it to access external data
networks.

Internet connectivity tests were performed using ICMP ping requests to
external servers. Successful responses were received with no packet
loss, indicating that user traffic was correctly forwarded through the
gNB, UPF, and external network gateway.

The experiment confirmed that signaling and user-plane communication
operated correctly throughout the network. Data packets successfully
traversed the complete path from the UE through the gNB and Open5GS Core
Network to the Internet and back.

**Results**

The UE successfully communicated with an external Internet host through
the complete 5G network architecture. Registration, PDU session
establishment, IP allocation, and Internet connectivity were achieved
successfully, demonstrating full end-to-end communication.

![](media/image13.png){width="6.322347987751531in"
height="5.689826115485564in"}

***Fig. 1. Packet capture at the Open5GS User Plane Function (UPF) using
tcpdump on the ogstun interface. The captured ICMP echo request and
reply packets confirm successful forwarding of user traffic through the
5G core network toward the external network***.

![](media/image14.png){width="4.531882108486439in"
height="4.417283464566929in"}

***Fig. 2. Internet connectivity verification from the UERANSIM User
Equipment (UE) using ICMP ping to Google\'s public DNS server (8.8.8.8).
The successful responses with an average round-trip time (RTT) of
approximately 31.87 ms demonstrate end-to-end communication from the UE
through the gNB, Open5GS core network, UPF, and the Internet.***

**Conclusion**

The experiment successfully demonstrated end-to-end communication in a
Standalone 5G network using Open5GS and UERANSIM. The UE registered with
the network, established a PDU session, obtained an IP address, and
accessed Internet services through the gNB and 5G Core Network. The
successful transmission and reception of packets confirmed the correct
operation of the complete communication path from UE → gNB → Core
Network → Internet.
