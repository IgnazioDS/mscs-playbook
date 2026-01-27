# Worked Examples

## Dynamic Programming: 0/1 Knapsack
**Input**
- values = [60, 100, 120]
- weights = [10, 20, 30]
- capacity = 50

**Idea**
`dp[c]` = best value with capacity `c` using items processed so far.

**Steps (capacity shown at key points)**
1) Start: dp[0..50] = 0
2) Item 0 (w=10, v=60): dp[10]=60, dp[20]=60, ..., dp[50]=60
3) Item 1 (w=20, v=100): dp[20]=100, dp[30]=160, dp[50]=160
4) Item 2 (w=30, v=120): dp[30]=160, dp[40]=220, dp[50]=220

**Result**
`dp[50]=220` (items with weights 20 + 30).

## Greedy: Interval Scheduling
**Input**
Intervals: (1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)

**Idea**
Always pick the interval with the earliest finish time.

**Steps**
1) Sort by end time.
2) Pick (1,4) → current_end=4.
3) Next compatible: (5,7) → current_end=7.
4) Next compatible: (8,11) → current_end=11.
5) Next compatible: (12,16) → current_end=16.

**Result**
4 intervals selected; greedy stays ahead of any optimal solution.

## Graphs: Dijkstra
**Input**
A→B(1), A→C(4), B→C(2), B→D(5), C→D(1)

**Steps**
1) dist[A]=0, heap=[(0,A)]
2) Pop A: relax B=1, C=4
3) Pop B: relax C=3, D=6
4) Pop C: relax D=4
5) Pop D: done

**Result**
A:0, B:1, C:3, D:4.

## Data Structures: Segment Tree (Range Sum)
**Input**
values = [1, 3, 5, 7, 9, 11]

**Steps**
1) Leaves stored at indices n..2n-1.
2) Internal nodes store sums of children.
3) Query [1,4): combine segments covering indices 1..3.
4) Update index 2 to 6: recompute parents on the path to root.

**Result**
- query(1,4) = 3 + 6 + 7 = 16 after update.

## Approximation: 2-Approx Vertex Cover
**Input**
Edges: (0,1), (1,2), (2,3)

**Steps**
1) Pick edge (0,1) → add {0,1}; remove incident edges.
2) Remaining edge (2,3) → add {2,3}.

**Result**
Cover = {0,1,2,3}; size 4, optimal is 2, so within 2x bound.
