from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import copy


# --------------------------------------------------
# COMPOSITION NODE
# --------------------------------------------------

@dataclass(slots=True)
class CompositionNode:
    """
    A node in the composition graph.
    Represents a transformation stage.
    """

    name: str
    engine: Any
    method: str
    params: Dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------
# COMPOSITION GRAPH
# --------------------------------------------------

class CompositionGraph:

    def __init__(self):
        self.nodes: List[CompositionNode] = []
        self.state: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []

    # -----------------------------
    # GRAPH BUILDING
    # -----------------------------

    def add_node(
        self,
        name: str,
        engine: Any,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ):
        """
        Adds processing step to graph.
        """

        self.nodes.append(
            CompositionNode(
                name=name,
                engine=engine,
                method=method,
                params=params or {}
            )
        )

    # -----------------------------
    # EXECUTION ENGINE
    # -----------------------------

    def run(self, input_data: Any) -> Any:
        """
        Executes full composition pipeline.
        """

        data = input_data

        for node in self.nodes:

            engine = node.engine
            method = getattr(engine, node.method)

            data = method(data, **node.params)

            self.state[node.name] = data

        self.history.append(copy.deepcopy(self.state))

        return data

    # -----------------------------
    # RESET
    # -----------------------------

    def clear(self):
        self.nodes.clear()
        self.state.clear()

    # -----------------------------
    # INTROSPECTION
    # -----------------------------

    def summary(self) -> List[str]:
        return [
            f"{n.name} -> {n.engine.__class__.__name__}.{n.method}"
            for n in self.nodes
        ]
        