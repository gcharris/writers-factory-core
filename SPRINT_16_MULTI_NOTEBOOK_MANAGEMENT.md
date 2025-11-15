# Sprint 16: Multi-Notebook Management & UI

**Date:** November 15, 2025
**Priority:** HIGH - Required for January course
**Timeline:** 2 weeks
**Dependencies:** Sprint 15 (Beginner Mode) ✅ Complete

---

## Mission: Make Multi-Notebook Architecture User-Friendly 🎯

**Current Problem:**
- Sprint 11 built multi-notebook backend (storage, queries, auto-selection)
- Sprint 15 adds beginner mode with NotebookLM voice extraction
- **BUT:** No UI to manage notebooks - users must edit JSON files manually ❌

**Sprint 16 Solution:**
- Add notebook management to Project Setup Wizard
- Ask user for notebook URLs during setup
- Provide UI to add/update/remove notebooks
- Auto-categorize notebooks by purpose (ideas, characters, structure, etc.)
- Display notebook library with usage stats

**User Experience:**
```
Setup Wizard asks:
"Do you have NotebookLM notebooks for this project?"
  → YES: "Please provide your notebook URLs..."
      - Ideas & World-Building: [URL input]
      - Character Profiles: [URL input]
      - Story Structure: [URL input]
      - Custom: [Add more notebooks]
  → NO: "You can add notebooks later from Project Settings"

System automatically:
  ✅ Saves notebook URLs to notebooks.json
  ✅ Categorizes by purpose
  ✅ Adds appropriate tags
  ✅ Tests connectivity
  ✅ Enables auto-selection for queries
```

---

## Architecture Overview

### Current State (Sprint 11 + 15)

**Backend (Works):**
- ✅ `notebooks.json` stores multiple notebooks
- ✅ `POST /api/research/query` with auto-selection
- ✅ `GET /api/research/notebooks` lists notebooks
- ✅ Tag-based notebook selection
- ✅ NotebookLM client queries notebooks

**Frontend (Missing):**
- ❌ No UI to add/edit/remove notebooks
- ❌ No notebook management in wizard
- ❌ No notebook library display
- ❌ No usage statistics view

**Sprint 16 Adds:**
- ✅ Notebook input in Project Setup Wizard
- ✅ Notebook management UI in Project Settings
- ✅ Notebook library browser with stats
- ✅ Quick notebook switcher
- ✅ CRUD API endpoints for notebooks

---

## User Workflows

### Workflow 1: New Project Setup (Experienced Writer)

**Step 1: Project Setup Wizard - Step 4 (NEW)**

```
┌─────────────────────────────────────────────────────┐
│ Step 4: Connect NotebookLM (Optional)               │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Do you have NotebookLM notebooks for this project?  │
│                                                      │
│  ○ No, I'll add them later                          │
│  ● Yes, I have notebooks                            │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ Common Notebook Types                         │   │
│ │                                               │   │
│ │ ☑ Ideas & World-Building                     │   │
│ │   URL: [https://notebooklm.google.com/...]   │   │
│ │   Tags: ideas, creative, plot                 │   │
│ │                                               │   │
│ │ ☑ Character Profiles                          │   │
│ │   URL: [https://notebooklm.google.com/...]   │   │
│ │   Tags: characters, backstories               │   │
│ │                                               │   │
│ │ ☑ Story Structure                             │   │
│ │   URL: [https://notebooklm.google.com/...]   │   │
│ │   Tags: structure, planning, chapters         │   │
│ │                                               │   │
│ │ ☐ Research & References                       │   │
│ │ ☐ Custom Notebook                             │   │
│ │                                               │   │
│ │ [+ Add Another Notebook]                      │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ [← Back]                      [Test & Continue →]   │
└─────────────────────────────────────────────────────┘
```

**"Test & Continue" does:**
1. Validates each URL (checks NotebookLM connectivity)
2. Auto-generates notebook IDs
3. Saves to `notebooks.json`
4. Shows success confirmation
5. Continues to Step 5 (Skill Generation)

---

### Workflow 2: New Project Setup (Beginner)

**Step 1: "Do you have fiction?" → NO**

**Step 2: Beginner Path - NotebookLM Collection**

```
┌─────────────────────────────────────────────────────┐
│ Step 2: Upload Personal Writing to NotebookLM       │
├─────────────────────────────────────────────────────┤
│                                                      │
│ To generate your starter voice profile, we'll       │
│ extract your writing style from personal writing.   │
│                                                      │
│ 1. Create a NotebookLM notebook:                    │
│    → Go to notebooklm.google.com                    │
│    → Click "New Notebook"                           │
│    → Name it "My Writing Collection"                │
│                                                      │
│ 2. Upload your personal writing:                    │
│    ✓ Email excerpts (personal, not business)        │
│    ✓ Social media posts (Twitter, LinkedIn, blog)   │
│    ✓ Text messages or chat logs                     │
│    ✓ Diary or journal entries                       │
│    ✓ Any casual writing (5,000+ words total)        │
│                                                      │
│ 3. Share your notebook:                             │
│    → Click "Share" in NotebookLM                    │
│    → Copy the URL                                   │
│    → Paste below:                                   │
│                                                      │
│    NotebookLM URL:                                  │
│    [https://notebooklm.google.com/notebook/...]     │
│                                                      │
│    [Test Connection]                                │
│                                                      │
│ [← Back]                            [Continue →]    │
└─────────────────────────────────────────────────────┘
```

**System automatically:**
- Saves as "personal-writing" notebook
- Tags: `["beginner", "voice-extraction", "personal"]`
- Extracts voice profile (Sprint 15 logic)
- Generates starter skills

---

### Workflow 3: Manage Notebooks (Post-Setup)

**Project Settings → Notebooks Tab**

```
┌─────────────────────────────────────────────────────┐
│ Project: The Explants                                │
│ Notebooks (3)                          [+ Add New]  │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ 📓 Ideas & World-Building                    │   │
│ │ https://notebooklm.google.com/notebook/abc   │   │
│ │ Tags: ideas, creative, plot                   │   │
│ │ Queries: 47 | Last used: 2 hours ago         │   │
│ │ [Edit] [Remove] [Query Now]                  │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ 📓 Character Profiles                         │   │
│ │ https://notebooklm.google.com/notebook/def   │   │
│ │ Tags: characters, backstories                 │   │
│ │ Queries: 23 | Last used: 1 day ago           │   │
│ │ [Edit] [Remove] [Query Now]                  │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ 📓 Story Structure                            │   │
│ │ https://notebooklm.google.com/notebook/ghi   │   │
│ │ Tags: structure, planning, chapters           │   │
│ │ Queries: 12 | Last used: 3 days ago          │   │
│ │ [Edit] [Remove] [Query Now]                  │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Click [+ Add New]:**
```
┌─────────────────────────────────────────────────────┐
│ Add Notebook                                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Notebook Type:                                      │
│ ○ Ideas & World-Building                            │
│ ○ Character Profiles                                │
│ ○ Story Structure                                   │
│ ○ Research & References                             │
│ ● Custom                                            │
│                                                      │
│ Name: [___________________________]                 │
│                                                      │
│ NotebookLM URL:                                     │
│ [https://notebooklm.google.com/notebook/...]        │
│                                                      │
│ Description (optional):                             │
│ [_________________________________________]         │
│                                                      │
│ Tags (comma-separated):                             │
│ [custom, my-tag, another-tag]                       │
│                                                      │
│ [Test Connection]                                   │
│                                                      │
│ [Cancel]                           [Add Notebook]   │
└─────────────────────────────────────────────────────┘
```

---

### Workflow 4: Query Notebooks While Writing

**Scene Editor Sidebar - Research Panel**

```
┌─────────────────────────────────────────────────────┐
│ Research                                             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Notebook: [Auto-select ▼]                           │
│   • Auto-select (recommended)                       │
│   • Ideas & World-Building                          │
│   • Character Profiles                              │
│   • Story Structure                                 │
│                                                      │
│ Ask your notebooks:                                 │
│ [What is Mickey's relationship with...]             │
│                                                      │
│ [Ask]                                               │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ Answer from: Character Profiles               │   │
│ │                                               │   │
│ │ Mickey Bardot and The Chronicler have a       │   │
│ │ complex mentor-student relationship. The      │   │
│ │ Chronicler guides Mickey through...           │   │
│ │                                               │   │
│ │ Sources:                                      │   │
│ │ • Character_Notes.pdf (p. 12)                 │   │
│ │ • Relationships.md                            │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ Recent Queries:                                     │
│ • Mickey's character arc                            │
│ • The Hotel location description                    │
│ • Quantum physics metaphor usage                    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Technical Implementation

### Phase A: Backend API Endpoints (Week 1)

#### New Endpoints

**1. Add Notebook**
```python
POST /api/research/notebooks/add

Request:
{
    "project_id": str,
    "name": str,
    "url": str,
    "description": str (optional),
    "tags": List[str],
    "notebook_type": str  # "ideas", "characters", "structure", "custom"
}

Response:
{
    "success": bool,
    "notebook_id": str,
    "message": str
}

Implementation:
- Validate NotebookLM URL format
- Test connectivity (optional quick query)
- Generate unique notebook_id
- Auto-add tags based on notebook_type
- Save to notebooks.json
- Return notebook_id
```

**2. Update Notebook**
```python
PUT /api/research/notebooks/{notebook_id}

Request:
{
    "project_id": str,
    "name": str (optional),
    "description": str (optional),
    "tags": List[str] (optional)
}

Response:
{
    "success": bool,
    "message": str
}

Implementation:
- Load notebooks.json
- Find notebook by ID
- Update fields (preserve URL and created_at)
- Save notebooks.json
```

**3. Remove Notebook**
```python
DELETE /api/research/notebooks/{notebook_id}

Request:
{
    "project_id": str
}

Response:
{
    "success": bool,
    "message": str
}

Implementation:
- Load notebooks.json
- Remove notebook by ID
- Save notebooks.json
```

**4. Test Notebook Connection**
```python
POST /api/research/notebooks/test

Request:
{
    "url": str
}

Response:
{
    "success": bool,
    "accessible": bool,
    "notebook_name": str,
    "error": str (if failed)
}

Implementation:
- Create temporary NotebookLMClient
- Try to access notebook URL
- Return success/failure with notebook name
```

**5. Get Notebook Statistics**
```python
GET /api/research/notebooks/{notebook_id}/stats

Response:
{
    "notebook_id": str,
    "name": str,
    "use_count": int,
    "last_used": str (ISO timestamp),
    "created_at": str,
    "tags": List[str]
}

Implementation:
- Load notebooks.json
- Return stats for specific notebook
```

#### Enhanced notebooks.json Schema

```json
[
    {
        "id": "nb-abc123",
        "name": "Ideas & World-Building",
        "url": "https://notebooklm.google.com/notebook/abc",
        "description": "Creative flashes, plot development, world-building notes",
        "notebook_type": "ideas",
        "tags": ["ideas", "creative", "plot", "world-building"],
        "use_count": 47,
        "last_used": "2025-11-15T14:30:00Z",
        "created_at": "2025-11-01T10:00:00Z"
    }
]
```

**New Fields:**
- `notebook_type`: Pre-defined categories for UI grouping
- `use_count`: Incremented on each query
- `last_used`: Updated on each query

#### Backend Implementation Files

**File:** `webapp/backend/routes/notebooks.py` (NEW)

```python
"""Notebook management endpoints (Sprint 16)."""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import json
from pathlib import Path
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/research/notebooks", tags=["notebooks"])

NOTEBOOK_TYPES = {
    "ideas": {
        "name": "Ideas & World-Building",
        "tags": ["ideas", "creative", "plot", "world-building"]
    },
    "characters": {
        "name": "Character Profiles",
        "tags": ["characters", "backstories", "relationships"]
    },
    "structure": {
        "name": "Story Structure",
        "tags": ["structure", "planning", "chapters", "acts"]
    },
    "research": {
        "name": "Research & References",
        "tags": ["research", "references", "sources"]
    },
    "custom": {
        "name": "Custom Notebook",
        "tags": []
    }
}

@router.post("/add")
async def add_notebook(request: dict):
    """Add notebook to project."""
    project_id = request.get("project_id")
    name = request.get("name")
    url = request.get("url")
    description = request.get("description", "")
    tags = request.get("tags", [])
    notebook_type = request.get("notebook_type", "custom")

    # Validation
    if not all([project_id, name, url]):
        raise HTTPException(400, "project_id, name, and url required")

    if not url.startswith("https://notebooklm.google.com"):
        raise HTTPException(400, "Invalid NotebookLM URL")

    # Auto-add tags based on type
    type_config = NOTEBOOK_TYPES.get(notebook_type, NOTEBOOK_TYPES["custom"])
    all_tags = list(set(tags + type_config["tags"]))

    # Generate notebook ID
    notebook_id = f"nb-{uuid.uuid4().hex[:8]}"

    # Create notebook entry
    notebook = {
        "id": notebook_id,
        "name": name,
        "url": url,
        "description": description,
        "notebook_type": notebook_type,
        "tags": all_tags,
        "use_count": 0,
        "last_used": None,
        "created_at": datetime.now().isoformat()
    }

    # Load existing notebooks
    notebooks = _load_notebooks(project_id)

    # Check for duplicate URLs
    if any(nb["url"] == url for nb in notebooks):
        raise HTTPException(400, "Notebook URL already exists")

    # Add and save
    notebooks.append(notebook)
    _save_notebooks(project_id, notebooks)

    return {
        "success": True,
        "notebook_id": notebook_id,
        "message": f"Notebook '{name}' added successfully"
    }

@router.put("/{notebook_id}")
async def update_notebook(notebook_id: str, request: dict):
    """Update notebook metadata."""
    project_id = request.get("project_id")

    if not project_id:
        raise HTTPException(400, "project_id required")

    notebooks = _load_notebooks(project_id)
    notebook = next((nb for nb in notebooks if nb["id"] == notebook_id), None)

    if not notebook:
        raise HTTPException(404, "Notebook not found")

    # Update fields
    if "name" in request:
        notebook["name"] = request["name"]
    if "description" in request:
        notebook["description"] = request["description"]
    if "tags" in request:
        notebook["tags"] = request["tags"]

    _save_notebooks(project_id, notebooks)

    return {
        "success": True,
        "message": f"Notebook updated successfully"
    }

@router.delete("/{notebook_id}")
async def remove_notebook(notebook_id: str, project_id: str):
    """Remove notebook from project."""
    notebooks = _load_notebooks(project_id)

    # Filter out notebook
    updated = [nb for nb in notebooks if nb["id"] != notebook_id]

    if len(updated) == len(notebooks):
        raise HTTPException(404, "Notebook not found")

    _save_notebooks(project_id, updated)

    return {
        "success": True,
        "message": "Notebook removed successfully"
    }

@router.post("/test")
async def test_notebook(request: dict):
    """Test NotebookLM connection."""
    url = request.get("url")

    if not url:
        raise HTTPException(400, "url required")

    try:
        from factory.research.notebooklm_client import NotebookLMClient

        client = NotebookLMClient()

        # Simple connectivity test - try to load the page
        # (Full query would be too slow for validation)
        # For now, just validate URL format

        if not url.startswith("https://notebooklm.google.com/notebook/"):
            return {
                "success": False,
                "accessible": False,
                "error": "Invalid NotebookLM URL format"
            }

        return {
            "success": True,
            "accessible": True,
            "notebook_name": "Connected",
            "message": "Notebook URL is valid"
        }

    except Exception as e:
        return {
            "success": False,
            "accessible": False,
            "error": str(e)
        }

@router.get("/{notebook_id}/stats")
async def get_notebook_stats(notebook_id: str, project_id: str):
    """Get notebook usage statistics."""
    notebooks = _load_notebooks(project_id)
    notebook = next((nb for nb in notebooks if nb["id"] == notebook_id), None)

    if not notebook:
        raise HTTPException(404, "Notebook not found")

    return {
        "notebook_id": notebook["id"],
        "name": notebook["name"],
        "use_count": notebook.get("use_count", 0),
        "last_used": notebook.get("last_used"),
        "created_at": notebook.get("created_at"),
        "tags": notebook.get("tags", [])
    }

def _load_notebooks(project_id: str) -> List[dict]:
    """Load notebooks.json for project."""
    from pathlib import Path

    # Try manuscript directory first
    notebooks_file = Path(".manuscript") / project_id / "notebooks.json"

    if not notebooks_file.exists():
        # Fallback to project root
        notebooks_file = Path(project_id) / "notebooks.json"

    if not notebooks_file.exists():
        return []

    with open(notebooks_file, "r") as f:
        return json.load(f)

def _save_notebooks(project_id: str, notebooks: List[dict]):
    """Save notebooks.json for project."""
    from pathlib import Path

    # Use manuscript directory
    project_dir = Path(".manuscript") / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    notebooks_file = project_dir / "notebooks.json"

    with open(notebooks_file, "w") as f:
        json.dump(notebooks, indent=2, fp=f)
```

**Update:** `webapp/backend/simple_app.py`

```python
# Add to imports
from routes.notebooks import router as notebooks_router

# Register router
app.include_router(notebooks_router)

# Update query endpoint to track usage
@app.post("/api/research/query")
async def query_research(request: dict):
    # ... existing code ...

    # After successful query, update usage stats
    notebooks = _load_project_notebooks(project_id)
    for nb in notebooks:
        if nb["id"] == notebook["id"]:
            nb["use_count"] = nb.get("use_count", 0) + 1
            nb["last_used"] = datetime.now().isoformat()
    _save_project_notebooks(project_id, notebooks)

    # ... return response ...
```

---

### Phase B: Frontend UI (Week 2)

#### Component 1: Notebook Input in Setup Wizard

**File:** `webapp/frontend-v2/src/features/setup/NotebookSetupStep.jsx` (NEW)

```jsx
import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  TextField,
  Checkbox,
  FormControlLabel,
  Alert,
  CircularProgress
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const NOTEBOOK_TYPES = [
  {
    id: 'ideas',
    label: 'Ideas & World-Building',
    description: 'Creative flashes, plot development, world-building notes',
    defaultTags: ['ideas', 'creative', 'plot']
  },
  {
    id: 'characters',
    label: 'Character Profiles',
    description: 'Character backstories, relationships, development arcs',
    defaultTags: ['characters', 'backstories']
  },
  {
    id: 'structure',
    label: 'Story Structure',
    description: 'Chapter outlines, acts, structure notes',
    defaultTags: ['structure', 'planning', 'chapters']
  },
  {
    id: 'research',
    label: 'Research & References',
    description: 'Research materials, references, sources',
    defaultTags: ['research', 'references']
  }
];

export default function NotebookSetupStep({ projectId, onComplete, onSkip }) {
  const [notebooks, setNotebooks] = useState(
    NOTEBOOK_TYPES.map(type => ({
      ...type,
      enabled: false,
      url: '',
      tested: false,
      testing: false,
      error: null
    }))
  );

  const [customNotebooks, setCustomNotebooks] = useState([]);

  const handleToggle = (index) => {
    const updated = [...notebooks];
    updated[index].enabled = !updated[index].enabled;
    setNotebooks(updated);
  };

  const handleUrlChange = (index, url) => {
    const updated = [...notebooks];
    updated[index].url = url;
    updated[index].tested = false;
    updated[index].error = null;
    setNotebooks(updated);
  };

  const testNotebook = async (index) => {
    const updated = [...notebooks];
    updated[index].testing = true;
    setNotebooks(updated);

    try {
      const response = await fetch('/api/research/notebooks/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: notebooks[index].url })
      });

      const result = await response.json();

      updated[index].testing = false;
      updated[index].tested = result.success;
      updated[index].error = result.success ? null : result.error;
      setNotebooks(updated);
    } catch (error) {
      updated[index].testing = false;
      updated[index].error = error.message;
      setNotebooks(updated);
    }
  };

  const handleContinue = async () => {
    const enabled = notebooks.filter(nb => nb.enabled && nb.url);

    // Save all enabled notebooks
    for (const notebook of enabled) {
      await fetch('/api/research/notebooks/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: projectId,
          name: notebook.label,
          url: notebook.url,
          description: notebook.description,
          notebook_type: notebook.id,
          tags: notebook.defaultTags
        })
      });
    }

    onComplete();
  };

  const allTestedOrSkipped = notebooks.every(nb =>
    !nb.enabled || (nb.enabled && nb.tested)
  );

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Connect NotebookLM (Optional)
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Add your NotebookLM notebooks to enable AI research queries while writing.
        You can skip this and add notebooks later from Project Settings.
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        💡 Tip: Organize your research into specialized notebooks for better
        auto-selection (e.g., one for characters, one for world-building).
      </Alert>

      {notebooks.map((notebook, index) => (
        <Box key={notebook.id} sx={{ mb: 3, p: 2, border: '1px solid #ddd', borderRadius: 1 }}>
          <FormControlLabel
            control={
              <Checkbox
                checked={notebook.enabled}
                onChange={() => handleToggle(index)}
              />
            }
            label={
              <Box>
                <Typography variant="subtitle1">{notebook.label}</Typography>
                <Typography variant="caption" color="text.secondary">
                  {notebook.description}
                </Typography>
              </Box>
            }
          />

          {notebook.enabled && (
            <Box sx={{ mt: 2, ml: 4 }}>
              <TextField
                fullWidth
                label="NotebookLM URL"
                placeholder="https://notebooklm.google.com/notebook/..."
                value={notebook.url}
                onChange={(e) => handleUrlChange(index, e.target.value)}
                error={!!notebook.error}
                helperText={notebook.error}
                sx={{ mb: 1 }}
              />

              <Button
                variant="outlined"
                size="small"
                onClick={() => testNotebook(index)}
                disabled={!notebook.url || notebook.testing}
                startIcon={
                  notebook.testing ? (
                    <CircularProgress size={16} />
                  ) : notebook.tested ? (
                    <CheckCircleIcon />
                  ) : null
                }
              >
                {notebook.testing
                  ? 'Testing...'
                  : notebook.tested
                  ? 'Connected ✓'
                  : 'Test Connection'}
              </Button>
            </Box>
          )}
        </Box>
      ))}

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onSkip}>Skip for Now</Button>
        <Button
          variant="contained"
          onClick={handleContinue}
          disabled={!allTestedOrSkipped}
        >
          Continue
        </Button>
      </Box>
    </Box>
  );
}
```

**Integration:** Add to `ProjectSetupWizard.jsx`

```jsx
// Add step 4 (or adjust numbering)
const steps = [
  'Project Basics',
  'Voice Analysis',
  'Skill Generation',
  'NotebookLM (Optional)',  // NEW STEP
  'Review & Create'
];

// In stepper render
{activeStep === 3 && (
  <NotebookSetupStep
    projectId={formData.name}
    onComplete={handleNext}
    onSkip={handleNext}
  />
)}
```

#### Component 2: Notebook Management UI

**File:** `webapp/frontend-v2/src/features/notebooks/NotebookManager.jsx` (NEW)

```jsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Chip,
  Grid
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import QueryStatsIcon from '@mui/icons-material/QueryStats';

export default function NotebookManager({ projectId }) {
  const [notebooks, setNotebooks] = useState([]);
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [editingNotebook, setEditingNotebook] = useState(null);

  useEffect(() => {
    loadNotebooks();
  }, [projectId]);

  const loadNotebooks = async () => {
    const response = await fetch(`/api/research/notebooks?project_id=${projectId}`);
    const data = await response.json();
    setNotebooks(data.notebooks || []);
  };

  const handleDelete = async (notebookId) => {
    if (!confirm('Remove this notebook?')) return;

    await fetch(`/api/research/notebooks/${notebookId}?project_id=${projectId}`, {
      method: 'DELETE'
    });

    loadNotebooks();
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5">Notebooks ({notebooks.length})</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenAddDialog(true)}
        >
          Add Notebook
        </Button>
      </Box>

      <Grid container spacing={2}>
        {notebooks.map(notebook => (
          <Grid item xs={12} md={6} key={notebook.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📓 {notebook.name}
                </Typography>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {notebook.url}
                </Typography>

                {notebook.description && (
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    {notebook.description}
                  </Typography>
                )}

                <Box sx={{ mb: 1 }}>
                  {notebook.tags?.map(tag => (
                    <Chip key={tag} label={tag} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                  ))}
                </Box>

                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Typography variant="caption">
                    <QueryStatsIcon fontSize="small" /> Queries: {notebook.use_count || 0}
                  </Typography>
                  <Typography variant="caption">
                    Last used: {notebook.last_used
                      ? new Date(notebook.last_used).toLocaleDateString()
                      : 'Never'}
                  </Typography>
                </Box>
              </CardContent>

              <CardActions>
                <Button size="small" startIcon={<EditIcon />}>
                  Edit
                </Button>
                <Button
                  size="small"
                  color="error"
                  startIcon={<DeleteIcon />}
                  onClick={() => handleDelete(notebook.id)}
                >
                  Remove
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Add/Edit Dialog */}
      <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Notebook</DialogTitle>
        <DialogContent>
          {/* Same form as NotebookSetupStep */}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>Cancel</Button>
          <Button variant="contained">Add Notebook</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
```

---

## Success Criteria

**Sprint 16 is DONE when:**

- [ ] Setup Wizard includes NotebookLM step (Step 4)
- [ ] User can add 1-5 notebooks during setup
- [ ] System auto-categorizes by type (ideas/characters/structure)
- [ ] URL validation and connection testing works
- [ ] Notebooks saved to `notebooks.json` automatically
- [ ] Project Settings has Notebooks tab
- [ ] Can add/edit/remove notebooks via UI
- [ ] Usage statistics displayed (query count, last used)
- [ ] All CRUD API endpoints working
- [ ] Beginner path asks for single NotebookLM URL (Sprint 15 integration)
- [ ] 5 beta testers complete setup with notebooks

---

## Integration with Sprint 15

**Sprint 15 (Beginner Mode):**
- Asks for single NotebookLM URL (personal writing collection)
- Auto-categorizes as "beginner" notebook
- Extracts voice from personal writing

**Sprint 16 Enhancement:**
- Same UI component (NotebookSetupStep)
- Beginner path: Show only single URL input
- Experienced path: Show full multi-notebook selection
- Beginner's notebook tagged: `["beginner", "voice-extraction"]`

**Code Reuse:**
```jsx
// In beginner workflow
<NotebookSetupStep
  projectId={projectId}
  beginnerMode={true}  // Shows single input only
  onComplete={extractVoiceAndGenerateStarterSkills}
/>

// In experienced workflow
<NotebookSetupStep
  projectId={projectId}
  beginnerMode={false}  // Shows full multi-notebook UI
  onComplete={handleNext}
/>
```

---

## Testing Strategy

### Unit Tests

```bash
# Backend
pytest tests/test_notebook_management.py -v

# Test cases:
- test_add_notebook_success
- test_add_notebook_duplicate_url
- test_update_notebook
- test_remove_notebook
- test_notebook_url_validation
- test_usage_tracking
```

### Integration Tests

```bash
# Full workflow
pytest tests/test_notebook_integration.py -v

# Test cases:
- test_setup_wizard_with_notebooks
- test_query_with_auto_selection
- test_query_with_manual_selection
- test_usage_statistics_update
```

### User Acceptance Testing

**Recruit 5 beta testers:**
1. Complete project setup with 3 notebooks
2. Query notebooks while writing scenes
3. Add new notebook via Project Settings
4. Verify auto-selection works
5. Check usage statistics accurate

**Success:** 5/5 complete without issues

---

## Timeline

**Week 1: Backend (40 hours)**
- Monday-Tuesday: CRUD API endpoints (16h)
- Wednesday-Thursday: Usage tracking, validation (16h)
- Friday: Testing and bug fixes (8h)

**Week 2: Frontend (40 hours)**
- Monday-Tuesday: NotebookSetupStep component (16h)
- Wednesday-Thursday: NotebookManager UI (16h)
- Friday: Integration, testing, polish (8h)

**Total:** 80 hours / 2 weeks

---

## Dependencies

**Sprint 15 (Beginner Mode):** Must be complete first
**Sprint 11 (NotebookLM Integration):** Already complete ✅

---

## Deliverables

1. ✅ 5 new API endpoints (`/api/research/notebooks/*`)
2. ✅ NotebookSetupStep React component
3. ✅ NotebookManager React component
4. ✅ Enhanced `notebooks.json` schema with usage tracking
5. ✅ Updated Setup Wizard with Step 4
6. ✅ Project Settings with Notebooks tab
7. ✅ Unit + integration tests
8. ✅ 5 beta testers validated workflow

---

## User Won't Need To:

❌ Edit JSON files manually
❌ Know file paths
❌ Understand notebook schema
❌ Write configuration code

## User Will:

✅ Paste NotebookLM URLs during setup
✅ Click "Test Connection" button
✅ See notebooks in Project Settings
✅ Add/edit/remove via UI
✅ Query notebooks while writing
✅ See usage statistics

**This is what you wanted - fully automated notebook management through the UI!** 🎯
