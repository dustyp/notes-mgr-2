# Notes Manager 2 Architecture

## Overview

The Notes Manager 2 project implements a system for extracting knowledge graphs from notes and managing project context. The architecture is designed to be modular, extensible, and focused on leveraging LLM capabilities through prompts rather than custom code.

## Core Components

### Context Management System

The context management system is responsible for maintaining and providing access to project context. It includes:

- **Snapshot System**: Hierarchical snapshots of project state at different detail levels
- **Context Manager**: Tools for loading and managing context with token budgeting
- **MCP Knowledge Graph Integration**: Integration with the MCP knowledge graph for enhanced context management

### Knowledge Graph Extraction

The knowledge graph extraction system is responsible for extracting structured information from unstructured notes. It includes:

- **Entity Extraction**: Identifying entities in notes using LLM prompts
- **Relationship Identification**: Identifying relationships between entities
- **Knowledge Graph Construction**: Building and maintaining the knowledge graph

### Multi-Agent Architecture

The multi-agent architecture enables collaboration between specialized AI agents. It includes:

- **Agent Management**: Tools for creating and managing agents
- **Messaging System**: Communication infrastructure for agents
- **Task Assignment**: Mechanisms for assigning tasks to appropriate agents

## Technical Decisions

### LLM-based Knowledge Graph Approach

- Using prompts instead of custom code for entity/relationship extraction
- Considering hybrid storage approaches for the knowledge graph
- Implementing entity merging and relationship identification via LLMs
- Supporting incremental knowledge graph construction with candidate promotion

### Multi-Agent Integration

- Assigned Heinz Doofenshmirtz (perpetual intern) to develop knowledge graph prompts
- Enhanced messaging system for agent communication with structured message types
- Using Claude Code CLI for agent activation and task processing
- Maintaining separation between agent management and project implementation

## Data Flow

1. Raw notes are processed through LLM prompts to extract entities and relationships
2. Extracted information is added to the knowledge graph
3. Context management system uses the knowledge graph to provide relevant context
4. Agents collaborate using the messaging system to perform tasks

## Future Extensions

- Integration with external sources (Slack, web content)
- Enhanced visualization of the knowledge graph
- Automated task generation based on knowledge graph insights