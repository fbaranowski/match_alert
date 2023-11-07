# Title
Functional requirements\
Date: `2023-10-24`

## Status

Accepted

## Context

We want to establish functional requirements for our project called match_alert

## Decision

We have setup assumptions as below:
1. Registration, logging, changing and resetting password
2. Use external API to make league table with points, match weeks played, goals*
3. Scheduling info about next matches with highlighting favourite teams
    - use external API to get info about next matches
    - use external API to get info about results from previous matches
4. Detail information about specific team
   - players and their stats
   - fun facts
   - history
   - schedule and results of this specific team*
## Consequences

1. We know what should be implemented in the project
2. Different types of Django applications are clear to do

## Keywords
- functional requirements
