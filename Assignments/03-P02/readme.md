## P03 Scheduling-Algorithm-Simulator
### Installation Process :
Open the folder with terminal and follow these commands to run the program. Choose python version correctly. If you use python3 to run python files then use pip3 instead. Also for the next command use python3.
- pip install -r requirement.txt

Afrer completing all the necessary packages run this command:
- python Main.py

### Description :
Simulator will show a graphical represestation of how processes done in a CPU . There are 5 Scheduling algorithm implemneted. They are :
- First-Come, First-Served (FCFS) Scheduling.
- Shortest-Job-Next (SJN) Scheduling.
- Priority Based (PB) Scheduling.
- Shortest Remaining Time First (SRTF).
- Round Robin(RR) Scheduling.
Each algorithm can be choosen by user . User can add process and select 6 CPUs max . GUI will show the realtime execution of the processes and create a 
Gantt chart. 
### Files
|   #   | File            | Description                                                         |
| :---: | --------------- | --------------------------------------------------------------------|
|   1   | Main.py         | Main driver of my project that launches Simulator.                  |
|   2   | fcfs.py         | Implementation of  FCFS Scheduling algorithm.                       |
|   3   | pb.py           | Implementation of Priority Based Scheduling algorithm.              |
|   4   | rr.py           | Implementation of Round Robin Scheduling algorithm.                 | 
|   5   | sjf.py          | Implemnetation of sortest job first scheduling algorithm.           |
|   6   | srtf.py         | Implementation of sortest remaining time first scheduling  algorithm|
|   7   | cpu.py          | Hold CPU class .                                                    |
|   8   | process.py      | processing the input data                                           |
|   9   | scheduler.py    | Record the history of the process.                                  |

### Instructions

- Make sure you install library PyQt5
- Run the Main.py file then give all the necessary data.

### Important
Total BT for a process = CPU Burst time + I/O Burst time + CPU Burst time.

I/O Burst time= I/O Burst time .










