/**
 * Writers Factory Web Interface
 * Frontend JavaScript for interacting with FastAPI backend
 */

const API_BASE = 'http://127.0.0.1:8000/api';

// Global state
let selectedModels = [];
let availableModels = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadModels();
    setupTabs();
    checkServerHealth();
});

// Tab switching
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;

            // Update button states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Update content visibility
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// Health check
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        console.log('Server health:', data);
    } catch (error) {
        console.error('Server not responding:', error);
        alert('Cannot connect to Writers Factory server. Please make sure it is running on port 8000.');
    }
}

// ============================================================================
// CREATION WIZARD
// ============================================================================

async function startWizard() {
    const projectName = document.getElementById('project-name').value.trim();

    if (!projectName) {
        alert('Please enter a project name');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/wizard/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_name: projectName })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('wizard-start').style.display = 'none';
            document.getElementById('wizard-active').style.display = 'block';

            updateWizardUI(data);
        }
    } catch (error) {
        console.error('Error starting wizard:', error);
        alert('Failed to start wizard. Check console for details.');
    }
}

async function submitAnswer() {
    const answer = document.getElementById('wizard-answer').value.trim();

    if (!answer) {
        alert('Please provide an answer');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/wizard/answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer })
        });

        const data = await response.json();

        if (data.success) {
            if (data.complete) {
                // Wizard complete - show story bible
                document.getElementById('wizard-active').style.display = 'none';
                document.getElementById('wizard-complete').style.display = 'block';
                document.getElementById('story-bible-output').value = data.story_bible;
            } else {
                // Continue to next question
                updateWizardUI(data);
                document.getElementById('wizard-answer').value = '';
            }
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Failed to submit answer. Check console for details.');
    }
}

function updateWizardUI(data) {
    // Update progress bar
    const progress = data.progress || 0;
    document.getElementById('wizard-progress').style.width = `${progress}%`;

    // Update phase info
    const phaseNames = {
        'foundation': 'Foundation',
        'character': 'Character Development',
        'plot': 'Plot Structure',
        'world': 'World Building',
        'symbolism': 'Symbolism & Theme'
    };

    const phaseName = phaseNames[data.current_phase] || data.current_phase;
    document.getElementById('wizard-phase-name').textContent = phaseName;

    // Update question
    document.getElementById('wizard-current-question').textContent = data.question;
}

function resetWizard() {
    document.getElementById('wizard-complete').style.display = 'none';
    document.getElementById('wizard-start').style.display = 'block';
    document.getElementById('project-name').value = '';
}

// ============================================================================
// MODEL COMPARISON
// ============================================================================

async function loadModels() {
    try {
        const response = await fetch(`${API_BASE}/models/available`);
        const data = await response.json();
        availableModels = data.models;

        renderModelGrid();
        updateModelCount();
    } catch (error) {
        console.error('Error loading models:', error);
    }
}

function renderModelGrid() {
    const grid = document.getElementById('model-grid');
    grid.innerHTML = '';

    availableModels.forEach(model => {
        const card = document.createElement('div');
        card.className = 'model-card';
        card.onclick = () => toggleModelSelection(model.id, card);

        const costText = model.cost_input === 0
            ? 'FREE'
            : `$${(model.cost_input * 1000).toFixed(2)}/M tokens`;

        card.innerHTML = `
            <div class="provider">${model.provider.toUpperCase()}</div>
            <h3>${model.id}</h3>
            <div class="description">${model.description}</div>
            <div class="cost">${costText}</div>
        `;

        grid.appendChild(card);
    });
}

function toggleModelSelection(modelId, cardElement) {
    const index = selectedModels.indexOf(modelId);

    if (index > -1) {
        // Deselect
        selectedModels.splice(index, 1);
        cardElement.classList.remove('selected');
    } else {
        // Select (max 4)
        if (selectedModels.length >= 4) {
            alert('Maximum 4 models can be compared at once');
            return;
        }
        selectedModels.push(modelId);
        cardElement.classList.add('selected');
    }

    console.log('Selected models:', selectedModels);
}

async function runComparison() {
    const prompt = document.getElementById('compare-prompt').value.trim();

    if (!prompt) {
        alert('Please enter a writing prompt');
        return;
    }

    if (selectedModels.length < 2) {
        alert('Please select at least 2 models to compare');
        return;
    }

    // Show loading
    document.getElementById('comparison-loading').style.display = 'block';
    document.getElementById('comparison-results').innerHTML = '';

    try {
        const response = await fetch(`${API_BASE}/compare`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                models: selectedModels
            })
        });

        const data = await response.json();

        if (data.success) {
            displayComparisonResults(data.results);
        }
    } catch (error) {
        console.error('Error running comparison:', error);
        alert('Failed to run comparison. Check console for details.');
    } finally {
        document.getElementById('comparison-loading').style.display = 'none';
    }
}

function displayComparisonResults(results) {
    const container = document.getElementById('comparison-results');
    container.innerHTML = '';

    Object.entries(results).forEach(([model, output]) => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <h3>${model}</h3>
            <div class="output">${output}</div>
        `;
        container.appendChild(card);
    });
}

function updateModelCount() {
    document.getElementById('models-available').textContent =
        `${availableModels.length} Models Available`;
}

// ============================================================================
// SCENE TOOLS
// ============================================================================

function switchSceneTool(tool) {
    if (tool === 'generate') {
        document.getElementById('scene-generate').style.display = 'block';
        document.getElementById('scene-enhance').style.display = 'none';
    } else {
        document.getElementById('scene-generate').style.display = 'none';
        document.getElementById('scene-enhance').style.display = 'block';
    }
}

async function generateScene() {
    const prompt = document.getElementById('scene-prompt').value.trim();
    const context = document.getElementById('scene-context').value.trim();
    const model = document.getElementById('scene-model').value;

    if (!prompt) {
        alert('Please enter a scene prompt');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/scene/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                context: context || null,
                model
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('scene-output').style.display = 'block';
            document.getElementById('generated-scene').value = data.scene;
        }
    } catch (error) {
        console.error('Error generating scene:', error);
        alert('Failed to generate scene. Check console for details.');
    }
}

async function enhanceScene() {
    const sceneText = document.getElementById('enhance-input').value.trim();
    const focus = document.getElementById('enhance-focus').value;

    if (!sceneText) {
        alert('Please paste a scene to enhance');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/scene/enhance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                scene_text: sceneText,
                focus,
                model: 'claude-sonnet-4.5'
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('enhance-output').style.display = 'block';
            document.getElementById('enhanced-scene').value = data.enhanced_scene;
        }
    } catch (error) {
        console.error('Error enhancing scene:', error);
        alert('Failed to enhance scene. Check console for details.');
    }
}

// ============================================================================
// KNOWLEDGE BASE
// ============================================================================

async function askKnowledge() {
    const question = document.getElementById('knowledge-question').value.trim();

    if (!question) {
        alert('Please enter a question');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/knowledge/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question,
                source: 'cognee'
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('knowledge-answer').style.display = 'block';
            document.getElementById('knowledge-answer-text').textContent = data.answer;
        }
    } catch (error) {
        console.error('Error querying knowledge base:', error);
        alert('Failed to query knowledge base. Check console for details.');
    }
}
