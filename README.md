Plentific Trello Job Interview
==============================

What Is This?
-------------

This is a demo Python testing framework created for job interview for Plentific.

Installation
---------------
1. Make sure you have Python 3.x installed on your computer
2. Download repository
3. Download Selenium WebDriver adequate to your browser. I was testing my framework with Chrome:  
`https://chromedriver.chromium.org/downloads`
3. Install packages from requirements.txt file:  
`pip install -r requiremnts.txt`

How To Run API Tests
---------------

1. To run API tests from root catalog execute following command:  
`pytest test_trello_api.py --menable=True --mtimestamp=True --mlogo=".\static\logo.jpg"`
2. HTML test results will be created in root directory and will have following syntax `pytest_metrics_DATE_TIME`

How To Run Selenium Tests
---------------

1. To run Selenium tests from root catalog execute following command:  
`pytest test_trello_selenium.py --menable=True --mtimestamp=True --mlogo=".\static\logo.jpg" --driver Chrome 
--driver-path "PATH_TO_YOUR_CHROME_DRIVER"`
2. HTML test results will be created in root directory and will have following syntax `pytest_metrics_DATE_TIME`

**IMPORTANT NOTICE**
-------

At first, when I was making this testing framework I misunderstood objectives and I assumed that "Objective 2" can be 
done without Selenium. So I based my whole framework (including negative cases) on API level tests, and these tests 
are much more polished (as it comes to technical implementation and tests organization) than Selenium tests. As it 
comes to Selenium platform, I must admit that I was using it last time around 5 years ago, so my solution probably 
won't be breathtaking, but it works. :) 

Assumptions, improvements and comments
-------

1. Trello account:  
`Username: kamilgrzywinski@gmail.com`  
`Password: Plentific`
2. Trello key and token are hardcoded. Normally I wouldn't put them in code. I did it to simplify running tests by 
recruiters. Instead, I would place them in environmental variables (please check conftest.py line 8-10). 
3. I assumed that my Trello account on which tests are executed is hermetic environment. That means that in the 
meantime no one is using it nor creating there boards/lists/cards. Such acctions might impact tests results.
3. Before each test Trello Board is created and then after execution it is removed (for both API and Selenium tests)
4. My Atlassian account has limitation for 10 boards. It means that commenting `teardown_method` in API or Selenium 
tests might require manual removal of some boar(s) to make tests working properly (as I mentioned in point 3 my Trello 
account should be hermetic). PS. I could handle this situation in code, but its out of scope for this recruitments so 
I didn't do it.
