# Writers Factory Web App - Quick Start

## Launch in 3 Commands

```bash
cd ~/writers-factory-core
source .venv/bin/activate && export PYTHONPATH=. && source .env
python3 webapp/launch.py
```

Your browser will open to the Writers Factory web interface.

## Features

- **Creation Wizard**: Generate story bibles through AI conversation
- **Model Comparison**: Test up to 4 AI models side-by-side
- **Scene Tools**: Generate and enhance scenes
- **Knowledge Base**: Query your story materials

## First Time Setup

If you haven't already:

```bash
# Install dependencies
pip install fastapi "uvicorn[standard]" websockets

# Test everything works
python3 webapp/test_webapp.py
```

## Stop the Server

Press `Ctrl+C` in the terminal where you ran `launch.py`

## Documentation

- Full documentation: [webapp/README.md](README.md)
- Deployment guide: [WEB_APP_READY.md](../WEB_APP_READY.md)
- API testing guide: [READY_FOR_TESTING.md](../READY_FOR_TESTING.md)

## Troubleshooting

**Can't connect to server?**
```bash
# Check it's running
curl http://127.0.0.1:8000/api/health
```

**Port 8000 in use?**
```bash
lsof -ti:8000 | xargs kill -9
```

**Missing API keys?**
```bash
source .env
echo $ANTHROPIC_API_KEY  # Should show your key
```

---

**Happy Writing!** ✨
