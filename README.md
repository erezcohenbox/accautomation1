#Aeonix Load Gen project
Special imports:
1. pip install paramiko
2. pip install configobj

SIPp sever (ubuntu) should include zip package installed

Type of Load Gen:
1. Intra (within) server incoming/outgoing calls (w/wo RTP streem)
2. Inter (between) servers incoming/outgoing calls (w/wo RTP streem)
3. External (trunk) incoming calls (w/wo RTP streem)
4. External (trunk) services incoming calls (w/wo RTP streem)

	[1, 1000, 2000, 3000, 5000]
	[2, 2000, 4000, 8000]
	[4, 4000, 10000, 12000]
	[6, 6000, 15000, 18000] 
	
	1000	30000 --> 30999 
	2000	30000 --> 31999
	3000	30000 --> 32999
	4000	30000 --> 33999
	5000	30000 --> 34999
	6000	30000 --> 35999
	8000	30000 --> 37999
   10000	30000 --> 39999
   12000	30000 --> 41999
   15000	30000 --> 44999
   18000	30000 --> 47999

Prepare for load running:
1.  Check if all are communicating? ANX | SIM GEN | SIPp    ?? 
2.  Create all nessesary scripts for all SIPp servers       DONE	 
3.  Backup previous SIPp run                                DONE
4.  Kill all SIPps in scope (killall sipp) if running       DONE   
4.  Clean all previous SIPp logs before start               DONE
5.  Upload SIPp with requiered load scenario type           DONE
6.  Stop all Aeonix's in scope gracfuly
7.  Clean all Aeonix's logs before start
8.  Aeonix Init Space if needed
9.  Aeonix join cluster if needed
10.  Aeonix Import users 
11. Aeonix Do restart if needed


