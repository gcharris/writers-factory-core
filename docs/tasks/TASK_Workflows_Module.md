# Task: Build Pre-Built Workflows Module

**Priority**: High
**Assigned To**: Cloud Agent
**Estimated Time**: 5-6 hours
**Dependencies**: Storage/Session Management, Master CLI

---

## Context

You are building the pre-built workflows module that automates complex multi-step operations in the Writers Factory. These workflows combine AI agents, knowledge systems, and analysis tools into seamless end-to-end processes.

Currently, users must manually:
1. Query knowledge systems for context
2. Generate content with AI models
3. Score and analyze results
4. Iterate on improvements

Your task is to automate these workflows so users can invoke a single command and get polished results.

---

## Architecture Overview

### Workflow Types

1. **Scene Generation Workflow**
   - Input: Scene outline/scaffold
   - Output: 5 variants, scored and ranked
   - Steps: Context retrieval → Multi-model generation → Scoring → Ranking

2. **Scene Enhancement Workflow**
   - Input: Rough draft scene
   - Output: Enhanced scene with voice consistency
   - Steps: Analysis → Voice guide retrieval → Enhancement → Validation

3. **Voice Testing Workflow**
   - Input: Scene outline + list of models
   - Output: Comparison report with winner
   - Steps: Parallel generation → Voice scoring → Comparison → Recommendation

4. **Batch Processing Workflow**
   - Input: Directory of scaffolds
   - Output: Directory of enhanced scenes + report
   - Steps: Load all → Process each → Track progress → Generate report

5. **Canon Consistency Workflow**
   - Input: Volume/chapter/scene
   - Output: Consistency report with issues
   - Steps: Extract facts → Compare to canon → Flag contradictions → Generate report

6. **Smart Scaffold Generation Workflow**
   - Input: Minimal outline
   - Output: Gold standard scaffold ready for generation
   - Steps: Query KB → Expand outline → Add context → Validate completeness

---

## Core Workflow Infrastructure

### Base Workflow Class

```python
# factory/core/workflows/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import asyncio

class WorkflowStep:
    """Single step in a workflow"""

    def __init__(self, name: str, func: callable, **kwargs):
        self.name = name
        self.func = func
        self.kwargs = kwargs
        self.result: Optional[Any] = None
        self.error: Optional[Exception] = None

    async def execute(self, context: Dict[str, Any]):
        """Execute this step"""
        try:
            self.result = await self.func(context, **self.kwargs)
            return self.result
        except Exception as e:
            self.error = e
            raise

class Workflow(ABC):
    """Base class for all workflows"""

    def __init__(self, app: 'WritersFactory'):
        self.app = app
        self.steps: List[WorkflowStep] = []
        self.context: Dict[str, Any] = {}

    def add_step(self, name: str, func: callable, **kwargs):
        """Add a step to the workflow"""
        step = WorkflowStep(name, func, **kwargs)
        self.steps.append(step)
        return self

    async def execute(self, initial_context: Dict[str, Any] = None):
        """Execute all steps in sequence"""
        if initial_context:
            self.context.update(initial_context)

        results = []

        for i, step in enumerate(self.steps):
            # Update UI
            self.app.ui.update_progress(
                current=i+1,
                total=len(self.steps),
                description=step.name
            )

            # Execute step
            try:
                result = await step.execute(self.context)
                results.append(result)

                # Add result to context for next steps
                self.context[f"step_{i}_result"] = result

            except Exception as e:
                self.app.console.print(f"[red]Error in step '{step.name}': {e}[/red]")
                raise

        return WorkflowResult(
            workflow=self.__class__.__name__,
            steps=self.steps,
            results=results,
            context=self.context
        )

    @abstractmethod
    async def run(self, **kwargs) -> WorkflowResult:
        """Main entry point for workflow"""
        pass
```

### Workflow Result Container

```python
# factory/core/workflows/result.py
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class WorkflowResult:
    """Container for workflow results"""
    workflow: str
    steps: List[WorkflowStep]
    results: List[Any]
    context: Dict[str, Any]
    total_cost: float = 0.0

    def get_final_result(self):
        """Get the final result from last step"""
        return self.results[-1] if self.results else None

    def get_step_result(self, step_name: str):
        """Get result from a specific step"""
        for step, result in zip(self.steps, self.results):
            if step.name == step_name:
                return result
        return None
```

---

## Workflow Implementations

### 1. Scene Generation Workflow

```python
# factory/core/workflows/scene_generation.py
from typing import List, Optional

class SceneGenerationWorkflow(Workflow):
    """
    Generate scene from outline with context and scoring

    Steps:
    1. Parse outline/scaffold
    2. Query knowledge base for context
    3. Generate N variants with selected model
    4. Score each variant
    5. Rank by score
    """

    async def run(
        self,
        outline: str,
        model: str,
        variants: int = 5,
        context_queries: Optional[List[str]] = None
    ) -> WorkflowResult:
        """Execute scene generation workflow"""

        # Step 1: Parse outline
        self.add_step(
            "Parse Outline",
            self._parse_outline,
            outline=outline
        )

        # Step 2: Get context from knowledge base
        self.add_step(
            "Retrieve Context",
            self._get_context,
            queries=context_queries or self._extract_context_queries(outline)
        )

        # Step 3: Generate variants
        self.add_step(
            "Generate Variants",
            self._generate_variants,
            model=model,
            count=variants
        )

        # Step 4: Score variants
        self.add_step(
            "Score Variants",
            self._score_variants
        )

        # Step 5: Rank results
        self.add_step(
            "Rank Results",
            self._rank_variants
        )

        # Execute workflow
        result = await self.execute({
            'outline': outline,
            'model': model
        })

        # Calculate total cost
        result.total_cost = await self._calculate_cost(result)

        return result

    async def _parse_outline(self, context: Dict) -> Dict:
        """Parse outline and extract metadata"""
        outline = context['outline']

        # Extract scene ID, POV, key beats
        parsed = {
            'scene_id': self._extract_scene_id(outline),
            'pov_character': self._extract_pov(outline),
            'key_beats': self._extract_beats(outline),
            'word_count_target': self._extract_word_count(outline),
            'raw_outline': outline
        }

        return parsed

    async def _get_context(self, context: Dict, queries: List[str]) -> Dict:
        """Query knowledge base for context"""
        router = self.app.knowledge_router

        context_data = {}

        for query in queries:
            result = await router.query(query)
            context_data[query] = result.answer

        return {
            'queries': queries,
            'context': context_data
        }

    async def _generate_variants(
        self,
        context: Dict,
        model: str,
        count: int
    ) -> List[str]:
        """Generate multiple scene variants"""
        agent = self.app.get_agent(model)

        # Get parsed outline and context
        outline = context['step_0_result']
        kb_context = context['step_1_result']

        # Build full prompt
        prompt = self._build_generation_prompt(outline, kb_context)

        # Generate variants in parallel
        tasks = [
            agent.generate_scene(prompt)
            for _ in range(count)
        ]

        variants = await asyncio.gather(*tasks)

        return variants

    async def _score_variants(self, context: Dict) -> List[Dict]:
        """Score each variant"""
        variants = context['step_2_result']
        outline = context['step_0_result']

        scorer = SceneScorer(self.app)

        scored = []
        for i, variant in enumerate(variants):
            score = await scorer.score(
                scene=variant,
                outline=outline,
                character_voice=True,
                plot_consistency=True
            )

            scored.append({
                'variant_index': i,
                'text': variant,
                'score': score.total_score,
                'breakdown': score.breakdown
            })

        return scored

    async def _rank_variants(self, context: Dict) -> List[Dict]:
        """Rank variants by score"""
        scored_variants = context['step_3_result']

        # Sort by score descending
        ranked = sorted(
            scored_variants,
            key=lambda x: x['score'],
            reverse=True
        )

        return ranked

    def _extract_context_queries(self, outline: str) -> List[str]:
        """Extract queries from outline"""
        # Look for character names, locations, etc.
        queries = []

        # Simple extraction (can be enhanced with NLP)
        for line in outline.split('\n'):
            if 'Character:' in line:
                char = line.split('Character:')[1].strip()
                queries.append(f"Who is {char}?")

            if 'Location:' in line:
                loc = line.split('Location:')[1].strip()
                queries.append(f"Describe {loc}")

        return queries

    def _build_generation_prompt(
        self,
        outline: Dict,
        kb_context: Dict
    ) -> str:
        """Build full prompt for scene generation"""
        prompt = f"""Generate a scene based on this outline:

**Scene ID**: {outline['scene_id']}
**POV Character**: {outline['pov_character']}
**Target Length**: {outline['word_count_target']} words

**Key Beats**:
{chr(10).join(f"- {beat}" for beat in outline['key_beats'])}

**Context from Knowledge Base**:
{chr(10).join(f"{q}: {a}" for q, a in kb_context['context'].items())}

**Outline**:
{outline['raw_outline']}

Generate the scene with authentic voice, embedded philosophy, and compressed phrasing.
"""
        return prompt
```

### 2. Scene Enhancement Workflow

```python
# factory/core/workflows/scene_enhancement.py

class SceneEnhancementWorkflow(Workflow):
    """
    Enhance existing scene with voice consistency

    Steps:
    1. Analyze current scene (identify issues)
    2. Get voice requirements from KB
    3. Enhance scene with AI
    4. Validate voice consistency
    5. Return enhanced version
    """

    async def run(
        self,
        scene: str,
        model: str,
        voice_character: str = "Enhanced Mickey"
    ) -> WorkflowResult:
        """Execute scene enhancement workflow"""

        self.add_step(
            "Analyze Scene",
            self._analyze_scene,
            scene=scene
        )

        self.add_step(
            "Get Voice Requirements",
            self._get_voice_requirements,
            character=voice_character
        )

        self.add_step(
            "Enhance Scene",
            self._enhance_scene,
            model=model
        )

        self.add_step(
            "Validate Voice",
            self._validate_voice,
            character=voice_character
        )

        result = await self.execute({
            'scene': scene,
            'model': model
        })

        return result

    async def _analyze_scene(self, context: Dict, scene: str) -> Dict:
        """Analyze scene for issues"""
        analyzer = SceneAnalyzer()

        analysis = await analyzer.analyze(scene)

        return {
            'word_count': analysis.word_count,
            'sentence_count': analysis.sentence_count,
            'voice_issues': analysis.voice_issues,
            'plot_issues': analysis.plot_issues,
            'suggestions': analysis.suggestions
        }

    async def _get_voice_requirements(
        self,
        context: Dict,
        character: str
    ) -> str:
        """Get voice requirements from KB"""
        query = f"What are the voice requirements for {character}?"

        result = await self.app.cognee.query(query)

        return result

    async def _enhance_scene(
        self,
        context: Dict,
        model: str
    ) -> str:
        """Enhance scene with AI"""
        scene = context['scene']
        analysis = context['step_0_result']
        voice_guide = context['step_1_result']

        agent = self.app.get_agent(model)

        prompt = f"""Enhance this scene while maintaining voice consistency:

**Current Scene**:
{scene}

**Analysis**:
{analysis}

**Voice Requirements**:
{voice_guide}

Enhance the scene by:
1. Fixing voice inconsistencies
2. Tightening prose
3. Deepening character voice
4. Embedding philosophy naturally

Return only the enhanced scene.
"""

        enhanced = await agent.enhance(prompt)

        return enhanced

    async def _validate_voice(
        self,
        context: Dict,
        character: str
    ) -> Dict:
        """Validate voice consistency of enhanced scene"""
        enhanced = context['step_2_result']

        tester = VoiceConsistencyTester()

        score = await tester.test_scene(enhanced, character)

        return {
            'score': score.total_score,
            'issues': score.issues,
            'passed': score.total_score >= 80
        }
```

### 3. Voice Testing Workflow

```python
# factory/core/workflows/voice_testing.py

class VoiceTestingWorkflow(Workflow):
    """
    Test multiple models for voice consistency

    Steps:
    1. Generate outputs from all models
    2. Score voice consistency for each
    3. Compare results
    4. Recommend winner
    """

    async def run(
        self,
        prompt: str,
        models: List[str],
        character: str = "Enhanced Mickey"
    ) -> WorkflowResult:
        """Execute voice testing workflow"""

        self.add_step(
            "Generate from All Models",
            self._generate_all_models,
            prompt=prompt,
            models=models
        )

        self.add_step(
            "Score Voice Consistency",
            self._score_all_outputs,
            character=character
        )

        self.add_step(
            "Compare Results",
            self._compare_results
        )

        self.add_step(
            "Recommend Winner",
            self._recommend_winner
        )

        result = await self.execute({
            'prompt': prompt,
            'models': models
        })

        return result

    async def _generate_all_models(
        self,
        context: Dict,
        prompt: str,
        models: List[str]
    ) -> Dict[str, str]:
        """Generate outputs from all models in parallel"""
        tasks = {}

        for model in models:
            agent = self.app.get_agent(model)
            tasks[model] = agent.generate_scene(prompt)

        # Execute in parallel
        results = {}
        for model, task in tasks.items():
            results[model] = await task

        return results

    async def _score_all_outputs(
        self,
        context: Dict,
        character: str
    ) -> Dict[str, float]:
        """Score voice consistency for all outputs"""
        outputs = context['step_0_result']

        tester = VoiceConsistencyTester()

        scores = {}
        for model, output in outputs.items():
            score = await tester.test_scene(output, character)
            scores[model] = score.total_score

        return scores

    async def _compare_results(self, context: Dict) -> Dict:
        """Compare all results"""
        outputs = context['step_0_result']
        scores = context['step_1_result']

        comparison = []

        for model in outputs.keys():
            comparison.append({
                'model': model,
                'output': outputs[model],
                'score': scores[model]
            })

        # Sort by score
        comparison.sort(key=lambda x: x['score'], reverse=True)

        return comparison

    async def _recommend_winner(self, context: Dict) -> Dict:
        """Recommend the best model"""
        comparison = context['step_2_result']

        winner = comparison[0]

        return {
            'winner': winner['model'],
            'score': winner['score'],
            'reasoning': f"{winner['model']} achieved the highest voice consistency score"
        }
```

### 4. Batch Processing Workflow

```python
# factory/core/workflows/batch_processing.py
from pathlib import Path
import json

class BatchProcessingWorkflow(Workflow):
    """
    Process multiple scaffolds in batch

    Steps:
    1. Load config and scaffolds
    2. Process each scaffold with scene generation
    3. Track progress
    4. Generate summary report
    """

    async def run(
        self,
        config_path: Path
    ) -> WorkflowResult:
        """Execute batch processing workflow"""

        self.add_step(
            "Load Configuration",
            self._load_config,
            config_path=config_path
        )

        self.add_step(
            "Load Scaffolds",
            self._load_scaffolds
        )

        self.add_step(
            "Process All Scaffolds",
            self._process_scaffolds
        )

        self.add_step(
            "Generate Report",
            self._generate_report
        )

        result = await self.execute({
            'config_path': config_path
        })

        return result

    async def _load_config(
        self,
        context: Dict,
        config_path: Path
    ) -> Dict:
        """Load batch configuration"""
        with open(config_path) as f:
            config = json.load(f)

        return config

    async def _load_scaffolds(self, context: Dict) -> List[Dict]:
        """Load all scaffolds from input directory"""
        config = context['step_0_result']
        input_dir = Path(config['input_dir'])

        scaffolds = []

        for file_path in input_dir.glob("*.md"):
            with open(file_path) as f:
                scaffolds.append({
                    'path': file_path,
                    'content': f.read()
                })

        return scaffolds

    async def _process_scaffolds(self, context: Dict) -> List[Dict]:
        """Process each scaffold"""
        config = context['step_0_result']
        scaffolds = context['step_1_result']

        results = []
        total = len(scaffolds)

        # Create scene generation workflow
        scene_workflow = SceneGenerationWorkflow(self.app)

        with self.app.ui.progress_bar(total=total, description="Processing scaffolds") as progress:
            for i, scaffold in enumerate(scaffolds):
                # Run scene generation
                result = await scene_workflow.run(
                    outline=scaffold['content'],
                    model=config['model'],
                    variants=config.get('variants', 5)
                )

                # Save best variant
                best = result.get_final_result()[0]

                output_path = Path(config['output_dir']) / scaffold['path'].name
                with open(output_path, 'w') as f:
                    f.write(best['text'])

                results.append({
                    'scaffold': scaffold['path'].name,
                    'output': output_path,
                    'score': best['score'],
                    'cost': result.total_cost
                })

                progress.update(i + 1)

        return results

    async def _generate_report(self, context: Dict) -> str:
        """Generate batch processing report"""
        results = context['step_2_result']

        total_cost = sum(r['cost'] for r in results)
        avg_score = sum(r['score'] for r in results) / len(results)

        report = f"""# Batch Processing Report

**Total Scaffolds**: {len(results)}
**Total Cost**: ${total_cost:.2f}
**Average Score**: {avg_score:.2f}

## Results

"""

        for result in results:
            report += f"""### {result['scaffold']}
- **Output**: {result['output']}
- **Score**: {result['score']:.2f}
- **Cost**: ${result['cost']:.2f}

"""

        return report
```

---

## Workflow Registry

```python
# factory/core/workflows/registry.py
from typing import Dict, Type

class WorkflowRegistry:
    """Registry of all available workflows"""

    _workflows: Dict[str, Type[Workflow]] = {}

    @classmethod
    def register(cls, name: str, workflow_class: Type[Workflow]):
        """Register a workflow"""
        cls._workflows[name] = workflow_class

    @classmethod
    def get(cls, name: str) -> Type[Workflow]:
        """Get workflow by name"""
        return cls._workflows.get(name)

    @classmethod
    def list_all(cls) -> List[str]:
        """List all registered workflows"""
        return list(cls._workflows.keys())

# Register workflows
WorkflowRegistry.register('scene_generation', SceneGenerationWorkflow)
WorkflowRegistry.register('scene_enhancement', SceneEnhancementWorkflow)
WorkflowRegistry.register('voice_testing', VoiceTestingWorkflow)
WorkflowRegistry.register('batch_processing', BatchProcessingWorkflow)
```

---

## File Structure

```
factory/core/workflows/
├── __init__.py
├── base.py                     # Base Workflow class
├── result.py                   # WorkflowResult
├── registry.py                 # WorkflowRegistry
├── scene_generation.py         # Scene generation workflow
├── scene_enhancement.py        # Scene enhancement workflow
├── voice_testing.py            # Voice testing workflow
├── batch_processing.py         # Batch processing workflow
├── canon_consistency.py        # Canon checking workflow
└── smart_scaffold.py           # Smart scaffold generation
```

---

## Success Criteria

Your implementation should enable:

1. ✅ Single command executes multi-step workflow
2. ✅ Progress tracking for all steps
3. ✅ Parallel execution where possible
4. ✅ Automatic cost calculation
5. ✅ Error recovery with graceful degradation
6. ✅ Workflow results are comprehensive and actionable
7. ✅ Easy to add new workflows
8. ✅ Workflows can be composed (workflow calls workflow)
9. ✅ Clear status updates during execution
10. ✅ Results saved to appropriate output directories

---

## Deliverables

1. **Base Workflow Infrastructure** - Workflow, WorkflowStep, WorkflowResult classes
2. **6 Pre-Built Workflows** - Scene generation, enhancement, voice testing, batch, canon, scaffold
3. **Workflow Registry** - Registration and discovery system
4. **Tests** - Unit and integration tests for each workflow
5. **Documentation** - Usage guide for each workflow
6. **Example Configs** - JSON configs for batch processing

---

## Questions? Clarifications Needed?

If any requirements are unclear, document your assumptions and proceed. Focus on creating robust, composable workflows that automate complex multi-step operations.
