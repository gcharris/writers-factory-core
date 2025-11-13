# Task: Build Intelligent Knowledge Router

**Priority**: High
**Assigned To**: Cloud Agent
**Estimated Time**: 3-4 hours
**Dependencies**: Storage/Session Management

---

## Context

You are building the Knowledge Router - an intelligent system that automatically routes queries to the most appropriate knowledge source (Cognee or NotebookLM) without requiring users to manually select which system to use.

**Key Architectural Decision**:
- **Cognee** runs automatically in the background, indexes all project files, and is NEVER exposed to users
- **NotebookLM** is optional, user-configured, and used for external writing advice/research
- **Gemini File Search** is NOT exposed to users (backend only, may be used internally by Cognee)

Users simply ask questions naturally, and the router intelligently sends queries to the right system.

---

## Design Philosophy

### Transparency Without Choice Paralysis

**Bad UX** (what we're avoiding):
```
User: "Who is Mickey Bardot?"
System: "Which knowledge base would you like to search?"
  1. Self Knowledge Graph (Cognee)
  2. NotebookLM
  3. Cloud Knowledge Graph
```

**Good UX** (what we're building):
```
User: "Who is Mickey Bardot?"
System: [Automatically routes to Cognee, returns answer]

Mickey Bardot is the protagonist of The Explants trilogy. She's a
former Las Vegas casino con artist and recovering addict who receives
a quantum neural implant...

Source: Project Knowledge
```

### Intelligent Routing Logic

**Query Classification**:

1. **Character/Plot Queries** → Cognee (fast, local, project-specific)
   - "Who is [character name]?"
   - "What happens in Chapter 5?"
   - "Describe the relationship between X and Y"
   - "What is [location/technology]?"

2. **Writing Technique Queries** → NotebookLM (if configured)
   - "How do I write compressed prose?"
   - "What are techniques for embedded philosophy?"
   - "How to write strong metaphors"
   - "Show me examples of present-tense narration"

3. **Hybrid Queries** → Both systems, merged results
   - "How should I write Mickey's voice in this scene?"
   - "What are the themes and how do I embed them?"

4. **Fallback** → Cognee (default for unclear queries)

---

## Architecture

### Knowledge Router Class

```python
# factory/core/knowledge/router.py
from typing import Optional, List
import asyncio

class KnowledgeRouter:
    """Intelligently route queries to appropriate knowledge systems"""

    def __init__(self, app: 'WritersFactory'):
        self.app = app
        self.cognee = app.cognee  # Always available
        self.notebooklm = app.notebooklm  # May be None if not configured

        # Query classifier
        self.classifier = QueryClassifier()

    async def query(self, query: str, context: Optional[Dict] = None) -> QueryResult:
        """
        Route query to best knowledge system(s)

        Args:
            query: Natural language question
            context: Optional context (current scene, character, etc.)

        Returns:
            QueryResult with answer and source attribution
        """

        # Classify query
        query_type = self.classifier.classify(query)

        # Route based on classification
        if query_type == QueryType.CHARACTER_LOOKUP:
            return await self._query_cognee(query, "character lookup")

        elif query_type == QueryType.PLOT_LOOKUP:
            return await self._query_cognee(query, "plot information")

        elif query_type == QueryType.WORLD_BUILDING:
            return await self._query_cognee(query, "worldbuilding")

        elif query_type == QueryType.WRITING_TECHNIQUE:
            if self.notebooklm and self.notebooklm.is_configured():
                return await self._query_notebooklm(query)
            else:
                # Fallback to Cognee if NotebookLM not available
                return await self._query_cognee(query, "general knowledge")

        elif query_type == QueryType.HYBRID:
            return await self._query_hybrid(query)

        else:
            # Default fallback
            return await self._query_cognee(query, "general knowledge")

    async def _query_cognee(self, query: str, category: str) -> QueryResult:
        """Query Cognee knowledge graph"""
        try:
            answer = await self.cognee.query(query)

            return QueryResult(
                query=query,
                answer=answer,
                source="Project Knowledge",
                source_detail="Local knowledge graph",
                confidence=0.9,
                cost=0.0  # Cognee is free/local
            )

        except Exception as e:
            return QueryResult(
                query=query,
                answer=f"Error querying knowledge base: {e}",
                source="Error",
                confidence=0.0,
                cost=0.0
            )

    async def _query_notebooklm(self, query: str) -> QueryResult:
        """Query NotebookLM for writing advice"""
        try:
            answer = await self.notebooklm.query(query)

            return QueryResult(
                query=query,
                answer=answer,
                source="NotebookLM",
                source_detail="External writing knowledge",
                confidence=0.85,
                cost=0.0  # NotebookLM is free
            )

        except Exception as e:
            # Fallback to Cognee on error
            return await self._query_cognee(query, "fallback")

    async def _query_hybrid(self, query: str) -> QueryResult:
        """Query both systems and merge results"""
        # Query both in parallel
        tasks = [
            self._query_cognee(query, "hybrid"),
        ]

        if self.notebooklm and self.notebooklm.is_configured():
            tasks.append(self._query_notebooklm(query))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Merge results
        merged_answer = self._merge_results(results)

        return QueryResult(
            query=query,
            answer=merged_answer,
            source="Multiple Sources",
            source_detail="Project Knowledge + NotebookLM",
            confidence=0.88,
            cost=0.0
        )

    def _merge_results(self, results: List[QueryResult]) -> str:
        """Merge multiple query results"""
        merged = ""

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                continue

            if i > 0:
                merged += "\n\n---\n\n"

            merged += f"**From {result.source}**:\n{result.answer}"

        return merged

    async def get_context_for_scene(self, outline: str) -> Dict[str, str]:
        """
        Get comprehensive context for scene generation

        Extracts entities from outline and queries KB for each
        """
        # Extract entities (characters, locations, etc.)
        entities = self._extract_entities(outline)

        context = {}

        for entity_type, entity_name in entities:
            query = self._build_entity_query(entity_type, entity_name)
            result = await self.query(query)
            context[entity_name] = result.answer

        return context

    def _extract_entities(self, text: str) -> List[tuple]:
        """
        Extract entities from text

        Returns: List of (entity_type, entity_name) tuples
        """
        entities = []

        # Simple extraction (can be enhanced with NLP)
        lines = text.split('\n')

        for line in lines:
            if 'Character:' in line or 'POV:' in line:
                char = line.split(':')[1].strip()
                entities.append(('character', char))

            elif 'Location:' in line:
                loc = line.split(':')[1].strip()
                entities.append(('location', loc))

        return entities

    def _build_entity_query(self, entity_type: str, entity_name: str) -> str:
        """Build appropriate query for entity type"""
        if entity_type == 'character':
            return f"Who is {entity_name}? Describe their personality, voice, and relationships."

        elif entity_type == 'location':
            return f"Describe {entity_name}. What happens there?"

        else:
            return f"Tell me about {entity_name}"
```

### Query Classifier

```python
# factory/core/knowledge/classifier.py
from enum import Enum
from typing import List
import re

class QueryType(Enum):
    CHARACTER_LOOKUP = "character"
    PLOT_LOOKUP = "plot"
    WORLD_BUILDING = "worldbuilding"
    WRITING_TECHNIQUE = "technique"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"

class QueryClassifier:
    """Classify queries to determine routing"""

    def __init__(self):
        self.patterns = {
            QueryType.CHARACTER_LOOKUP: [
                r"who is",
                r"describe .+ (character|personality|voice)",
                r"what does .+ (want|fear|believe)",
                r"relationship between",
                r"character profile",
            ],
            QueryType.PLOT_LOOKUP: [
                r"what happens in",
                r"summary of chapter",
                r"plot of",
                r"what occurs",
                r"scene where",
            ],
            QueryType.WORLD_BUILDING: [
                r"describe .+ (location|technology|world)",
                r"what is .+ (implant|quantum|morphic)",
                r"how does .+ work",
                r"setting of",
            ],
            QueryType.WRITING_TECHNIQUE: [
                r"how do i write",
                r"how to write",
                r"technique for",
                r"examples of",
                r"show me how",
                r"writing advice",
                r"craft of",
            ],
            QueryType.HYBRID: [
                r"how should i write .+ voice",
                r"write .+ in the style of",
                r"embed .+ theme",
            ]
        }

    def classify(self, query: str) -> QueryType:
        """Classify query type"""
        query_lower = query.lower()

        # Check patterns for each type
        for query_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return query_type

        # Default
        return QueryType.UNKNOWN
```

### Query Result Container

```python
# factory/core/knowledge/models.py
from dataclasses import dataclass

@dataclass
class QueryResult:
    """Result from knowledge query"""
    query: str
    answer: str
    source: str  # "Project Knowledge", "NotebookLM", "Multiple Sources"
    source_detail: str = ""
    confidence: float = 0.0
    cost: float = 0.0

    def format_for_display(self) -> str:
        """Format for terminal display"""
        return f"""
{self.answer}

Source: {self.source}
"""
```

---

## Cognee Integration

### Automatic Indexing

```python
# factory/core/knowledge/cognee_client.py
from pathlib import Path
import asyncio

class CogneeKnowledgeGraph:
    """
    Cognee knowledge graph client

    Automatically indexes project files and provides queries
    NEVER exposed to users - runs silently in background
    """

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.indexed_files: Set[Path] = set()

    async def initialize(self):
        """Initialize Cognee and index project"""
        # Auto-index reference materials
        await self._index_directory(self.project_path / "project" / "reference")

        # Auto-index existing manuscript
        await self._index_directory(self.project_path / "project" / "manuscript")

        # Auto-index planning docs
        await self._index_directory(self.project_path / "project" / "planning")

    async def _index_directory(self, directory: Path):
        """Recursively index directory"""
        if not directory.exists():
            return

        for file_path in directory.rglob("*.md"):
            if file_path not in self.indexed_files:
                await self._index_file(file_path)
                self.indexed_files.add(file_path)

    async def _index_file(self, file_path: Path):
        """Index a single file"""
        # Call Cognee indexing API
        # (Implementation depends on Cognee's actual API)
        pass

    async def query(self, query: str) -> str:
        """Query the knowledge graph"""
        # Call Cognee query API
        # (Implementation depends on Cognee's actual API)
        pass

    async def watch_for_changes(self):
        """Watch for new/modified files and auto-index"""
        # Use watchdog to monitor file changes
        watcher = ProjectFileWatcher(self.project_path)

        async for changed_file in watcher.watch():
            await self._index_file(changed_file)
```

---

## NotebookLM Integration

### Optional Configuration

```python
# factory/core/knowledge/notebooklm_client.py
from typing import Optional

class NotebookLMClient:
    """
    NotebookLM integration for external writing knowledge

    Optional - user configures during Creation Wizard or later
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config
        self._configured = config is not None and 'notebook_url' in config

    def is_configured(self) -> bool:
        """Check if NotebookLM is configured"""
        return self._configured

    async def configure(self, notebook_url: str):
        """Configure NotebookLM integration"""
        self.config = {
            'notebook_url': notebook_url,
            'api_key': None  # If NotebookLM requires auth
        }
        self._configured = True

    async def query(self, query: str) -> str:
        """Query NotebookLM notebook"""
        if not self.is_configured():
            raise ValueError("NotebookLM not configured")

        # Call NotebookLM API
        # (Implementation depends on NotebookLM's API)
        pass
```

---

## CLI Integration

### Query Command

```python
# In factory/core/commands.py

@cli.command()
@click.argument('query')
@click.option('--source', type=click.Choice(['auto', 'cognee', 'notebooklm']), default='auto')
@click.pass_obj
async def query(app: WritersFactory, query: str, source: str):
    """
    Query knowledge base

    Examples:
        ./factory.py query "Who is Mickey Bardot?"
        ./factory.py query "How do I write compressed prose?"
    """

    if source == 'auto':
        # Use intelligent routing
        result = await app.knowledge_router.query(query)
    elif source == 'cognee':
        result = await app.knowledge_router._query_cognee(query, "manual")
    elif source == 'notebooklm':
        result = await app.knowledge_router._query_notebooklm(query)

    # Display result
    app.console.print(f"\n[bold]{query}[/bold]\n")
    app.console.print(result.answer)
    app.console.print(f"\n[dim]Source: {result.source}[/dim]")

@cli.group()
def knowledge():
    """Knowledge base management"""
    pass

@knowledge.command()
@click.pass_obj
async def status(app: WritersFactory):
    """Show knowledge base status"""
    cognee_status = "✓ Active" if app.cognee else "✗ Not initialized"

    notebooklm_status = (
        "✓ Configured" if app.notebooklm.is_configured()
        else "○ Not configured (optional)"
    )

    app.console.print(f"""
[bold]Knowledge Base Status[/bold]

Project Knowledge: {cognee_status}
  └─ Auto-indexes: manuscript, reference, planning

NotebookLM: {notebooklm_status}
  └─ External writing knowledge (optional)
""")

@knowledge.command()
@click.option('--notebook-url', required=True)
@click.pass_obj
async def configure_notebooklm(app: WritersFactory, notebook_url: str):
    """Configure NotebookLM integration"""
    await app.notebooklm.configure(notebook_url)

    app.console.print("[green]✓ NotebookLM configured successfully[/green]")

@knowledge.command()
@click.pass_obj
async def reindex(app: WritersFactory):
    """Reindex all project files"""
    app.console.print("[yellow]Reindexing knowledge base...[/yellow]")

    await app.cognee.initialize()

    app.console.print("[green]✓ Reindexing complete[/green]")
```

---

## UI Integration

### Query Input Component

```python
# factory/core/ui/components/query_input.py
from rich.console import Console
from rich.panel import Panel

class QueryInputComponent:
    """Interactive query input with live results"""

    def __init__(self, app: 'WritersFactory'):
        self.app = app
        self.console = Console()

    async def run(self):
        """Run interactive query session"""
        self.console.print("[bold]Knowledge Query[/bold]")
        self.console.print("Ask any question about your project or writing craft.")
        self.console.print("Type 'exit' to quit.\n")

        while True:
            query = self.console.input("[cyan]Query:[/cyan] ")

            if query.lower() in ['exit', 'quit', 'q']:
                break

            if not query.strip():
                continue

            # Show loading indicator
            with self.console.status("[yellow]Searching...[/yellow]"):
                result = await self.app.knowledge_router.query(query)

            # Display result
            panel = Panel(
                result.answer,
                title=f"Answer (from {result.source})",
                border_style="green"
            )

            self.console.print(panel)
            self.console.print()
```

---

## File Structure

```
factory/core/knowledge/
├── __init__.py
├── router.py                   # KnowledgeRouter class
├── classifier.py               # QueryClassifier, QueryType
├── models.py                   # QueryResult
├── cognee_client.py            # CogneeKnowledgeGraph
└── notebooklm_client.py        # NotebookLMClient

factory/core/ui/components/
├── query_input.py              # QueryInputComponent
```

---

## Success Criteria

Your implementation should enable:

1. ✅ Users query naturally without choosing knowledge system
2. ✅ Cognee runs silently, never mentioned to users
3. ✅ NotebookLM is optional, configurable in wizard
4. ✅ Query routing is accurate (>90% correct classification)
5. ✅ Results clearly show source attribution
6. ✅ Hybrid queries merge results intelligently
7. ✅ Fallback to Cognee if NotebookLM unavailable
8. ✅ Context retrieval for scene generation works seamlessly
9. ✅ Auto-indexing keeps Cognee up-to-date
10. ✅ CLI query command is fast and intuitive

---

## Testing Strategy

### Unit Tests

```python
# test_classifier.py
def test_character_query_classification():
    classifier = QueryClassifier()
    query = "Who is Mickey Bardot?"
    assert classifier.classify(query) == QueryType.CHARACTER_LOOKUP

def test_technique_query_classification():
    classifier = QueryClassifier()
    query = "How do I write compressed prose?"
    assert classifier.classify(query) == QueryType.WRITING_TECHNIQUE

# test_router.py
@pytest.mark.asyncio
async def test_router_cognee_query():
    router = KnowledgeRouter(mock_app)
    result = await router.query("Who is Mickey?")

    assert result.source == "Project Knowledge"
    assert "Mickey" in result.answer

@pytest.mark.asyncio
async def test_router_fallback():
    # NotebookLM not configured
    router = KnowledgeRouter(mock_app)
    router.notebooklm = None

    result = await router.query("How to write metaphors?")

    # Should fallback to Cognee
    assert result.source == "Project Knowledge"
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_end_to_end_query():
    app = WritersFactory(test_project_path)
    await app.start()

    result = await app.knowledge_router.query("Who is Mickey Bardot?")

    assert result.answer
    assert result.source in ["Project Knowledge", "NotebookLM"]
```

---

## Deliverables

1. **KnowledgeRouter** - Main routing class
2. **QueryClassifier** - Query type classification
3. **CogneeKnowledgeGraph** - Cognee integration with auto-indexing
4. **NotebookLMClient** - Optional NotebookLM integration
5. **CLI Commands** - Query, status, configuration
6. **UI Component** - Interactive query interface
7. **Tests** - Unit and integration tests
8. **Documentation** - Architecture guide, usage examples

---

## Questions? Clarifications Needed?

If any requirements are unclear, document your assumptions and proceed. Focus on creating an intelligent, transparent system that routes queries without user intervention.
