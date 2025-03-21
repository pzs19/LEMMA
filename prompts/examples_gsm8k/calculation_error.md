#### Example 1

[Question]
Tobias is buying a new pair of shoes that costs $95. He has been saving up his money each month for the past three months. He gets a $5 allowance a month. He also mows lawns and shovels driveways. He charges $15 to mow a lawn and $7 to shovel. After buying the shoes, he has $15 in change. If he mows 4 lawns, how many driveways did he shovel?

[Ground-truth Solution]
He saved up $110 total because 95 + 15 = <<95+15=110>>110
He saved $15 from his allowance because 3 x 5 = <<3*5=15>>15
He earned $60 mowing lawns because 4 x 15 = <<4*15=60>>60
He earned $35 shoveling driveways because 110 - 60 - 15 = <<110-60-15=35>>35
He shoveled 5 driveways because 35 / 7 = <<35/7=5>>5
The answer is: 5

[Error-Injected Solution]
Tobias needs 95 dollars for the shoes. He has been saving 5 dollars a month for three months. So he had 3 x 5  = 15 dollars to start. After the shoes, he has 15 dollars left. So he earned 15 + 95 = 110 dollars from mowing and shoveling. He earned 15 dollars from mowing 4 lawns, so he made 110 - 4 x 15 = 65 from shoveling. Since he charges 7 dollars to shovel a driveway, he has 65 / 7 = 9.285 driveways. Since he can't shovel a fraction of a driveway, we round down to 9. The answer is: 9
<explanation>  
The error in this solution is a 'calculation_error'. The solution is incorrect, the first wrong step arises because the amount earned from mowing lawns was miscalculated. 110 - 4 x 15 should be 110 - 60 = 50, not 65. This leads to an incorrect total amount earned from shoveling driveways.
</explanation>

#### Example 2

[Question]
A Statistics student wants to find out the average daily allowance of the middle school students. According to his survey, 2/3 of the students receive an average of $6 allowance per day while the rest gets an average of $4 a day. If he surveyed 60 students, what is the total amount of money those 60 students get in a day?

[Ground-truth Solution]
There are 60 students x 2/3 = <<60*2/3=40>>40 students who have a $6 daily allowance.
While there are 60 students - 40 students = <<60-40=20>>20 students who have a $4 daily allowance.
The sum of the allowances of the 40 students who received $6 daily is 40 students x $6/day = $<<40*6=240>>240.
The sum of the allowances of the 20 students who received $4 daily is 20 students x $4/day = $<<20*4=80>>80.
The total daily amount of money of those 60 students is $240 + $80 = $<<240+80=320>>320.
The answer is: 320

[Error-Injected Solution]
According to the survey, 2/3 of 60 students get the average of $6 a day. There are 2/3 * 60 = 40 students. 1/3 of 60 students get the average of $4 a day. There are 1/3 * 60 = 20 students. The total amount of money the 60 students get in a day is (40 students * $6) + (20 students * $4) = $480. The answer is: $480.
<explanation>The error in this solution is a 'calculation_error'. The total amount of money the 60 students get in a day is (40 students * $6) + (20 students * $4) = $320 instead of $480. </explanation>

#### Example 3

[Question]
Jim collects model cars, and he has 301 models total.  Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys.  How many Buicks does Jim have?

[Ground-truth Solution]
Let x represent the number of Chevys
Fords:3+2x
Buicks:4(3+2x)=12+8x
Total:x+3+2x+12+8x=301
11x+15=301
11x=286
x=<<26=26>>26
Buicks:12+8(26)=220
The answer is: 220

[Error-Injected Solution]
Jim has 301 models total. Let's say that Jim has x Chevys. He has 2x + 3 Fords. And he has 4(2x + 3) Buicks. We now have an equation in terms of x. x + 2x + 3 + 4(2x + 3) = 301. Solving we get 11x = 281. So x = 25.63. But we can't have a fraction of a car. So let's try 24 Chevys. Then 2x + 3 = 51 Fords. And 4(2x + 3) = 204 Buicks. 24 + 51 + 204 is indeed 301. Jim has 204 Buicks. 
The answer is: 204
<explanation>The error in this solution is a 'calculation_error'. The solution is incorrect because the equation was solved incorrectly. The correct equation is 11x + 15 = 301, and solving for x should give x = 26, not x = 25.63. The proposed solution then uses an incorrect value for x, leading to the wrong number of Buicks. </explanation>
