*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Register Page And Log Out

*** Test Cases ***
Click Home Page Link
    Click Link  Home page
    Login Page Should Be Open

Register With Already Existing Username
    Set Username  testi
    Set Password  testi
    Set Password Confirmation  testi
    Submit Register
    Register Page Should Be Open
    Page Should Contain  Username taken

Register With Username Too Short
    Set Username  t
    Set Password  testi
    Set Password Confirmation  testi
    Submit Register
    Alert Should Be Present  Username must be between 2-20 characters.
    Register Page Should Be Open

Register With Username Too Long
    Set Username  123456789012345678901
    Set Password  testi
    Set Password Confirmation  testi
    Submit Register
    Alert Should Be Present  Username must be between 2-20 characters.
    Register Page Should Be Open

Register With Non Matching Password
    Set Username  testi3
    Set Password  testi2
    Set Password Confirmation  testi
    Submit Register
    Register Page Should Be Open
    Page Should Contain  Passwords not identical

Register With Password Too Short
    Set Username  testi3
    Set Password  test
    Set Password Confirmation  test
    Submit Register
    Alert Should Be Present  Password must be between 5-50 characters.
    Register Page Should Be Open

Register With Password Too Long
    Set Username  testi3
    Set Password  123456789012345678901234567890123456789012345678901
    Set Password Confirmation  123456789012345678901234567890123456789012345678901
    Submit Register
    Alert Should Be Present  Password must be between 5-50 characters.
    Register Page Should Be Open

Register With Valid Credentials
    Set Username  testi2
    Set Password  testi
    Set Password Confirmation  testi
    Submit Register
    Main Page Should Be Open

*** Keywords ***
Go To Register Page And Log Out
    Go To  ${LOGOUT URL}
    Go To Register Page

Submit Register
    Click Button  submitCreate

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Text  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Text  passwordConfirm  ${password}
