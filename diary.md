# FYP Diary 

**13/03/2025**
Add print statements to debug the errors ending the simulations, where the simulations end with None since there are no remaning childs which can be added. Furthermore, I am trying to implement a new approach for the calculating territory method.  

**08/03/2025**
Conducting further research into the extensions of the MCTS algorithm firstly I will start optimizing the computational time required for each move enabling the algorithm to calculate more than 10000 rollouts within seconds, furthermore, I will add multiprocessing allowing the rollouts to be run in batch simulations and updating the rollouts accordingly, extending this by adding passing and resignation thresholds for the simulations and potentially adding opening moves to strengthen the start of every simulated game rollouts.  

**27/02/2025**
Made a new mode for player to play against the MCTs agent to see how the strength compares to the random agent however due to the inefficiency of the current MCTs implementation it takes too long to play against the engine with more than 10 rollouts which is unfeasible to make a good bot, therefore I will create new method to improve this later on. Further, I added a bot vs bot mode for the MCTs agent which will be used for paramater analysis later on in the project.  

**25/02/2025**
I used the UCB algorithm to determine the best next move for the selection step using information from previous rollouts, choosing the child with the highest winrate alongside other variables including the 'temperature' variable which is a variable balancing between exploration and exploitation, also improved the simulation step by creating a method to play the game until the game_over where there are no legal_moves left.  

**23/02/2025**
MCTsAgent class where all 4 steps of the MCTs algorithm will be implemented, firstly the select_move method which includes the selection, expansion, simulation, and backpropagation step, where the simulation and expansion steps are currently random and will be improved later for more optimal outcomes such as better simulation games, batch simulations, choices of opening moves and more. 

**22/02/2025**
New class called MCTsNode, defining the data structure for the MCTs tree containing information such as the game_state, parents and children of the current rollouts, furthermore randomizing the child for the expansion step and updating rollouts. Added new method called Legal_moves to only randomize from valid moves during the simulation steps. Next will create the class MCTsAgent where all the 4 steps of MCTs occurs.  

**21/02/2025**
Added a function where the bot will also pass turn when the player passes turn, this allows the game to enter the final scoring stage since when the player passes, it signals that the game state is nearing the end and no significant moves can really be made therefore it is better to both pass and counts the score to determine the winner.  

**18/02/2025**
Creating a bot where it selects random Valid moves, where it doesnt fill its own eyes and randomly selects legal moves, added a new mode to the Go menu to for player to play against this random bot however the bot strength is very weak and the computational time per move is rather slow. 

**17/02/2025**
Tried a new flood_fill method which is similar to DFS but will be expanding differently, however the same issues still arise therefore I will return to this method at a later stage, refactored player_input into a class therefore it call be reused for any type of game either between players or bots.  

**13/02/2025**
Trying new calculate_territory function since the old one seeems to be counting the borders of each side as either neutral or the opposing colour leading to white having no points even with large areas, therefore this implementation will could the adjacent points where its stored in a set and count the amount of territories inside the adjacent points.  

**12/02/2025**
Due to the issues with calculating the territories, both in calcualate_territory and final_scoring, I have created test cases to determine where the error is and what should be changed since currently I know the issue is to do with the borders but not specifically what the scoring classifies it as.  

**15/01/2025** 
Started continuing my research on MCTs and reading the Deep Learning and the Game of GO book, expanding my understanding on the MCTs algorithm and implementation using Python, this implementation uses dictionary which I will follow first then improve by using Numpy Array for computational efficiency. Further researching what GUI library I should use.  

**12/12/2024**
Due to changes to the bandit problem, I decided to add red dots instead of statistical labels to avoid clutter while providing a visual method of comparing the accuracy of how well each algorithm estimates the mean probability of each arm since the more linear the models, the better the estimation. Furthermore, finalised the calculate_territory method to avoid neutral points be mistaken as black points especially at the start of the games with no points or no defined territories yet. 

**11/12/2024**
Increased the number of arms from 10 arms to 99 arms in the bandit problems since this allows for better understanding between the tradeoff of exploration vs exploitation since the more number of possible moves, the harder it is to get the best results. Hence now arm 0 starts at 0% and increases by 1% per arm until arm 99, with this the simulations will be reduced from 100 to 10 due to lack of computational power and graph compiling times. Due to the no. of arms changed, experimentation and change in variable values was required especially the epsilon variables. 

  
**09/12/2024**
Added the calculate_territory method while calculates the territories of each player and where there are neutral territory which does not contribute to the final scoring, this is included in the final_score function where the territory are counted at the end and will be displayed in the CLI also printing who the winner is (player with the most territory), this still requires further testing since territory is inaccurately scoring the neutral territories as black territories.

**08/12/2024**
Using Matplotlib and the average results gathered, I decided to make 3 graphs with the first graph on the left being the average rewards per arm then the average pull count per arm then estimated mean probablities per arm with the total rewards of each algorithm displayed at the top. The most important variable is the average pull per arm since this determines which algorithm prioritises the total rewards while also explores other arms efficiently, with careful variable testing, the UCB score is best for this method since it only prioritises the arms with higher rewards unlike e-greedy where the lower arms are randomly pulled. 
  
**07/12/2024** 
For the visual representation in the presentation, I decided to revisit the bandit problem and created matplotlib graphs for each simulated to illustrate the difference in each algorithms for the bandit problem. For a reliable and accurate results, I implemented a way to gather average results from 100 simulation of each algorithm where each simulation is a 1000 iterations each. Next I will be finalizing the values gather and also display these values in a graph. Furthermore, I am finalizing the presentation and will be using the graph displayed by MatPlotlib.
  
**06/12/2024**
New file to incorporate all the previous classes into a player_vs_player method where a new game starts once called, the players inputs plays representing stones on the board and prints an "invalid move" if the move is invalid such as the ko rule or the rows are larger than board size. The player can also pass turn or resign by typing in "pass" and "resign" respectively however I will be implementing a scoring method to calculate the territories next and further testing required. 
  
**05/12/2024**
Had the third meeting with my supervisor, shown him my progress so far with the outlines to my presentation and reports, Got feedback on what I could include in my reports such as A plan for next term and also explanation for the research and experimentation I have done. He also suggested to fully complete the PVP mode then focus on creating a GUI in the next term to make a completed early deliverable on time. 
  
**04/12/2024**
New str method which will represent the go board in CLI using x and o as black and white stones and columns will be defined with letters from A to I, rows are defined with numbers from 1 to 9. However, testing this method has been a challenge since I would have to convery the board into a string while keeping the same format and also find a way to compare the values rather than instances. 
  
**03/12/2024**
Implemented another special rule called the Ko Rule which is when then board can't return to the previous state after capturing a stone since this could end in an infinite loop of capturing the same points over and over again, this Rule is implemented by comparing next move with the previous state of the board. While testing, the comparing between board states was an issue since it was comparing instances instead of values therefore I had to make my own __eq__ method, lastly combined both previous rules into valid_move which determines if the next move played is a valid move, if not an "invalid move" prompt will appear. 
  
**01/12/2024**
Implemented a self_capture method which is a rule in go where the player can't place stone if it results in its own stones being captured, this prevents certain moves from the game therefore it is required and requires copying the state of the board to compare number of liberties to a point. Furthermore, testing all the gameover function implemented earlier including the self_capture method
  
**30/11/2024**
New class of Gostate which will be storing the board positions, next player, previous game states(will be used in the Ko Rule) and the last move played. Also including function like starting a new game including the variable values initialised when the game is starting such as the starting player will be the Player with black stones, another function is the is_over to state that the game ends when both player passes or either resigns.
  
**29/11/2024**
Completed the Board class with the addition of remove_string method since this is used to remove strings with no liberties left when the stones are placed, also added a function to merge strings if they are connected to same coloured stones. Furthermore, improved these methods through testing and making sure each method is functioning as expected. Will be starting the GoState class next which will contain method such as starting a new game. 

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
