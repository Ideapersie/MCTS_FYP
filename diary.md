# FYP Diary    

**01/11/2024**
Tested UCB algorithm with increased numbers of total pulls analysing whether it will results in a better average estimated mean value of each arm, which it does until a certain point alongside increasing the number of arms from 3 to 10 and analysing the difference in average rewards. Furthermore, implemented the 'temperature' variable in the UCB algorithm which is used to balance the exploration and exploitation. Started with 1.5 which was suggested in a book for GO however this was too high for the 10 arm bandit problem therefore currently the best found value is around 0.8, not resulting in the best rewards however it is more consistent and gives a better estimate of each arms's probabilities.  

**28/10/2024**
Improved the decay epsilon-greedy algorithm and implemented the UCB algorithm, using the confidence bound score to determine the next arm selected. Next I will be including a 
'temperature' variable or the exploration score to determine the balance between exploitation and exploration, further also increasing the number of arms in the problem to 
estimate the efficiency of the algorithm and different number of exploration options.  

**24/10/2024**
Added 3 different algorithms for the Bandit problem, Random selection, epsilon-greedy and decay epsilon-greedy algorithm. Displaying total numbers of pull and mean rewards per arm,
allowing to track the efficiency of each algorithm (will be illustrated in a latter stage). Next I will be experimenting with the UCB algorithm and analysing which algorithm is more
efficient.  

**22/10/2024**
Made a simple CLI for the main menu with options leading to a page where the bandit problems will be experimented and analysed, and another page for the Command-Line GO game.Will continue researching the algorithm and constantly keep testing it in the respective files, starting with a simple bandit problem with naive strategies.  
  
**18/10/2024**
Understanding the formulas of each algorithms and will be comparing between naive and non-naive strategies, will plan to implement a GUI to show these results later on as per my supervisor recommendations.
Once I fully grasp these formulas and how they work, I will implement each one into Python therefore showing statistical results between each algorithm and compare it to UCB.   
  
**15/10/2024**
Doing research on the Multi-Armed Bandit problem and understanding the UCB algorithm, asked my supervisor about the Bandit problem early deliverables.  
Next I will be implementing the Bandit problem into Python trying out different selection algorithms and comparing it to the UCB algorithm.  

**12/10/2024**
Finalised and submitted the Project Plan yesterday, I have been continuing research on MCTs and gained a lot of knowledge therefore next week I will start
extending my research on Bandit Problems to understand the trade-off between exploration and exploitation and the UCB score.  

**08/10/2024**
Read more research papers and the book which taught me new knowledge about AI and MCTs therefore I can improve the abstract section of the project plan.
Furthermore, finalising the timeline of the project and next I will be continuing research while determining about the possible risks and mitigations.  

**03/10/2024**
Attended my supervisor meeting and improved my project plan especially the timeline and how I should structure each week.
Next step will be to continue research especially a book I came across explaining how to make an AI for the game of GO.  
