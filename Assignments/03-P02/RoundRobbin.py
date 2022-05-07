from rich.console import Console
from rich.table import Table

class RR_ALGO:

    def __init__(self):
        # Default Data set
        # self.data = [10, 2, 3, 4, 4, 6, 7, 8, 9, 5]
        # self.n = 10  # No of processes
        # The queue of process burst time
        
        self.data = []  #2,1,1,1,1
        self.n = 0  # No of processes


    # Getting the No of processes & burst time
    def getData(self):
        # for i in range(int(self.n)):
        #     temp = input("Enter The BurstTime for Process p" + str(i)+"\n")
        #     self.data.append(temp)
        with open('rr_process', 'r') as file:
            for line in file:
                l = line.split()
                self.data.append(l[len(l) - 1])
                
        self.n = len(self.data)

    def RoundRobin(self):
        Twt = 0
        Bst = 0.0
        w=0.0
        Tat = [0]               #0,1,3,6
        aTat=0.0                #1
        Wt = [0]                #0,0
        quantum=int(input("Enter the quantum:\n"))
        B = list(self.data)     #1,2,3
        rem_bt = list(self.data)#0,1 2
        t = 0 # Current time  3
        while(1): 
            done = True
            for i in range(int(self.n) ): 
                if (int(rem_bt[i]) > 0) : 
                    done = False # There is a pending process 
                    if (int(rem_bt[i]) > quantum) : 
                        t += quantum  
                        rem_bt[i] =int(rem_bt[i])- quantum  
                    else: 
                        t = t + int(rem_bt[i])  
                        Wt.append(t - int(B[i]))  
                        rem_bt[i] = 0                
            if (done == True): 
                break
        for i in range(int(self.n)+1):
            Twt = int(Twt) + int(Wt[i])
        for i in range(int(self.n)): 
            temp=int(B[i]) + int(Wt[i])
            Tat.append(temp)
            aTat = aTat + Tat[i]

        print("\n\n")
        # creating the table object
        table = Table(title="[#D0FB59]Round Robin RESULT[/]")

        # adding the columns
        table.add_column("[cyan]Total Waiting Time[/]", style="cyan", no_wrap=True)
        table.add_column("[magenta]Average Waiting Time[/]", style="magenta")
        table.add_column("[#D0FB59]Total Turnaround Time[/]", justify="right", style="#D0FB59")
        table.add_column("[blue]Average Turnaround Time[/]", justify="right", style="blue")

        # adding the rows
        table.add_row(str(Twt), str(Twt/int(self.n)), str(aTat), str(aTat/int(self.n)))

        # creating the console object
        console = Console()

        # displaying the table using the console object
        console.print(table)

        # print("Total Waiting Time:"+str(Twt))
        # print("Average Waiting Time:"+str(Twt/int(self.n)))
        # print("Total Turnaround Time:"+str(aTat))
        # print("Average Turnaround Time:"+str(aTat/int(self.n)))

# if __name__ == '__main__':
#     RR = RR()
#     RR.getData()
#     RR.Fcfs()