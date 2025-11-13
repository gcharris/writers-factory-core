# Writers Factory Core - Testing Guide

This guide shows you how to test and interact with the Writers Factory Core system.

---

## 🚀 Quick Test (No Setup Required)

### 1. Interactive Demo - **START HERE!**
```bash
cd /home/user/writers-factory-core
python3 demo_interactive.py
```

This shows you:
- ✅ Single agent generation UX
- ✅ Multi-model tournament comparison
- ✅ Knowledge router in action
- ✅ Project genesis workflow
- ✅ Agent pool statistics
- ✅ Database analytics

**No API keys needed!** Uses mock data to demonstrate the full UX.

---

## 🧪 Test Suite

### Run All Tests
```bash
# Run complete test suite
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=factory --cov-report=html

# Run specific test file
pytest tests/test_workflow_engine.py -v -s
pytest tests/test_knowledge_router.py -v -s
pytest tests/test_agents.py -v -s
```

### What Tests Show You
- **Workflow Engine**: Step execution, dependency resolution, parallel processing
- **Knowledge Router**: Query classification, source routing, fallback chain
- **Agents**: Configuration, cost calculation, token counting
- **Workflows**: Lifecycle management, error handling

---

## 🔬 Interactive Python Testing

### Test Agent Configuration
```bash
python3 -c "
from factory.agents.base_agent import AgentConfig

config = AgentConfig(
    name='test-agent',
    model='test-model',
    context_window=100000,
    cost_per_1k_input=0.003
)

print('Agent Config:')
print(f'  Name: {config.name}')
print(f'  Context: {config.context_window:,} tokens')
print(f'  Cost: \${config.cost_per_1k_input}/1k tokens')
"
```

### Test Workflow Engine
```bash
python3 -c "
import asyncio
from factory.core.workflow_engine import Workflow

async def test():
    wf = Workflow('test-workflow')
    wf.add_step('step1', lambda ctx: print('Step 1 executed'))
    wf.add_step('step2', lambda ctx: print('Step 2 executed'), dependencies=['step1'])
    print(f'Workflow \"{wf.name}\" has {len(wf.steps)} steps')
    return wf

workflow = asyncio.run(test())
print(f'Steps: {[s.name for s in workflow.steps]}')
"
```

### Test Knowledge Router
```bash
python3 -c "
from factory.knowledge.router import KnowledgeRouter, QueryType

router = KnowledgeRouter()

queries = [
    'What is Mickey\\'s age?',
    'How are Mickey and Noni related?',
    'Why does Mickey avoid his powers?',
]

for q in queries:
    qtype = router.classify_query(q)
    source = router.route_query(q)
    print(f'{qtype.value.upper():12} -> {source.value:20} | {q}')
"
```

### Load Agent Registry
```bash
python3 -c "
import yaml

with open('factory/core/config/agents.yaml') as f:
    config = yaml.safe_load(f)

agents = config['agents']
print(f'Total agents configured: {len(agents)}')
print('\nEnabled agents:')
for name, info in agents.items():
    if info.get('enabled'):
        print(f'  • {name:20} ({info[\"provider\"]})')
"
```

---

## 🎨 CLI Interface Testing

### List Available Commands
```bash
python3 -m factory.ui.cli --help
```

### Test Agent Listing
```bash
python3 -c "
from factory.core.agent_pool import AgentPool
import yaml

# Load config
with open('factory/core/config/agents.yaml') as f:
    config = yaml.safe_load(f)

# Create pool
pool = AgentPool()

# Show enabled agents
print('Enabled Agents:')
for name, info in config['agents'].items():
    if info.get('enabled'):
        print(f'  {name}')
        print(f'    Provider: {info[\"provider\"]}')
        print(f'    Model: {info[\"model\"]}')
        print(f'    Cost: \${info[\"cost_per_1k_input\"]}/\${info[\"cost_per_1k_output\"]} per 1k tokens')
        print()
"
```

---

## 📊 Database Testing

### Inspect Database Schema
```bash
# View schema
cat factory/storage/schema.sql

# Count tables
grep "CREATE TABLE" factory/storage/schema.sql | wc -l

# Count views
grep "CREATE VIEW" factory/storage/schema.sql | wc -l
```

### Test Database Operations
```bash
python3 -c "
from factory.storage.database import Database
import asyncio

async def test():
    db = Database(':memory:')  # In-memory database
    await db.initialize()

    # Test session creation
    session_id = await db.create_session(
        workflow_name='test-workflow',
        context={'test': True}
    )

    print(f'Created session: {session_id}')

    # Test result storage
    result_id = await db.store_result(
        session_id=session_id,
        agent_name='test-agent',
        prompt='test prompt',
        output='test output',
        tokens_input=100,
        tokens_output=200,
        cost=0.01,
        response_time_ms=1500
    )

    print(f'Stored result: {result_id}')

    # Query analytics
    stats = await db.get_agent_stats('test-agent')
    print(f'Agent stats: {stats}')

asyncio.run(test())
"
```

---

## 🔧 Testing With Real API Keys (When Ready)

### 1. Create Credentials File
```bash
mkdir -p config
cat > config/credentials.json << 'EOF'
{
  "anthropic_api_key": "YOUR_ANTHROPIC_KEY",
  "openai_api_key": "YOUR_OPENAI_KEY",
  "google_api_key": "YOUR_GOOGLE_KEY",
  "xai_api_key": "YOUR_XAI_KEY",
  "deepseek_api_key": "YOUR_DEEPSEEK_KEY",
  "qwen_api_key": "YOUR_QWEN_KEY",
  "doubao_api_key": "YOUR_DOUBAO_KEY",
  "baichuan_api_key": "YOUR_BAICHUAN_KEY",
  "kimi_api_key": "YOUR_KIMI_KEY"
}
EOF
```

### 2. Test Single Agent (Replace API key)
```bash
# Edit examples/simple_generation.py - replace YOUR_DEEPSEEK_API_KEY
python3 examples/simple_generation.py
```

### 3. Test Multi-Model Tournament
```bash
# Edit examples/multi_model_comparison.py - replace API keys
python3 examples/multi_model_comparison.py
```

---

## 🎭 Custom Test Scenarios

### Create Your Own Test Workflow
```python
# test_custom_workflow.py
import asyncio
from factory.core.workflow_engine import Workflow, WorkflowEngine

async def main():
    # Create workflow
    workflow = Workflow("my-test-workflow")

    # Add steps
    workflow.add_step("prepare", lambda ctx: {"status": "prepared"})
    workflow.add_step("process", lambda ctx: {"result": "processed"}, dependencies=["prepare"])
    workflow.add_step("finalize", lambda ctx: {"status": "done"}, dependencies=["process"])

    # Execute
    engine = WorkflowEngine()
    result = await engine.run_workflow(workflow)

    print(f"Status: {result.status.value}")
    print(f"Steps: {result.steps_completed}/{result.steps_total}")
    print(f"Duration: {result.duration:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

### Test Knowledge Router With Custom Queries
```python
# test_custom_routing.py
from factory.knowledge.router import KnowledgeRouter

router = KnowledgeRouter(prefer_local=True)

custom_queries = [
    "What is the capital of France?",
    "How does quantum entanglement relate to consciousness?",
    "Why did the character make that choice?",
    "Analyze the themes in Chapter 3",
]

for query in custom_queries:
    qtype = router.classify_query(query)
    source = router.route_query(query)
    print(f"{query}")
    print(f"  Type: {qtype.value}")
    print(f"  Source: {source.value}")
    print()
```

---

## 📈 Performance Testing

### Benchmark Workflow Engine
```bash
python3 -c "
import asyncio
import time
from factory.core.workflow_engine import Workflow, WorkflowEngine

async def benchmark():
    workflow = Workflow('benchmark')

    # Add 10 steps
    for i in range(10):
        workflow.add_step(f'step_{i}', lambda ctx: f'result_{i}')

    engine = WorkflowEngine()

    start = time.time()
    result = await engine.run_workflow(workflow, parallel=True)
    duration = time.time() - start

    print(f'Executed {result.steps_completed} steps in {duration:.3f}s')
    print(f'Avg: {duration/result.steps_completed*1000:.1f}ms per step')

asyncio.run(benchmark())
"
```

### Test Parallel Execution
```bash
python3 -c "
import asyncio
import time

async def slow_task(n):
    await asyncio.sleep(0.5)
    return f'Task {n} done'

async def test_parallel():
    start = time.time()

    # Sequential
    results = []
    for i in range(5):
        results.append(await slow_task(i))
    sequential_time = time.time() - start

    # Parallel
    start = time.time()
    results = await asyncio.gather(*[slow_task(i) for i in range(5)])
    parallel_time = time.time() - start

    print(f'Sequential: {sequential_time:.2f}s')
    print(f'Parallel:   {parallel_time:.2f}s')
    print(f'Speedup:    {sequential_time/parallel_time:.1f}x')

asyncio.run(test_parallel())
"
```

---

## 🐛 Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```bash
# Test just the workflow engine
pytest tests/test_workflow_engine.py::test_workflow_execution -v -s

# Test just query classification
pytest tests/test_knowledge_router.py::test_query_classification -v -s
```

### Check Imports
```bash
python3 -c "
import factory.core.workflow_engine
import factory.agents.base_agent
import factory.knowledge.router
import factory.workflows.base_workflow
print('✓ All imports successful')
"
```

---

## 📚 Next Steps

1. **Start with demo**: `python3 demo_interactive.py`
2. **Run tests**: `pytest tests/ -v`
3. **Try examples**: Edit API keys and run examples
4. **Build custom workflows**: Use the patterns from examples
5. **Add real API credentials**: Test with actual LLMs
6. **Integrate with your project**: Import factory modules

---

## 🎯 Quick Command Reference

```bash
# Demo (no setup needed)
python3 demo_interactive.py

# Run all tests
pytest tests/ -v

# Test specific component
pytest tests/test_workflow_engine.py -v

# View agent configuration
cat factory/core/config/agents.yaml

# Check database schema
cat factory/storage/schema.sql

# List all Python modules
find factory -name "*.py" -type f

# Show documentation
ls docs/

# Run example (needs API key)
python3 examples/simple_generation.py
```

---

**Happy Testing!** 🚀

For more information, see:
- `README.md` - Project overview
- `docs/QUICKSTART.md` - 5-minute getting started guide
- `docs/ARCHITECTURE.md` - System architecture
- `IMPLEMENTATION_REPORT.md` - Complete implementation status
