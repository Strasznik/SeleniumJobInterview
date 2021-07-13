Trello Selenium/API Job Interview
==============================

What Is This?
-------------

This is a demo Python testing framework created for job interviews.

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

I based this whole "framework" (including negative cases) on API level tests and these tests are much more polished (as it comes to technical implementation and tests organization) than Selenium tests. 
As it comes to Selenium platform, I must admit that I was using it last time around 5 years ago, so my solution probably won't be breathtaking, but it works. :) 

Assumptions, improvements and comments
-------

1. Trello account:  
`Username: XXX`  
`Password: YYY`
2. Trello key and token are hardcoded must be delivered in system environmental variables (TRELLO_KEY, TRELLO_TOKEN)
3. I assumed that my Trello account on which tests are executed is hermetic environment. That means that in the 
meantime no one is using it nor creating there boards/lists/cards. Such acctions might impact tests results.
3. Before each test Trello Board is created and then after execution it is removed (for both API and Selenium tests)
