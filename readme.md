# A* algoritm for solving 8-puzzle
Challenge was the part of assignment-3 in the Artificial Intelligence course
---

Problem: find the shortest path to win the 8-puzzle game
Input: initial configuration, goal
---

- This is a search space problem, where we must find a shortest path to reach the given node from the starting node
- We can use heuristic algorithms A* to tackle this challenge
- In Dijkstra's algorithm there is no heiristics (informed search) involved; but because of heiristics A* performs better
- The A* uses weighted path to traverse in the graph data-structure
- We can use priority queue to pick the best path (minimum cost path) from the available paths at any given point
- Path cost are calculated using `f(n) = g(n) + h(n)`
- n = next node on the path
- f(n) = total cost to reach the node n
- g(n) = cost to reach to the node n from the start
- h(n) = heuristic cost to reach the goal from node n, which in this proble the number of misplaced tiles at the configuration from the goal

---
On the finite graphs with non-negative weight on the edges of the nodes; A* is complete and always find a solution if it exists.

## Instructions to run the A* algorithm
python puzzle8.py


---
- You can change the initial and goal configuration in the main function on line 16 & 17 to check with other configurations
- The program works with 15-puzzles as well for that when instanitating the grid you must to pass the third parameter `size=4` on the lines 63 to 66
- If the configuration is doesn't have a solution, it will take a long time to produce the output because the A* is not optimized; and it will try to visit reachable configuration in order to find the solution.
- To mitigate above issue, we can write a method in the grid to check weather the given configuration is solvable or not.
- The proposed algorithm will need to count the number of inversions of the given configuration; which will be at the worst **O(n<sup>2</sup>)**, where n is size of the grid


---
- Some configurations of 8-puzzle and 15-puzzle are not solvable from given configuration
- It must depend on the inversion counts of the current game configuration and width of the board
- You can read more on that [here](https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/)
