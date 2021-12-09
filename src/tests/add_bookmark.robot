*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Bookmark Page

*** Test Cases ***
Click Home Page Link
    Click Link  Home page
    Main Page Should Be Open

Select Book Updates Page
    Set Type  Book
    Page Should Contain  ISBN:

Add Valid Book Bookmark
    Set Title  test book
    Set Description  test
    Set Author  test
    Set ISBN  9783161484100
    Submit Bookmark
    Main Page Should Be Open
    Page Should Contain  test book

Add Book Bookmark Without Valid Title
    Set Description  test book2
    Set Author  test
    Set ISBN  9783161484100
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test book2

Add Book Bookmark Without Valid Description
    Set Title  test book3
    Set Author  test
    Set ISBN  9783161484100
    Submit Bookmark
    Verify Invalid Bookmark Not Added  test book3

Add Book Bookmark Without Valid Author
    Set Title  test book4
    Set Description  test
    Set ISBN  9783161484100
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test book4

Add Book Bookmark Without Valid ISBN
    Set Title  test book5
    Set Description  test
    Set Author  test
    Set ISBN  testitestitesti
    Submit Bookmark
    Page Should Contain  Invalid ISBN
    Verify Invalid Bookmark Not Added  test book5

Select Video Updates Page
    Set Type  Video
    Page Should Contain  Link:

Add Valid Video Bookmark
    Set Type  Video
    Set Title  test video
    Set Description  test
    Set Author  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Main Page Should Be Open

Add Video Bookmark Without Valid Title
    Set Type  Video
    Set Description  test video2
    Set Author  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test video2

Add Video Bookmark Without Valid Description
    Set Type  Video
    Set Title  test video3
    Set Author  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Verify Invalid Bookmark Not Added  test video3

Add Video Bookmark Without Valid Author
    Set Type  Video
    Set Title  test video4
    Set Description  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test video4

Select Blog Updates Page
    Set Type  Blog
    Page Should Contain  Link:

Add Valid Blog Bookmark
    Set Type  Blog
    Set Title  test blog
    Set Description  test
    Set Author  test
    Set Link  https://wikipedia.org/
    Submit Bookmark
    Main Page Should Be Open

Add Blog Bookmark Without Valid Title
    Set Type  Blog
    Set Description  test blog2
    Set Author  test
    Set Link  https://wikipedia.org/
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test blog2

Add Blog Bookmark Without Valid Description
    Set Type  Blog
    Set Title  test blog3
    Set Author  test
    Set Link  https://wikipedia.org/
    Submit Bookmark
    Verify Invalid Bookmark Not Added  test blog3

Add Blog Bookmark Without Valid Author
    Set Type  Blog
    Set Title  test blog4
    Set Description  test
    Set Link  https://wikipedia.org/
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test blog4

Select Podcast Updates Page
    Set Type  Podcast
    Page Should Contain  Episode:

Add Valid Podcast Bookmark
    Set Type  Podcast
    Set Title  test podcast
    Set Episode  1
    Set Description  test
    Set Author  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Main Page Should Be Open

Add Podcast Bookmark Without Valid Title
    Set Type  Podcast
    Set Description  test podcast2
    Set Episode  1
    Set Author  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test podcast2

Add Podcast Bookmark Without Valid Description
    Set Type  Podcast
    Set Title  test podcast3
    Set Episode  1
    Set Author  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Verify Invalid Bookmark Not Added  test podcast3

Add Podcast Bookmark Without Valid Author
    Set Type  Podcast
    Set Title  test podcast4
    Set Episode  1
    Set Description  test
    Set Link  https://youtube.com/
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test podcast4

Select Article Updates Page
    Set Type  Scientific Article
    Page Should Contain  Publication Title:

Add Valid Article Bookmark
    Set Type  Scientific Article
    Set Title  test article
    Set Publication Title  test
    Set Year  2000
    Set Doi  10.1000/182
    Set Publisher  test
    Set Description  test
    Set Author  test
    Submit Bookmark
    Main Page Should Be Open

Add Article Bookmark Without Valid Title
    Set Type  Scientific Article
    Set Publication Title  test
    Set Year  2000
    Set Doi  10.1000/182
    Set Publisher  test
    Set Description  test article2
    Set Author  test
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test article2

Add Article Bookmark Without Valid Description
    Set Type  Scientific Article
    Set Title  test article3
    Set Publication Title  test
    Set Year  2000
    Set Doi  10.1000/182
    Set Publisher  test
    Set Author  test
    Submit Bookmark
    Verify Invalid Bookmark Not Added  test article3

Add Article Bookmark Without Valid Author
    Set Type  Scientific Article
    Set Title  test article4
    Set Publication Title  test
    Set Year  2000
    Set Doi  10.1000/182
    Set Publisher  test
    Set Description  test
    Submit Bookmark
    Alert Should Be Present  Name must be between 1-50 characters
    Verify Invalid Bookmark Not Added  test article4

Creating New Tags Makes Them Usable
    Add Tag  Test Tag1
    Add Bookmark Page Should Be Open
    Page Should Contain  Test Tag1

Add Tags To Bookmark
    Add Tag  Test Tag2
    Set Title  tag test1
    Set Description  test
    Set Author  test
    Set ISBN  9783161484100
    Set Tag  Test Tag2
    Submit Bookmark
    Main Page Should Be Open
    Page Should Contain  tag test1
    Page Should Contain  Test Tag2

Add Multiple Tags To Bookmark
    Add Tag  Test Tag3
    Set Title  tag test2
    Set Description  test
    Set Author  test
    Set ISBN  9783161484100
    Set Tag  Test Tag1
    Set Tag  Test Tag3
    Submit Bookmark
    Main Page Should Be Open
    Page Should Contain  tag test2
    Page Should Contain  Test Tag1
    Page Should Contain  Test Tag2

*** Keywords ***
Submit Bookmark
    Click Button  submitBookmark

Set Type
    [Arguments]  ${name}
    Select From List By Label  bookmark  ${name}

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

Set Link
    [Arguments]  ${link}
    Input Text  link  ${link}

Set Episode
    [Arguments]  ${name}
    Input Text  episode  ${name}

Set Publication Title
    [Arguments]  ${name}
    Input Text  publication_title  ${name}

Set Year
    [Arguments]  ${number}
    Input Text  year  ${number}

Set Doi
    [Arguments]  ${doi}
    Input Text  doi  ${doi}

Set Publisher
    [Arguments]  ${name}
    Input Text  publisher  ${name}

Add Tag
    [Arguments]  ${name}
    Input Text  new_tag_name  ${name}
    Click Button  submitTag

Set Tag
    [Arguments]  ${name}
    Select Checkbox   xpath=//input[@id=(//label[text()="${name}"]/@for)]

Verify Invalid Bookmark Not Added
    [Arguments]  ${title}
    Add Bookmark Page Should Be Open
    Go To Main Page
    Page Should Not Contain  ${title}
