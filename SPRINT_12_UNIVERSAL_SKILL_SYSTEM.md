# Sprint 12: Universal Skill Orchestration System + Creation Wizard

**Date**: November 14, 2025
**Priority**: CRITICAL - Transform Writers Factory into intelligent multi-agent platform
**Estimated Time**: 30-35 hours (with agent efficiency, much faster in reality)
**Goal**: Make all 6 Explants skills accessible + enable ANY writer to create their own custom skills

---

## 🎯 Vision

Transform Writers Factory from "tool with baked-in skills" to **"platform where ANY writer can codify THEIR craft expertise into reusable AI skills."**

### What This Sprint Delivers

**For G.C. Harris (Immediate):**
- ✅ All 6 Explants Claude Skills accessible through Writers Factory UI
- ✅ Intelligent orchestrator routing to best available provider
- ✅ Can create NEW skills for Volume 2 without coding
- ✅ Complete workflow from outline → final scene with craft automation

**For Students (Near Future):**
- ✅ Native Python agents work offline (no Claude Code dependency)
- ✅ Can create their OWN craft skills via wizard
- ✅ Define their OWN voice profiles
- ✅ Link their OWN reference materials

**For The Product (Long Term):**
- ✅ Platform architecture, not just a tool
- ✅ Skill marketplace potential
- ✅ Every writer becomes a craft expert
- ✅ Viral growth through skill sharing

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Writers Factory UI                           │
│  (Scene Editor, File Tree, AI Tools Panel, Craft Panel, Wizard) │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               Skill Orchestrator (The Brain)                     │
│  • Routes skill requests to best available provider              │
│  • Handles authentication, fallbacks, error handling             │
│  • Tracks usage, costs, performance                              │
│  • Service discovery and capability declaration                  │
│  • Executes custom skills from wizard                            │
└───┬──────────────────┬──────────────────┬──────────────────────┘
    │                  │                  │
    ▼                  ▼                  ▼
┌──────────────┐  ┌───────────────┐  ┌─────────────────┐
│  MCP Bridge  │  │ Native Python │  │ Custom Skills   │
│  (Claude     │  │ Agents        │  │ (Wizard-created)│
│   Skills)    │  │ (Offline)     │  │                 │
└──────────────┘  └───────────────┘  └─────────────────┘
    │
    ▼
Your 6 Claude Skills:
1. explants-scene-analyzer-scorer
2. explants-scene-enhancement
3. mickey-bardot-character-identity
4. explants-mickey-scene-writer
5. explants-scene-multiplier
6. explants-smart-scaffold-generator
```

---

## 📋 Implementation Tasks

### Phase A: Foundation & Your Skills (22-25h)

#### Task 12-01: MCP Skill Bridge (4h)

**Goal:** Build bridge that exposes Claude Skills via MCP protocol

**File:** `factory/mcp/claude_skill_bridge.py`

**Key Components:**

1. **SkillDefinition dataclass** - Metadata for each skill
   - name, skill_id, capability, version
   - requires_auth, cost_tier, description
   - input_schema, output_schema

2. **MCPSkillBridge class** - Main bridge logic
   - `_register_skills()` - Register all 6 Explants skills with metadata
   - `call_skill()` - Call a Claude Skill via MCP protocol
   - `_call_claude_skill()` - Actually invoke the skill
   - `_check_entitlement()` - Check user access to skill tier
   - `_fallback_response()` - Return fallback when skill unavailable
   - `_error_response()` - Standardized MCP error responses
   - `list_skills()` - List available skills with metadata
   - `get_skill_info()` - Get detailed info about specific skill

**Skills to Register:**

```python
self.skills_registry = {
    "scene-analyzer": SkillDefinition(
        name="explants-scene-analyzer-scorer",
        capability="analyze",
        input_schema={
            "scene_content": "string",
            "mode": "enum[detailed|quick|variant_comparison]",
            "reference_files": "array[string]"
        },
        output_schema={
            "total_score": "integer",
            "category_scores": "object",
            "quality_tier": "string",
            "fixes": "array[object]"
        }
    ),
    "scene-enhancer": SkillDefinition(...),
    "character-validator": SkillDefinition(...),
    "scene-writer": SkillDefinition(...),
    "scene-multiplier": SkillDefinition(...),
    "scaffold-generator": SkillDefinition(...)
}
```

**MCP Protocol Compliance:**
- All requests/responses follow MCP JSON schema
- Authentication handled via API keys
- Structured error objects with codes
- Metadata included in all responses

**Testing:**
- Unit tests for each skill registration
- Integration test calling actual Claude Skill
- Error handling tests (auth failure, rate limit, etc.)

---

#### Task 12-02: Skill Orchestrator (4h)

**Goal:** Central routing system for all writing craft skills

**File:** `factory/core/skill_orchestrator.py`

**Key Components:**

1. **SkillProvider enum** - Available providers
   - CLAUDE_SKILL, NATIVE_PYTHON, OPENAI, LOCAL_LLM, CUSTOM

2. **SkillRequest dataclass** - Standardized request format
   - skill_name, capability, input_data, context
   - user_id, preferred_provider, allow_fallback

3. **SkillResponse dataclass** - Standardized response format
   - status, provider, data, metadata
   - cost, execution_time

4. **SkillOrchestrator class** - The brain
   - `execute_skill()` - Route and execute skill request
   - `_get_provider_priority()` - Determine provider order based on:
     * User preference
     * User entitlement (premium vs standard)
     * Provider health
     * Cost optimization
   - `_call_provider()` - Route to specific provider
   - `list_available_skills()` - List skills available to user
   - `get_skill_info()` - Get skill details
   - `health_check()` - Check all providers

**Routing Logic:**

```python
# Premium users
1. Try Claude Skill (battle-tested, premium)
2. Fall back to Native Python (offline, free)

# Standard users
1. Try Native Python (free, offline)
2. Fall back to Claude Skill (if available)
```

**Provider Integration:**
- MCPSkillBridge for Claude Skills
- Native agent classes for Python implementations
- Extensible for future providers (OpenAI, local LLMs)

**Usage Tracking:**
- Log all skill executions
- Track costs per provider
- Monitor execution times
- Health check status

**Testing:**
- Test routing logic for different user tiers
- Test fallback behavior
- Test error recovery
- Test health checks

---

#### Task 12-03: Native Scene Analyzer Agent (5h)

**Goal:** First native Python implementation - proof of concept and most critical skill

**File:** `factory/agents/explants/scene_analyzer.py`

**Key Components:**

1. **SceneScore dataclass** - Complete scoring breakdown
   - total_score (0-100)
   - 5 category scores
   - quality_tier, fixes, details

2. **SceneAnalyzerAgent class** - Native implementation
   - `execute()` - Main entry point (MCP-compatible)
   - `_score_scene()` - Run complete scoring
   - `_score_voice_authenticity()` - Observer/Consciousness War/Cognitive Fusion tests
   - `_score_character_consistency()` - Psychology/capabilities/relationships
   - `_score_metaphor_discipline()` - Domain rotation/simile elimination
   - `_score_anti_patterns()` - Zero-tolerance violations
   - `_score_phase_appropriateness()` - Voice complexity matching
   - `_generate_fixes()` - Specific line-by-line fixes
   - `_load_knowledge()` - Load reference materials
   - `_compile_anti_patterns()` - Regex patterns for detection
   - `_load_metaphor_domains()` - Domain classification rules

**Scoring Framework (100 points):**

| Category | Weight | Implementation |
|----------|--------|----------------|
| Voice Authenticity | 30 | Observer/Consciousness War/Cognitive Fusion tests |
| Character Consistency | 20 | Psychology/capabilities/relationships validation |
| Metaphor Discipline | 20 | Domain rotation, simile detection, transformation check |
| Anti-Pattern Compliance | 15 | Zero-tolerance violations (-2 pts), formulaic patterns (-1 pt) |
| Phase Appropriateness | 15 | Voice complexity + technical language validation |

**Anti-Pattern Detection (Regex):**

```python
self.anti_patterns = {
    "first_person_italics": re.compile(r'\*[^*]*\b(we|I)\b[^*]*\*'),
    "with_precision": re.compile(r'\bwith \w+ precision\b'),
    "with_adjective_noun": re.compile(r'\bwith (the |a |an )?([\w]+) ([\w]+)\b'),
    "computer_psychology": re.compile(r'\b(processed|downloaded|uploaded)\b.*\b(emotion|thought|feeling)\b'),
    "weak_similes": re.compile(r'\b(like (a|an|the)|as if|resembled|seemed like)\b'),
    "formulaic_walking": re.compile(r'\bwalked \w+ly\b'),
    "academic_tone": re.compile(r'\b(furthermore|moreover|in conclusion)\b')
}
```

**Quality Tiers:**

```python
95-100: Gold Standard (publishable as-is)
90-94:  A+ Excellent (minor polish only)
85-89:  A Strong (enhancement pass recommended)
80-84:  A- Good (1-2 specific issues)
75-79:  B+ Acceptable (enhancement required)
70-74:  B Functional (multiple issues)
<70:    Needs Rework (consider multiplier or major revision)
```

**Output Format:**

```json
{
  "status": "success",
  "data": {
    "total_score": 87,
    "category_scores": {
      "voice_authenticity": 26,
      "character_consistency": 18,
      "metaphor_discipline": 17,
      "anti_pattern_compliance": 13,
      "phase_appropriateness": 13
    },
    "quality_tier": "A Strong (85-89)",
    "fixes": [
      {
        "type": "anti-pattern",
        "pattern": "with_precision",
        "old_string": "with practiced precision",
        "suggested_fix": "[DELETE THIS PHRASE]",
        "priority": "high"
      }
    ],
    "details": { ... }
  }
}
```

**Testing:**
- Test scoring on real Explants scenes
- Validate against Claude Skill results
- Test anti-pattern detection accuracy
- Test quality tier assignment

---

#### Task 12-04: Backend API Endpoints (2h)

**Goal:** Expose skills via REST API

**File:** `webapp/backend/simple_app.py` (additions)

**New Endpoints:**

```python
@app.post("/api/skills/execute")
async def execute_skill(request: dict):
    """
    Execute any skill via orchestrator.

    Request:
    {
        "skill_name": "scene-analyzer",
        "input_data": { "scene_content": "...", "mode": "detailed" },
        "context": { "project_id": "...", "user_id": "..." },
        "preferred_provider": "claude-skill"  # optional
    }

    Response:
    {
        "status": "success",
        "provider": "claude-skill",
        "data": { ... },
        "metadata": { "execution_time": 2.3, "cost": 0.05 }
    }
    """
    orchestrator = SkillOrchestrator()

    skill_request = SkillRequest(
        skill_name=request["skill_name"],
        capability=request.get("capability", ""),
        input_data=request["input_data"],
        context=request.get("context"),
        user_id=request.get("context", {}).get("user_id"),
        preferred_provider=request.get("preferred_provider"),
        allow_fallback=request.get("allow_fallback", True)
    )

    result = await orchestrator.execute_skill(skill_request)

    return {
        "status": result.status,
        "provider": result.provider.value,
        "data": result.data,
        "metadata": {
            "execution_time": result.execution_time,
            "cost": result.cost,
            **result.metadata
        }
    }

@app.get("/api/skills/list")
async def list_skills(user_id: Optional[str] = None):
    """
    List all skills available to user.

    Response:
    {
        "skills": [
            {
                "name": "scene-analyzer",
                "capability": "analyze",
                "providers": ["claude-skill", "native-python"],
                "cost_tier": "premium",
                "description": "100-point objective scene scoring"
            }
        ]
    }
    """
    orchestrator = SkillOrchestrator()
    skills = orchestrator.list_available_skills(user_id)
    return {"skills": skills}

@app.get("/api/skills/{skill_name}/info")
async def get_skill_info(skill_name: str):
    """Get detailed information about a specific skill."""
    orchestrator = SkillOrchestrator()
    info = orchestrator.get_skill_info(skill_name)
    if info:
        return info
    raise HTTPException(status_code=404, detail="Skill not found")

@app.get("/api/skills/health")
async def skills_health_check():
    """Check health of all skill providers."""
    orchestrator = SkillOrchestrator()
    health = await orchestrator.health_check()
    return health
```

**CORS Configuration:**
- Allow frontend origin (localhost:5173)
- Handle OPTIONS preflight requests

**Error Handling:**
- Return structured error responses
- Log errors for debugging
- Handle timeout scenarios

**Testing:**
- Test each endpoint with curl/Postman
- Integration tests with frontend
- Load testing for performance

---

#### Task 12-05: Frontend Integration (3h)

**Goal:** Expose skills in Writers Factory UI

**New Component:** `webapp/frontend-v2/src/features/craft/CraftPanel.jsx`

**Features:**

1. **Skill Selector**
   - Dropdown with all available skills
   - Show provider badge (Claude Skill vs Native)
   - Display skill description

2. **Input Area**
   - Text input for scene content
   - Mode selector (for analyzer: detailed/quick/comparison)
   - Context options (project, character, etc.)

3. **Execute Button**
   - Shows loading state during execution
   - Displays execution time and cost
   - Shows which provider was used

4. **Results Display**
   - For Scene Analyzer: Score breakdown, quality tier, fixes
   - For Scene Enhancer: Before/after comparison, preservation check
   - For Scene Writer: Generated scene with quality metrics
   - For Multiplier: 5 variants with scores

**Example Component:**

```jsx
import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';

export function CraftPanel({ projectId }) {
  const [selectedSkill, setSelectedSkill] = useState('scene-analyzer');
  const [input, setInput] = useState('');
  const [mode, setMode] = useState('detailed');

  // Get available skills
  const { data: skills } = useQuery(['skills'],
    () => fetch('/api/skills/list').then(r => r.json())
  );

  // Execute skill
  const executeMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('/api/skills/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skill_name: selectedSkill,
          input_data: {
            scene_content: input,
            mode: mode
          },
          context: { project_id: projectId }
        })
      });
      return res.json();
    }
  });

  return (
    <div className="craft-panel">
      <h2>Craft Tools</h2>

      {/* Skill Selector */}
      <div className="skill-selector">
        <label>Select Skill:</label>
        <select value={selectedSkill} onChange={e => setSelectedSkill(e.target.value)}>
          {skills?.skills.map(skill => (
            <option key={skill.name} value={skill.name}>
              {skill.name} ({skill.providers.join(', ')})
            </option>
          ))}
        </select>
      </div>

      {/* Input Area */}
      <div className="skill-input">
        <label>Scene Content:</label>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          rows={10}
          placeholder="Paste scene content here..."
        />

        {selectedSkill === 'scene-analyzer' && (
          <div className="mode-selector">
            <label>Mode:</label>
            <select value={mode} onChange={e => setMode(e.target.value)}>
              <option value="detailed">Detailed Analysis</option>
              <option value="quick">Quick Audit</option>
              <option value="variant_comparison">Compare Variants</option>
            </select>
          </div>
        )}
      </div>

      {/* Execute Button */}
      <button
        onClick={() => executeMutation.mutate()}
        disabled={!input || executeMutation.isLoading}
      >
        {executeMutation.isLoading ? 'Processing...' : 'Execute Skill'}
      </button>

      {/* Results Display */}
      {executeMutation.data && (
        <div className="skill-results">
          <div className="metadata">
            <span>Provider: {executeMutation.data.provider}</span>
            <span>Time: {executeMutation.data.metadata.execution_time.toFixed(2)}s</span>
            {executeMutation.data.metadata.cost > 0 && (
              <span>Cost: ${executeMutation.data.metadata.cost.toFixed(4)}</span>
            )}
          </div>

          {selectedSkill === 'scene-analyzer' && (
            <AnalyzerResults data={executeMutation.data.data} />
          )}

          {selectedSkill === 'scene-enhancer' && (
            <EnhancerResults data={executeMutation.data.data} />
          )}
        </div>
      )}
    </div>
  );
}

function AnalyzerResults({ data }) {
  return (
    <div className="analyzer-results">
      <div className="score-summary">
        <h3>Total Score: {data.total_score}/100</h3>
        <div className="quality-tier">{data.quality_tier}</div>
      </div>

      <div className="category-scores">
        <h4>Category Breakdown:</h4>
        <ul>
          <li>Voice Authenticity: {data.category_scores.voice_authenticity}/30</li>
          <li>Character Consistency: {data.category_scores.character_consistency}/20</li>
          <li>Metaphor Discipline: {data.category_scores.metaphor_discipline}/20</li>
          <li>Anti-Pattern Compliance: {data.category_scores.anti_pattern_compliance}/15</li>
          <li>Phase Appropriateness: {data.category_scores.phase_appropriateness}/15</li>
        </ul>
      </div>

      {data.fixes.length > 0 && (
        <div className="fixes">
          <h4>Recommended Fixes:</h4>
          <ul>
            {data.fixes.map((fix, i) => (
              <li key={i} className={`priority-${fix.priority}`}>
                <strong>{fix.pattern}:</strong> "{fix.old_string}" → {fix.suggested_fix}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

**UI/UX:**
- Clean, professional design
- Clear provider indicators
- Real-time execution feedback
- Copy-to-clipboard for results
- Export results as markdown

**Testing:**
- Test all skills through UI
- Test error handling
- Test loading states
- Test result display formatting

---

#### Task 12-06: Reference Knowledge Migration (2h)

**Goal:** Make reference materials accessible to agents

**Create Directory Structure:**

```
factory/knowledge/
├── craft/
│   ├── voice-gold-standard.md
│   ├── anti-patterns.md
│   ├── metaphor-domains.md
│   ├── polishing-ritual.md
│   ├── voice-authentication-tests.md
│   └── enhanced-strategy-advanced.md
├── character/
│   ├── mickey-psychology.md
│   ├── mickey-capabilities.md
│   ├── mickey-relationships.md
│   └── character-decision-framework.md
└── scoring/
    ├── rubrics.md
    ├── quality-tiers.md
    └── output-templates.md
```

**Migration Tasks:**

1. **Copy Reference Files**
   - From `.claude/skills/*/references/`
   - To `factory/knowledge/`
   - Organize by category

2. **Update Agent Code**
   - Update paths in SceneAnalyzerAgent
   - Update paths in future agents
   - Test loading works correctly

3. **Add to .gitignore (if needed)**
   - If reference materials are proprietary
   - Or commit if making open-source

**Testing:**
- Verify all reference files load correctly
- Test agents can access knowledge
- Check for missing dependencies

---

#### Task 12-07: Testing & Documentation (2h)

**Goal:** Comprehensive testing and documentation

**Testing Checklist:**

- [ ] MCP Bridge unit tests
- [ ] Orchestrator routing tests
- [ ] Native Scene Analyzer tests
- [ ] API endpoint integration tests
- [ ] Frontend component tests
- [ ] End-to-end workflow tests

**Documentation to Create:**

1. **SKILL_SYSTEM_GUIDE.md**
   - Architecture overview
   - How to use skills
   - Available skills catalog
   - Provider differences

2. **ADDING_NEW_SKILLS.md**
   - How to add native Python agent
   - How to register with orchestrator
   - Testing requirements
   - Integration checklist

3. **API_REFERENCE.md**
   - All skill endpoints
   - Request/response formats
   - Error codes
   - Examples

**Testing with Real Scenes:**
- Test Scene Analyzer on actual Explants scenes
- Compare results with Claude Skill version
- Validate scoring accuracy
- Check fix suggestions quality

---

### Phase B: Democratization (8-10h)

#### Task 12-08: Skill Creation Wizard Backend (4-5h)

**Goal:** Enable writers to create custom skills without coding

**File:** `factory/wizards/skill_creator.py`

**Key Components:**

1. **SkillTemplate enum** - Available templates
   - SCENE_ENHANCER, SCENE_ANALYZER, DIALOGUE_POLISHER
   - CHARACTER_VALIDATOR, VOICE_AUTHENTICATOR
   - PACING_ANALYZER, WORLDBUILDING_CHECKER, CUSTOM

2. **VoiceProfile dataclass** - Writer's voice characteristics
   - name, description, example_passages
   - tone_attributes (cynical, compressed, philosophical)
   - prohibited_patterns (similes, adverbs, passive voice)
   - signature_techniques (direct metaphors, short sentences)
   - domain_preferences (gambling: 25%, music: 20%)

3. **ProjectResources dataclass** - Reference materials
   - style_guides, character_sheets, world_bible
   - reference_scenes, glossaries, custom_docs

4. **SkillConfig dataclass** - Complete skill configuration
   - skill_id, skill_name, template
   - voice_profile, resources, parameters
   - success_criteria, version, created_by, created_at

5. **SkillCreationWizard class** - Main wizard logic
   - `create_skill()` - Interactive wizard flow
   - `_step_project_setup()` - Step 1
   - `_step_voice_definition()` - Step 2
   - `_step_resource_linking()` - Step 3
   - `_step_template_selection()` - Step 4
   - `_step_customize_skill()` - Step 5
   - `_step_test_skill()` - Step 6
   - `_register_skill()` - Step 7

**Template Library:**

```python
self.template_library = {
    SkillTemplate.SCENE_ENHANCER: {
        "name": "Scene Enhancer",
        "description": "Enhance scenes with voice-specific improvements",
        "parameters": {
            "mode": {
                "type": "enum",
                "options": ["full", "surgical", "voice_only"],
                "default": "full"
            },
            "preservation_rules": {
                "type": "list[string]",
                "description": "Elements to never modify"
            },
            "enhancement_passes": {
                "type": "list[string]",
                "options": [
                    "sensory_anchoring",
                    "verb_promotion",
                    "metaphor_rotation",
                    "voice_embedding",
                    "italics_gate"
                ]
            }
        },
        "required_resources": ["voice_profile", "anti_patterns"],
        "optional_resources": ["example_scenes", "style_guide"]
    },
    # ... more templates
}
```

**Wizard Flow:**

```
Step 1: Project Setup
→ Select existing project or create new
→ Define genre/style

Step 2: Voice Definition
→ Paste 2-3 example passages
→ Select tone attributes from presets
→ Define prohibited patterns
→ Specify signature techniques
→ Set metaphor domain preferences

Step 3: Resource Linking
→ Upload or select style guides
→ Link character sheets
→ Attach world bible
→ Add reference scenes

Step 4: Template Selection
→ Choose from template library
→ View required/optional resources
→ Preview parameters

Step 5: Skill Customization
→ Adjust template parameters
→ Define success criteria
→ Set quality thresholds

Step 6: Test & Validate
→ Provide sample text
→ Run skill with config
→ Review output
→ Accept or iterate

Step 7: Save & Register
→ Save skill config to database
→ Register with orchestrator
→ Make available to project
```

**File Storage:**

```
factory/skills/custom/
├── [project-id]_scene_enhancer.json
├── [project-id]_scene_analyzer.json
└── [project-id]_dialogue_polisher.json
```

**Testing:**
- Test wizard flow end-to-end
- Test skill config validation
- Test skill registration
- Test template library

---

#### Task 12-09: Custom Skill Executor (3h)

**Goal:** Execute writer-created skills

**File:** `factory/core/custom_skill_executor.py`

**Key Components:**

1. **CustomSkillExecutor class**
   - `execute()` - Execute custom skill
   - `_get_template_executor()` - Get executor for template
   - `_prepare_context()` - Load voice profile and resources
   - `_load_file()` - Load resource file content

**Execution Flow:**

```python
async def execute(
    self,
    skill_config: SkillConfig,
    input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute a custom skill."""

    # Load template executor (Scene Enhancer, Analyzer, etc.)
    executor = self._get_template_executor(skill_config.template)

    # Prepare context from voice profile and resources
    context = self._prepare_context(skill_config)
    # context = {
    #     "voice_profile": {
    #         "tone_attributes": ["cynical", "compressed"],
    #         "prohibited_patterns": ["similes", "adverbs"],
    #         "signature_techniques": ["direct metaphors"],
    #         "domain_preferences": {"gambling": 25, "music": 20}
    #     },
    #     "resources": {
    #         "style_guides": ["...content..."],
    #         "character_sheets": ["...content..."],
    #         "world_bible": "...content..."
    #     }
    # }

    # Execute with parameters
    result = await executor.execute(
        input_data=input_data,
        context=context,
        parameters=skill_config.parameters
    )

    return result
```

**Context Preparation:**

- Load voice profile from config
- Read all linked resource files
- Format as context dict for executor
- Cache frequently used resources

**Template Executor Mapping:**

```python
def _get_template_executor(self, template: SkillTemplate):
    if template == SkillTemplate.SCENE_ENHANCER:
        from factory.agents.explants.scene_enhancer import SceneEnhancerAgent
        return SceneEnhancerAgent()
    elif template == SkillTemplate.SCENE_ANALYZER:
        from factory.agents.explants.scene_analyzer import SceneAnalyzerAgent
        return SceneAnalyzerAgent()
    # ... more templates
```

**Integration with Orchestrator:**

```python
# In SkillOrchestrator._call_provider()
elif provider == SkillProvider.CUSTOM:
    # Load custom skill config
    skill_config = load_custom_skill(skill_name)

    # Execute via custom executor
    executor = CustomSkillExecutor()
    return await executor.execute(skill_config, input_data)
```

**Testing:**
- Test with various skill configs
- Test resource loading
- Test context preparation
- Test executor selection

---

#### Task 12-10: Wizard UI Components (4h)

**Goal:** Beautiful, intuitive wizard interface

**File:** `webapp/frontend-v2/src/features/wizard/SkillCreationWizard.jsx`

**Main Wizard Component:**

```jsx
export function SkillCreationWizard({ projectId, onComplete }) {
  const [step, setStep] = useState(1);
  const [config, setConfig] = useState({
    voiceProfile: null,
    resources: [],
    template: null,
    parameters: {}
  });

  return (
    <div className="wizard-container">
      <WizardProgress currentStep={step} totalSteps={7} />

      {step === 1 && <ProjectSetup onNext={...} />}
      {step === 2 && <VoiceDefinition onNext={...} />}
      {step === 3 && <ResourceLinking onNext={...} />}
      {step === 4 && <TemplateSelection onNext={...} />}
      {step === 5 && <SkillCustomization onNext={...} />}
      {step === 6 && <SkillTesting onAccept={...} onIterate={...} />}
      {step === 7 && <SkillRegistration onComplete={...} />}
    </div>
  );
}
```

**Key Step Components:**

**1. VoiceDefinition Component:**
- 3 textarea fields for example passages
- Checkbox grid for tone attributes (20+ presets)
- Dynamic list for prohibited patterns
- Dynamic list for signature techniques
- Slider inputs for metaphor domain percentages

**2. ResourceLinking Component:**
- File upload for style guides
- File upload for character sheets
- File upload for world bible
- File browser for existing project files
- Drag-and-drop support

**3. TemplateSelection Component:**
- Grid of template cards
- Each card shows:
  * Name and description
  * Required resources
  * Optional resources
  * Example use cases
- Hover preview of parameters

**4. SkillCustomization Component:**
- Dynamic form based on template parameters
- Parameter types:
  * Text input
  * Dropdown (enum)
  * Checkbox (boolean)
  * Multi-select (list)
  * Slider (range)
- Tooltips explaining each parameter
- Default values from template

**5. SkillTesting Component:**
- Large textarea for test input
- "Run Test" button
- Loading spinner during execution
- Output display with formatting
- Side-by-side before/after (for enhancer)
- Score display (for analyzer)
- Action buttons:
  * ✓ Accept & Register
  * ← Refine Parameters
  * ✗ Start Over

**6. SkillRegistration Component:**
- Summary of skill configuration
- Skill name input (editable)
- Visibility settings (private/project/public)
- "Register Skill" button
- Success confirmation with skill ID

**Styling:**
- Clean, modern design
- Progress indicator always visible
- Smooth transitions between steps
- Form validation with helpful errors
- Mobile-responsive layout

**API Endpoints for Wizard:**

```python
@app.post("/api/wizard/create-skill")
async def create_skill_wizard(request: dict):
    """Create skill via wizard."""
    wizard = SkillCreationWizard()
    config = await wizard.create_skill(
        project_id=request["project_id"],
        writer_id=request["writer_id"]
    )
    return {"skill_config": config}

@app.get("/api/wizard/templates")
async def list_templates():
    """List available skill templates."""
    wizard = SkillCreationWizard()
    return {"templates": wizard.list_templates()}

@app.post("/api/wizard/test-skill")
async def test_skill(request: dict):
    """Test skill config before registration."""
    executor = CustomSkillExecutor()
    result = await executor.execute(
        skill_config=request["config"],
        input_data=request["input"]
    )
    return result
```

**Testing:**
- Test each wizard step
- Test navigation (next/back)
- Test form validation
- Test file uploads
- Test skill execution in step 6
- End-to-end wizard completion

---

## 🗂️ File Structure

**New files to create:**

```
writers-factory-core/
├── factory/
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── claude_skill_bridge.py          # Task 12-01
│   ├── core/
│   │   ├── skill_orchestrator.py           # Task 12-02
│   │   └── custom_skill_executor.py        # Task 12-09
│   ├── agents/
│   │   └── explants/
│   │       ├── __init__.py
│   │       └── scene_analyzer.py           # Task 12-03
│   ├── wizards/
│   │   ├── __init__.py
│   │   └── skill_creator.py                # Task 12-08
│   ├── knowledge/                          # Task 12-06
│   │   ├── craft/
│   │   ├── character/
│   │   └── scoring/
│   └── skills/
│       └── custom/                         # Wizard-created skills
├── webapp/
│   ├── backend/
│   │   └── simple_app.py                   # Task 12-04 (additions)
│   └── frontend-v2/
│       └── src/
│           └── features/
│               ├── craft/
│               │   └── CraftPanel.jsx      # Task 12-05
│               └── wizard/
│                   └── SkillCreationWizard.jsx  # Task 12-10
└── docs/
    ├── SKILL_SYSTEM_GUIDE.md               # Task 12-07
    ├── ADDING_NEW_SKILLS.md                # Task 12-07
    └── API_REFERENCE.md                    # Task 12-07
```

---

## 🧪 Testing Strategy

### Unit Tests

**MCP Bridge Tests:**
```python
# test_mcp_bridge.py
async def test_skill_registration():
    bridge = MCPSkillBridge()
    assert len(bridge.skills_registry) == 6
    assert "scene-analyzer" in bridge.skills_registry

async def test_call_skill_success():
    bridge = MCPSkillBridge()
    result = await bridge.call_skill(
        "scene-analyzer",
        {"scene_content": "test scene", "mode": "quick"}
    )
    assert result["status"] == "success"

async def test_fallback_response():
    bridge = MCPSkillBridge()
    result = bridge._fallback_response("scene-analyzer", {})
    assert result["status"] == "fallback"
```

**Orchestrator Tests:**
```python
# test_orchestrator.py
async def test_routing_premium_user():
    orchestrator = SkillOrchestrator()
    providers = orchestrator._get_provider_priority(
        SkillRequest(
            skill_name="scene-analyzer",
            capability="analyze",
            input_data={},
            user_id="premium_user"
        )
    )
    assert providers[0] == SkillProvider.CLAUDE_SKILL

async def test_fallback_behavior():
    orchestrator = SkillOrchestrator()
    # Mock Claude Skill failure
    result = await orchestrator.execute_skill(...)
    assert result.provider == SkillProvider.NATIVE_PYTHON
```

**Scene Analyzer Tests:**
```python
# test_scene_analyzer.py
async def test_anti_pattern_detection():
    analyzer = SceneAnalyzerAgent()
    scene = "Mickey walked slowly with practiced precision."
    score = analyzer._score_anti_patterns(scene)
    assert score["score"] < 15  # Deductions for violations

async def test_quality_tier_assignment():
    analyzer = SceneAnalyzerAgent()
    assert analyzer._get_quality_tier(97) == "Gold Standard (95-100)"
    assert analyzer._get_quality_tier(82) == "A- Good (80-84)"
```

### Integration Tests

**API Integration:**
```bash
# Test skill execution endpoint
curl -X POST http://localhost:8000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "scene-analyzer",
    "input_data": {
      "scene_content": "Test scene content...",
      "mode": "detailed"
    }
  }'

# Test skill listing
curl http://localhost:8000/api/skills/list

# Test health check
curl http://localhost:8000/api/skills/health
```

**End-to-End Workflow:**
1. Load Writers Factory UI
2. Navigate to Craft Panel
3. Select "Scene Analyzer" skill
4. Paste real Explants scene
5. Execute skill
6. Verify results display correctly
7. Check provider indicator
8. Verify cost tracking

### Validation Tests

**Compare with Claude Skills:**
```python
# Test native vs Claude Skill consistency
async def test_native_vs_claude_skill():
    scene_content = load_test_scene("1.3.2_blackjack.md")

    # Execute via Claude Skill
    claude_result = await mcp_bridge.call_skill(
        "scene-analyzer",
        {"scene_content": scene_content, "mode": "detailed"}
    )

    # Execute via Native Python
    native_result = await scene_analyzer.execute(
        {"scene_content": scene_content, "mode": "detailed"}
    )

    # Scores should be within 5 points
    assert abs(
        claude_result["data"]["total_score"] -
        native_result["data"]["total_score"]
    ) <= 5
```

---

## 📚 Documentation to Create

### 1. SKILL_SYSTEM_GUIDE.md

**Contents:**
- System architecture overview
- Available skills catalog
- How to use each skill
- Provider differences (Claude vs Native)
- Cost tiers and entitlements
- Troubleshooting common issues

### 2. ADDING_NEW_SKILLS.md

**Contents:**
- Step-by-step guide to adding native agent
- Skill template structure
- Registration with orchestrator
- Testing requirements
- Integration checklist
- Example implementations

### 3. API_REFERENCE.md

**Contents:**
- All skill endpoints with examples
- Request/response schemas
- Error codes and handling
- Rate limiting information
- Authentication requirements
- WebSocket support (future)

### 4. WIZARD_USER_GUIDE.md

**Contents:**
- How to create custom skills
- Voice profile best practices
- Resource linking tips
- Template selection guide
- Testing your skill
- Sharing skills with team

---

## 🎯 Success Criteria

### Sprint 12A Complete When:

- [ ] MCP Bridge connects to all 6 Claude Skills
- [ ] Orchestrator routes to correct provider
- [ ] Native Scene Analyzer scores scenes accurately
- [ ] All API endpoints working
- [ ] Craft Panel UI functional
- [ ] Reference materials migrated
- [ ] Can execute any of 6 skills through UI
- [ ] Can analyze a real Explants scene successfully
- [ ] Documentation complete

### Sprint 12B Complete When:

- [ ] Wizard creates skill configs successfully
- [ ] Custom Skill Executor runs wizard-created skills
- [ ] Wizard UI is intuitive and beautiful
- [ ] Can create Scene Enhancer via wizard
- [ ] Can test skill before registration
- [ ] Custom skills appear in Craft Panel
- [ ] Can execute custom skills through UI
- [ ] Documentation for wizard complete

### Overall Success:

- [ ] G.C. Harris can use all 6 Explants skills in Writers Factory
- [ ] Students can create their own custom skills
- [ ] System gracefully falls back when provider unavailable
- [ ] Cost tracking works correctly
- [ ] Performance is acceptable (< 5s for most skills)
- [ ] No critical bugs in production usage

---

## 🚀 Launch Plan

### For G.C. Harris (Immediate):

**Day 1 Post-Sprint:**
1. Test Scene Analyzer on actual Volume 1 scenes
2. Compare scores with personal assessments
3. Identify any scoring inaccuracies

**Week 1:**
1. Use all 6 skills for Volume 2 work
2. Document any issues or desired improvements
3. Test wizard by creating a new custom skill

**Month 1:**
1. Build custom skills for Volume 2 specific needs
2. Share feedback on skill accuracy
3. Build reference materials for student onboarding

### For Students (Rollout):

**Phase 1: Alpha Testing (2-3 students)**
1. Invite technically savvy students
2. Have them create their own skills
3. Collect detailed feedback
4. Fix critical bugs

**Phase 2: Beta Testing (10 students)**
1. Broader student group
2. Test with various writing styles/genres
3. Monitor server load and performance
4. Refine UI based on feedback

**Phase 3: Public Launch**
1. Open to all course participants
2. Skill marketplace (writers share skills)
3. Community templates
4. Usage analytics and optimization

---

## 📊 Monitoring & Metrics

**Track These Metrics:**

1. **Skill Usage:**
   - Which skills used most frequently
   - Which provider preferred
   - Execution success rate
   - Average execution time

2. **Cost Analysis:**
   - Cost per skill execution
   - Total cost per user per month
   - Claude Skill vs Native cost comparison

3. **Quality Metrics:**
   - Scene scores before/after enhancement
   - Fix acceptance rate (user applies suggested fixes)
   - Custom skill creation completion rate

4. **Performance:**
   - Skill execution time (p50, p95, p99)
   - API response time
   - Error rate by provider

5. **User Behavior:**
   - Wizard completion rate
   - Most popular skill templates
   - Resource file types uploaded
   - Skill sharing frequency

---

## 🔮 Future Enhancements (Post-Sprint 12)

**Sprint 13: Additional Native Agents**
- Scene Enhancer (native Python)
- Character Validator (native Python)
- Scene Writer (native Python)

**Sprint 14: Advanced Features**
- Skill chaining (output of one skill → input of another)
- Batch processing (analyze entire manuscript)
- Scheduled skills (nightly enhancement runs)
- Skill versioning and rollback

**Sprint 15: Marketplace**
- Public skill library
- Skill ratings and reviews
- Featured skills
- Skill analytics (usage, ratings, forks)

**Sprint 16: Collaboration**
- Team skill libraries
- Skill permissions (private/team/public)
- Collaborative skill editing
- Skill templates from community

**Sprint 17: Advanced AI**
- Multi-model ensemble (combine Claude + GPT-4 + local)
- Active learning (skills improve from user feedback)
- Personalized scoring (adapts to writer's preferences)
- Generative skill creation (AI generates new skill templates)

---

## 🛠️ Implementation Notes

### Dependencies to Install:

```bash
# Python backend
pip install anthropic  # For Claude API
pip install httpx      # For HTTP requests
pip install pydantic   # For data validation

# Frontend
cd webapp/frontend-v2
npm install @tanstack/react-query  # Already installed
```

### Environment Variables:

```bash
# .env
ANTHROPIC_API_KEY=your_key_here
CLAUDE_SKILL_ACCESS=true
SKILL_CACHE_ENABLED=true
SKILL_CACHE_TTL=3600
```

### Database Schema (if using DB instead of JSON files):

```sql
CREATE TABLE custom_skills (
    skill_id VARCHAR(255) PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    writer_id VARCHAR(255) NOT NULL,
    template VARCHAR(100) NOT NULL,
    voice_profile JSON NOT NULL,
    resources JSON NOT NULL,
    parameters JSON NOT NULL,
    success_criteria JSON,
    version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visibility VARCHAR(50) DEFAULT 'private',
    usage_count INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2)
);

CREATE INDEX idx_project_skills ON custom_skills(project_id);
CREATE INDEX idx_writer_skills ON custom_skills(writer_id);
CREATE INDEX idx_template ON custom_skills(template);
```

### Performance Optimization:

**Caching:**
- Cache skill configs (1 hour TTL)
- Cache reference materials (in-memory)
- Cache provider health status (5 min TTL)

**Connection Pooling:**
- Reuse HTTP connections to Claude API
- Database connection pool

**Async Processing:**
- All skill executions async
- Parallel execution when possible
- Background task queue for heavy operations

---

## 💬 Prompt for Cloud Agent

```
Sprint 12: Universal Skill Orchestration System + Creation Wizard

Please implement the complete specification in SPRINT_12_UNIVERSAL_SKILL_SYSTEM.md

This is a comprehensive sprint that transforms Writers Factory into an intelligent multi-agent
platform with two major components:

PHASE A - Foundation (22-25h):
1. MCP Skill Bridge - Connect all 6 Explants Claude Skills
2. Skill Orchestrator - Intelligent routing to best provider
3. Native Scene Analyzer - First Python implementation (proof of concept)
4. Backend API - Expose skills via REST endpoints
5. Frontend Integration - Craft Panel UI
6. Reference Migration - Copy knowledge base materials
7. Testing & Documentation

PHASE B - Democratization (8-10h):
8. Skill Creation Wizard Backend - Writer-friendly skill builder
9. Custom Skill Executor - Run wizard-created skills
10. Wizard UI Components - Beautiful multi-step wizard

CRITICAL REQUIREMENTS:
- Follow MCP protocol standards exactly
- All skills must be MCP-compatible
- Graceful fallback when providers unavailable
- Track costs and execution time
- Test with real Explants scenes
- Beautiful, intuitive UI

TESTING:
- Unit tests for all core components
- Integration tests for API endpoints
- End-to-end workflow tests
- Validate against actual Explants content

Begin with Task 12-01 (MCP Skill Bridge).
This is a large sprint but builds the foundation for everything.
Take your time and do it right.
```

---

## 🎉 The Vision Realized

After Sprint 12, Writers Factory becomes:

✅ **Scrivener** - File management (Sprint 9-10) ✓
✅ **VS Code** - Clean editing (TipTap editor) ✓
✅ **NotebookLM** - Research queries (Sprint 11) ⏳
✅ **Your 6 Explants Skills** - Craft mastery (Sprint 12A) ← NEW
✅ **Universal Skill Platform** - Any writer, any craft (Sprint 12B) ← NEW

**Result:** Complete novel-writing system with world-class craft automation built in.

**Impact:** Writers codify their expertise once, use it forever. Students learn craft from masters. Platform scales virally through skill sharing.

---

**Ready to wake up to a transformed Writers Factory? Let's ship this! 🚀**
