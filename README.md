Paper Reivew   
---
[Mobility-Aware Call Admission Control Algorithm With Handoff Queue in Mobile Hotspots](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6457513)    
Y. Kim, H. Ko, S. Pack, W. Lee and X. Shen  
IEEE Transactions on Vehicular Technology, vol. 62, no. 8, pp. 3903-3912, Oct. 2013.   

Motivation
---
* Because the vehicles can act as hotspots nowadays, people spend increasingly more time in vehicles like cars, subways or trains. 
* Since the WLAN capacity is shared by multiple vehicular users and session-oriented applications (e.g., VoIP) are sensitive to disconnection/disruption due to handover, a well-defined CAC algorithm should be devised to satisfy QoS requirements in hotspots. 
* This paper put forward CAC algorithm, to increase the channel utilization.

Mechanism
---
* It is easy to know the vehicles have two phase: stop and move. The main mechanism is that
the system will maintain guard channels and a queue for hand-off calls in stop phase. We need
to note that the events in different phase are different.

<div align=center> <img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/paper%20figure/two%20phase.png" width="400"/></div>

* At the stop phase   
A vehicle stays at a location (e.g., a bus stop or a subway station).   
Vehicular users can join the AP (i.e., riding on the vehicle).   
In this situation, a handoff priority scheme with guard channels is examined to protect vehicular handoff users from vehicular new users.   
* At the moving phase   
There are no vehicular handoff users since no one can ride on the moving vehicle.    
No guard channels for handoff users are allocated to maximally utilize the AP resource. 

Notations
---
<div align=center> <img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/paper%20figure/notation.png" width="400"/>
<img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/paper%20figure/notations.png" width="400"/>
</div>

Markov Chain
---
* Authors used the Markov Chain to solve this problem. Beacause of the Poisson Process, Markov Chain is a good mothod. What we want to derived are the **Hand-off call dropping probability** and the **New call blocking probability**
<div align=center> <img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/paper%20figure/markov%20chain.png" width="500"/>
</div>

* Using **Balance Equation** to derived the transfer probability of each state. It is hard to derived the closed form, so we can use [Iterative algorithm](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1343902)

MA-CAC Algorithm
---
* The simulation algorithm was shown as below:  
<div align=center> <img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/paper%20figure/algorithm.png" width="400"/>
</div>

Simulation Result
---
* Compared the results of paper, they were the same.
<div align=center> <img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/figure/sim_NCBP.png" width="350"/>
<img src="https://github.com/AvisChiu/IEEE_TVT_2013/blob/master/figure/sim_HCDP.png" width="300"/>
</div>

