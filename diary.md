# FYP Diary 

**26/11/2024**
Implemented the Board class which allows specifying the size of the board and the main size used in this project will be 9x9 since it is much more computational viable and easier for 
the MCTS algorithm to be implemented and understood. This class includes a place_stone method which is very crucial since it places the specified stone on the point while determining 
the liberties surrounding that point which will be used in the capturing method later on. Also included the method to retrieves the player's colour and string connected to a certain stone.

**24/11/2024**
Started with the Player class and move class including functions such as playing moves, passing turn and resigning while the Player class has 2 players, black or white and a neighbour function determining the neighbours of each point. This is tested using unittest and this will be used throughout the project.


**23/11/2024** 
After understanding the implementation of the GO board in Python and applying a random algorithm, I decided to create a new branch to implement those files again with proper testing and coverage tests to make sure the codes will be efficient and follow coding standards, starting with the Player files and possible move functions. Next will be the implementation of the GO board and I will continue this until I implement a basic algorithm and enable player vs player game in CLI then work on a GUI for the game. 

**15/11/2024**
I Added 2 new files, containing functions which will help determine if a point is an eye therefore helping to end the game of GO since without this function, the AI might self-capture itself but filling the eye which will lead to a loss. Furthermore, I have been continuing to understand and research about implementing algorithms into the game of GO using Python and Next I will be starting with an AI which plays random moves then further implement other algorithms from there on. 


**12/11/2024**
Since the last entry, I have been constantly implementing the game of Go using Python, recently I have added the Ko and Self-capture rules which are illegal moves in most international rulesets for Go, currently there are 4 different classes specifying Go moving options, a Go string containing each groups of same coloured Go, Board and GameState class. Next, I will be implementing how to end the game of Go including many conditions to check for while ending the game of Go.   

**07/11/2024**
Had the second meeting with My Supervisor to catch up on my progress. I demonstrated my findings so far on the bandit problem solver on different algorithms and asked about the best way to illustrate this, my Supervisor recommended to show it in a graph form therefore it can easily be determined which algorithms yield the best results with a good predicted on the estimated probability of each arm, my Supervisor also suggested building my own GUI for the GO game and also look into Parallelism while running the MCTs for the GO game to be able to reduce the search tree. Next I will continue implementing GO using Python. 

**06/11/2024**
Increased the number of arms for the bandit problem on each algorithm and further optimizing it and analysing the difference the number of arms affecting the constant values of each algorithm since for the Epsilon algorithms, the epsilon value had to be increased from 0.12 to around 0.35 to advocate for the increase in number of arms and promote exploration since it was too focused on exploitation. Further improved UCB algorithm and merged with Main branch to start working on a new branch (test-go-game), which will start the implementation of the GO board game using Python, first in CLI and further along the line as a GUI. Next I will be continuing this implementation and solidify the rules of Go in this branch making sure its playable and efficient. 

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
