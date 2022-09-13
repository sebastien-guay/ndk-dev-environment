*** Settings ***
Library     srl.py
Library     SSHLibrary
Library     String

*** Test Cases ***

Test agent running
    Wait Until Keyword Succeeds     30x     1s  
    ...    Agent Should Run

Test agent stop
    Stop Agent
    Wait Until Keyword Succeeds     30x     1s  
    ...    Agent Should Not Run
    Sleep    5

Test agent start
    Start Agent
    Wait Until Keyword Succeeds     30x     1s  
    ...    Agent Should Run
    Sleep    5

Test set name and check greeting
    ${name}    Set Variable    agent007
    Set Agent Name    ${name}
    Sleep    5
    ${result}=    Get Greeting
    Should Contain    ${result}    Hello ${name}, my uptime is  

*** Keywords ***

Agent Should Run
    ${result}=    Get Agent Status
    Should Be Equal    ${result}    running

Agent Should Not Run
    ${result}=    Get Agent Status
    Should Not Be Equal    ${result}    running