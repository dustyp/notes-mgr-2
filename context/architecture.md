# Notes Manager 2 Architecture

## Overview

Notes Manager 2 is a system designed to extract, organize, and manage knowledge from various sources using a dynamic knowledge graph approach. The system prioritizes flexibility, LLM-based processing, and minimal custom code.

## Core Components

### Knowledge Graph
- **Entity Extraction**: LLM-based identification of entities from documents
- **Relationship Identification**: Prompt-based discovery of connections between entities
- **Candidate Management**: Tracking potential entities/relationships before promotion
- **Graph Storage**: Hybrid approach using MCP knowledge graph and local snapshots

### Context Management
- **Hierarchical Snapshots**: Multi-level context storage with varying detail
- **Token Budgeting**: Smart allocation of context tokens based on relevance
- **Context Loading**: Dynamic loading of project context with focus areas
- **MCP Integration**: Extension of context manager to work with MCP knowledge graph

### Multi-Agent Architecture
- **Agent Coordination**: System for managing multiple specialized agents
- **Agent Communication**: Structured message passing between agents
- **Role Specialization**: Agents with specific personalities and responsibilities
- **Memory Persistence**: Independent memory and context for each agent

## Technical Decisions

### LLM-First Approach
The system prioritizes LLM-based processing over custom code whenever possible:
- Using prompts for entity and relationship extraction
- Implementing entity merging via LLM reasoning
- Dynamically evolving taxonomy through LLM analysis

### Knowledge Graph Implementation
The knowledge graph is implemented using a hybrid approach:
- **MCP Knowledge Graph**: Primary storage for entities and relationships
- **Local Snapshots**: Point-in-time captures for persistence and sharing
- **Incremental Construction**: Building the graph progressively as documents are processed

### Context Management Strategy
Context is managed through a hierarchical system:
- **Detail Levels**: Summary, standard, and detailed views of context
- **Focus Areas**: Ability to prioritize specific aspects of context
- **Token Budgeting**: Smart allocation of context tokens based on importance

### Agent Integration
The multi-agent architecture is implemented through:
- **Separate Agent Directory**: Agents maintained in `/Users/aidan/_projects/ai-agents/`
- **Messaging System**: Communication via inbox.json/outbox.json files
- **Independent Sessions**: Each agent runs in its own LLM session
- **Specialized Roles**: Agents like Heinz Doofenshmirtz assigned to specific tasks

## Data Flow

1. **Document Processing**:
   - Documents are processed by LLMs to extract potential entities and relationships
   - Candidates are tracked and promoted based on significance or frequency

2. **Knowledge Graph Construction**:
   - Entities and relationships are added to the MCP knowledge graph
   - Graph is queried to discover connections and patterns

3. **Context Management**:
   - Context is loaded from the knowledge graph based on current needs
   - Token budgeting ensures efficient use of context window

4. **Agent Collaboration**:
   - Agents communicate through structured messages
   - Each agent maintains its own context and memory
   - Coordinator manages task assignment and result collection

## Implementation Status

The project is currently in the Knowledge Graph Extraction Design phase (25% complete):
- Context management system implemented
- MCP knowledge graph integration in progress
- Agent architecture established with initial prototype (Heinz)
- Prompt-based entity extraction approach defined

Next steps include:
- Finalizing knowledge graph extraction prompts
- Implementing entity merging and relationship identification
- Enhancing agent communication for knowledge graph tasks
- Developing workflow for incremental graph construction