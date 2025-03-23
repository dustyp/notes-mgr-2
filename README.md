# Notes Manager 2

## Notes to Knowledge Graph to Executive Organization System

## Project Context Management

Obviously the most important learning was we need guardrails and rules up front and have to think about it from the get go. 

Rules
1. For every task the agent should reason if it is possibly destructive and then stop and make sure they highlight their concern and ask for permission to proceed. Think about deleting files either directly or indirectly with things like git reset from Github branches. 
2. Use git from the beginning as your backup so you can always roll back to a previous commit. Having a lot of data locally with no backup and letting an agent go HAM in there is a recipe for disaster. 
3. There is a need for a "team rules" type construct that applies to all character/agents and humans collaborating on the project. 
4. No need to fake Jira, just integrate the linear MCP from the beginning and establish the ticket-based workflow early so you can iterate. 

Knowledge Graph Milestones
- I can extract satisfactory expanding tag/category taxonomy and entity types, and relationships between them using just prompts. 
- I optimize the system to save money on LLM usage with local python development. 
- I connect to Slack and inventory all the links and contents I have stored in my DMs. 
- I follow the links with a web parser and then do the entity extraction and consider if there is a "content/notes" extraction as well
- At this point we should consider what we can use this knowledge graph for. 

Project Context Milestones
- I have a satisfactory observation log to record learnings, challenges, milestones, and insights to support writing about this journey/project in the future. 
- I have a rule set that I am building as I go that continually is applied to agent actions.
- I have a project context/plan where I am recording execution notes and challenges