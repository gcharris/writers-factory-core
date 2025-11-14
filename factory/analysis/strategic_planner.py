"""Strategic Planner - Sprint 13 Task 13-05.

Generate actionable rewrite plan from analysis results.

Creates:
- Prioritized action items
- Estimated effort per fix
- Dependencies between fixes
- Suggested implementation order
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class ActionItem:
    """Action item in rewrite plan.

    Attributes:
        item_id: Unique identifier
        priority: P0, P1, P2, P3
        type: Type of fix (plot_hole, low_quality_scene, etc.)
        description: What needs to be fixed
        location: Where to fix it (scene ID, chapter, etc.)
        specific_fixes: Detailed fix suggestions
        effort_estimate: Hours to implement
        status: pending, in_progress, completed
        dependencies: Other items this depends on
    """
    item_id: str
    priority: str
    type: str
    description: str
    location: str
    specific_fixes: List[Dict] = None
    effort_estimate: float = 0.0
    status: str = "pending"
    dependencies: List[str] = None

    def __post_init__(self):
        """Initialize mutable defaults."""
        if self.specific_fixes is None:
            self.specific_fixes = []
        if self.dependencies is None:
            self.dependencies = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class StrategicPlanner:
    """Generate strategic rewrite plan from analysis results.

    Takes comprehensive analysis data and creates a prioritized,
    actionable plan for improving the manuscript.
    """

    def __init__(self):
        """Initialize strategic planner."""
        self.action_items = []

    def generate_plan(
        self,
        analysis_results: Dict[str, Any],
        manuscript_chunks: List[Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive rewrite plan.

        Args:
            analysis_results: Results from AnalysisPipeline
            manuscript_chunks: List of ManuscriptChunk objects

        Returns:
            Strategic rewrite plan with action items and estimates
        """
        logger.info("Generating strategic rewrite plan")

        # Generate overview
        overview = self._generate_overview(analysis_results)

        # Generate action items
        action_items = self._generate_action_items(analysis_results, manuscript_chunks)

        # Determine implementation order
        implementation_order = self._determine_order(action_items)

        # Estimate effort
        effort_estimate = self._estimate_effort(action_items)

        # Estimate expected improvement
        expected_improvement = self._estimate_improvement(analysis_results, action_items)

        plan = {
            "manuscript_id": analysis_results.get("manuscript_id"),
            "overview": overview,
            "action_items": [item.to_dict() for item in action_items],
            "implementation_order": implementation_order,
            "effort_estimate": effort_estimate,
            "expected_improvement": expected_improvement,
            "summary": self._generate_summary(analysis_results, action_items)
        }

        logger.info(f"Generated plan with {len(action_items)} action items")

        return plan

    def _generate_overview(self, results: Dict) -> str:
        """Generate plan overview.

        Args:
            results: Analysis results

        Returns:
            Overview text
        """
        scene_stats = results.get("scene_scores", {}).get("statistics", {})
        priority_matrix = results.get("priority_matrix", {})

        priority_counts = {
            "P0": len(priority_matrix.get("P0", [])),
            "P1": len(priority_matrix.get("P1", [])),
            "P2": len(priority_matrix.get("P2", [])),
            "P3": len(priority_matrix.get("P3", []))
        }

        total_scenes = scene_stats.get("total_scenes", 0)
        avg_score = scene_stats.get("average", 0)
        gold_count = scene_stats.get("gold_standard", 0)
        needs_work = scene_stats.get("needs_work", 0)

        overview = f"""
Manuscript Analysis Overview:

Current State:
• Total Scenes: {total_scenes}
• Average Scene Score: {avg_score:.1f}/100
• Gold Standard Scenes: {gold_count} ({gold_count/max(total_scenes,1)*100:.1f}%)
• Needs Significant Work: {needs_work} ({needs_work/max(total_scenes,1)*100:.1f}%)

Priority Issues:
• P0 (Critical - Must Fix): {priority_counts['P0']} issues
• P1 (Important - Should Fix): {priority_counts['P1']} issues
• P2 (Recommended): {priority_counts['P2']} issues
• P3 (Optional Polish): {priority_counts['P3']} issues

Total Issues to Address: {sum(priority_counts.values())}
        """

        return overview.strip()

    def _generate_action_items(
        self,
        results: Dict,
        chunks: List[Any]
    ) -> List[ActionItem]:
        """Generate specific action items.

        Args:
            results: Analysis results
            chunks: Manuscript chunks

        Returns:
            List of ActionItem objects
        """
        items = []
        item_counter = 0

        # Process priority matrix
        priority_matrix = results.get("priority_matrix", {})

        for priority_level in ["P0", "P1", "P2", "P3"]:
            for issue in priority_matrix.get(priority_level, []):
                # Find corresponding chunk for location context
                chunk_id = issue.get("location", "")
                chunk_context = self._get_chunk_context(chunk_id, chunks)

                action_item = ActionItem(
                    item_id=f"action-{item_counter}",
                    priority=priority_level,
                    type=issue.get("type", "unknown"),
                    description=issue.get("description", ""),
                    location=chunk_context,
                    specific_fixes=issue.get("fixes", []),
                    effort_estimate=self._estimate_item_effort(issue),
                    status="pending"
                )

                items.append(action_item)
                item_counter += 1

        return items

    def _get_chunk_context(self, chunk_id: str, chunks: List[Any]) -> str:
        """Get human-readable context for chunk.

        Args:
            chunk_id: Chunk identifier
            chunks: List of chunks

        Returns:
            Context string (e.g., "Act 1, Chapter 3, Scene 2")
        """
        for chunk in chunks:
            if chunk.chunk_id == chunk_id:
                metadata = chunk.metadata
                return f"{metadata.get('act', 'Act')} > {metadata.get('chapter', 'Chapter')} > {metadata.get('scene_title', chunk_id)}"

        return chunk_id

    def _estimate_item_effort(self, issue: Dict) -> float:
        """Estimate effort for fixing an issue.

        Args:
            issue: Issue description

        Returns:
            Estimated hours
        """
        issue_type = issue.get("type", "")

        # Effort estimates by type
        effort_map = {
            "plot_hole": 4.0,  # 4 hours - requires rewriting
            "low_quality_scene": 3.0,  # 3 hours - major revision
            "needs_improvement": 2.0,  # 2 hours - moderate revision
            "pacing_issue": 1.5,  # 1.5 hours - restructuring
            "polish_needed": 1.0,  # 1 hour - light polish
            "metaphor_improvement": 0.5,  # 30 min - quick fixes
            "unknown": 1.0
        }

        base_effort = effort_map.get(issue_type, 1.0)

        # Adjust based on severity
        severity = issue.get("severity", "medium")
        if severity == "high":
            base_effort *= 1.5
        elif severity == "low":
            base_effort *= 0.7

        # Adjust based on number of specific fixes
        fixes = issue.get("fixes", [])
        if fixes:
            base_effort += len(fixes) * 0.1  # 6 minutes per fix

        return round(base_effort, 1)

    def _determine_order(self, items: List[ActionItem]) -> List[str]:
        """Determine implementation order for fixes.

        Args:
            items: List of action items

        Returns:
            List of item IDs in recommended order
        """
        # Order by priority, then by type
        # Priority order: P0 -> P1 -> P2 -> P3
        # Within priority, fix plot holes first, then low quality, etc.

        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        type_order = {
            "plot_hole": 0,
            "low_quality_scene": 1,
            "needs_improvement": 2,
            "pacing_issue": 3,
            "polish_needed": 4,
            "metaphor_improvement": 5
        }

        # Sort items
        sorted_items = sorted(
            items,
            key=lambda x: (
                priority_order.get(x.priority, 99),
                type_order.get(x.type, 99),
                x.effort_estimate  # Shorter tasks first within same type
            )
        )

        return [item.item_id for item in sorted_items]

    def _estimate_effort(self, items: List[ActionItem]) -> Dict[str, Any]:
        """Estimate total effort for plan.

        Args:
            items: List of action items

        Returns:
            Effort breakdown
        """
        total_hours = sum(item.effort_estimate for item in items)

        # Break down by priority
        by_priority = {}
        for priority in ["P0", "P1", "P2", "P3"]:
            priority_items = [item for item in items if item.priority == priority]
            by_priority[priority] = {
                "count": len(priority_items),
                "hours": sum(item.effort_estimate for item in priority_items)
            }

        # Estimate timeline
        # Assuming 4 hours of focused revision per day
        hours_per_day = 4
        total_days = total_hours / hours_per_day

        # Critical path (P0 + P1 must be done)
        critical_hours = by_priority.get("P0", {}).get("hours", 0) + by_priority.get("P1", {}).get("hours", 0)
        critical_days = critical_hours / hours_per_day

        return {
            "total_hours": round(total_hours, 1),
            "total_days": round(total_days, 1),
            "critical_path_hours": round(critical_hours, 1),
            "critical_path_days": round(critical_days, 1),
            "by_priority": by_priority,
            "hours_per_day_assumed": hours_per_day
        }

    def _estimate_improvement(
        self,
        results: Dict,
        items: List[ActionItem]
    ) -> Dict[str, Any]:
        """Estimate expected improvement from fixes.

        Args:
            results: Analysis results
            items: Action items

        Returns:
            Improvement estimates
        """
        current_avg = results.get("scene_scores", {}).get("statistics", {}).get("average", 0)

        # Estimate improvement per priority level
        improvement_map = {
            "P0": 15,  # Critical fixes add 15 points average
            "P1": 8,   # Important fixes add 8 points average
            "P2": 4,   # Recommended fixes add 4 points average
            "P3": 2    # Optional fixes add 2 points average
        }

        # Calculate weighted improvement
        total_scenes = results.get("scene_scores", {}).get("statistics", {}).get("total_scenes", 1)
        weighted_improvement = 0

        for priority, improvement in improvement_map.items():
            priority_items = [item for item in items if item.priority == priority]
            scenes_affected = len(priority_items)
            weighted_improvement += (scenes_affected / max(total_scenes, 1)) * improvement

        projected_avg = min(current_avg + weighted_improvement, 100)

        # Estimate tier improvements
        current_gold = results.get("scene_scores", {}).get("statistics", {}).get("gold_standard", 0)
        current_needs_work = results.get("scene_scores", {}).get("statistics", {}).get("needs_work", 0)

        # Assume fixing P0/P1 items moves scenes up one tier
        p0_p1_fixes = len([item for item in items if item.priority in ["P0", "P1"]])
        projected_gold = current_gold + int(p0_p1_fixes * 0.3)  # 30% of fixes reach gold
        projected_needs_work = max(0, current_needs_work - p0_p1_fixes)

        return {
            "current_average": round(current_avg, 1),
            "projected_average": round(projected_avg, 1),
            "improvement_points": round(weighted_improvement, 1),
            "current_gold_standard": current_gold,
            "projected_gold_standard": projected_gold,
            "current_needs_work": current_needs_work,
            "projected_needs_work": projected_needs_work
        }

    def _generate_summary(
        self,
        results: Dict,
        items: List[ActionItem]
    ) -> str:
        """Generate executive summary.

        Args:
            results: Analysis results
            items: Action items

        Returns:
            Summary text
        """
        effort = self._estimate_effort(items)
        improvement = self._estimate_improvement(results, items)

        p0_count = len([i for i in items if i.priority == "P0"])
        p1_count = len([i for i in items if i.priority == "P1"])

        summary = f"""
Strategic Rewrite Plan Summary:

Current Manuscript Quality: {improvement['current_average']:.1f}/100
Projected Quality (After Fixes): {improvement['projected_average']:.1f}/100
Expected Improvement: +{improvement['improvement_points']:.1f} points

Critical Issues (Must Fix): {p0_count}
Important Issues (Should Fix): {p1_count}
Total Action Items: {len(items)}

Estimated Effort:
• Critical Path: {effort['critical_path_hours']} hours ({effort['critical_path_days']:.1f} days)
• Full Plan: {effort['total_hours']} hours ({effort['total_days']:.1f} days)
• Assuming {effort['hours_per_day_assumed']} hours/day of focused revision

Recommendation: Start with P0 issues (plot holes and low-quality scenes) to establish
a solid foundation, then proceed to P1 issues for major improvements. P2 and P3 can
be addressed in subsequent polishing passes.
        """

        return summary.strip()
