#Aeonix Load Gen project
Special imports:
1. pip install paramiko
2. pip install configobj

Type of Load Gen:
1. Intra (within) server incoming/outgoing calls (w/wo RTP streem)
2. Inter (between) servers incoming/outgoing calls (w/wo RTP streem)
3. External (trunk) incoming calls (w/wo RTP streem)
4. External (trunk) services incoming calls (w/wo RTP streem)

SA		2000, 3000, 5000 (Intra tests)
CLUSTER	2000, 3000, 5000 (Intra Tests)
CLUSTER	2000, 3000, 5000 (Inter Tests)

Prepare for load running:
1.  Check if ANX <-- --> SIPp communication alive
2.  Kill all SIPps in scope (killall sipp) if running
3.  Clean all SIPp logs before start
4.  Upload SIPp with requiered load scenario type
5.  Stop all Aeonix's in scope gracfuly
6.  Clean all Aeonix's logs before start
7.  Aeonix Init Space if needed
8.  Aeonix join cluster if needed
9.  Aeonix Import users 
10. Aeonix Do restart if needed


