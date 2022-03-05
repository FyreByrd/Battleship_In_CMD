# Statistics for the AI
Tested on an HP laptop with intel CORE i7 8th Gen and 8GB RAM
## Solo
A test of how the AI performs on randomly generated boards.
### StupidAI
Iterations: 1,000,000  
Time:       7:18.17  
|             | Mean  | Range    |
|---          |:-:    |:-:       |
| First Sunk  | 50.56 | [2, 96]  |
| Second Sunk | 68.89 | [8, 97]  |
| Third Sunk  | 80.28 | [20, 98] |
| Fourth Sunk | 88.69 | [33, 99] |
| Gameover    | 95.39 | [44, 100]|
### BasicAI
Iterations: 1,000,000  
Time:       6:19.83  
|             | Mean  | Range    |
|---          |:-:    |:-:       |
| First Sunk  | 12.06 | [2, 49]  |
| Second Sunk | 23.70 | [5, 64]  |
| Third Sunk  | 35.48 | [8, 72]  |
| Fourth Sunk | 47.97 | [14, 79] |
| Gameover    | 62.17 | [23, 100]|
### AdvancedAI
Untested

## Head-to-Head
A test of how the AI compares in a competitive match against the other AI.
### StupidAI x BasicAI
Iterations: 1,000,000  
Time:       5:36.99  
Win Rate: 0.878% (StupidAI)  
Win Rate: 99.12% (BasicAI)
### StupidAI x AdvancedAI
Untested
### BasicAI x AdvancedAI
Untested