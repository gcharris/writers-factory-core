# Agent Configuration Summary

Complete list of all LLM agents configured for Writers Factory Core.

## Total Agents: 23 Models

### Anthropic (4 models)
1. **claude-opus-4** - Most capable Claude for complex creative tasks
2. **claude-sonnet-4.5** - Best balance of quality and cost for creative writing
3. **claude-sonnet-3.5** - Fast and reliable for general creative writing
4. **claude-3-opus** ⭐ - Previous generation Opus, excellent creative writing

### OpenAI (5 models)
5. **gpt-4o** - Excellent for dialogue and polished prose
6. **gpt-4-turbo** - Strong reasoning for complex world-building
7. **gpt-3.5-turbo** ⭐ - Surprisingly good for creative writing (better than 4o for narrative)
8. **gpt-3.5-turbo-16k** ⭐ - Longer context, good creative writing quality

### Google (3 models)
9. **gemini-2-flash** - Free with massive 1M context window
10. **gemini-1.5-pro** - Best for analyzing large reference materials (2M context)
11. **gemini-1.0-pro** ⭐ - Earlier Gemini, good for creative writing experiments

### xAI (1 model)
12. **grok** - Unconventional and creative perspectives

### Chinese LLMs (9 models)
13. **qwen-max** - Qwen (通义千问) Alibaba's flagship model
14. **qwen-turbo** - Faster, cheaper Qwen variant
15. **deepseek-v3** - DeepSeek V3, extremely cost-effective
16. **doubao** - Doubao (豆包) ByteDance's model
17. **baichuan** - Baichuan (百川) Strong reasoning model
18. **kimi** - Kimi (月之暗面) Long context specialist (128k)
19. **chatglm** ✨ - ChatGLM/Zhipu AI, strong dialogue and everyday speech
20. **ernie** ✨ - Baidu ERNIE (文心一言) Strong Chinese language model
21. **hunyuan** ✨ - Tencent Hunyuan (混元) Versatile creative writing
22. **yi** ✨ - 01.AI Yi (零一万物) Strong narrative and descriptive capabilities

### Open Source (2 models)
23. **mistral-large** - Mistral's largest model
24. **llama-3-70b** - Meta's Llama 3 70B (requires local setup, free)

⭐ = Older model version specifically chosen for creative writing quality
✨ = Newly added Chinese model

## API Access Links

### Western LLMs
- **Anthropic Claude**: https://console.anthropic.com/
- **OpenAI GPT**: https://platform.openai.com/
- **Google Gemini**: https://ai.google.dev/
- **xAI Grok**: https://x.ai/api
- **Mistral**: https://console.mistral.ai/
- **Meta Llama**: https://ai.meta.com/llama/ (local or via providers)

### Chinese LLMs
- **Qwen (Alibaba)**: https://tongyi.aliyun.com/qianwen
- **DeepSeek**: https://deepseek.com/api
- **Doubao (ByteDance)**: https://console.volcengine.com/aiservice
- **Baichuan**: https://open.baichuan-ai.com
- **Kimi (Moonshot)**: https://kimi.moonshot.cn/api
- **ChatGLM (Zhipu AI)**: https://open.bigmodel.cn
- **ERNIE (Baidu)**: https://cloud.baidu.com/product/wenxin
- **Hunyuan (Tencent)**: https://cloud.tencent.com/product/hunyuan
- **Yi (01.AI)**: https://platform.01.ai/docs/overview/yi-api

## Agent Groups (Presets)

### Premium (3 models)
- claude-opus-4
- gpt-4o
- gemini-1.5-pro

### Balanced (4 models)
- claude-sonnet-4.5
- gpt-4o
- gemini-2-flash
- deepseek-v3

### Budget (4 models)
- claude-sonnet-3.5
- gemini-2-flash
- deepseek-v3
- doubao

### Chinese (5 models)
- qwen-max
- deepseek-v3
- doubao
- baichuan
- kimi

### Creative (3 models)
- claude-sonnet-4.5
- grok
- qwen-max

### Dialogue (3 models)
- gpt-4o
- claude-sonnet-3.5
- doubao

## Creative Writing Strengths by Model

### Best for Narrative Flow
- gpt-3.5-turbo (⭐ surprisingly better than 4o)
- gpt-3.5-turbo-16k (⭐ longer context)
- claude-3-opus (⭐ previous generation)
- claude-sonnet-4.5

### Best for Dialogue
- gpt-4o
- chatglm (Chinese vernacular)
- doubao (Chinese dialogue)
- claude-sonnet-3.5

### Best for Philosophical Depth
- claude-opus-4
- claude-3-opus
- qwen-max

### Best for Descriptive Passages
- yi (mood setting, stylistic experimentation)
- claude-opus-4
- gemini-1.5-pro

### Best for Character Development
- claude-opus-4
- claude-3-opus
- claude-sonnet-4.5

### Best for World Building
- gpt-4-turbo (technical accuracy)
- gemini-2-flash (long context, free)
- deepseek-v3 (long-form consistency)

### Best for Cost-Effective Testing
- gemini-2-flash (FREE, 1M context)
- deepseek-v3 ($0.00027/1k input)
- gpt-3.5-turbo ($0.0005/1k input)
- doubao ($0.0008/1k input)

## Configuration Files

### 1. Agent Registry
**File**: `factory/core/config/agents.yaml`
- Contains all 23+ agent configurations
- Model-specific parameters (context window, costs, strengths)
- Handler class references
- Enable/disable flags

### 2. API Credentials
**File**: `config/credentials.json`
- API keys for all providers
- Base URLs for Chinese LLMs
- NotebookLM configuration

### 3. Environment Variables
**File**: `.env` (copy from `.env.template`)
- API keys as environment variables
- System paths (Cognee, database, sessions)

## Usage Examples

### List All Agents
```bash
factory agent list
```

### Run Model Comparison (Tournament)
```bash
factory compare --prompt "Write a scene where Mickey discovers..." \
  --models claude-opus-4,gpt-3.5-turbo,deepseek-v3,yi
```

### Test Creative Writing Group
```bash
factory compare --prompt "Describe the quantum space..." \
  --group creative
```

### Compare Old vs New Models
```bash
# Test if older models write better
factory compare --prompt "Write dialogue between Noni and Ben..." \
  --models gpt-3.5-turbo,gpt-4o,claude-3-opus,claude-opus-4
```

### Test Chinese Models
```bash
factory compare --prompt "Write a scene with Chinese cultural elements..." \
  --group chinese
```

### Budget Testing
```bash
# Use free/cheap models for rapid iteration
factory compare --prompt "Draft a scene outline..." \
  --models gemini-2-flash,deepseek-v3,gpt-3.5-turbo
```

## Cost Comparison (per 1M tokens)

### Most Expensive
1. claude-opus-4: $15/$75 (input/output)
2. claude-3-opus: $15/$75
3. gpt-4-turbo: $10/$30
4. ernie: $12/$12
5. kimi: $12/$12

### Mid-Range
6. gpt-4o: $2.50/$10
7. hunyuan: $10/$10
8. baichuan: $10/$10
9. qwen-max: $8/$8
10. chatglm: $5/$5

### Most Cost-Effective
11. gpt-3.5-turbo: $0.50/$1.50 ⭐
12. gemini-1.0-pro: $0.50/$1.50
13. gemini-2-flash: FREE
14. deepseek-v3: $0.27/$1.10 (cheapest paid)
15. doubao: $0.80/$2.00

## Next Steps

1. **Add API Keys**: Edit `config/credentials.json` and `.env` with your actual keys
2. **Test Agents**: Run `python3 test_setup.py` to verify imports
3. **Initialize Cognee**: Run `python3 init_cognee.py` (requires API keys)
4. **Run Tournament**: Test Phase 1 demo with `python3 demo_interactive.py`
5. **Wait for Phase 2**: Cloud Agent is building the full Rich TUI workflow

## Notes

- All agents are **enabled by default** except those requiring local setup
- **Older models** (claude-3-opus, gpt-3.5-turbo, gemini-1.0-pro) included because they often produce better creative writing than newer versions
- **Chinese models** cover major providers: Alibaba, ByteDance, Baidu, Tencent, Moonshot, Zhipu, 01.AI
- **Open source** models (Mistral, Llama) available but may require additional setup
- Cost estimates are approximate and subject to change by providers

---

**Total Models Enabled**: 23
**Configuration Status**: ✅ Complete
**Ready for Testing**: ⏳ Add API keys first
