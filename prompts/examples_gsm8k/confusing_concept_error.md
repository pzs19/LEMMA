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
Tobias mows 4 lawns. Each lawn earns him 15 dollars. So he mows 4 x 15. He shovels driveways. The money he earns shoveling, along with his allowance, buys shoes and leaves $15 in change. So he must shuffle 95 - 15 or 80 dollars. 15 + 4 x 15 = 80. So 80 = 15 + 4 x 15. So we subtract 15 from both sides and we have 65 = 4 x 15. So shovels are 7 dollars. So 65 = 4 x 7. So he shovels 4 driveways. 
The answer is: 4.
<explanation>The error in this solution is a 'confusing_concept_error'. The solution incorrectly assumes that the total amount of money Tobias saved is $80, which is only the cost of the shoes minus the change. However, the total amount saved is actually $110, which includes the cost of the shoes plus the change. </explanation>

#### Example 2

[Question]
If it takes 10 people 10 days to shovel 10,000 pounds of coal, how many days will it take half of these ten people to shovel 40,000 pounds of coal?

[Ground-truth Solution]
The 10 people shovel 10,000 pounds per 10 days, or 10,000/10=<<10000/10=1000>>1000 pounds per day per 10 people.
And 1000 pounds per day per 10 people is 1000/10=<<1000/10=100>>100 pounds per day per person.
Half of ten people is 10/2=<<10/2=5>>5 people.
At 100 pounds per day per person, 5 people can shovel 5*100=<<5*100=500>>500 pounds per day.
Therefore, for 5 people to shovel 40,000 pounds, it will take 40,000/500=<<40000/500=80>>80 days.
The answer is: 80

[Error-Injected Solution]
It takes 10 people 10 days to shovel 10,000 pounds of coal. So 5 people will take 20 days to shovel 10,000 pounds of coal. Then it is directly proportional, so 5 people will take 20 days to shovel 20,000 pounds of coal. Then again 5 people will take 20 days to shovel 40,000 pounds of coal. 
The answer is: 20.
<explanation>The error in this solution is a 'confusing_concept_error'. The solution incorrectly assumes that the number of days to shovel 40,000 pounds of coal is the same as the number of days to shovel 20,000 pounds of coal, which is a misunderstanding of the proportional relationship. </explanation>

#### Example 3
[Question]
Toby wants to walk an average of 9,000 steps per day over the next week. On Sunday he walked 9,400 steps. On Monday he walked 9,100 steps. On Tuesday he walked 8,300 steps. On Wednesday he walked 9,200 steps. On Thursday he walked 8,900 steps. How many steps does he need to average on Friday and Saturday to meet his goal?

[Ground-truth Solution]
He needs to walk 63,000 steps in a week because 7 x 9,000 = <<7*9000=63000>>63,000
He has 18,100 steps to walk on Friday and Saturday because 63,000 - 9,400 - 9,100 - 8,300 - 9,200 - 8,900 = <<63000-9400-9100-8300-9200-8900=18100>>18,100
He needs to walk an average of 9,050 on Friday and Saturday because 18,100 / 2 = <<18100/2=9050>>9,050
The answer is: 9,050

[Error-Injected Solution]
Toby wants to walk an average of 9000 steps per day over 1 week. If he has already walked 9400 + 9100 + 8300 + 9200 + 8900 = 44900 steps from Sunday to Thursday inclusive. Over 5 days he has walked 44900 steps. So over 7 days (the whole week) he has walked (44900/5)x7 = 62860 steps. He has still to walk (9000x7)-62860 = 7140 steps over the weekend. So he has to walk 7140/2 = 3570 steps per day over the weekend. The answer is: 3570.
<explanation>The error in this solution is a 'confusing_concept_error'. The first wrong step arises because the proposed solution incorrectly calculates the total number of steps Toby has walked over the entire week. Instead of simply adding the steps from Sunday to Thursday, the solution incorrectly scales the steps from 5 days to 7 days, leading to an incorrect total. </explanation>