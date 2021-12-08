*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Login Page And Log Out

*** Test Cases ***
Click Home Page Link
    Click Link  Home page
    Login Page Should Be Open

Login With Invalid Username
    Set Username  testi_notfound
    Set Password  testi
    Submit Login
    Login Page Should Be Open
    Page Should Contain  Username and password not matching

Login With Invalid Password
    Set Username  testi
    Set Password  testi2
    Submit Login
    Login Page Should Be Open
    Page Should Contain  Username and password not matching

Login With Valid Credentials
    Set Username  testi
    Set Password  testi
    Submit Login
    Main Page Should Be Open

*** Keywords ***
Go To Login Page And Log Out
    Go To  ${LOGOUT URL}
    Go To Login Page

Submit Login
    Click Button  submitLogin

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Text  password  ${password}
