"""Knowledge Graph Construction - Sprint 13 Task 13-03.

Build interactive knowledge graph from extracted entities.

Provides:
- Visual exploration of entities and relationships
- Query interface for finding connections
- Export formats (JSON, GraphML, etc.)
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class GraphNode:
    """Node in knowledge graph.

    Attributes:
        node_id: Unique node identifier
        node_type: Type (character, location, motif, theme, event)
        name: Node name
        attributes: Node-specific attributes
        metadata: Additional metadata
    """
    node_id: str
    node_type: str
    name: str
    attributes: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class GraphEdge:
    """Edge in knowledge graph.

    Attributes:
        edge_id: Unique edge identifier
        edge_type: Type (relationship, timeline, causality, reference)
        source_id: Source node ID
        target_id: Target node ID
        attributes: Edge-specific attributes
        weight: Edge weight (strength of connection)
    """
    edge_id: str
    edge_type: str
    source_id: str
    target_id: str
    attributes: Dict[str, Any]
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class NovelKnowledgeGraph:
    """Knowledge graph for novel universe.

    Represents all entities (characters, locations, events) and their
    relationships in an interactive graph structure.
    """

    def __init__(self, manuscript_id: str):
        """Initialize knowledge graph.

        Args:
            manuscript_id: Unique manuscript identifier
        """
        self.manuscript_id = manuscript_id
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.node_counter = 0
        self.edge_counter = 0

    def add_node(
        self,
        node_type: str,
        name: str,
        attributes: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """Add node to graph.

        Args:
            node_type: Type of node
            name: Node name
            attributes: Node attributes
            metadata: Node metadata

        Returns:
            Node ID
        """
        node_id = f"{node_type}-{self.node_counter}"
        self.node_counter += 1

        node = GraphNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            attributes=attributes or {},
            metadata=metadata or {}
        )

        self.nodes[node_id] = node
        logger.debug(f"Added node: {node_id} ({name})")
        return node_id

    def add_edge(
        self,
        edge_type: str,
        source_id: str,
        target_id: str,
        attributes: Optional[Dict] = None,
        weight: float = 1.0
    ) -> str:
        """Add edge to graph.

        Args:
            edge_type: Type of edge
            source_id: Source node ID
            target_id: Target node ID
            attributes: Edge attributes
            weight: Edge weight

        Returns:
            Edge ID
        """
        # Validate nodes exist
        if source_id not in self.nodes:
            logger.warning(f"Source node {source_id} not found")
            return ""

        if target_id not in self.nodes:
            logger.warning(f"Target node {target_id} not found")
            return ""

        edge_id = f"{edge_type}-{self.edge_counter}"
        self.edge_counter += 1

        edge = GraphEdge(
            edge_id=edge_id,
            edge_type=edge_type,
            source_id=source_id,
            target_id=target_id,
            attributes=attributes or {},
            weight=weight
        )

        self.edges[edge_id] = edge
        logger.debug(f"Added edge: {source_id} -> {target_id} ({edge_type})")
        return edge_id

    def populate_from_entities(
        self,
        characters: List[Any],
        locations: List[Any],
        plot_threads: List[Any],
        motifs: List[Any]
    ) -> None:
        """Populate graph from extracted entities.

        Args:
            characters: List of Character objects
            locations: List of Location objects
            plot_threads: List of PlotThread objects
            motifs: List of Motif objects
        """
        logger.info("Populating knowledge graph from extracted entities")

        # Add character nodes
        character_ids = {}
        for char in characters:
            node_id = self.add_node(
                node_type="character",
                name=char.name,
                attributes={
                    "aliases": char.aliases,
                    "traits": char.traits,
                    "psychology": char.psychology,
                    "arc_notes": char.arc_notes
                },
                metadata={
                    "first_appearance": char.first_appearance,
                    "appearances": char.appearances,
                    "appearance_count": len(char.appearances)
                }
            )
            character_ids[char.name] = node_id

        # Add location nodes
        location_ids = {}
        for loc in locations:
            node_id = self.add_node(
                node_type="location",
                name=loc.name,
                attributes={
                    "type": loc.type,
                    "description": loc.description,
                    "sub_locations": loc.sub_locations
                },
                metadata={
                    "first_appearance": loc.first_appearance,
                    "appearances": loc.appearances,
                    "parent_location": loc.parent_location
                }
            )
            location_ids[loc.name] = node_id

        # Add plot thread nodes
        thread_ids = {}
        for thread in plot_threads:
            node_id = self.add_node(
                node_type="plot_thread",
                name=thread.name,
                attributes={
                    "type": thread.type,
                    "status": thread.status,
                    "resolution": thread.resolution
                },
                metadata={
                    "first_mention": thread.first_mention,
                    "mentions": thread.mentions,
                    "mention_count": len(thread.mentions)
                }
            )
            thread_ids[thread.thread_id] = node_id

        # Add motif nodes
        motif_ids = {}
        for motif in motifs:
            node_id = self.add_node(
                node_type="motif",
                name=motif.name,
                attributes={
                    "type": motif.type,
                    "pattern": motif.pattern,
                    "significance": motif.significance,
                    "examples": motif.examples
                },
                metadata={
                    "frequency": motif.frequency,
                    "appearances": motif.appearances
                }
            )
            motif_ids[motif.motif_id] = node_id

        # Add relationship edges (character-to-character)
        for char in characters:
            source_id = character_ids.get(char.name)
            if not source_id:
                continue

            for related_char, rel_type in char.relationships.items():
                target_id = character_ids.get(related_char)
                if target_id:
                    self.add_edge(
                        edge_type="relationship",
                        source_id=source_id,
                        target_id=target_id,
                        attributes={"type": rel_type},
                        weight=1.0
                    )

        # Add co-location edges (characters appearing in same location)
        self._add_colocation_edges(characters, locations, character_ids, location_ids)

        # Add plot participation edges (characters in plot threads)
        self._add_plot_participation_edges(characters, plot_threads, character_ids, thread_ids)

        logger.info(f"Graph populated: {len(self.nodes)} nodes, {len(self.edges)} edges")

    def _add_colocation_edges(
        self,
        characters: List[Any],
        locations: List[Any],
        character_ids: Dict[str, str],
        location_ids: Dict[str, str]
    ):
        """Add edges for characters appearing in locations.

        Args:
            characters: Character entities
            locations: Location entities
            character_ids: Character name to node ID mapping
            location_ids: Location name to node ID mapping
        """
        # For each location, find characters that appear in same chunks
        for loc in locations:
            loc_id = location_ids.get(loc.name)
            if not loc_id:
                continue

            # Find characters appearing in this location
            for char in characters:
                char_id = character_ids.get(char.name)
                if not char_id:
                    continue

                # Check if character and location share any appearances
                shared_appearances = set(char.appearances) & set(loc.appearances)
                if shared_appearances:
                    self.add_edge(
                        edge_type="appears_at",
                        source_id=char_id,
                        target_id=loc_id,
                        attributes={"shared_scenes": list(shared_appearances)},
                        weight=len(shared_appearances) / max(len(char.appearances), 1)
                    )

    def _add_plot_participation_edges(
        self,
        characters: List[Any],
        plot_threads: List[Any],
        character_ids: Dict[str, str],
        thread_ids: Dict[str, str]
    ):
        """Add edges for characters participating in plot threads.

        Args:
            characters: Character entities
            plot_threads: Plot thread entities
            character_ids: Character name to node ID mapping
            thread_ids: Thread ID to node ID mapping
        """
        # For each plot thread, find participating characters
        for thread in plot_threads:
            thread_node_id = thread_ids.get(thread.thread_id)
            if not thread_node_id:
                continue

            # Find characters whose appearances overlap with thread mentions
            for char in characters:
                char_id = character_ids.get(char.name)
                if not char_id:
                    continue

                # Check overlap
                shared_mentions = set(char.appearances) & set(thread.mentions)
                if shared_mentions:
                    self.add_edge(
                        edge_type="participates_in",
                        source_id=char_id,
                        target_id=thread_node_id,
                        attributes={"shared_scenes": list(shared_mentions)},
                        weight=len(shared_mentions) / max(len(thread.mentions), 1)
                    )

    def query_connections(
        self,
        node_id: str,
        max_depth: int = 2
    ) -> Dict[str, Any]:
        """Query connections from a node.

        Args:
            node_id: Starting node ID
            max_depth: Maximum depth to traverse

        Returns:
            Dictionary of connected nodes and paths
        """
        if node_id not in self.nodes:
            return {"error": "Node not found"}

        visited = set()
        connections = {
            "node": self.nodes[node_id].to_dict(),
            "direct_connections": [],
            "indirect_connections": []
        }

        # Find direct connections
        for edge in self.edges.values():
            if edge.source_id == node_id:
                target = self.nodes.get(edge.target_id)
                if target:
                    connections["direct_connections"].append({
                        "node": target.to_dict(),
                        "edge": edge.to_dict()
                    })
                    visited.add(edge.target_id)
            elif edge.target_id == node_id:
                source = self.nodes.get(edge.source_id)
                if source:
                    connections["direct_connections"].append({
                        "node": source.to_dict(),
                        "edge": edge.to_dict()
                    })
                    visited.add(edge.source_id)

        # Find indirect connections if max_depth > 1
        if max_depth > 1:
            for connected_node in connections["direct_connections"]:
                connected_id = connected_node["node"]["node_id"]
                indirect = self.query_connections(connected_id, max_depth=1)

                for indirect_conn in indirect.get("direct_connections", []):
                    indirect_node_id = indirect_conn["node"]["node_id"]
                    if indirect_node_id not in visited and indirect_node_id != node_id:
                        connections["indirect_connections"].append(indirect_conn)
                        visited.add(indirect_node_id)

        return connections

    def export_json(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Export graph to JSON format.

        Args:
            output_path: Optional path to save JSON file

        Returns:
            Graph data as dictionary
        """
        graph_data = {
            "manuscript_id": self.manuscript_id,
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()],
            "statistics": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "node_types": self._count_node_types(),
                "edge_types": self._count_edge_types()
            }
        }

        if output_path:
            output_path.write_text(json.dumps(graph_data, indent=2))
            logger.info(f"Graph exported to {output_path}")

        return graph_data

    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type.

        Returns:
            Dictionary of node type counts
        """
        counts = {}
        for node in self.nodes.values():
            counts[node.node_type] = counts.get(node.node_type, 0) + 1
        return counts

    def _count_edge_types(self) -> Dict[str, int]:
        """Count edges by type.

        Returns:
            Dictionary of edge type counts
        """
        counts = {}
        for edge in self.edges.values():
            counts[edge.edge_type] = counts.get(edge.edge_type, 0) + 1
        return counts

    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics.

        Returns:
            Dictionary of graph statistics
        """
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": self._count_node_types(),
            "edge_types": self._count_edge_types(),
            "avg_connections_per_node": len(self.edges) / max(len(self.nodes), 1)
        }
