# CLI Interface

Rich command-line interface for Writers Factory Core.

## Commands

### Initialize Project
```bash
factory init --name "My Novel" --genre "sci-fi thriller"
```

### Agent Management
```bash
# List all agents
factory agent list

# List only enabled agents
factory agent list --enabled-only

# Test agent connection
factory agent test claude-sonnet-4.5
```

### Run Workflows
```bash
# Run multi-model generation
factory workflow run multi-model-generation --agents "claude,gpt4o,gemini"

# Run project genesis
factory workflow run project-genesis
```

### Session Management
```bash
# List recent sessions
factory session list --limit 20

# Show session details
factory session show session-123

# Compare session results
factory session compare session-123
```

### Statistics
```bash
# Show system statistics
factory stats

# Show agent statistics
factory agent stats claude-sonnet-4.5

# Show cost breakdown
factory stats --costs --days 30
```

## Features

- **Rich formatting**: Colorful tables and panels
- **Progress bars**: Real-time workflow progress
- **Interactive prompts**: User-friendly input
- **Error handling**: Clear error messages
- **Batch operations**: Process multiple items

## Future Enhancements

- Real-time tournament monitoring (TUI)
- Side-by-side result comparison
- Interactive scoring interface
- Export to various formats
- Configuration management
