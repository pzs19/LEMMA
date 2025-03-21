#### Example 1

[Question]
Alyssa, Keely, and Kendall ordered 100 chicken nuggets from a fast-food restaurant. Keely and Kendall each ate twice as many as Alyssa. How many did Alyssa eat?

[Ground-truth Solution]
To figure out this problem we need to turn it into an equation. Let’s make A the number of nuggets Alyssa ate. We know all three girls ate 100 nuggets total, so 100 nuggets = A (how many Alyssa ate) + 2A (how many Keely ate) + 3A (how many Kendall ate) or 100 = A + 2A + 3A which is 100 = 5A
Then we will divide each side by 5 to figure out how many nuggets Alyssa ate, 100/5 = 5A/5 or 20 = A.
The answer is: 20

[Error-Injected Solution]
Since the number of nuggets is 100, and we know that Keely and Kendall each ate twice as many as Alyssa, we can say that together they ate three times as many as Alyssa. Therefore, we can use the equation 3A = 100 to find the number of nuggets Alyssa ate. Solving for A, we get A = 33.333... Since Alyssa cannot eat a fraction of a nugget, we round down to the nearest whole number, which is 33. Therefore, Alyssa ate 33 chicken nuggets. The answer is: 33
<explanation>The error in this solution is a 'confusing_formula_error'. The the equation used in the proposed solution is incorrect. The correct equation should be 100 = A + 2A + 2A, not 3A = 100. The proposed solution incorrectly combines the number of nuggets eaten by Keely and Kendall into a single term, leading to the wrong equation. </explanation>

#### Example 2

[Question]
James and Ali together own $250. If you know that James owns $40 more than Ali, then calculate the amount owned by James.

[Ground-truth Solution]
Let X be the amount owned by James. The amount owned by Ali is X - $40.
The total amount owned by both of them X + (X - $40) = $250.
Combining like terms, we get X*2 - $40 = $250.
Adding $40 to both sides, we get X*2 = $290.
Dividing both sides by 2, we get X = $145.
The answer is: 145

[Error-Injected Solution]
James and Ali are both picking up the total amount. But we are told that James has $40 more. So this means he has a total of 250/2 + 40 = 175. The answer is: 175.
<explanation>The error in this solution is a 'confusing_formula_error'. The method of dividing the total amount by 2 and then adding the difference is incorrect. This approach does not account for the correct distribution based on the given ratio and difference. </explanation>

