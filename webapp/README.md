# Writers Factory Web Application

Browser-based interface for the Writers Factory multi-model AI novel writing system.

## Features

- **Creation Wizard**: 5-phase conversational story bible generator with 15-beat narrative structure
- **Model Comparison**: Side-by-side comparison of up to 4 AI models
- **Scene Tools**: Generate and enhance scenes with AI assistance
- **Knowledge Base**: Query your story bible and reference materials

## Quick Start

### Option 1: One-Command Launch (Recommended)

```bash
cd ~/writers-factory-core
source .venv/bin/activate
export PYTHONPATH=.
source .env  # Load API keys
python3 webapp/launch.py
```

The launcher will:
1. Start the FastAPI backend on port 8000
2. Open your browser to the web interface
3. Run until you press Ctrl+C

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd ~/writers-factory-core
source .venv/bin/activate
export PYTHONPATH=.
source .env
python3 webapp/backend/app.py
```

**Terminal 2 - Frontend:**
```bash
open webapp/frontend/index.html
```

## Architecture

```
webapp/
├── backend/
│   └── app.py          # FastAPI server with REST API + WebSocket
├── frontend/
│   ├── index.html      # Main web interface
│   └── static/
│       └── app.js      # Frontend JavaScript
├── launch.py           # One-command launcher
└── README.md           # This file
```

## API Endpoints

### Health Check
- `GET /api/health` - Server status

### Creation Wizard
- `POST /api/wizard/start` - Start new wizard session
- `POST /api/wizard/answer` - Submit answer
- `GET /api/wizard/progress` - Get current progress

### Model Comparison
- `POST /api/compare` - Compare 2-4 models
- `GET /api/models/available` - List all models
- `GET /api/models/groups` - Get model presets

### Scene Operations
- `POST /api/scene/generate` - Generate new scene
- `POST /api/scene/enhance` - Enhance existing scene

### Knowledge Base
- `POST /api/knowledge/query` - Ask question

### Session Management
- `GET /api/session/status` - Session info
- `POST /api/session/save` - Manual save

### WebSocket
- `WS /ws/stream` - Real-time streaming (TODO)

## Usage Examples

### Creation Wizard

1. Click "Creation Wizard" tab
2. Enter project name (e.g., "my-novel")
3. Answer questions through 5 phases:
   - Foundation (genre, theme, concept)
   - Character (protagonist, supporting cast)
   - Plot (15-beat narrative structure)
   - World (setting, context)
   - Symbolism (thematic layers)
4. Receive 4,000-6,000 word story bible

### Model Comparison

1. Click "Model Comparison" tab
2. Enter writing prompt
3. Select 2-4 models to compare
4. Click "Run Comparison"
5. View outputs side-by-side

### Scene Generation

1. Click "Scene Tools" tab
2. Enter scene prompt
3. Optionally add context
4. Select model
5. Click "Generate Scene"

## Sharing with Friends

### Local Hosting (Current)
- Web app runs on your machine
- Friends need to install their own copy
- API keys stay private on your machine

### Future Options

**Option A: Self-Hosted (Private)**
```bash
# Deploy to your own server with authentication
# Friends access via https://yourserver.com
# You provide API keys (shared cost)
```

**Option B: Cloud Hosted (Private)**
```bash
# Deploy to Vercel/Netlify/Railway
# Add simple password protection
# You manage API keys and costs
```

**Option C: Public SaaS (User Keys)**
```bash
# Public deployment where users bring own API keys
# No shared cost, maximum privacy
# Requires key management UI
```

## Security Notes

- API keys are loaded from `.env` on the backend
- Keys never sent to frontend
- All API calls go through backend
- CORS enabled for local development only

## Troubleshooting

### "Cannot connect to server"
- Make sure backend is running on port 8000
- Check: `curl http://127.0.0.1:8000/api/health`

### "Module not found" errors
- Ensure PYTHONPATH includes writers-factory-core root
- Run from correct directory: `cd ~/writers-factory-core`

### "No API keys configured"
- Load environment: `source .env`
- Check keys exist in `.env` file

### Port 8000 already in use
```bash
# Find and kill existing process
lsof -ti:8000 | xargs kill -9
```

## Development

### Add New Endpoint

1. Add route to `backend/app.py`:
```python
@app.post("/api/my-feature")
async def my_feature(request: MyRequest):
    # Implementation
    return {"success": True}
```

2. Add frontend function to `frontend/static/app.js`:
```javascript
async function myFeature() {
    const response = await fetch(`${API_BASE}/my-feature`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...})
    });
    const data = await response.json();
    // Handle response
}
```

3. Add UI element to `frontend/index.html`:
```html
<button class="button" onclick="myFeature()">My Feature</button>
```

### Hot Reload

Backend auto-reloads on code changes:
```bash
uvicorn webapp.backend.app:app --reload
```

## Next Steps

- [ ] Implement WebSocket streaming for real-time responses
- [ ] Add authentication for sharing with friends
- [ ] Create Docker container for easy deployment
- [ ] Add progress indicators during model generation
- [ ] Implement diff view for model comparison
- [ ] Add cost tracking dashboard
- [ ] Create mobile-responsive layout

## Support

For issues or questions:
- Check `READY_FOR_TESTING.md` for setup help
- Review `PHASE_2_IMPLEMENTATION_REPORT.md` for architecture details
- See main project README for API key configuration
