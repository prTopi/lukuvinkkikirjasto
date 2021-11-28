*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Bookmark Page

*** Test Cases ***
Click Home Page Link
    Click Link  Home page
    Main Page Should Be Open

Add Valid Book Bookmark
    Set Title  test book
    Set Description  test
    Set Author  test
    Set ISBN  test
    Submit Bookmark
    Main Page Should Be Open
    Page Should Contain  test book

Add Book Bookmark Without Valid Title
    Set Description  test book2
    Set Author  test
    Set ISBN  test
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test book2

Add Book Bookmark Without Valid Description
    Set Title  test book3
    Set Author  test
    Set ISBN  test
    Submit Bookmark
    Verify Invalid Bookmark Not Added  test book3

Add Book Bookmark Without Valid Author
    Set Title  test book4
    Set Description  test
    Set ISBN  test
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test book4

*** Keywords ***
Submit Bookmark
    Click Button  submitBookmark

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Description
    [Arguments]  ${description}
    Input Text  description  ${description}

Set Author
    [Arguments]  ${author}
    Input Text  author  ${author}

Set ISBN
    [Arguments]  ${isbn}
    Input Text  ISBN  ${isbn}

Set Video
    Click Button  typeVideo

Set Link
    [Arguments]  ${link}
    Input Text  link  ${link}

Verify Invalid Bookmark Not Added
    [Arguments]  ${title}
    Add Bookmark Page Should Be Open
    Go To Main Page
    Page Should Not Contain  ${title}
