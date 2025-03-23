# Notes Manager 2 Project Rules

## Core Project Rules

### Dynamic Taxonomy Development
- Build taxonomy dynamically as documents are processed
- Update prompts with new entity/relationship types as discovered
- Allow for taxonomy evolution based on content patterns

### Code Minimalism
- Only write Python (or other code) if absolutely necessary
- Keep all code as short and simple as possible
- Prefer LLM-based processing over complex code when feasible

### Entity Management
- Track entity/relationship 'candidates' before promotion to full status
- Require multiple appearances or significance threshold for promotion
- Consider approach for retroactive identification when new entities are found

### Context Preservation
- Maintain structured snapshots of project state
- Document all significant decisions and their rationale
- Ensure knowledge continuity between AI assistant sessions

### Observation Separation
- Keep meta-observations about the project in separate location
- Store observations in `~/_projects/ai-workflow/observations.md`
- Use observations to inform project improvements without cluttering implementation

## Agent Behavior Rules

### Safety First
- For every task, reason if it is possibly destructive
- Highlight concerns and ask for permission before proceeding with potentially destructive actions
- Be especially cautious with file deletion operations or git commands like reset

### Version Control
- Use git from the beginning as backup
- Commit changes frequently to allow rollback if needed
- Never perform destructive git operations without explicit permission

### Multi-Agent Architecture
- Follow team rules that apply to all characters/agents and humans collaborating on the project
- Maintain separation between agent management and project implementation
- Respect the distinct personalities and roles of different agents (like Heinz Doofenshmirtz)

### Workflow Management
- Use Linear MCP for ticket-based workflow
- Establish ticket-based workflow early to enable iteration
- Document all significant decisions and their rationale

## Implementation Rules

### Knowledge Graph Approach
- Use prompts instead of custom code for entity/relationship extraction
- Implement entity merging and relationship identification via LLMs
- Support incremental knowledge graph construction with candidate promotion

### Agent Communication
- Use structured message types for agent communication
- Maintain separation between agent management and project implementation
- Follow the established messaging system for agent communication

### Project Progress
- Focus on prompt-based knowledge graph extraction
- Minimize custom code and support flexible entity types
- Document all progress and challenges in the appropriate location