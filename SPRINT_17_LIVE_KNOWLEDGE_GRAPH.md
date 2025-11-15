# Sprint 17: Live Knowledge Graph - Incremental Updates & Queries

**Date:** November 15, 2025
**Priority:** HIGH - Core feature for ongoing continuity tracking
**Timeline:** 2-3 weeks
**Dependencies:** Sprint 16 (Multi-Notebook Management) ✅ Complete

---

## Mission: Make Knowledge Graph Continuous & Queryable 🎯

**Current Problem:**
- Knowledge graph exists (Sprint 13) but is built ONCE at manuscript analysis time
- NOT updated as you write new scenes
- NO query interface exposed during writing
- You can't ask "Has Mickey been to this location before?" while writing

**Sprint 17 Solution:**
- Update knowledge graph incrementally on every scene save
- Add "Ask Your Novel" query interface in scene editor
- Real-time continuity checking while writing
- Nightly batch verification (full re-extraction)

**User Experience:**
```
While writing Scene 47:
[Ask Your Novel] "Has Mickey been to The Hotel before?"

System queries knowledge graph →
"Yes, Mickey appeared at The Hotel in 3 previous scenes:
 • Scene 12 (Chapter 2): First encounter with Chronicler
 • Scene 23 (Chapter 5): Returns for information
 • Scene 31 (Chapter 7): Confrontation in lobby"

[Insert Reference] [Continue Writing]
```

---

## Your Original Vision (From Earlier Conversation)

> "The original idea was that ongoing information being created would be thrown into this knowledge graph and could be queried for things as one was writing."

**This is EXACTLY what Sprint 17 builds!**

---

## What Already Exists (Sprint 13)

### Knowledge Graph Components ✅

**File:** `factory/analysis/knowledge_graph.py`

**Classes:**
```python
class NovelKnowledgeGraph:
    """Knowledge graph for novel universe."""

    def add_node(node_type, name, attributes, metadata) -> str
    def add_edge(edge_type, source_id, target_id, attributes, weight) -> str
    def populate_from_entities(characters, locations, plot_threads, motifs)
    def query_connections(node_id, max_depth=2) -> Dict
    def export_json(output_path) -> Dict
```

**Node Types:**
- `character` - Characters with traits, psychology, arcs
- `location` - Settings, world details
- `plot_thread` - Main plot and subplots
- `motif` - Recurring images, symbols
- `event` - Specific plot events

**Edge Types:**
- `relationship` - Character-to-character relationships
- `appears_at` - Character appears at location
- `participates_in` - Character in plot thread
- `timeline` - Sequential events
- `causality` - Cause-and-effect chains

### Entity Extraction (Sprint 13) ✅

**Agents that extract entities from manuscript:**
- `CharacterExtractor` - Names, aliases, traits, psychology
- `LocationExtractor` - Settings, world details
- `PlotThreadTracker` - Main plot, subplots, resolution
- `MotifAnalyzer` - Recurring images, symbols, themes
- `TimelineBuilder` - Sequence of events
- `DialogueAnalyzer` - Character voice distinctness

**Current Usage:**
1. Upload complete manuscript
2. Run all 6 extractors in parallel
3. Populate knowledge graph from extracted entities
4. Export to JSON
5. Use for analysis/reports

**Problem:** One-time build only. Not updated as you write.

---

## What's Missing (Sprint 17 Adds)

### 1. Incremental Updates ❌

**Need:** Update graph on every scene save

```python
# Every time user saves a scene
async def on_scene_save(project_id: str, scene_id: str, scene_text: str):
    """Update knowledge graph with new scene."""
    # Mini extraction (just this scene)
    entities = await extract_entities_from_scene(scene_text)

    # Load existing graph
    graph = load_knowledge_graph(project_id)

    # Merge new entities
    graph.merge_entities(entities)

    # Save updated graph
    save_knowledge_graph(project_id, graph)
```

### 2. Query Interface ❌

**Need:** "Ask Your Novel" input in scene editor

```python
# User asks while writing
query = "Has Mickey been to The Hotel before?"

# System queries graph
results = graph.query_natural_language(query)

# Returns relevant scenes
{
    "answer": "Yes, 3 previous appearances",
    "scenes": [
        {"scene_id": "scene-12", "chapter": "Chapter 2", "summary": "..."},
        {"scene_id": "scene-23", "chapter": "Chapter 5", "summary": "..."},
        {"scene_id": "scene-31", "chapter": "Chapter 7", "summary": "..."}
    ]
}
```

### 3. Natural Language Queries ❌

**Need:** Parse questions and map to graph queries

**Question Types:**
- **Location history:** "Has [character] been to [location]?"
- **Character interactions:** "Have [character1] and [character2] met?"
- **Plot threads:** "Is the [subplot] resolved?"
- **Timeline:** "When did [event] happen?"
- **Motif tracking:** "How many times is [motif] used?"

### 4. Nightly Verification ❌

**Need:** Full re-extraction to catch incremental errors

```python
# Runs nightly at 2am
async def verify_knowledge_graph(project_id: str):
    """Re-extract entire manuscript and compare with incremental graph."""

    # Full extraction (all scenes)
    full_graph = await extract_full_graph(project_id)

    # Load incremental graph
    incremental_graph = load_knowledge_graph(project_id)

    # Compare and fix discrepancies
    discrepancies = compare_graphs(full_graph, incremental_graph)

    if discrepancies:
        # Log differences
        log_discrepancies(project_id, discrepancies)

        # Replace with full graph
        save_knowledge_graph(project_id, full_graph)
```

---

## Architecture Overview

### Current Flow (Sprint 13)

```
Upload Complete Manuscript
         ↓
Run 6 Extractors in Parallel
         ↓
Populate Knowledge Graph (one-time)
         ↓
Export to JSON
         ↓
Use for Analysis/Reports
         ↓
[DEAD END - Never updated]
```

### New Flow (Sprint 17)

```
┌──────────────────────────────────────────┐
│  User Writes Scene 47                    │
│  [Save Scene]                            │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Mini Extraction (Just Scene 47)         │
│  - Characters mentioned                  │
│  - Locations described                   │
│  - Plot threads advanced                 │
│  - Motifs used                           │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Load Existing Knowledge Graph           │
│  (Built from Scenes 1-46)                │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Merge New Entities                      │
│  - Add new characters/locations          │
│  - Update existing nodes (traits change) │
│  - Add new edges (new relationships)     │
│  - Update edge weights (strengthen)      │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Save Updated Graph                      │
│  (Now includes Scene 47)                 │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  User Continues Writing Scene 48         │
│  [Ask Your Novel] "Has Mickey been to    │
│  The Hotel before?"                      │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Query Knowledge Graph                   │
│  - Find Mickey node                      │
│  - Find Hotel node                       │
│  - Check "appears_at" edges              │
│  - Return connected scenes               │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Display Results in UI                   │
│  "Yes, Mickey appeared at The Hotel in   │
│  3 previous scenes: [Scene 12], [Scene   │
│  23], [Scene 31]"                        │
└──────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Nightly at 2am:                         │
│  - Re-extract entire manuscript          │
│  - Compare with incremental graph        │
│  - Fix any discrepancies                 │
│  - Log differences                       │
└──────────────────────────────────────────┘
```

---

## Implementation Tasks

### Phase A: Incremental Extraction (Week 1)

#### Task 17-01: Mini Entity Extractor (3-4h)

**Goal:** Extract entities from single scene (not entire manuscript)

**File:** `factory/analysis/incremental_extractor.py` (NEW)

```python
"""Incremental entity extraction from single scenes."""

from typing import Dict, List
from dataclasses import dataclass
from factory.agents.character_analyzer import CharacterAnalyzer
from factory.agents.claude_agent import ClaudeAgent

@dataclass
class SceneEntities:
    """Entities extracted from a single scene."""
    characters: List[str]  # Character names mentioned
    locations: List[str]   # Locations described
    plot_threads: List[str]  # Plot threads advanced
    motifs: List[str]  # Motifs/metaphors used
    events: List[Dict]  # Events that occurred

class IncrementalExtractor:
    """Extract entities from single scene for graph updates."""

    def __init__(self, anthropic_client):
        self.client = anthropic_client

    async def extract_from_scene(
        self,
        scene_text: str,
        existing_graph: 'NovelKnowledgeGraph'
    ) -> SceneEntities:
        """
        Extract entities from single scene.

        Uses existing graph for context (known characters, locations).
        Returns only NEW or UPDATED entities.

        Args:
            scene_text: Full scene text
            existing_graph: Current knowledge graph

        Returns:
            SceneEntities with extracted data
        """
        # Get known entities for context
        known_characters = [node.name for node in existing_graph.nodes.values()
                          if node.node_type == "character"]
        known_locations = [node.name for node in existing_graph.nodes.values()
                         if node.node_type == "location"]

        # Prompt LLM to extract entities
        prompt = f"""
        Extract entities from this scene. Focus on:
        1. Characters mentioned (known: {known_characters})
        2. Locations described (known: {known_locations})
        3. Plot developments
        4. Motifs/metaphors used
        5. Key events

        Scene:
        {scene_text}

        Return JSON:
        {{
            "characters": ["name1", "name2"],
            "locations": ["location1"],
            "plot_threads": ["thread description"],
            "motifs": ["motif1"],
            "events": [{{"description": "...", "characters_involved": [...]}}]
        }}
        """

        response = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        import json
        entities_json = json.loads(response.content[0].text)

        return SceneEntities(
            characters=entities_json.get("characters", []),
            locations=entities_json.get("locations", []),
            plot_threads=entities_json.get("plot_threads", []),
            motifs=entities_json.get("motifs", []),
            events=entities_json.get("events", [])
        )
```

---

#### Task 17-02: Graph Merger (4-5h)

**Goal:** Merge new entities into existing graph

**File:** `factory/analysis/knowledge_graph.py` (UPDATE)

```python
class NovelKnowledgeGraph:
    # ... existing methods ...

    def merge_scene_entities(
        self,
        scene_id: str,
        entities: SceneEntities
    ) -> Dict[str, int]:
        """
        Merge entities from new scene into graph.

        Returns:
            Statistics: {
                "nodes_added": int,
                "nodes_updated": int,
                "edges_added": int,
                "edges_updated": int
            }
        """
        stats = {
            "nodes_added": 0,
            "nodes_updated": 0,
            "edges_added": 0,
            "edges_updated": 0
        }

        # Add or update character nodes
        for char_name in entities.characters:
            existing = self._find_node_by_name(char_name, "character")

            if existing:
                # Update existing node
                existing.metadata["appearances"].append(scene_id)
                stats["nodes_updated"] += 1
            else:
                # Add new node
                self.add_node(
                    node_type="character",
                    name=char_name,
                    attributes={"first_appearance": scene_id},
                    metadata={"appearances": [scene_id]}
                )
                stats["nodes_added"] += 1

        # Add or update location nodes
        for loc_name in entities.locations:
            existing = self._find_node_by_name(loc_name, "location")

            if existing:
                existing.metadata["appearances"].append(scene_id)
                stats["nodes_updated"] += 1
            else:
                self.add_node(
                    node_type="location",
                    name=loc_name,
                    attributes={"first_appearance": scene_id},
                    metadata={"appearances": [scene_id]}
                )
                stats["nodes_added"] += 1

        # Add edges for character-location co-occurrence
        for char_name in entities.characters:
            char_node = self._find_node_by_name(char_name, "character")
            if not char_node:
                continue

            for loc_name in entities.locations:
                loc_node = self._find_node_by_name(loc_name, "location")
                if not loc_node:
                    continue

                # Check if edge exists
                existing_edge = self._find_edge(
                    char_node.node_id,
                    loc_node.node_id,
                    "appears_at"
                )

                if existing_edge:
                    # Strengthen edge (increase weight)
                    existing_edge.weight += 0.1
                    existing_edge.attributes["scenes"].append(scene_id)
                    stats["edges_updated"] += 1
                else:
                    # Create new edge
                    self.add_edge(
                        edge_type="appears_at",
                        source_id=char_node.node_id,
                        target_id=loc_node.node_id,
                        attributes={"scenes": [scene_id]},
                        weight=1.0
                    )
                    stats["edges_added"] += 1

        # Similar logic for plot threads, motifs, events...

        return stats

    def _find_node_by_name(self, name: str, node_type: str):
        """Find node by name and type."""
        for node in self.nodes.values():
            if node.node_type == node_type and node.name.lower() == name.lower():
                return node
        return None

    def _find_edge(self, source_id: str, target_id: str, edge_type: str):
        """Find edge between two nodes."""
        for edge in self.edges.values():
            if (edge.source_id == source_id and
                edge.target_id == target_id and
                edge.edge_type == edge_type):
                return edge
        return None
```

---

#### Task 17-03: Scene Save Hook (2-3h)

**Goal:** Trigger graph update on scene save

**File:** `webapp/backend/simple_app.py` (UPDATE)

```python
from factory.analysis.incremental_extractor import IncrementalExtractor
from factory.analysis.knowledge_graph import NovelKnowledgeGraph

# Add to scene save endpoint
@app.post("/api/manuscript/{manuscript_id}/scenes")
async def save_scene(manuscript_id: str, request: dict):
    """Save scene and update knowledge graph."""

    scene_id = request.get("scene_id")
    scene_text = request.get("content")

    # Save scene (existing logic)
    # ... existing code ...

    # Update knowledge graph (NEW)
    try:
        await update_knowledge_graph_from_scene(
            project_id=manuscript_id,
            scene_id=scene_id,
            scene_text=scene_text
        )
    except Exception as e:
        # Log error but don't block scene save
        logger.error(f"Knowledge graph update failed: {e}")

    return {"success": True, "scene_id": scene_id}

async def update_knowledge_graph_from_scene(
    project_id: str,
    scene_id: str,
    scene_text: str
):
    """Update knowledge graph with new scene."""

    # Load existing graph
    graph_path = Path(f".manuscript/{project_id}/knowledge_graph.json")

    if graph_path.exists():
        with open(graph_path, "r") as f:
            graph_data = json.load(f)
        graph = NovelKnowledgeGraph.from_json(graph_data)
    else:
        # Create new graph
        graph = NovelKnowledgeGraph(manuscript_id=project_id)

    # Extract entities from scene
    extractor = IncrementalExtractor(get_anthropic_client())
    entities = await extractor.extract_from_scene(scene_text, graph)

    # Merge into graph
    stats = graph.merge_scene_entities(scene_id, entities)

    # Save updated graph
    graph_data = graph.export_json()
    with open(graph_path, "w") as f:
        json.dump(graph_data, f, indent=2)

    logger.info(f"Graph updated: {stats}")
```

---

### Phase B: Query Interface (Week 2)

#### Task 17-04: Natural Language Query Parser (5-6h)

**Goal:** Parse user questions and map to graph queries

**File:** `factory/analysis/graph_query_engine.py` (NEW)

```python
"""Natural language query engine for knowledge graph."""

from typing import Dict, List, Optional
from factory.analysis.knowledge_graph import NovelKnowledgeGraph

class GraphQueryEngine:
    """Natural language queries against knowledge graph."""

    def __init__(self, anthropic_client, knowledge_graph: NovelKnowledgeGraph):
        self.client = anthropic_client
        self.graph = knowledge_graph

    async def query(self, question: str) -> Dict:
        """
        Query knowledge graph with natural language question.

        Examples:
        - "Has Mickey been to The Hotel before?"
        - "Have Mickey and The Chronicler met?"
        - "Is the quantum consciousness plot resolved?"
        - "How many times is 'ghost' mentioned?"
        - "When did Mickey first meet Sarah?"

        Returns:
            {
                "answer": str,  # Natural language answer
                "scenes": List[Dict],  # Relevant scenes
                "entities": List[Dict],  # Relevant entities
                "confidence": float  # 0.0-1.0
            }
        """
        # Classify question type
        question_type = await self._classify_question(question)

        if question_type == "location_history":
            return await self._query_location_history(question)
        elif question_type == "character_interaction":
            return await self._query_character_interaction(question)
        elif question_type == "plot_thread":
            return await self._query_plot_thread(question)
        elif question_type == "motif_frequency":
            return await self._query_motif_frequency(question)
        elif question_type == "timeline":
            return await self._query_timeline(question)
        else:
            return await self._general_query(question)

    async def _classify_question(self, question: str) -> str:
        """Classify question type using LLM."""
        prompt = f"""
        Classify this question about a novel's knowledge graph:

        Question: {question}

        Types:
        - location_history: "Has [character] been to [location]?"
        - character_interaction: "Have [char1] and [char2] met?"
        - plot_thread: "Is [subplot] resolved?"
        - motif_frequency: "How many times is [motif] used?"
        - timeline: "When did [event] happen?"
        - general: Other questions

        Return only the type (one word).
        """

        response = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip().lower()

    async def _query_location_history(self, question: str) -> Dict:
        """Query: Has [character] been to [location]?"""

        # Extract character and location names
        entities = await self._extract_entities_from_question(question)
        char_name = entities.get("character")
        loc_name = entities.get("location")

        if not char_name or not loc_name:
            return {"answer": "Could not parse question", "confidence": 0.0}

        # Find nodes
        char_node = self.graph._find_node_by_name(char_name, "character")
        loc_node = self.graph._find_node_by_name(loc_name, "location")

        if not char_node or not loc_node:
            return {
                "answer": f"{char_name} or {loc_name} not found in story",
                "confidence": 0.0
            }

        # Find "appears_at" edges
        edge = self.graph._find_edge(char_node.node_id, loc_node.node_id, "appears_at")

        if edge:
            scenes = edge.attributes.get("scenes", [])
            return {
                "answer": f"Yes, {char_name} appeared at {loc_name} in {len(scenes)} scene(s)",
                "scenes": scenes,
                "entities": [char_node.to_dict(), loc_node.to_dict()],
                "confidence": 1.0
            }
        else:
            return {
                "answer": f"No, {char_name} has not appeared at {loc_name}",
                "confidence": 1.0
            }

    async def _extract_entities_from_question(self, question: str) -> Dict:
        """Extract entity names from question using LLM."""
        prompt = f"""
        Extract entity names from this question:

        Question: {question}

        Return JSON:
        {{
            "character": "Character Name" or null,
            "location": "Location Name" or null,
            "plot_thread": "Thread description" or null,
            "motif": "Motif word" or null
        }}
        """

        response = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        return json.loads(response.content[0].text)

    # Similar methods for other query types...
```

---

#### Task 17-05: Query API Endpoint (2-3h)

**File:** `webapp/backend/simple_app.py` (ADD)

```python
@app.post("/api/manuscript/{manuscript_id}/query-graph")
async def query_knowledge_graph(manuscript_id: str, request: dict):
    """Query knowledge graph with natural language question.

    Request:
        {
            "question": str  # "Has Mickey been to The Hotel before?"
        }

    Response:
        {
            "answer": str,
            "scenes": List[Dict],
            "entities": List[Dict],
            "confidence": float
        }
    """
    question = request.get("question")

    if not question:
        raise HTTPException(400, "Question required")

    # Load knowledge graph
    graph_path = Path(f".manuscript/{manuscript_id}/knowledge_graph.json")

    if not graph_path.exists():
        raise HTTPException(404, "Knowledge graph not found. Save some scenes first.")

    with open(graph_path, "r") as f:
        graph_data = json.load(f)

    graph = NovelKnowledgeGraph.from_json(graph_data)

    # Query graph
    query_engine = GraphQueryEngine(get_anthropic_client(), graph)
    result = await query_engine.query(question)

    return result
```

---

#### Task 17-06: Frontend Query UI (4-5h)

**File:** `webapp/frontend-v2/src/features/scenes/ResearchPanel.jsx` (NEW)

```jsx
import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

export default function ResearchPanel({ manuscriptId }) {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuery = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/manuscript/${manuscriptId}/query-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const result = await response.json();
      setAnswer(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Ask Your Novel
      </Typography>

      <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
        <TextField
          fullWidth
          placeholder="Has Mickey been to The Hotel before?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
          size="small"
        />
        <Button
          variant="contained"
          onClick={handleQuery}
          disabled={loading || !question.trim()}
          startIcon={loading ? <CircularProgress size={16} /> : <SearchIcon />}
        >
          Ask
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {answer && (
        <Card>
          <CardContent>
            <Typography variant="body1" gutterBottom>
              {answer.answer}
            </Typography>

            {answer.scenes && answer.scenes.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Referenced Scenes:
                </Typography>
                {answer.scenes.map((scene, idx) => (
                  <Chip
                    key={idx}
                    label={scene.scene_id || `Scene ${idx + 1}`}
                    size="small"
                    sx={{ mr: 0.5, mb: 0.5 }}
                  />
                ))}
              </Box>
            )}

            {answer.confidence !== undefined && (
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                Confidence: {(answer.confidence * 100).toFixed(0)}%
              </Typography>
            )}
          </CardContent>
        </Card>
      )}

      <Box sx={{ mt: 3 }}>
        <Typography variant="caption" color="text.secondary">
          Example questions:
        </Typography>
        <Box sx={{ mt: 1 }}>
          <Chip
            label="Has Mickey been to The Hotel?"
            size="small"
            onClick={() => setQuestion("Has Mickey been to The Hotel?")}
            sx={{ mr: 0.5, mb: 0.5 }}
          />
          <Chip
            label="Have Mickey and The Chronicler met?"
            size="small"
            onClick={() => setQuestion("Have Mickey and The Chronicler met?")}
            sx={{ mr: 0.5, mb: 0.5 }}
          />
          <Chip
            label="Is the quantum plot resolved?"
            size="small"
            onClick={() => setQuestion("Is the quantum plot resolved?")}
            sx={{ mr: 0.5, mb: 0.5 }}
          />
        </Box>
      </Box>
    </Box>
  );
}
```

**Integration:** Add to scene editor sidebar

```jsx
// In SceneEditor.jsx
import ResearchPanel from './ResearchPanel';

<Box sx={{ width: 300, borderLeft: '1px solid #ddd', p: 2 }}>
  <ResearchPanel manuscriptId={projectId} />
</Box>
```

---

### Phase C: Nightly Verification (Week 3)

#### Task 17-07: Full Re-extraction (3-4h)

**File:** `factory/analysis/batch_verification.py` (NEW)

```python
"""Nightly batch verification of knowledge graph."""

import asyncio
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BatchVerification:
    """Verify incremental graph against full extraction."""

    async def verify_all_projects(self):
        """Run verification for all projects."""
        projects_dir = Path(".manuscript")

        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                project_id = project_dir.name
                await self.verify_project(project_id)

    async def verify_project(self, project_id: str):
        """Verify single project's knowledge graph."""
        logger.info(f"Verifying knowledge graph for {project_id}")

        try:
            # Load incremental graph
            incremental_graph = self._load_incremental_graph(project_id)

            # Full re-extraction
            full_graph = await self._full_extraction(project_id)

            # Compare
            discrepancies = self._compare_graphs(incremental_graph, full_graph)

            if discrepancies:
                logger.warning(f"Found {len(discrepancies)} discrepancies in {project_id}")
                self._log_discrepancies(project_id, discrepancies)

                # Replace with full graph
                self._save_graph(project_id, full_graph)
                logger.info(f"Replaced incremental graph with full extraction")
            else:
                logger.info(f"No discrepancies found in {project_id}")

        except Exception as e:
            logger.error(f"Verification failed for {project_id}: {e}")

    async def _full_extraction(self, project_id: str):
        """Run full extraction on entire manuscript."""
        # Load all scenes
        scenes = self._load_all_scenes(project_id)

        # Run Sprint 13 extractors
        from factory.analysis.entity_extractors import (
            CharacterExtractor,
            LocationExtractor,
            PlotThreadTracker,
            MotifAnalyzer
        )

        # Extract from all scenes
        # ... (Sprint 13 logic)

        return full_graph

    def _compare_graphs(self, incremental, full):
        """Compare two graphs and find discrepancies."""
        discrepancies = []

        # Compare node counts
        if len(incremental.nodes) != len(full.nodes):
            discrepancies.append({
                "type": "node_count_mismatch",
                "incremental": len(incremental.nodes),
                "full": len(full.nodes)
            })

        # Compare specific nodes
        for node_id, full_node in full.nodes.items():
            inc_node = incremental.nodes.get(node_id)

            if not inc_node:
                discrepancies.append({
                    "type": "missing_node",
                    "node_id": node_id,
                    "name": full_node.name
                })
            elif inc_node.attributes != full_node.attributes:
                discrepancies.append({
                    "type": "node_attribute_mismatch",
                    "node_id": node_id,
                    "name": full_node.name
                })

        return discrepancies
```

---

#### Task 17-08: Scheduled Job (2h)

**File:** `scripts/nightly_verification.py` (NEW)

```python
"""Run nightly knowledge graph verification."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory.analysis.batch_verification import BatchVerification

async def main():
    """Run verification for all projects."""
    verifier = BatchVerification()
    await verifier.verify_all_projects()

if __name__ == "__main__":
    asyncio.run(main())
```

**Cron job (runs at 2am daily):**
```bash
0 2 * * * cd /path/to/writers-factory-core && python scripts/nightly_verification.py
```

---

## Success Criteria

**Sprint 17 is DONE when:**

- [ ] Knowledge graph updates on every scene save
- [ ] Mini extraction works (entities from single scene)
- [ ] Graph merger adds new nodes and edges correctly
- [ ] "Ask Your Novel" UI in scene editor
- [ ] Can query: "Has [character] been to [location]?"
- [ ] Can query: "Have [char1] and [char2] met?"
- [ ] Can query: "Is [plot thread] resolved?"
- [ ] Natural language parsing works (5+ question types)
- [ ] Nightly verification runs and logs discrepancies
- [ ] All tests pass (unit + integration)
- [ ] 5 beta testers use query feature successfully

---

## Integration with Sprints 15-16

**Sprint 15 (Beginner Mode):**
- Beginner starts with 0 scenes → empty knowledge graph
- As they write 2,500 words → graph grows incrementally
- At upgrade: Graph has ~10-15 scenes worth of entities

**Sprint 16 (Multi-Notebook):**
- NotebookLM = External research (user-curated)
- Knowledge Graph = Internal continuity (AI-extracted)
- User can query BOTH:
  - NotebookLM: "What was my original plan for Mickey's arc?"
  - Knowledge Graph: "What is Mickey's ACTUAL arc so far?"

**Together:** Vision (NotebookLM) vs. Execution (Knowledge Graph)

---

## Testing Strategy

### Unit Tests

```bash
pytest tests/test_incremental_extraction.py -v
pytest tests/test_graph_merger.py -v
pytest tests/test_graph_queries.py -v
```

### Integration Tests

```bash
pytest tests/test_live_knowledge_graph.py -v

# Test flow:
1. Create project
2. Write Scene 1 (introduce Mickey)
3. Check graph has Mickey node
4. Write Scene 2 (Mickey at Hotel)
5. Check graph has Hotel node and "appears_at" edge
6. Query: "Has Mickey been to Hotel?"
7. Verify returns Scene 2
8. Write Scene 3 (Mickey returns to Hotel)
9. Check edge weight increased
10. Query again - verify returns Scenes 2 and 3
```

### User Acceptance Testing

**5 beta testers:**
1. Write 10 scenes
2. Use "Ask Your Novel" 10+ times
3. Verify answers are accurate
4. Test question types (location, character, plot, motif, timeline)

**Success:** 4/5 report accurate answers

---

## Timeline

**Week 1: Incremental Extraction (40h)**
- Mini extractor (3-4h)
- Graph merger (4-5h)
- Scene save hook (2-3h)
- Testing (8h)
- Documentation (4h)
- Buffer (18h)

**Week 2: Query Interface (40h)**
- Query parser (5-6h)
- Query engine (6-7h)
- API endpoint (2-3h)
- Frontend UI (4-5h)
- Testing (10h)
- Documentation (4h)
- Buffer (10h)

**Week 3: Verification & Polish (40h)**
- Batch verification (3-4h)
- Scheduled job (2h)
- Discrepancy logging (3h)
- Integration testing (10h)
- Bug fixes (12h)
- Documentation (5h)
- Beta testing (5h)

**Total:** 120 hours / 3 weeks

---

## Deliverables

1. ✅ Incremental extraction system
2. ✅ Graph merger with statistics
3. ✅ Scene save hook (auto-update)
4. ✅ Natural language query engine
5. ✅ "Ask Your Novel" UI component
6. ✅ Query API endpoint
7. ✅ Nightly batch verification
8. ✅ Scheduled verification job
9. ✅ Unit + integration tests
10. ✅ 5 beta testers validated

---

## What User Gets

**While Writing:**
```
Scene Editor:
┌────────────────────────────────────────┐
│ Scene 47: Mickey Returns to Hotel      │
│                                         │
│ Mickey pushed through the revolving... │
│                                         │
└────────────────────────────────────────┘

Research Panel (Sidebar):
┌────────────────────────────────────────┐
│ Ask Your Novel                          │
│ [Has Mickey been to The Hotel before?] │
│ [Ask]                                   │
│                                         │
│ Answer:                                │
│ Yes, Mickey appeared at The Hotel in   │
│ 3 previous scenes:                     │
│ • Scene 12 (Chapter 2)                 │
│ • Scene 23 (Chapter 5)                 │
│ • Scene 31 (Chapter 7)                 │
│                                         │
│ Example questions:                     │
│ • Have Mickey and Sarah met?           │
│ • Is the quantum plot resolved?        │
│ • How many times is "ghost" mentioned? │
└────────────────────────────────────────┘
```

**This is YOUR vision - ongoing knowledge graph queries while writing!** 🎯
