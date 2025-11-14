# Cloud Agent Sprint 5 Tasks

**Date**: November 14, 2025
**Status**: Ready to start
**Previous Work**: Sprint 1+2+3+4 ALL APPROVED ✅ (All A+ grades!)

---

## 🎉 Sprint 4 Review Results

**Your work was PERFECT!** Here's what Claude Code found:

- ✅ All 7 tasks delivered (100% complete)
- ✅ Code quality: A+ (100/100)
- ✅ Beautiful landing page with gradients
- ✅ Complete 4-phase wizard
- ✅ Build succeeds (107.75kB gzipped, 1.11s)
- ✅ Zero bugs or issues

**Approved for merge** 🚀

**That's 4 consecutive A+ sprints!** Outstanding work!

---

## 🎯 Sprint 5: Character Development Panel ⭐ CRITICAL FEATURE

This is the **#1 missing feature** identified by the user's NotebookLM craft knowledge analysis.

**Why Critical**: "Complexity is created by CONTRADICTION" - this is THE differentiator between amateur flat characters and professional dimensional ones.

**Timeline**: 3-4 days
**Priority**: **CRITICAL** (This makes Writers Factory professional-grade)

---

## 📋 Background: The Problem

### Amateur Characters (Flat "Stick Figures"):
- No internal contradictions
- True Character mirrors Characterization (predictable)
- Shallow flaws (observations, not psychological conflicts)
- Supporting cast doesn't reveal protagonist dimensions

### Professional Characters (Dimensional):
- Internal contradictions ("guilt-ridden ambition")
- External contradictions ("charming thief", "lonely but always smiling")
- Deep flaws driven by mistaken beliefs
- Supporting cast specifically designed to reveal protagonist complexity

**Your job**: Build software that **automatically detects** these problems and **guides writers** to fix them.

---

## 📋 Tasks

### Task 5-01: Character Data Model

**Backend**: `factory/core/manuscript.py`

Add Character class to manuscript model:

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Character:
    """Represents a character in the manuscript."""
    id: str
    name: str
    role: str  # 'protagonist', 'antagonist', 'supporting'

    # True Character (inner core)
    core_traits: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)

    # Characterization (observable)
    appearance: str = ""
    mannerisms: str = ""
    speech_pattern: str = ""
    observable_traits: List[str] = field(default_factory=list)

    # Flaw & Arc
    fatal_flaw: str = ""
    mistaken_belief: str = ""
    transformation_goal: str = ""

    # Relationships (for supporting cast)
    reveals_protagonist_dimension: str = ""  # Which side they reveal
    serves_protagonist_goal: str = ""  # How they help protagonist

    # Metadata
    arc_notes: str = ""
    scene_appearances: List[str] = field(default_factory=list)


@dataclass
class Manuscript:
    # ... existing fields ...
    characters: List[Character] = field(default_factory=list)

    def add_character(self, character: Character):
        """Add a character to the manuscript."""
        self.characters.append(character)

    def get_protagonist(self) -> Optional[Character]:
        """Get the protagonist character."""
        for char in self.characters:
            if char.role == 'protagonist':
                return char
        return None

    def get_supporting_cast(self) -> List[Character]:
        """Get all supporting characters."""
        return [c for c in self.characters if c.role == 'supporting']
```

**Acceptance**:
- ✅ Character class added to manuscript model
- ✅ Separates True Character vs Characterization
- ✅ Includes flaw with mistaken_belief field
- ✅ Supporting cast tracks relationship to protagonist
- ✅ Manuscript can store and retrieve characters

---

### Task 5-02: Character Contradiction Analyzer (Backend)

**Create**: `factory/agents/character_analyzer.py`

This is the **core algorithm** from NotebookLM insights:

```python
"""Character dimensional depth analyzer.

Detects contradictions and complexity in character design.
"""

from typing import Dict, List, Any
import re


def analyze_character_depth(character_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze character for dimensional depth through contradiction.

    Returns analysis with:
    - depth_score (0-100)
    - flags (list of issues detected)
    - recommendations (list of fixes)
    """
    results = {
        "depth_score": 0,
        "flags": [],
        "recommendations": []
    }

    # 1. CHECK: External Contradiction (True Character vs Characterization)
    core_traits = character_data.get("core_traits", [])
    observable_traits = character_data.get("observable_traits", [])

    if not core_traits or not observable_traits:
        results["flags"].append({
            "severity": "HIGH",
            "type": "INCOMPLETE_CHARACTER_DEFINITION",
            "message": "Character lacks both True Character and Characterization data.",
            "recommendation": "Define core internal traits (True Character) and observable external traits (Characterization)"
        })
    elif are_traits_identical(core_traits, observable_traits):
        results["flags"].append({
            "severity": "HIGH",
            "type": "NO_EXTERNAL_CONTRADICTION",
            "message": "True Character directly mirrors Characterization. Character is predictable and flat.",
            "example": "If core is 'Courageous, Loyal' and actions are always 'Bold, Honorable', there's no mask or conflict.",
            "recommendation": "Create dissonance: e.g., 'loyal' internally but appears 'untrustworthy' externally (a charming thief)"
        })
    else:
        results["depth_score"] += 25

    # 2. CHECK: Internal Contradiction (Within True Character)
    internal_contradiction = detect_trait_polarity(core_traits)

    if not internal_contradiction:
        results["flags"].append({
            "severity": "CRITICAL",
            "type": "NO_INTERNAL_CONTRADICTION",
            "message": "Character has no internal contradictions detected.",
            "example": "Need opposing forces like 'guilt-ridden ambition' or 'compassionate yet cruel'",
            "recommendation": "Add contradictory core traits that create internal tension"
        })
    else:
        results["depth_score"] += 35
        results["recommendations"].append({
            "type": "STRENGTH",
            "message": f"Good internal contradiction detected: {internal_contradiction}"
        })

    # 3. CHECK: Fatal Flaw Depth
    flaw = character_data.get("fatal_flaw", "")
    mistaken_belief = character_data.get("mistaken_belief", "")

    if not flaw or len(flaw) < 10:
        results["flags"].append({
            "severity": "MEDIUM",
            "type": "MISSING_FLAW",
            "message": "Character lacks a defined fatal flaw.",
            "recommendation": "Define a flaw that will drive character transformation"
        })
    elif not mistaken_belief or len(mistaken_belief) < 20:
        results["flags"].append({
            "severity": "HIGH",
            "type": "SHALLOW_FLAW",
            "message": "Flaw description lacks clear mistaken belief or transformational potential.",
            "example": "'Impatient' (observation) vs 'Must control everything or will fail' (deep psychological conflict)",
            "recommendation": "Reframe flaw as a mistaken belief the character must overcome to transform"
        })
    else:
        results["depth_score"] += 20

    # 4. CHECK: Supporting Cast Utility (if protagonist)
    if character_data.get("role") == "protagonist":
        # This check needs supporting cast data (done in separate endpoint)
        pass

    return results


def are_traits_identical(core_traits: List[str], observable_traits: List[str]) -> bool:
    """Check if core and observable traits are too similar (no contradiction)."""
    # Simple heuristic: if >70% of traits overlap semantically, they're too similar
    core_set = set([t.lower().strip() for t in core_traits])
    obs_set = set([t.lower().strip() for t in observable_traits])

    overlap = len(core_set & obs_set)
    total = max(len(core_set), len(obs_set))

    if total == 0:
        return True  # No traits defined

    similarity = overlap / total
    return similarity > 0.7  # >70% similarity = no real contradiction


def detect_trait_polarity(traits: List[str]) -> Optional[str]:
    """
    Detect if contradictory traits exist within character.

    Returns description of contradiction if found, None otherwise.
    """
    # Known opposition pairs
    oppositions = [
        (["ambitious", "driven", "determined"], ["guilty", "self-doubting", "ashamed"]),
        (["compassionate", "kind", "empathetic"], ["cruel", "ruthless", "cold"]),
        (["loyal", "faithful", "devoted"], ["betraying", "traitorous", "deceitful"]),
        (["charming", "charismatic", "likable"], ["thief", "criminal", "dishonest"]),
        (["lonely", "isolated", "alone"], ["smiling", "cheerful", "upbeat"]),
        (["brave", "courageous", "bold"], ["fearful", "cowardly", "hesitant"]),
    ]

    traits_lower = [t.lower().strip() for t in traits]

    for group1, group2 in oppositions:
        has_group1 = any(t1 in traits_lower for t1 in group1)
        has_group2 = any(t2 in traits_lower for t2 in group2)

        if has_group1 and has_group2:
            # Found contradiction!
            t1_found = [t for t in traits_lower if t in group1][0]
            t2_found = [t for t in traits_lower if t in group2][0]
            return f"{t1_found} yet {t2_found}"

    return None


def analyze_protagonist_dimensionality(
    protagonist_data: Dict[str, Any],
    supporting_cast_data: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check if protagonist is most dimensional character.

    Analyzes supporting cast to ensure they serve protagonist's complexity.
    """
    results = {
        "is_most_dimensional": True,
        "flags": []
    }

    # Get protagonist depth score
    protagonist_analysis = analyze_character_depth(protagonist_data)
    protagonist_score = protagonist_analysis["depth_score"]

    # Check each supporting character
    for support_char in supporting_cast_data:
        support_analysis = analyze_character_depth(support_char)
        support_score = support_analysis["depth_score"]

        if support_score > protagonist_score:
            results["is_most_dimensional"] = False
            results["flags"].append({
                "severity": "CRITICAL",
                "type": "PROTAGONIST_LESS_DIMENSIONAL",
                "message": f"Protagonist is less dimensional than Supporting Character '{support_char.get('name')}'.",
                "protagonist_score": protagonist_score,
                "support_score": support_score,
                "recommendation": "Protagonist MUST be the most dimensional character in the cast. Add more contradictions to protagonist."
            })

        # Check if supporting character reveals protagonist dimension
        reveals_dimension = support_char.get("reveals_protagonist_dimension", "")
        if not reveals_dimension:
            results["flags"].append({
                "severity": "MEDIUM",
                "type": "REDUNDANT_SUPPORTING_CHARACTER",
                "message": f"Character '{support_char.get('name')}' does not delineate protagonist's complexity.",
                "recommendation": "Each secondary character should reveal a specific contradictory side of protagonist (e.g., cruel side, compassionate side)"
            })

    return results
```

**Acceptance**:
- ✅ Implements all 4 checks from NotebookLM
- ✅ Returns depth_score (0-100)
- ✅ Flags specific problems with severity levels
- ✅ Provides actionable recommendations
- ✅ Detects trait polarity (internal contradiction)

---

### Task 5-03: Character Panel UI (Frontend)

**Create**: `src/features/character/CharacterPanel.jsx`

```jsx
import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { AlertTriangle, CheckCircle2, Lightbulb, Users } from 'lucide-react';
import { toast } from 'sonner';

export function CharacterPanel({ manuscript }) {
  const [selectedCharacterId, setSelectedCharacterId] = useState(null);

  // Fetch character list
  const { data: characters } = useQuery({
    queryKey: ['characters', manuscript?.id],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/manuscript/${manuscript.id}/characters`);
      return res.json();
    },
    enabled: !!manuscript
  });

  // Analyze character
  const { data: analysis, isLoading: analyzing } = useQuery({
    queryKey: ['character-analysis', selectedCharacterId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/character/${selectedCharacterId}/analyze`, {
        method: 'POST'
      });
      return res.json();
    },
    enabled: !!selectedCharacterId
  });

  const selectedCharacter = characters?.find(c => c.id === selectedCharacterId);

  return (
    <div className="h-full flex flex-col bg-gray-800">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3 flex items-center gap-2">
          <Users size={20} />
          Character Development
        </h3>

        {/* Character Selector */}
        <select
          value={selectedCharacterId || ''}
          onChange={(e) => setSelectedCharacterId(e.target.value)}
          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm"
        >
          <option value="">Select a character...</option>
          {characters?.map(char => (
            <option key={char.id} value={char.id}>
              {char.name} ({char.role})
            </option>
          ))}
        </select>
      </div>

      {/* Analysis Results */}
      {selectedCharacter && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Depth Score */}
          <div className="p-4 bg-gray-700 rounded-lg">
            <div className="text-sm text-gray-400 mb-2">Dimensional Depth</div>
            <div className="flex items-end gap-3">
              <div className="text-4xl font-bold">
                {analysis?.depth_score || 0}
              </div>
              <div className="text-gray-400 mb-1">/100</div>
            </div>
            <div className="mt-2 h-2 bg-gray-600 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all ${
                  (analysis?.depth_score || 0) < 50 ? 'bg-red-500' :
                  (analysis?.depth_score || 0) < 80 ? 'bg-yellow-500' :
                  'bg-green-500'
                }`}
                style={{ width: `${analysis?.depth_score || 0}%` }}
              />
            </div>
            <div className="text-xs text-gray-400 mt-2">
              {(analysis?.depth_score || 0) < 50 ? '⚠️ Flat character - needs contradictions' :
               (analysis?.depth_score || 0) < 80 ? '🔶 Developing - add more complexity' :
               '✅ Dimensional - well-developed'}
            </div>
          </div>

          {/* Flags */}
          {analyzing && (
            <div className="text-center text-gray-400 py-8">
              Analyzing character depth...
            </div>
          )}

          {analysis?.flags && analysis.flags.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-semibold text-sm flex items-center gap-2">
                <AlertTriangle size={16} />
                Issues Detected
              </h4>
              {analysis.flags.map((flag, idx) => (
                <div
                  key={idx}
                  className={`p-4 rounded-lg border-l-4 ${
                    flag.severity === 'CRITICAL' ? 'bg-red-900/20 border-red-500' :
                    flag.severity === 'HIGH' ? 'bg-orange-900/20 border-orange-500' :
                    'bg-yellow-900/20 border-yellow-500'
                  }`}
                >
                  <div className="flex items-start gap-2 mb-2">
                    <AlertTriangle size={16} className="mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="font-semibold text-sm mb-1">{flag.message}</div>
                      {flag.example && (
                        <div className="text-xs text-gray-400 mt-2 italic">
                          <strong>Example:</strong> {flag.example}
                        </div>
                      )}
                      {flag.recommendation && (
                        <div className="text-xs text-blue-300 mt-2 flex items-start gap-1">
                          <Lightbulb size={14} className="mt-0.5 flex-shrink-0" />
                          {flag.recommendation}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {analysis?.flags && analysis.flags.length === 0 && (
            <div className="p-4 bg-green-900/20 border border-green-700/50 rounded-lg flex items-center gap-2">
              <CheckCircle2 size={20} className="text-green-400" />
              <span className="text-green-300">No issues detected - character is well-developed!</span>
            </div>
          )}

          {/* Contradiction Workshop */}
          <div className="p-4 bg-blue-900/20 border border-blue-700/50 rounded-lg">
            <h4 className="font-semibold text-sm mb-2 flex items-center gap-2">
              <Lightbulb size={16} />
              Contradiction Workshop
            </h4>
            <p className="text-xs text-gray-400 mb-3">
              Professional characters are built on contradictions. Add opposing traits to create dimensional depth.
            </p>
            <button className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors">
              Generate Contradiction Ideas
            </button>
          </div>
        </div>
      )}

      {!selectedCharacter && (
        <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
          Select a character to analyze dimensional depth
        </div>
      )}
    </div>
  );
}
```

**Acceptance**:
- ✅ Shows character selector dropdown
- ✅ Displays depth score (0-100) with color-coded bar
- ✅ Lists all flags with severity indicators
- ✅ Shows recommendations with lightbulb icon
- ✅ Includes example text for context
- ✅ Contradiction workshop section
- ✅ Loading states while analyzing

---

### Task 5-04: Backend Endpoints

**Update**: `webapp/backend/simple_app.py`

Add endpoints for character analysis:

```python
from factory.agents.character_analyzer import (
    analyze_character_depth,
    analyze_protagonist_dimensionality
)

@app.get("/api/manuscript/{manuscript_id}/characters")
async def get_characters(manuscript_id: str):
    """Get all characters in manuscript."""
    try:
        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            # Load from disk
            manuscript_path = project_path / ".manuscript" / manuscript_id
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        if not manuscript:
            return {"characters": []}

        # Return character data
        return {
            "characters": [
                {
                    "id": char.id,
                    "name": char.name,
                    "role": char.role,
                    "core_traits": char.core_traits,
                    "observable_traits": char.observable_traits,
                    "fatal_flaw": char.fatal_flaw,
                    "mistaken_belief": char.mistaken_belief,
                    "reveals_protagonist_dimension": char.reveals_protagonist_dimension
                }
                for char in manuscript.characters
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/character/{character_id}/analyze")
async def analyze_character(character_id: str):
    """Analyze character for dimensional depth."""
    try:
        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Find character
        character = None
        for char in manuscript.characters:
            if char.id == character_id:
                character = char
                break

        if not character:
            raise HTTPException(status_code=404, detail="Character not found")

        # Convert to dict for analyzer
        character_data = {
            "id": character.id,
            "name": character.name,
            "role": character.role,
            "core_traits": character.core_traits,
            "observable_traits": character.observable_traits,
            "fatal_flaw": character.fatal_flaw,
            "mistaken_belief": character.mistaken_belief,
            "reveals_protagonist_dimension": character.reveals_protagonist_dimension
        }

        # Run analysis
        results = analyze_character_depth(character_data)

        # If protagonist, also check dimensionality vs supporting cast
        if character.role == "protagonist":
            supporting_cast = [
                {
                    "id": c.id,
                    "name": c.name,
                    "core_traits": c.core_traits,
                    "observable_traits": c.observable_traits,
                    "fatal_flaw": c.fatal_flaw,
                    "mistaken_belief": c.mistaken_belief,
                    "reveals_protagonist_dimension": c.reveals_protagonist_dimension
                }
                for c in manuscript.characters if c.role == "supporting"
            ]

            protagonist_check = analyze_protagonist_dimensionality(
                character_data,
                supporting_cast
            )

            # Merge flags
            results["flags"].extend(protagonist_check["flags"])

        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Acceptance**:
- ✅ GET /api/manuscript/{id}/characters returns all characters
- ✅ POST /api/character/{id}/analyze runs depth analysis
- ✅ Returns depth_score and flags
- ✅ Checks protagonist dimensionality vs supporting cast
- ✅ Proper error handling

---

### Task 5-05: Integrate Character Panel into App

**Update**: `webapp/frontend-v2/src/App.jsx`

Add Character panel to right sidebar options:

```jsx
import { CharacterPanel } from './features/character/CharacterPanel';

function App() {
  // ... existing state ...
  const [rightPanel, setRightPanel] = useState('tools'); // 'tools' | 'knowledge' | 'tournament' | 'character'

  return (
    <div className="h-screen flex flex-col bg-gray-900 text-gray-100">
      {/* Top Bar */}
      <div className="h-12 border-b border-gray-700 flex items-center justify-between px-4 bg-gray-800">
        <div className="flex items-center gap-4">
          {/* ... existing buttons ... */}

          <button
            onClick={() => setRightPanel('character')}
            className={`px-3 py-1 rounded text-sm ${rightPanel === 'character' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
          >
            Character
          </button>

          {/* ... rest of buttons ... */}
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex-1 overflow-hidden">
        <PanelGroup direction="horizontal">
          {/* ... Left and Center panels ... */}

          {/* Right: Tools Panel */}
          <Panel defaultSize={30} minSize={20} className="border-l border-gray-700 bg-gray-800">
            {rightPanel === 'tools' && <AIToolsPanel currentScene={selectedScene} models={models} />}
            {rightPanel === 'knowledge' && <KnowledgePanel />}
            {rightPanel === 'tournament' && <TournamentPanel currentScene={selectedScene} models={models} />}
            {rightPanel === 'character' && <CharacterPanel manuscript={manuscript} />}
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
}
```

**Acceptance**:
- ✅ Character button added to top bar
- ✅ CharacterPanel shows when selected
- ✅ Integrates with existing right panel system
- ✅ Has access to manuscript data

---

## 🎯 Success Criteria

**Sprint 5 Complete When**:
- ✅ Character data model added to manuscript
- ✅ Character analyzer implements all 4 checks (external contradiction, internal contradiction, flaw depth, protagonist dimensionality)
- ✅ Frontend panel shows depth score and flags
- ✅ Backend endpoints return analysis results
- ✅ Character panel integrated into app
- ✅ All previous features still work

---

## 📁 File Changes Expected

**New Files**:
- `factory/agents/character_analyzer.py` (core algorithm)
- `src/features/character/CharacterPanel.jsx` (UI)

**Modified Files**:
- `factory/core/manuscript.py` (add Character class)
- `webapp/backend/simple_app.py` (add 2 endpoints)
- `src/App.jsx` (add Character button + panel)

---

## 🧪 Testing

After implementation:

1. **Test Character Analysis**:
   - Create a character with no contradictions
   - Should flag "NO_INTERNAL_CONTRADICTION"
   - Add opposing traits (e.g., "ambitious" + "guilty")
   - Depth score should increase by 35 points

2. **Test Protagonist Check**:
   - Make supporting character more complex than protagonist
   - Should flag "PROTAGONIST_LESS_DIMENSIONAL"

3. **Test UI**:
   - Select character from dropdown
   - Should show depth score and color-coded bar
   - Should list all flags with recommendations

---

## 💡 Design Notes

**This is the most important feature from NotebookLM analysis.**

Your craft knowledge emphasized:
- "Complexity is created by contradiction" - THE formula
- Amateur characters are "stick figures" (one-dimensional)
- Professional characters have internal + external contradictions
- Protagonist MUST be most dimensional character

**Implementation Philosophy**:
- Algorithmic detection (not subjective)
- Specific, measurable metrics
- Actionable recommendations
- Based on proven craft principles

---

## 🚀 Ready to Start?

You have all the context:
- ✅ Sprint 1-4 code is solid foundation
- ✅ Character model defined
- ✅ Analyzer algorithm specified (from NotebookLM)
- ✅ UI mockup provided
- ✅ Integration pattern clear

**Estimated time**: 3-4 days (5 tasks)

**Expected outcome**: Professional-grade character development tool that **automatically detects flat characters** and **guides writers to add dimensional depth**!

This is what separates amateur writing tools from professional craft assistance. Let's build it! 💪

---

**Document Created**: November 14, 2025
**For**: Cloud Agent (Sprint 5)
**Previous Grade**: A+ on Sprint 1+2+3+4
**Status**: Ready to start immediately
**Priority**: CRITICAL (Based on NotebookLM craft analysis)
