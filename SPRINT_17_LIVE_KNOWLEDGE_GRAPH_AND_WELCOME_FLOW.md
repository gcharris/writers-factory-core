# Sprint 17: Live Knowledge Graph + Enhanced Welcome Flow

**Status:** Ready for Implementation
**Priority:** HIGH - Foundation for January Course
**Timeline:** 3 weeks
**Dependencies:** Sprint 15 ✅ Complete, Sprint 16 ✅ Complete

---

## Executive Summary

Sprint 17 implements TWO major features that work together:

1. **Enhanced Welcome Flow** - Intelligent path selection for all user types
2. **Live Knowledge Graph** - Auto-updating story intelligence with export capabilities

**Why Together:** The welcome flow sets up the initial knowledge base, and the knowledge graph maintains it during writing.

---

## Part 1: Enhanced Welcome Flow

### Problem Statement

Current welcome flow (Sprint 14) assumes users either have:
- Existing manuscript to import, OR
- Nothing (start from scratch with wizard)

**Missing:** The BEST path - users with NotebookLM notebooks full of ideas/research who need help organizing and extracting that knowledge.

### Solution: Three-Path Welcome Flow

```
New Project Creation
    │
    ├─ Path 1: Experienced Writer (existing work)
    │  └─> Import manuscript → Existing Sprint 14 flow
    │
    ├─ Path 2: Prepared Writer (NotebookLM ready) ⭐ RECOMMENDED
    │  └─> AI Wizard extracts & organizes from NotebookLM
    │
    └─ Path 3: New Writer (no notebook)
       │
       ├─ "Show me NotebookLM guide" → Guide → User exits to build notebook
       │
       └─ "Continue interactive" → Manual Q&A wizard (fallback)
```

---

### Week 1: Welcome Flow UI Implementation

#### 1.1 Modify Existing Welcome Modal

**File:** `webapp/frontend-v2/src/components/WelcomeModal.jsx`

**Change:** Replace Step 3 with new path selection

**Before (Step 3):**
```jsx
{
  title: "Three Ways to Start",
  content: (
    // Static options: Creation Wizard, Import, Example
  )
}
```

**After (Step 3):**
```jsx
{
  title: "Choose Your Path",
  content: <PathSelectionStep onComplete={handlePathSelection} />
}
```

#### 1.2 New Component: PathSelectionStep

**File:** `webapp/frontend-v2/src/components/onboarding/PathSelectionStep.jsx`

**Purpose:** Three-option selector with validation

**Features:**
- ✅ Three path cards (Experienced, Prepared, New)
- ✅ "Prepared Writer" marked as RECOMMENDED ⭐
- ✅ Visual selection state (border highlight, scale effect)
- ✅ Disabled continue button until selection made
- ✅ Routing to appropriate next step

**Design:**
```jsx
<PathOption
  icon={<Notebook />}
  title="Prepared Writer"
  description="I have a NotebookLM notebook ready"
  details={[
    "I've collected ideas, research, and notes",
    "Extract and organize from my notebook",
    "RECOMMENDED for best results ⭐"
  ]}
  badge="Recommended"
  recommended={true}
/>
```

#### 1.3 New Modal: NotebookLM Recommendation

**File:** `webapp/frontend-v2/src/components/onboarding/NotebookLMRecommendation.jsx`

**Triggered:** When user selects "New Writer" path

**Purpose:** Gently nudge toward NotebookLM setup

**Two Options:**
1. **"Show me how to set up NotebookLM" (RECOMMENDED)**
   - Opens NotebookLM guide in new tab/window
   - User can bookmark and return later
   - No lost progress

2. **"Continue with interactive questions"**
   - Fallback to manual Q&A wizard
   - Less rich but workable

**Design:**
```jsx
<div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/50">
  <h3>💡 RECOMMENDATION: Build a NotebookLM notebook first</h3>
  <p>Why? NotebookLM lets you:</p>
  <ul>
    <li>Collect ideas freely (no structure required)</li>
    <li>Upload research, inspirations, examples</li>
    <li>Save random thoughts and character notes</li>
    <li>Let AI help you explore your ideas</li>
  </ul>
</div>
```

#### 1.4 New Page: NotebookLM Setup Guide

**File:** `webapp/frontend-v2/src/pages/NotebookLMGuide.jsx`

**Purpose:** Comprehensive guide for new writers

**5 Steps:**
1. Create free NotebookLM account
2. Create new notebook for novel
3. Start adding content (with suggested categories)
4. Let it grow naturally (days/weeks)
5. Come back when ready

**Suggested Content Categories:**
- 📝 **Character Ideas** - Profiles, traits, backgrounds, conflicts
- 🌍 **World & Setting Notes** - Locations, time period, world rules, research
- 📖 **Story Ideas & Plot Threads** - Main conflict, key scenes, themes
- ✍️ **Writing Samples** - Personal writing for voice analysis
- 🔍 **Research & Inspiration** - Articles, character inspirations, genre examples

**Action Buttons:**
- [Save This Guide] - Downloads/bookmarks guide
- [I'm Ready Now] - Returns to wizard with NotebookLM URL input
- [Continue Without NotebookLM] - Fallback to interactive Q&A

#### 1.5 Routing Updates

**File:** `webapp/frontend-v2/src/App.jsx`

**New Routes:**
```jsx
<Route path="/onboarding/notebooklm-guide" element={<NotebookLMGuide />} />
<Route path="/onboarding/ai-wizard" element={<AIWizard />} />
<Route path="/onboarding/interactive-qa" element={<InteractiveQA />} />
```

**Routing Logic:**
```javascript
function handlePathSelection(path) {
  switch(path) {
    case 'experienced':
      navigate('/import-manuscript');  // Existing Sprint 14
      break;

    case 'prepared':
      navigate('/onboarding/ai-wizard');  // NEW: Part 2 of Sprint 17
      break;

    case 'new':
      // Show recommendation modal first
      setShowRecommendation(true);
      break;
  }
}
```

---

## Part 2: AI Wizard for NotebookLM Extraction

### Architecture: Intelligent Conversation, Not Dumb Form

**Key Principle:** This is an AI agent having a conversation, not a programmed wizard.

### Week 2: AI Wizard Backend

#### 2.1 Model Configuration System

**File:** `factory/ai/model_router.py`

**Purpose:** Route different tasks to appropriate models

**Default Model:** Llama 3.3 (local via Ollama) - Free, good enough for extraction

**Optional Premium Models:**
- Claude Sonnet 4.5 (via Anthropic API or MCP)
- GPT-4o (via OpenAI API)
- Gemini 2.0 Flash (via Google API)

**Configuration:**
```json
// projects/{project-id}/config.json
{
  "models": {
    "setup_wizard": "llama3.3",           // Default: free local
    "knowledge_extraction": "llama3.3",    // Default: free local
    "scene_writing": "claude-sonnet-4.5",  // Premium for creative work
    "voice_analysis": "claude-sonnet-4.5"  // Premium for nuance
  },
  "fallback_model": "llama3.3"
}
```

**Model Router Implementation:**
```python
class ModelRouter:
    """Route operations to appropriate models."""

    async def get_model_for_task(self, task_type: str):
        """Return model based on task and user config."""

        task_defaults = {
            "setup_wizard": "llama3.3",
            "knowledge_extraction": "llama3.3",
            "knowledge_query": "llama3.3",
            "scene_writing": "claude-sonnet-4.5",
            "scene_analysis": "llama3.3",
            "voice_analysis": "claude-sonnet-4.5"
        }

        configured = self.config.get_model(task_type)
        return configured or task_defaults[task_type]
```

#### 2.2 Ollama Integration

**File:** `factory/ai/ollama_setup.py`

**First-Time Setup Check:**
```python
async def ensure_ollama_ready():
    """Check if Ollama installed and has required model."""

    try:
        # Check Ollama installed
        result = subprocess.run(["ollama", "list"], capture_output=True)

        # Check if llama3.3 available
        if "llama3.3" not in result.stdout.decode():
            print("Downloading Llama 3.3 (4.7GB)...")
            subprocess.run(["ollama", "pull", "llama3.3"])

        return True

    except FileNotFoundError:
        # Ollama not installed
        return False
```

**User Prompt (if Ollama missing):**
```
┌─────────────────────────────────────────────┐
│ AI Model Setup                              │
├─────────────────────────────────────────────┤
│ No API keys configured. Would you like to:  │
│                                              │
│ ○ Use free local Llama 3.3 (recommended)    │
│   • Requires Ollama installation            │
│   • 4.7GB download                          │
│   • $0 cost, runs offline                   │
│                                              │
│ ○ Configure API keys (Claude, GPT, Gemini)  │
│   • Higher quality                          │
│   • Costs $15-30/month for active project   │
│   • Requires internet                       │
│                                              │
│ [Install Ollama] [Configure APIs] [Skip]    │
└─────────────────────────────────────────────┘
```

#### 2.3 AI Wizard Agent System

**File:** `factory/ai/setup_wizard_agent.py`

**Architecture:** Agent with tools, not scripted flow

**System Prompt:**
```python
SETUP_WIZARD_PROMPT = """
You are the Writers Factory Setup Agent. Your job is to help the user
organize their story knowledge from NotebookLM into structured category folders.

For each category:
1. Query NotebookLM intelligently for relevant information
2. Present findings to user for validation
3. Disambiguate confusing references (Is "Tom" a character or research subject?)
4. Ask clarifying questions when information is unclear
5. Suggest organizational structures based on content volume
6. Fill gaps interactively through conversation
7. Create final structured files only after user confirmation

You are helpful, intelligent, and adaptive. Don't make assumptions - always
validate with the user.

IMPORTANT: Use the category templates as guides, but adapt based on what you
find in the user's NotebookLM. If they have 20 characters, suggest subcategories.
If they have 2 characters, keep it flat.

Current category: {category_name}
Template structure: {template_fields}
NotebookLM URL: {notebook_url}
"""
```

**Agent Tools:**
```python
class SetupWizardAgent:

    def __init__(self, project_id, notebook_url, model="llama3.3"):
        self.tools = [
            self.query_notebooklm,
            self.create_category_file,
            self.suggest_subcategories,
            self.present_findings_to_user
        ]

    async def query_notebooklm(self, question: str) -> str:
        """Query user's NotebookLM for specific information."""
        # Uses existing Sprint 11 NotebookLM client

    async def create_category_file(
        self,
        category: str,
        filename: str,
        content: dict
    ):
        """Create structured markdown file from template + extracted data."""

    async def suggest_subcategories(
        self,
        category: str,
        item_count: int
    ) -> dict:
        """Suggest subcategory structure based on content volume."""

    async def present_findings_to_user(
        self,
        summary: str,
        question: str
    ) -> str:
        """Show findings to user, get feedback via UI."""
```

#### 2.4 Category Templates

**File:** `factory/templates/category_templates.py`

**8 Core Categories (Tier 1 & 2 from our discussion):**

1. **Characters**
2. **Story_Structure**
3. **World_Building**
4. **Themes_and_Philosophy**
5. **Voice_and_Craft**
6. **Antagonism_and_Conflict**
7. **Key_Beats_and_Pacing**
8. **Research_and_Setting_Specifics**

**Character Template Example:**
```python
CHARACTER_TEMPLATE = {
    "name": "character_profile",
    "fields": [
        {
            "section": "Basic Information",
            "fields": [
                {
                    "name": "role_in_story",
                    "query": "What is {character_name}'s role in the story?",
                    "required": True
                },
                {
                    "name": "first_appearance",
                    "query": "When/where does {character_name} first appear?",
                    "required": False,
                    "auto_populate": True  # Fill during writing
                }
            ]
        },
        {
            "section": "Core Dimensions",
            "fields": [
                {
                    "name": "internal_conflicts",
                    "query": "What are {character_name}'s internal conflicts?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "fears_and_insecurities",
                    "query": "What are {character_name}'s fears and insecurities?",
                    "required": False,
                    "prompt_if_empty": True
                },
                {
                    "name": "motivations_and_goals",
                    "query": "What motivates {character_name}? What are their goals?",
                    "required": True
                }
            ]
        },
        {
            "section": "Character Arc and Growth",
            "fields": [
                {
                    "name": "starting_state",
                    "query": "What is {character_name}'s starting state/situation?",
                    "required": False
                },
                {
                    "name": "transformation",
                    "query": "How does {character_name} transform during the story?",
                    "required": False,
                    "note": "Will be tracked during writing"
                },
                {
                    "name": "ending_state",
                    "query": "What is {character_name}'s ending state?",
                    "required": False,
                    "note": "Will be filled as you write"
                }
            ]
        }
    ]
}
```

#### 2.5 Wizard Conversation Flow

**Example: Characters Category**

```python
async def process_characters_category(self):
    """AI-driven conversation for character extraction."""

    # Step 1: Discover characters
    response = await self.agent.query_notebooklm(
        "Who are the main characters in this story? List all named characters mentioned."
    )

    # Step 2: Parse and validate with user
    characters = self.parse_character_list(response)

    validated_characters = await self.present_to_user(
        f"I found {len(characters)} characters in your notebook: " +
        ", ".join(characters) +
        "\n\nAre these all main characters, or are some just references/research?"
    )

    # Step 3: For each validated character, extract details
    for char in validated_characters:
        char_profile = {}

        for field in CHARACTER_TEMPLATE["fields"]:
            # Query NotebookLM for this specific field
            query = field["query"].format(character_name=char)
            result = await self.agent.query_notebooklm(query)

            if result:
                # Found data
                char_profile[field["name"]] = f"[EXTRACTED FROM NOTEBOOKLM: {result}]"
            else:
                # No data found
                if field.get("prompt_if_empty"):
                    # Ask user now
                    user_input = await self.ask_user(
                        f"{char} - {field['name']}\n" +
                        f"No information found in your NotebookLM.\n\n" +
                        f"Would you like to:\n" +
                        f"○ Add this information now\n" +
                        f"● Leave blank (add later during writing)"
                    )

                    if user_input == "add_now":
                        char_profile[field["name"]] = await self.get_user_input(field["name"])
                    else:
                        char_profile[field["name"]] = f"[USER CHOSE: Leave blank - will add during writing]"

                elif field.get("auto_populate"):
                    char_profile[field["name"]] = "[TO BE AUTO-POPULATED DURING DRAFTING]"
                else:
                    char_profile[field["name"]] = f"[NO DATA - USER WILL DISCOVER DURING WRITING]"

        # Step 4: Create character file
        await self.create_category_file(
            category="Characters",
            filename=f"{char.replace(' ', '_')}_profile.md",
            content=char_profile
        )
```

#### 2.6 Subcategory Intelligence

**Adaptive Structure Based on Content Volume:**

```python
async def suggest_character_subcategories(self, character_count: int):
    """Suggest subcategories based on how many characters found."""

    if character_count < 5:
        return {
            "structure": "flat",
            "message": "You have {character_count} characters. Keeping structure flat for simplicity."
        }

    elif character_count < 15:
        return {
            "structure": "basic",
            "subcategories": ["Core_Cast", "Supporting_Cast"],
            "message": "You have {character_count} characters. I suggest organizing into:\n" +
                      "• Core_Cast/ - Main characters\n" +
                      "• Supporting_Cast/ - Supporting characters\n\n" +
                      "Does this work for you?"
        }

    else:
        # Check for antagonist keywords in notebook
        has_antagonist = await self.check_for_antagonist_keywords()

        subcats = ["Core_Cast", "Supporting_Cast"]
        if has_antagonist:
            subcats.append("Antagonists")

        return {
            "structure": "detailed",
            "subcategories": subcats + ["Relationships"],
            "message": f"You have {character_count} characters - that's a large cast! " +
                      "I suggest organizing into:\n" +
                      "".join(f"• {sub}/\n" for sub in subcats) +
                      "\nWould you like to use this structure?"
        }
```

---

### Week 3: Frontend AI Wizard UI

#### 3.1 AI Wizard Page

**File:** `webapp/frontend-v2/src/pages/AIWizard.jsx`

**Purpose:** Chat-like interface for wizard conversation

**Design:**
```jsx
<div className="min-h-screen bg-gray-900 flex">
  {/* Left: Progress Sidebar */}
  <div className="w-64 bg-gray-800 border-r border-gray-700">
    <h2>Project Setup</h2>
    <ProgressSteps
      steps={[
        { name: "Characters", status: "complete" },
        { name: "Story Structure", status: "in_progress" },
        { name: "World Building", status: "pending" },
        { name: "Themes & Philosophy", status: "pending" },
        { name: "Voice & Craft", status: "pending" },
        { name: "Conflict", status: "pending" },
        { name: "Beats & Pacing", status: "pending" },
        { name: "Research", status: "pending" }
      ]}
    />
  </div>

  {/* Right: Conversation */}
  <div className="flex-1 flex flex-col">
    {/* Chat Messages */}
    <div className="flex-1 overflow-y-auto p-8 space-y-4">
      {messages.map(msg => (
        <ChatMessage
          key={msg.id}
          sender={msg.sender}  // 'ai' or 'user'
          content={msg.content}
          type={msg.type}      // 'text', 'options', 'confirmation'
        />
      ))}
    </div>

    {/* Input Area */}
    <div className="border-t border-gray-700 p-4">
      {waitingForInput ? (
        <UserInputField
          type={inputType}  // 'text', 'choice', 'confirmation'
          options={inputOptions}
          onSubmit={handleUserResponse}
        />
      ) : (
        <div className="text-gray-500 text-center">
          AI is analyzing your notebook...
        </div>
      )}
    </div>
  </div>
</div>
```

#### 3.2 Chat Message Components

**File:** `webapp/frontend-v2/src/components/wizard/ChatMessage.jsx`

**AI Message:**
```jsx
<div className="flex items-start gap-3">
  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
    <Sparkles className="w-4 h-4 text-white" />
  </div>
  <div className="flex-1 bg-gray-800 rounded-lg p-4">
    <ReactMarkdown>{content}</ReactMarkdown>
  </div>
</div>
```

**User Message:**
```jsx
<div className="flex items-start gap-3 justify-end">
  <div className="flex-1 bg-blue-600 rounded-lg p-4 max-w-2xl">
    <p className="text-white">{content}</p>
  </div>
  <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
    <User className="w-4 h-4 text-white" />
  </div>
</div>
```

**Option Selection:**
```jsx
<div className="space-y-2 mt-2">
  {options.map(opt => (
    <button
      key={opt.value}
      onClick={() => onSelect(opt.value)}
      className="w-full text-left p-3 bg-gray-700 hover:bg-gray-600 rounded-lg"
    >
      {opt.label}
    </button>
  ))}
</div>
```

#### 3.3 WebSocket Communication

**File:** `webapp/backend/routes/wizard.py`

**Real-time AI conversation via WebSocket:**

```python
@router.websocket("/ws/wizard/{project_id}")
async def wizard_websocket(websocket: WebSocket, project_id: str):
    """Real-time AI wizard conversation."""

    await websocket.accept()

    # Initialize wizard agent
    wizard = SetupWizardAgent(
        project_id=project_id,
        notebook_url=request.notebook_url,
        model="llama3.3"  # Or user's configured model
    )

    # Process each category
    for category in CATEGORIES:
        # AI agent processes category
        async for message in wizard.process_category(category):
            # Send AI message to frontend
            await websocket.send_json({
                "type": "ai_message",
                "content": message.content,
                "requires_input": message.requires_input,
                "input_type": message.input_type
            })

            if message.requires_input:
                # Wait for user response
                user_response = await websocket.receive_json()
                wizard.provide_user_response(user_response["content"])

    # All categories complete
    await websocket.send_json({
        "type": "complete",
        "message": "Setup complete! Initializing knowledge graph..."
    })

    # Initial knowledge graph ingest
    await wizard.initialize_knowledge_graph()

    await websocket.send_json({
        "type": "redirect",
        "url": "/editor"
    })
```

---

## Part 3: Live Knowledge Graph

### Week 2-3: Knowledge Graph Implementation

#### 3.1 Category Folder Structure (Created by Wizard)

```
projects/{project-id}/
├── scenes/                         # User writes here (empty initially)
│
├── reference/                      # Created by wizard, user-maintained
│   ├── Characters/
│   │   ├── Mickey_Bardot_profile.md
│   │   └── Noni_profile.md
│   ├── Story_Structure/
│   ├── World_Building/
│   ├── Themes_and_Philosophy/
│   ├── Voice_and_Craft/
│   ├── Antagonism_and_Conflict/
│   ├── Key_Beats_and_Pacing/
│   └── Research_and_Setting_Specifics/
│
├── exports_for_notebooklm/         # HIGH in hierarchy - easy access
│   ├── development_docs/           # Query/answer logs
│   │   └── (empty initially)
│   └── summaries/                  # Consolidated exports (on-demand)
│       └── (empty initially)
│
└── knowledge/
    └── graph/
        └── knowledge_graph.json    # Populated after wizard, auto-updated
```

#### 3.2 Initial Knowledge Graph Ingest

**File:** `factory/analysis/knowledge_graph_manager.py`

**After wizard completes:**

```python
class KnowledgeGraphManager:

    async def initialize_from_categories(self, project_id: str):
        """Initial population from category files."""

        graph = NovelKnowledgeGraph()

        # Ingest from each category folder
        categories = [
            "Characters",
            "World_Building",
            "Story_Structure",
            "Themes_and_Philosophy",
            # ... etc
        ]

        for category in categories:
            category_path = f"projects/{project_id}/reference/{category}"

            if category == "Characters":
                # Extract character nodes
                for char_file in glob(f"{category_path}/*.md"):
                    char_data = self.parse_character_file(char_file)
                    graph.add_node(
                        node_type="character",
                        name=char_data["name"],
                        attributes=char_data["attributes"]
                    )

            elif category == "World_Building":
                # Extract location nodes
                for loc_file in glob(f"{category_path}/Locations/*.md"):
                    loc_data = self.parse_location_file(loc_file)
                    graph.add_node(
                        node_type="location",
                        name=loc_data["name"],
                        attributes=loc_data["attributes"]
                    )

            # ... similar for other categories

        # Save initialized graph
        graph.save(f"projects/{project_id}/knowledge/graph/knowledge_graph.json")

        return graph
```

#### 3.3 Scene Completion Workflow

**When user marks scene "draft complete":**

```python
@router.post("/api/scenes/{scene_id}/complete")
async def complete_scene(scene_id: str, project_id: str):
    """Handle scene completion."""

    # Step 1: Extract entities from completed scene
    scene_content = load_scene(project_id, scene_id)
    extractor = EntityExtractor(model="llama3.3")

    entities = await extractor.extract_from_scene(scene_content)
    # Returns: {characters: [...], locations: [...], plot_threads: [...], motifs: [...]}

    # Step 2: Update knowledge graph
    graph = load_knowledge_graph(project_id)

    for char in entities["characters"]:
        # Add or update character node
        if graph.has_node(char["name"]):
            graph.update_node(char["name"], char["new_attributes"])
        else:
            graph.add_node("character", char["name"], char["attributes"])

    # ... similar for locations, plot threads, motifs

    # Step 3: Check for modified category files since last sync
    modified_files = get_modified_category_files(project_id)

    if modified_files:
        # Re-ingest modified files
        for file_path in modified_files:
            category = detect_category(file_path)
            await graph.ingest_category_file(category, file_path)

    # Step 4: Save updated graph
    graph.save(f"projects/{project_id}/knowledge/graph/knowledge_graph.json")

    # Step 5: Notify user
    notification = {
        "scene_complete": True,
        "knowledge_graph_updated": True,
        "updates": {
            "new_entities": len(entities["characters"]) + len(entities["locations"]),
            "category_files_synced": len(modified_files)
        },
        "development_docs_count": count_development_docs(project_id, scene_id)
    }

    return notification
```

#### 3.4 Development Docs Workflow

**Every knowledge graph query saves answer:**

```python
@router.post("/api/knowledge/query")
async def query_knowledge_graph(
    project_id: str,
    scene_id: str,
    question: str
):
    """Query knowledge graph during writing."""

    # Load graph
    graph = load_knowledge_graph(project_id)

    # Query
    answer = await graph.query(question)

    # Save query/answer to development docs
    doc_filename = generate_meaningful_filename(scene_id, question)
    # Example: "scene_03_mickey_emotional_state.md"

    save_development_doc(
        project_id=project_id,
        filename=doc_filename,
        content=f"# Query\n\n{question}\n\n# Answer\n\n{answer}\n\n---\n\nScene: {scene_id}\nDate: {datetime.now()}"
    )

    return {
        "answer": answer,
        "doc_saved": f"exports_for_notebooklm/development_docs/{doc_filename}"
    }
```

**Meaningful filename generation:**
```python
def generate_meaningful_filename(scene_id: str, question: str) -> str:
    """Create descriptive filename from query."""

    # Extract key terms from question
    keywords = extract_keywords(question)
    # Example: "What's Mickey's emotional state?" → ["mickey", "emotional", "state"]

    # Limit to 3-4 keywords
    key_terms = "_".join(keywords[:3])

    # Format: scene_XX_term1_term2_term3.md
    return f"{scene_id}_{key_terms}.md"
```

#### 3.5 User Notification After Scene Complete

**Frontend Component:**

```jsx
// webapp/frontend-v2/src/components/SceneCompleteNotification.jsx

function SceneCompleteNotification({ sceneId, updates }) {
  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-8 max-w-lg">
        <h2 className="text-2xl font-bold text-white mb-4">
          Scene {sceneId} Complete! 🎉
        </h2>

        <div className="space-y-3 text-gray-300 mb-6">
          <p>✅ Knowledge graph updated with:</p>
          <ul className="list-disc list-inside ml-4">
            <li>{updates.new_entities} new entities extracted</li>
            {updates.category_files_synced > 0 && (
              <li>{updates.category_files_synced} category files synced</li>
            )}
          </ul>

          {updates.development_docs_count > 0 && (
            <>
              <p className="mt-4">📝 Development files created:</p>
              <p className="text-sm text-gray-400">
                {updates.development_docs_count} query/answer files
              </p>

              <div className="bg-gray-700 rounded p-4 mt-4">
                <p className="font-semibold text-white mb-2">
                  Upload these to your NotebookLM "Development Docs" notebook?
                </p>
                <p className="text-sm text-gray-400">
                  Files location:<br/>
                  <code className="bg-gray-900 px-2 py-1 rounded">
                    exports_for_notebooklm/development_docs/
                  </code>
                </p>
              </div>
            </>
          )}
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => openFolder('exports_for_notebooklm/development_docs')}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded"
          >
            Open Folder
          </button>
          <button
            onClick={() => dismissNotification()}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
          >
            Remind Me Later
          </button>
          <button
            onClick={() => markDone()}
            className="px-4 py-2 bg-green-600 hover:bg-green-500 rounded"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
```

#### 3.6 Export Summaries (On-Demand)

**File:** `factory/analysis/knowledge_graph_exporter.py`

**Purpose:** Generate consolidated markdown files for NotebookLM upload

**Export Categories:**
1. `all_characters.md` - All characters with traits, arcs, appearances
2. `all_locations.md` - All locations with descriptions, significance
3. `plot_threads.md` - Plot threads, status, resolution
4. `themes_motifs.md` - Themes, motifs, metaphors
5. `timeline.md` - Chronological events (optional)

**Implementation:**
```python
class KnowledgeGraphExporter:

    async def export_characters(self, project_id: str) -> str:
        """Generate consolidated character summary."""

        graph = load_knowledge_graph(project_id)
        characters = graph.get_nodes_by_type("character")

        md_content = "# Characters\n\n"
        md_content += f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        for char in characters:
            md_content += f"## {char['name']}\n\n"
            md_content += f"**Role:** {char['attributes'].get('role', 'N/A')}\n\n"
            md_content += f"**Internal Conflicts:** {char['attributes'].get('internal_conflicts', 'N/A')}\n\n"
            md_content += f"**Motivations:** {char['attributes'].get('motivations', 'N/A')}\n\n"
            md_content += f"**Appearances:** {len(char['metadata']['appearances'])} scenes\n"
            md_content += f"- First: {char['metadata']['first_appearance']}\n"
            md_content += f"- Latest: {char['metadata']['appearances'][-1]}\n\n"

            # Relationships
            relationships = graph.get_edges_from_node(char['node_id'])
            if relationships:
                md_content += f"**Relationships:**\n"
                for rel in relationships:
                    target = graph.get_node(rel['target_id'])
                    md_content += f"- {target['name']}: {rel['edge_type']}\n"

            md_content += "\n---\n\n"

        # Save to exports folder
        export_path = f"projects/{project_id}/exports_for_notebooklm/summaries/all_characters.md"
        save_file(export_path, md_content)

        return export_path
```

**API Endpoint:**
```python
@router.post("/api/knowledge/export/{category}")
async def export_knowledge_summary(project_id: str, category: str):
    """Export consolidated summary for NotebookLM."""

    exporter = KnowledgeGraphExporter()

    export_map = {
        "characters": exporter.export_characters,
        "locations": exporter.export_locations,
        "plot": exporter.export_plot_threads,
        "themes": exporter.export_themes_motifs,
        "timeline": exporter.export_timeline
    }

    if category not in export_map:
        raise HTTPException(400, f"Unknown category: {category}")

    file_path = await export_map[category](project_id)

    return {
        "success": True,
        "file_path": file_path,
        "message": f"{category.title()} summary exported successfully"
    }
```

**Frontend Export UI:**
```jsx
// In Project Settings or Tools panel

<div className="space-y-3">
  <h3 className="text-lg font-bold">Export for NotebookLM</h3>
  <p className="text-sm text-gray-400">
    Generate consolidated summaries to upload to your NotebookLM notebooks
  </p>

  <button onClick={() => exportCategory('characters')}>
    Export All Characters
  </button>
  <button onClick={() => exportCategory('locations')}>
    Export All Locations
  </button>
  <button onClick={() => exportCategory('plot')}>
    Export Plot Threads
  </button>
  <button onClick={() => exportCategory('themes')}>
    Export Themes & Motifs
  </button>
  <button onClick={() => exportCategory('timeline')}>
    Export Timeline
  </button>

  <button onClick={() => exportAll()} className="bg-blue-600">
    Export All Categories
  </button>
</div>
```

---

## Success Criteria

### Part 1: Enhanced Welcome Flow

- [ ] Welcome Modal Step 3 replaced with PathSelectionStep
- [ ] Three paths clearly presented (Experienced, Prepared, New)
- [ ] "Prepared Writer" marked as RECOMMENDED
- [ ] NotebookLM Recommendation modal works for "New Writer" path
- [ ] NotebookLM Setup Guide page complete with 5 steps
- [ ] Routing works for all three paths
- [ ] Guide can be saved/bookmarked
- [ ] User can return to wizard after reading guide

### Part 2: AI Wizard

- [ ] Model Router supports Llama 3.3 (local) and premium models
- [ ] Ollama integration with setup check
- [ ] SetupWizardAgent processes all 8 categories
- [ ] Intelligent conversation (validates findings, disambiguates, fills gaps)
- [ ] Category files created with template + extracted data
- [ ] Subcategory intelligence (adaptive based on content volume)
- [ ] WebSocket real-time communication works
- [ ] Frontend chat UI with progress sidebar
- [ ] Initial knowledge graph ingest after wizard completes

### Part 3: Live Knowledge Graph

- [ ] Knowledge graph auto-updates on scene complete
- [ ] Entity extraction from scenes (characters, locations, plot, motifs)
- [ ] Modified category files synced on scene complete
- [ ] Development docs saved for every query with meaningful filenames
- [ ] User notified after scene complete with update summary
- [ ] "Open Folder" button works for development docs
- [ ] Export summaries generate correctly (all 5 categories)
- [ ] Export UI in Project Settings/Tools panel
- [ ] Bidirectional knowledge flow works:
  - NotebookLM → Category folders → Knowledge graph → Scenes
  - Scenes → Knowledge graph → Development docs → NotebookLM

---

## File Checklist

### Frontend (React)

**New Files:**
1. `webapp/frontend-v2/src/components/onboarding/PathSelectionStep.jsx`
2. `webapp/frontend-v2/src/components/onboarding/PathOption.jsx`
3. `webapp/frontend-v2/src/components/onboarding/NotebookLMRecommendation.jsx`
4. `webapp/frontend-v2/src/pages/NotebookLMGuide.jsx`
5. `webapp/frontend-v2/src/pages/AIWizard.jsx`
6. `webapp/frontend-v2/src/components/wizard/ChatMessage.jsx`
7. `webapp/frontend-v2/src/components/wizard/ProgressSteps.jsx`
8. `webapp/frontend-v2/src/components/SceneCompleteNotification.jsx`
9. `webapp/frontend-v2/src/components/settings/ExportPanel.jsx`

**Modified Files:**
1. `webapp/frontend-v2/src/components/WelcomeModal.jsx` - Replace Step 3
2. `webapp/frontend-v2/src/App.jsx` - Add new routes

### Backend (Python)

**New Files:**
1. `factory/ai/model_router.py` - Model selection logic
2. `factory/ai/ollama_setup.py` - Ollama integration
3. `factory/ai/setup_wizard_agent.py` - AI wizard agent
4. `factory/templates/category_templates.py` - All 8 category templates
5. `factory/analysis/knowledge_graph_manager.py` - Graph lifecycle management
6. `factory/analysis/entity_extractor.py` - Extract entities from scenes
7. `factory/analysis/knowledge_graph_exporter.py` - Export summaries
8. `webapp/backend/routes/wizard.py` - WebSocket wizard endpoint
9. `webapp/backend/routes/knowledge.py` - Knowledge graph API endpoints

**Modified Files:**
1. `webapp/backend/simple_app.py` - Register new routers
2. `webapp/backend/routes/scenes.py` - Add scene completion logic

---

## Testing Strategy

### Week 1 Tests: Welcome Flow
- User selects "Experienced Writer" → Routes to import
- User selects "Prepared Writer" → Routes to AI wizard
- User selects "New Writer" → Shows recommendation modal
- "Show NotebookLM guide" → Opens guide in new window
- "Continue interactive" → Routes to Q&A wizard (fallback)
- Guide bookmark/save works

### Week 2 Tests: AI Wizard Backend
- Ollama check detects installation
- Llama 3.3 download triggered if missing
- Model Router selects correct model for task
- NotebookLM queries return data
- Template field extraction works
- Subcategory logic adapts to content volume
- Category files created correctly

### Week 3 Tests: AI Wizard Frontend + Knowledge Graph
- WebSocket connection established
- Chat messages render correctly
- User input captured and sent
- Progress sidebar updates
- Knowledge graph initialized from categories
- Scene completion extracts entities
- Modified category files synced
- Development docs saved with meaningful names
- User notification displays correctly
- Export summaries generate correctly

---

## Budget Estimate

**Using Default (Llama 3.3 Local):**
- $0/month for knowledge extraction
- Only cost: Scene writing with Claude (via MCP credits)

**Using Premium Models:**
- Setup wizard: ~$2-5 (one-time per project)
- Knowledge extraction: ~$5-10/month (active writing)
- Total: ~$15-30/month for full premium experience

**Recommended for January Course:**
- Default Llama for extraction (free)
- Claude via MCP for scene writing (included in course)
- Total additional cost: $0

---

## Timeline

**Week 1:** Welcome Flow UI (Part 1)
- Days 1-2: PathSelectionStep, NotebookLM Recommendation
- Days 3-4: NotebookLM Guide page
- Day 5: Routing, testing

**Week 2:** AI Wizard Backend (Part 2)
- Days 1-2: Model Router, Ollama integration
- Days 3-4: SetupWizardAgent, category templates
- Day 5: WebSocket endpoint, testing

**Week 3:** AI Wizard Frontend + Knowledge Graph (Part 3)
- Days 1-2: Chat UI, WebSocket frontend
- Days 3-4: Knowledge graph lifecycle, development docs
- Day 5: Export summaries, notifications, testing

---

## Ready for Claude Cloud! 🚀

This sprint combines the intelligent welcome flow with the live knowledge graph system. The two parts work together:

1. **Welcome flow** → User selects path → AI wizard extracts from NotebookLM
2. **Knowledge graph** → Initialized from categories → Auto-updates during writing → Exports back to NotebookLM

**Bidirectional knowledge flow complete!**
