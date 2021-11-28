*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Click Home Page Link
    Click Link  Home page
    Main Page Should Be Open

Click Add Bookmark Link
    Click Link  Add bookmark
    Add Bookmark Page Should Be Open
