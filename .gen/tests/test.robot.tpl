*** Settings ***
Library     srl.py
Library     SSHLibrary
Library     String

*** Keywords ***

Write SRL Command
    [Arguments]         ${cmd}

    ${tmp}=             Write               ${cmd}
    ${out}=             Read Until          [admin@srl2 ~]$
    [return]            ${out}

Open SRL Bash
    Open Connection     clab-{{ getenv "APPNAME" }}-dev-srl1    width=500
    Login               admin      admin
    Write               bash
    Read Until          [admin@srl1 ~]$

Agent Should Run
    ${result}=              get_agent_status
    Should Be Equal         ${result}   running


*** Test Cases ***
Test agent running
    Agent Should Run