# Facebook's public posts crawler example
Since FB discontinued their API for searching through public posts,
this is an example how to circumvent that limitation with simulating an
user. Here Selenium is used.

Since navigating FB with Selenium is tedious due to FB generating selectors
on their backend, found selectors and tricks might help you in your related
FB projects. Note that due to said problems, simple timeouts were used
instead of researching which element has to be loaded in order to complete
the AJAX call.

## Dependencies
+ chromedriver
+ chrome profile with the user already logged in
+ python dependencies from requirements.txt

## Usage
Setup your virtual environment and start the script:
$python fb_automation
