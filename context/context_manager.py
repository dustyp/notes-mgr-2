#!/usr/bin/env python3
"""
Context Manager for Notes Manager 2

This module provides functions for loading and managing project context
from the hierarchical snapshot system. It supports different context types,
detail levels, and token budgeting.
"""

import os
import json
import datetime
from pathlib import Path
import re

# Base directory for context
CONTEXT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Default token budgets for different context components
DEFAULT_TOKEN_BUDGETS = {
    "minimal": {
        "readme": 500,
        "architecture": 1000,
        "glossary": 500,
        "snapshots": 1000,
        "total": 3000
    },
    "standard": {
        "readme": 1000,
        "architecture": 2000,
        "glossary": 1000,
        "snapshots": 4000,
        "total": 8000
    },
    "comprehensive": {
        "readme": 2000,
        "architecture": 3000,
        "glossary": 2000,
        "snapshots": 8000,
        "total": 15000
    }
}

# Snapshot type priorities (order of importance)
SNAPSHOT_TYPE_PRIORITIES = ["general", "architecture", "knowledge_graph", "workflow"]

# Important section keywords for prioritization
IMPORTANT_SECTIONS = {
    "general": ["Status Summary", "Active Components", "Current Challenges"],
    "architecture": ["Architecture Overview", "Component Structure", "Technical Decisions"],
    "knowledge_graph": ["Graph Schema", "Entity Types", "Relationship Types"],
    "workflow": ["User Workflows", "Data Processing Pipeline", "Note Management Procedures"]
}

def estimate_tokens(text):
    """Estimate the number of tokens in a text (rough approximation)"""
    # A very simple approximation: ~4 characters per token for English text
    return len(text) // 4

def truncate_to_token_budget(text, budget, preserve_sections=None):
    """
    Truncate text to fit within token budget while preserving important sections
    
    Args:
        text (str): The text to truncate
        budget (int): Token budget
        preserve_sections (list): List of section titles to prioritize
        
    Returns:
        str: Truncated text
    """
    if estimate_tokens(text) <= budget:
        return text
    
    # If no sections to preserve, simple truncation
    if not preserve_sections:
        # Estimate characters based on token budget (4 chars per token)
        char_budget = budget * 4
        return text[:char_budget] + "\n\n[Content truncated due to token budget]"
    
    # Split text into sections
    sections = []
    current_section = {"title": "Header", "content": "", "priority": 0}
    
    for line in text.split('\n'):
        if line.startswith('## '):
            # Save previous section
            sections.append(current_section)
            
            # Start new section
            section_title = line[3:].strip()
            priority = 2 if section_title in preserve_sections else 1
            current_section = {"title": section_title, "content": line + '\n', "priority": priority}
        else:
            current_section["content"] += line + '\n'
    
    # Add the last section
    sections.append(current_section)
    
    # Sort sections by priority (high to low)
    sections.sort(key=lambda x: x["priority"], reverse=True)
    
    # Allocate tokens to sections based on priority
    result = ""
    remaining_budget = budget
    
    # First pass: include high priority sections
    for section in [s for s in sections if s["priority"] == 2]:
        section_tokens = estimate_tokens(section["content"])
        if section_tokens <= remaining_budget:
            result += section["content"]
            remaining_budget -= section_tokens
        else:
            # Truncate section to fit
            char_budget = remaining_budget * 4
            result += section["content"][:char_budget] + "\n\n[Section truncated due to token budget]\n\n"
            remaining_budget = 0
            break
    
    # Second pass: include medium priority sections if budget remains
    if remaining_budget > 0:
        for section in [s for s in sections if s["priority"] == 1]:
            section_tokens = estimate_tokens(section["content"])
            if section_tokens <= remaining_budget:
                result += section["content"]
                remaining_budget -= section_tokens
            else:
                # Truncate section to fit
                char_budget = remaining_budget * 4
                result += section["content"][:char_budget] + "\n\n[Section truncated due to token budget]\n\n"
                remaining_budget = 0
                break
    
    # Third pass: include low priority sections if budget remains
    if remaining_budget > 0:
        for section in [s for s in sections if s["priority"] == 0]:
            section_tokens = estimate_tokens(section["content"])
            if section_tokens <= remaining_budget:
                result += section["content"]
                remaining_budget -= section_tokens
            else:
                # Truncate section to fit
                char_budget = remaining_budget * 4
                result += section["content"][:char_budget] + "\n\n[Section truncated due to token budget]\n\n"
                remaining_budget = 0
                break
    
    return result

def get_latest_snapshot(snapshot_type, hierarchy_level="standard"):
    """
    Get the latest snapshot of a specific type and hierarchy level
    
    Args:
        snapshot_type (str): Type of snapshot (general, architecture, etc.)
        hierarchy_level (str): Hierarchy level (summary, standard, detailed)
        
    Returns:
        tuple: (path to snapshot, snapshot content)
    """
    snapshot_dir = CONTEXT_DIR / "snapshots" / snapshot_type / hierarchy_level
    
    if not snapshot_dir.exists():
        return None, f"No snapshots found for type '{snapshot_type}' at level '{hierarchy_level}'"
    
    # Find the latest snapshot file
    snapshot_files = list(snapshot_dir.glob("*.md"))
    if not snapshot_files:
        return None, f"No snapshots found for type '{snapshot_type}' at level '{hierarchy_level}'"
    
    # Sort by modification time (newest first)
    latest_snapshot = max(snapshot_files, key=lambda p: p.stat().st_mtime)
    
    # Read the content
    with open(latest_snapshot, 'r') as f:
        content = f.read()
    
    return latest_snapshot, content

def load_readme(token_budget=1000):
    """Load the project README with token budget"""
    readme_path = CONTEXT_DIR.parent / "README.md"
    
    if not readme_path.exists():
        return "README not found"
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    return truncate_to_token_budget(content, token_budget)

def load_architecture(token_budget=2000):
    """Load the architecture document with token budget"""
    architecture_path = CONTEXT_DIR / "architecture.md"
    
    if not architecture_path.exists():
        return "Architecture document not found"
    
    with open(architecture_path, 'r') as f:
        content = f.read()
    
    return truncate_to_token_budget(content, token_budget)

def load_glossary(token_budget=1000):
    """Load the glossary document with token budget"""
    glossary_path = CONTEXT_DIR / "glossary.md"
    
    if not glossary_path.exists():
        return "Glossary not found"
    
    with open(glossary_path, 'r') as f:
        content = f.read()
    
    return truncate_to_token_budget(content, token_budget)

def load_snapshots(detail_level="standard", snapshot_types=None, token_budget=4000):
    """
    Load project snapshots based on detail level and types
    
    Args:
        detail_level (str): Level of detail (minimal, standard, comprehensive)
        snapshot_types (list): Types of snapshots to include (defaults to all in priority order)
        token_budget (int): Token budget for snapshots
        
    Returns:
        str: Formatted snapshot content
    """
    # If no snapshot types specified, use all in priority order
    if snapshot_types is None:
        snapshot_types = SNAPSHOT_TYPE_PRIORITIES
    
    # Map detail level to hierarchy level
    hierarchy_level_map = {
        "minimal": "summary",
        "standard": "standard",
        "comprehensive": "detailed"
    }
    
    hierarchy_level = hierarchy_level_map.get(detail_level, "standard")
    
    # Load snapshots
    snapshots = []
    
    for snapshot_type in snapshot_types:
        snapshot_path, snapshot_content = get_latest_snapshot(snapshot_type, hierarchy_level)
        
        if snapshot_path:
            snapshots.append({
                "type": snapshot_type,
                "path": snapshot_path,
                "content": snapshot_content,
                "tokens": estimate_tokens(snapshot_content)
            })
    
    # Sort snapshots by priority
    snapshots.sort(key=lambda x: SNAPSHOT_TYPE_PRIORITIES.index(x["type"]) if x["type"] in SNAPSHOT_TYPE_PRIORITIES else 999)
    
    # Format snapshots within token budget
    result = "# Project Snapshots\n\n"
    remaining_budget = token_budget
    
    for snapshot in snapshots:
        # Check if we have budget for this snapshot
        if remaining_budget <= 0:
            break
        
        # Add snapshot header
        snapshot_header = f"## {snapshot['type'].capitalize()} Snapshot\n\n"
        header_tokens = estimate_tokens(snapshot_header)
        
        if header_tokens <= remaining_budget:
            result += snapshot_header
            remaining_budget -= header_tokens
        else:
            break
        
        # Add snapshot content with truncation if needed
        important_sections = IMPORTANT_SECTIONS.get(snapshot["type"], [])
        truncated_content = truncate_to_token_budget(snapshot["content"], remaining_budget, important_sections)
        result += truncated_content + "\n\n"
        
        # Update remaining budget
        remaining_budget -= estimate_tokens(truncated_content)
    
    return result

def load_project_context(detail_level="standard", focus_area=None, max_tokens=8000):
    """
    Load project context based on detail level and focus area
    
    Args:
        detail_level (str): Level of detail (minimal, standard, comprehensive)
        focus_area (str): Area to focus on (general, architecture, knowledge_graph, agent)
        max_tokens (int): Maximum tokens for the entire context
        
    Returns:
        str: Formatted project context
    """
    # Get token budgets based on detail level
    token_budgets = DEFAULT_TOKEN_BUDGETS.get(detail_level, DEFAULT_TOKEN_BUDGETS["standard"])
    
    # Adjust token budgets based on focus area
    if focus_area:
        # Increase budget for the focus area
        focus_budget_multiplier = 2.0
        
        if focus_area == "general":
            token_budgets["readme"] = int(token_budgets["readme"] * focus_budget_multiplier)
        elif focus_area == "architecture":
            token_budgets["architecture"] = int(token_budgets["architecture"] * focus_budget_multiplier)
        elif focus_area in ["knowledge_graph", "workflow", "agent"]:
            token_budgets["snapshots"] = int(token_budgets["snapshots"] * focus_budget_multiplier)
    
    # Ensure total budget doesn't exceed max_tokens
    total_budget = sum(token_budgets.values())
    if total_budget > max_tokens:
        # Scale down all budgets proportionally
        scale_factor = max_tokens / total_budget
        for key in token_budgets:
            if key != "total":
                token_budgets[key] = int(token_budgets[key] * scale_factor)
        token_budgets["total"] = max_tokens
    
    # Load context components
    context = "# Notes Manager 2 Project Context\n\n"
    context += f"*Context loaded at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    # Load README
    readme_content = load_readme(token_budgets["readme"])
    context += "## Project Overview\n\n" + readme_content + "\n\n"
    
    # Load architecture document
    architecture_content = load_architecture(token_budgets["architecture"])
    context += "## Architecture\n\n" + architecture_content + "\n\n"
    
    # Load glossary
    glossary_content = load_glossary(token_budgets["glossary"])
    context += "## Glossary\n\n" + glossary_content + "\n\n"
    
    # Load snapshots based on focus area
    snapshot_types = None
    if focus_area and focus_area in SNAPSHOT_TYPE_PRIORITIES:
        # Prioritize the focus area snapshot
        snapshot_types = [focus_area] + [st for st in SNAPSHOT_TYPE_PRIORITIES if st != focus_area]
    
    snapshots_content = load_snapshots(detail_level, snapshot_types, token_budgets["snapshots"])
    context += snapshots_content
    
    return context

def get_available_snapshot_types():
    """Get list of available snapshot types"""
    snapshot_dir = CONTEXT_DIR / "snapshots"
    
    if not snapshot_dir.exists():
        return []
    
    return [d.name for d in snapshot_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

def get_available_hierarchy_levels():
    """Get list of available hierarchy levels"""
    return ["summary", "standard", "detailed"]

def get_context_summary(detail_level="standard", focus_area=None):
    """
    Get a summary of available context
    
    Args:
        detail_level (str): Level of detail (minimal, standard, comprehensive)
        focus_area (str): Area to focus on (general, architecture, knowledge_graph, agent)
        
    Returns:
        dict: Summary of available context
    """
    # Map detail level to hierarchy level
    hierarchy_level_map = {
        "minimal": "summary",
        "standard": "standard",
        "comprehensive": "detailed"
    }
    
    hierarchy_level = hierarchy_level_map.get(detail_level, "standard")
    
    # Get available snapshot types
    snapshot_types = get_available_snapshot_types()
    
    # Get snapshot information
    snapshots = []
    
    for snapshot_type in snapshot_types:
        snapshot_path, _ = get_latest_snapshot(snapshot_type, hierarchy_level)
        
        if snapshot_path:
            # Get modification time
            mod_time = snapshot_path.stat().st_mtime
            mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            
            snapshots.append({
                "type": snapshot_type,
                "path": str(snapshot_path),
                "last_updated": mod_time_str
            })
    
    # Check for README, architecture, and glossary
    readme_path = CONTEXT_DIR.parent / "README.md"
    architecture_path = CONTEXT_DIR / "architecture.md"
    glossary_path = CONTEXT_DIR / "glossary.md"
    
    documents = []
    
    if readme_path.exists():
        mod_time = readme_path.stat().st_mtime
        mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        documents.append({
            "type": "readme",
            "path": str(readme_path),
            "last_updated": mod_time_str
        })
    
    if architecture_path.exists():
        mod_time = architecture_path.stat().st_mtime
        mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        documents.append({
            "type": "architecture",
            "path": str(architecture_path),
            "last_updated": mod_time_str
        })
    
    if glossary_path.exists():
        mod_time = glossary_path.stat().st_mtime
        mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        documents.append({
            "type": "glossary",
            "path": str(glossary_path),
            "last_updated": mod_time_str
        })
    
    return {
        "detail_level": detail_level,
        "hierarchy_level": hierarchy_level,
        "focus_area": focus_area,
        "documents": documents,
        "snapshots": snapshots
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Notes Manager 2 Context Manager")
    parser.add_argument("--detail", choices=["minimal", "standard", "comprehensive"], default="standard", help="Detail level")
    parser.add_argument("--focus", help="Focus area")
    parser.add_argument("--tokens", type=int, default=8000, help="Maximum tokens")
    parser.add_argument("--summary", action="store_true", help="Get context summary")
    
    args = parser.parse_args()
    
    if args.summary:
        summary = get_context_summary(args.detail, args.focus)
        print(json.dumps(summary, indent=2))
    else:
        context = load_project_context(args.detail, args.focus, args.tokens)
        print(context)