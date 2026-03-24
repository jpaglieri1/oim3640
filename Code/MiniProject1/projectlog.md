Project Log:

2/22/2026
Wrote the proposal (milestone 0) for this mini project, using AI to help me come up with some unique features to my financial calculator application. Through this, I was able to come up with the idea to have the application develop an amortiztion table if the user elects, and allow the user to input information about another loan/investment to compare the two.

2/23/2026
I developed the code for part of the calculator function and the amortization table function. I did not use AI very much during the code development, however I did use it to identify errors in my code in the amortization function. Initially, I had left out line 53:
    endbal_list.append(endbal)
which made it so that this list did not have any values in it. Therefore, the dataframe was not able to be created because the lists did not all have the same number of items in the list.

3/1/2026
I finished the calculator function, using AI to help me with the equations to calculate each variable. To do so, I wrote out the equation and inputted them into ChatGPT and asked it to determine what is being solved for. It was able to identify an error in my equation for calculating the number of periods, and I was able to adjust it accordingly. I also created this project log and inputted descriptions for the work I had done and when.

3/23/2026
Today I worked on some minor errors in my code tested it to ensure that it was working properly. I also created the README.md and began working on it. I used ChatGPT to help ensure that the instructions I wrote were clear.
I also decided that I was not going to include the compare function and instead keep it so that the user can just input new data. This way if they want to analyze more than two loans/investments, they can continue inputting the data and view the amortization table for each set of data.

3/23/2026
I finalized the README.md and asked one of my peers to try my code to ensure that they were able to get it to work properly and understand my instructions.