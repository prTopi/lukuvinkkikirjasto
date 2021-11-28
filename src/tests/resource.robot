*** Settings ***
Library  SeleniumLibrary


*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0 seconds
${HOME URL}  http://${SERVER}
${ADD URL}  http://${SERVER}/add_bookmark

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}  options= add_argument("--no-sandbox"); add_argument("--disable-dev-shm-usage")
    Set Selenium Speed  ${DELAY}

Main Page Should Be Open
    Title Should Be  Lukuvinkkikirjasto

Add Bookmark Page Should Be Open
    Title Should Be  Add bookmark

Go to Main Page
    Go To  ${HOME URL}

Go to Add Bookmark Page
    Go To  ${ADD URL}
