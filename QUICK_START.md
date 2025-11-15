# Writers Factory - Quick Start Guide

Get up and running with Writers Factory in 5 minutes!

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.10+** - [Download here](https://www.python.org/downloads/)
- ✅ **Node.js 18+** - [Download here](https://nodejs.org/)
- ✅ **Git** - [Download here](https://git-scm.com/)

**Check your versions**:
```bash
python3 --version  # Should be 3.10 or higher
node --version     # Should be 18.0 or higher
git --version      # Any recent version is fine
```

---

## 🚀 Installation (First Time Only)

### Step 1: Clone the Repository

```bash
git clone https://github.com/gcharris/writers-factory-core.git
cd writers-factory-core
```

### Step 2: Run Setup

```bash
./setup.sh
```

This will:
- Create Python virtual environment
- Install Python dependencies
- Install Node.js dependencies
- Set up project structure

**Time**: 2-3 minutes

---

## ▶️ Starting Writers Factory

Every time you want to use Writers Factory:

```bash
./start.sh
```

That's it! The script will:
1. Start the backend server
2. Start the frontend server
3. Open your browser automatically to http://localhost:5173

**You should see**: "✨ Writers Factory is ready!"

---

## 🛑 Stopping Writers Factory

Press `Ctrl+C` in the terminal where you ran `./start.sh`

The script will automatically:
- Stop the backend server
- Stop the frontend server
- Clean up processes

---

## 🎯 Using Writers Factory

### Creating Your First Project

1. Click **"New Project"** (or use Creation Wizard)
2. Enter project details:
   - Title: "My Novel"
   - Author: Your name
   - Genre, word count goal, etc.
3. Click **"Create Project"**

### Writing Scenes

1. **Left Panel**: Navigate file tree
   - Expand Acts → Chapters → Scenes
2. **Center Panel**: Write in TipTap editor
   - Click a scene to open
   - Start writing!
   - Auto-saves as you type
3. **Right Panel**: AI tools
   - Generate scene from outline
   - Enhance existing prose
   - Analyze characters

### File Management

- **Create scene**: Right-click chapter → "New Scene"
- **Rename scene**: Right-click scene → "Rename"
- **Delete scene**: Right-click scene → "Delete"
- **Reorder**: Drag and drop (coming soon!)

---

## 🤖 AI Models

### Option 1: Local Models (Free, Private)

**Install Ollama** (one-time setup):
```bash
# Mac
brew install ollama

# Start Ollama
ollama serve

# Pull models (in another terminal)
ollama pull llama3.2
ollama pull mistral
ollama pull qwen2.5
```

**In Writers Factory**:
- Models automatically detected
- Select from dropdown in AI Tools panel
- No API keys needed!

### Option 2: Cloud Models (Paid, High Quality)

**Add API keys** (one-time setup):

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your keys:
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
# GOOGLE_API_KEY=...
```

**In Writers Factory**:
- Cloud models appear in dropdown
- Track costs in real-time
- Economy mode for cost savings

---

## 📁 Project Structure

Your manuscripts are stored as regular files:

```
project/
└── .manuscript/
    └── your-project/
        ├── manifest.json        # Project metadata
        └── scenes/              # Your scenes as .md files
            ├── act-1/
            │   ├── chapter-1/
            │   │   ├── scene-abc123.md
            │   │   └── scene-def456.md
            └── act-2/
```

**You can**:
- Edit `.md` files in VS Code, Cursor AI, Typora, etc.
- Back up by copying the folder
- Version control with Git
- Share with collaborators

---

## 🐛 Troubleshooting

### "Command not found: ./start.sh"

Make sure the script is executable:
```bash
chmod +x start.sh setup.sh
```

### "Backend failed to start"

Check the logs:
```bash
cat .tmp/backend.log
```

Common fixes:
- Make sure Python 3.10+ is installed
- Try deleting `factory/venv` and re-running `./setup.sh`
- Check if port 8000 is already in use

### "Frontend failed to start"

Check the logs:
```bash
cat .tmp/frontend.log
```

Common fixes:
- Make sure Node.js 18+ is installed
- Delete `webapp/frontend-v2/node_modules` and re-run `./setup.sh`
- Check if port 5173 is already in use

### "No AI models available"

**For local models**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama
ollama serve
```

**For cloud models**:
- Check your `.env` file has API keys
- Restart Writers Factory after adding keys

### "Port already in use"

**Backend (port 8000)**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

**Frontend (port 5173)**:
```bash
# Find process using port 5173
lsof -i :5173

# Kill it
kill -9 <PID>
```

---

## 💡 Tips & Tricks

### 1. Use Economy Mode
- Toggle in AI Tools panel
- Uses local models when possible
- Saves on API costs

### 2. Tournament Mode
- Compare multiple models on same prompt
- Find which model excels at what
- Mix and match best outputs

### 3. Character Analysis
- Use Character Panel for deep analysis
- Check for contradictions
- Track character arcs

### 4. External Editing
- Edit `.md` files in your favorite editor
- Changes sync automatically
- Use powerful text editors alongside Writers Factory

### 5. Keyboard Shortcuts
- `Cmd+S` (Mac) / `Ctrl+S` (Windows): Save (auto-saves anyway)
- `Cmd+B`: Toggle left panel
- `Cmd+J`: Toggle right panel

---

## 📚 Next Steps

1. **Read the User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
2. **Watch Tutorial Videos**: Coming soon
3. **Join Community**: [GitHub Discussions](https://github.com/gcharris/writers-factory-core/discussions)
4. **Report Bugs**: [GitHub Issues](https://github.com/gcharris/writers-factory-core/issues)

---

## 🆘 Getting Help

- **Documentation**: Check [docs/](docs/) folder
- **GitHub Issues**: [Report bugs or request features](https://github.com/gcharris/writers-factory-core/issues)
- **GitHub Discussions**: [Ask questions, share ideas](https://github.com/gcharris/writers-factory-core/discussions)

---

## ✅ Checklist

First-time setup:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Repository cloned
- [ ] `./setup.sh` run successfully
- [ ] (Optional) Ollama installed
- [ ] (Optional) API keys added to `.env`

Every session:
- [ ] Run `./start.sh`
- [ ] Wait for "✨ Writers Factory is ready!"
- [ ] Create or open project
- [ ] Start writing!

---

**Happy writing!** ✍️

If you find Writers Factory useful, please ⭐ star the repository!
