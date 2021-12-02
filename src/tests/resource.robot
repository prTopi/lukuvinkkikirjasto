*** Settings ***
Library  SeleniumLibrary


*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0 seconds
${HOME URL}  http://${SERVER}
${ADD URL}  http://${SERVER}/add_bookmark
${LOGIN URL}  http://${SERVER}/login
${LOGOUT URL}  http://${SERVER}/logout
${CREATE URL}  http://${SERVER}/create

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}  options= add_argument("--no-sandbox"); add_argument("--disable-dev-shm-usage")
    Set Selenium Speed  ${DELAY}
    Go To  ${LOGIN URL}
    Input Text  username  testi
    Input Text  password  testi
    Click Button  submitLogin

Main Page Should Be Open
    Title Should Be  Lukuvinkkikirjasto

Add Bookmark Page Should Be Open
    Title Should Be  Add bookmark

Login Page Should Be Open
    Title Should Be  Log In

Register Page Should Be Open
    Title Should Be  Create Account

Go to Main Page
    Go To  ${HOME URL}

Go to Add Bookmark Page
    Go To  ${ADD URL}

Go to Login Page
    Go To  ${LOGIN URL}

Go to Register Page
    Go To  ${CREATE URL}
