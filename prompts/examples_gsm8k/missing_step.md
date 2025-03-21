#### Example 1

[Question]
Janet pays $40/hour for 3 hours per week of clarinet lessons and $28/hour for 5 hours a week of piano lessons. How much more does she spend on piano lessons than clarinet lessons in a year?

[Ground-truth Solution]
First find the total Janet spends on clarinet lessons per week: $40/hour * 3 hours/week = $<<40*3=120>>120/week
Then find the total Janet spends on piano lessons per week: $28/hour * 5 hours/week = $<<28*5=140>>140/week
Then subtract her weekly clarinet spending from her weekly piano spending to find the weekly difference: $140/week - $120/week = $<<140-120=20>>20/week
Then multiply the weekly difference by the number of weeks in a year to find the annual difference: $20/week * 52 weeks/year = $<<20*52=1040>>1040/year
The answer is: 1040

[Error-Injected Solution]
Janet pays 40 for 3 hours of clarinet lessons. So she pays a total of 40 x 3 = 120 for the clarinet lessons. She pays 28 for 5 hours of piano lessons. So she pays a total of 28 x 5 = 140 for piano lessons. 140 - 120 = 20. So she spends 20 more on piano lessons than she does on clarinet lessons. The answer is: 20.
<explanation>The error in this solution is a 'missing_step'. The solution only calculates the weekly difference in cost between piano and clarinet lessons, but it does not account for the annual difference. </explanation>

#### Example 2

[Question]
There are 70 cookies in a jar. If there are only 28 cookies left after a week, and Paul took out the same amount each day, how many cookies did he take out in four days?

[Ground-truth Solution]
Paul took out a total of 70-28 = <<70-28=42>>42 cookies in a week.
Paul took out 42/7 = <<42/7=6>>6 cookies out of the jar each day.
Over four days, Paul took out 6*4 = <<6*4=24>>24 cookies from the jar.
The answer is: 24

[Error-Injected Solution]
There were originally 70 cookies. And after a week there are 28. So 70 - 28 = 42 were eaten. Paul took out the same amount each day for a week. So he took out 42 / 7 = 6 each day. The answer is: 6.
<explanation>The error in this solution is a 'missing_step'. The solution only calculates the number of cookies Paul took out each day, but it does not account for the number of days he took out cookies. </explanation>

#### Example 3

[Question]
Hank reads the newspaper every morning, 5 days a week for 30 minutes.  He reads part of a novel every evening, 5 days a week, for 1 hour.  He doubles his reading time on Saturday and Sundays.  How many minutes does Hank spend reading in 1 week?

[Ground-truth Solution]
He reads 30 minutes in the morning 5 days a week for a total of 30*5 = <<30*5=150>>150 minutes
He doubles his reading time on the weekends so 30*2 = <<30*2=60>>60 minutes per day
He reads 60 minutes on Saturday and Sunday in the mornings for a total of 60+60 = <<60+60=120>>120 minutes
He reads 1 hour in the evenings 5 days a week for a total of 1*5 = <<1*5=5>>5 hours
He doubles his reading time on the weekends so 1*2 = <<1*2=2>>2 hours per day
He reads 2 hours on Saturday and Sunday in the evenings for a total of 2+2 = <<2+2=4>>4 hours
He read 5+4 = 9 hours which, when converted to minutes is 9*60 = 540 minutes
He reads 150 minutes in the morning and 120 minutes in the evenings and 540 over the weekend for a total of 150+120+540 = 810 minutes in 1 week
The answer is: 810

[Error-Injected Solution]
Hank reads 30 minutes in the morning 5 days a week for a total of 30*5 = 150 minutes. He doubles his reading time on the weekends, so 30*2 = 60 minutes per day on Saturday and Sunday. He reads 60 minutes on Saturday and Sunday for a total of 60+60 = 120 minutes. He reads 1 hour in the evenings 5 days a week for a total of 1*5 = 5 hours. On the weekends, he reads for 2 hours in the evenings, so 2+2 = 4 hours total. He reads 150 minutes in the mornings, 120 minutes on weekends, and 4 hours in the evenings, which is 4*60 = 240 minutes. So, 150 + 120 + 240 = 510 minutes in a week. 
The answer is: 510.

<explanation>The error in this solution is a 'missing_step'. The solution neglects to account for the fact that Hank reads both in the mornings and evenings on the weekends. The total weekend reading time should have been calculated for both morning and evening separately, then summed to get the correct total for the weekend, which would lead to a higher weekly total. </explanation>
