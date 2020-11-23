Plentific Trello Job Interview
==============================

What Is This?
-------------

This is a demo Python testing framework created for job interview for Plentific.

Installation
---------------
1. Make sure you have Python 3.x installed on your computer
2. Download repository
3. Install packages from requirements.txt file (`pip install -r requiremnts.txt`)


How To Run This
---------------

1. From root catalog execute following command:  
`pytest test_trello.py --menable=True --mtimestamp=True --mlogo=".\static\logo.jpg"`
2. HTML test results will be created in root directory and will have followin syntax `pytest_metrics_Nov_23_2020_15_07`

Assumptions and improvements
-------
1. Objective one says `Create 3 cards on that board` and objective two says `Verify that there are 2 cards on board`. 
I assumed that this is a typo :)
2. Objective two says `Please write a selenium test (or equivalent)`. I assumed that "equivalent" does not mean that it
needs to be GUI based. That is why my testing framework is based on testing backend/API layer. If testing frontend by
Selenium or similar GUI based tool is required please let me know(!). I will add this solution to my framework.

Comments
-------

1. Trello account:  
`Username: kamilgrzywinski@gmail.com`  
`Password: Plentific`
2. Trello key and token are hardcoded. Normally I wouldn't put them in code. I did it to simplify running tests by 
recruiters. Instead, I would place them in environmental variables (please check conftest.py line 8 and 9). 
3. Before each test Trello Board is created and then after execution it is removed. If recruiters would like to see
them, please comment `teardown_method` in test_trello.py file.
4. Please, be aware that my Atlassian account has limitation for 10 boards. It means that commenting `teardown_method`
might require manual removal of some board to make it working properly. PS. I could handle this case in code, but its 
out of scope of this recruitments so I didn't do it.