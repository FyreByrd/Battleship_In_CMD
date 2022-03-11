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
Time:       6:13.28  
|             | Mean  | Range    |
|---          |:-:    |:-:       |
| First Sunk  | 11.99 | [2, 51]  |
| Second Sunk | 23.59 | [5, 59]  |
| Third Sunk  | 35.31 | [8, 70]  |
| Fourth Sunk | 47.69 | [14, 77] |
| Gameover    | 61.32 | [22, 84] |
### AdvancedAI
Iterations: 100,000  
Time:       1:41:55.47  
|             | Mean  | Range    |
|---          |:-:    |:-:       |
| First Sunk  | 8.74  | [2, 26]  |
| Second Sunk | 17.44 | [5, 53]  |
| Third Sunk  | 26.56 | [10, 66] |
| Fourth Sunk | 37.07 | [15, 71] |
| Gameover    | 51.03 | [21, 81] |

## Head-to-Head
A test of how the AI compares in a competitive match against the other AI.
### StupidAI x BasicAI
Iterations: 1,000,000  
Time:       5:24.51  
Win Rate: 0.078% (StupidAI)  
Win Rate: 99.92% (BasicAI)
### StupidAI x AdvancedAI
Iterations: 100,000  
Time:       1:42:32.66  
Win Rate: 0.028% (StupidAI)  
Win Rate: 99.97% (AdvancedAI)
### BasicAI x AdvancedAI
Iterations: 100,000  
Time:       1:35:46.68  
Win Rate: 24.67% (BasicAI)  
Win Rate: 75.33% (AdvancedAI)