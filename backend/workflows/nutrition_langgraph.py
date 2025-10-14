"""LangGraph workflow for nutrition estimation with iterative refinement and streaming."""

from typing import Literal, Optional, AsyncIterator, Dict, Any, TypedDict

from langgraph.graph import StateGraph, END

from agents.input_agent import InputAgent
from agents.input_critic import InputCritic
from config.nutrients import NUTRIENTS
from config.settings import settings


# LangGraph State Schema
class NutritionEstimationState(TypedDict, total=False):
    """State for nutrition estimation workflow."""

    # Input
    description: str
    max_iterations: int

    # Iteration tracking
    current_iteration: int
    feedback: Optional[str]

    # Estimator outputs
    estimates: Optional[Dict[str, float]]
    reasoning: Optional[str]
    confidence_level: Optional[str]
    assumptions: Optional[list[str]]

    # Verifier outputs
    approved: bool
    approval_percentage: int
    issues_found: Optional[list[Dict[str, Any]]]
    overall_feedback: Optional[str]

    # Final outputs
    final_estimates: Optional[Dict[str, float]]
    iterations_used: int


class NutritionEstimationWorkflow:
    """LangGraph-based workflow with WebSocket streaming support matching nutrition_workflow.py."""

    def __init__(self, approval_threshold: int = 80):
        """Initialize workflow.

        Args:
            approval_threshold: Minimum approval percentage to accept estimates (default: 80%)
        """
        self.estimator = InputAgent()
        self.verifier = InputCritic()
        self.approval_threshold = approval_threshold
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create LangGraph workflow for nutrition estimation.

        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(NutritionEstimationState)

        # Add nodes
        workflow.add_node("estimator", self.estimator)
        workflow.add_node("verifier", self.verifier)
        workflow.add_node("increment", self._increment_iteration)
        workflow.add_node("finalize", self._finalize_results)

        # Set entry point
        workflow.set_entry_point("increment")

        # Add edges
        workflow.add_edge("increment", "estimator")
        workflow.add_edge("estimator", "verifier")

        # Add conditional edge from verifier
        workflow.add_conditional_edges(
            "verifier",
            self._should_continue,
            {
                "estimator": "increment",
                "finalize": "finalize",
            },
        )

        # End after finalize
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def _increment_iteration(self, state: NutritionEstimationState) -> NutritionEstimationState:
        """Increment iteration counter."""
        current = state.get("current_iteration", 0)
        state["current_iteration"] = current + 1
        return state

    def _should_continue(self, state: NutritionEstimationState) -> Literal["estimator", "finalize"]:
        """Decide whether to continue iterating or finalize."""
        # Check if approved
        if state.get("approved", False):
            return "finalize"

        # Check approval percentage threshold
        approval_pct = state.get("approval_percentage", 0)
        if approval_pct >= self.approval_threshold:
            return "finalize"

        # Check iteration limit
        current_iteration = state.get("current_iteration", 0)
        max_iterations = state.get("max_iterations", settings.max_iterations)

        if current_iteration >= max_iterations:
            return "finalize"

        return "estimator"

    def _finalize_results(self, state: NutritionEstimationState) -> NutritionEstimationState:
        """Finalize the results and prepare final output."""
        state["final_estimates"] = state.get("estimates", {})
        state["iterations_used"] = state.get("current_iteration", 0)
        return state

    async def estimate_meal(
        self,
        description: str,
        websocket=None,
        max_iterations: int = 3,
    ) -> Dict:
        """Estimate nutrition for a meal with iterative refinement (matches nutrition_workflow.py).

        Args:
            description: Natural language meal description
            websocket: Optional WebSocket for streaming progress
            max_iterations: Maximum refinement iterations

        Returns:
            Dict containing final estimates and metadata
        """
        # Initialize state
        state: NutritionEstimationState = {
            "description": description,
            "max_iterations": max_iterations,
            "current_iteration": 0,
            "approved": False,
            "approval_percentage": 0,
        }

        # Notify start
        if websocket:
            await websocket.send_json({
                "type": "workflow_start",
                "description": description,
                "max_iterations": max_iterations,
            })

        # Stream through the graph
        async for event in self.graph.astream(state, stream_mode="updates"):
            for node_name, node_state in event.items():
                # After increment node
                if node_name == "increment":
                    iteration = node_state.get("current_iteration", 1)
                    if websocket:
                        await websocket.send_json({
                            "type": "iteration",
                            "iteration": iteration,
                            "max": max_iterations,
                        })

                # After estimator node
                elif node_name == "estimator":
                    iteration = node_state.get("current_iteration", 1)
                    if websocket:
                        await websocket.send_json({
                            "type": "status",
                            "status": "estimating",
                            "message": f"Analyzing meal (iteration {iteration})...",
                        })

                    estimates = node_state.get("estimates", {})

                    # Extract macros for display
                    macros = self._extract_macros(estimates)

                    if websocket:
                        await websocket.send_json({
                            "type": "estimates",
                            "macros": macros,
                            "confidence": node_state.get("confidence_level"),
                            "reasoning": node_state.get("reasoning"),
                            "full_count": len(estimates),
                        })

                # After verifier node
                elif node_name == "verifier":
                    if websocket:
                        await websocket.send_json({
                            "type": "status",
                            "status": "verifying",
                            "message": "Verifying accuracy...",
                        })

                    approval = node_state.get("approval_percentage", 0)
                    issues = node_state.get("issues_found", [])

                    if websocket:
                        await websocket.send_json({
                            "type": "verification",
                            "approval": approval,
                            "issues_count": len(issues),
                            "issues": issues[:3],  # Send top 3 issues
                        })

                    # Check if consensus reached
                    if node_state.get("approved") or approval >= self.approval_threshold:
                        iteration = node_state.get("current_iteration", 0)
                        if websocket:
                            await websocket.send_json({
                                "type": "consensus",
                                "message": f"Consensus reached! ({approval}% approval)",
                                "iterations": iteration,
                            })
                    elif websocket and node_state.get("current_iteration", 0) < max_iterations:
                        await websocket.send_json({
                            "type": "refining",
                            "message": f"Refining estimates based on feedback... ({approval}% approval)",
                        })

                # Update state reference
                state = node_state

        # Prepare final result
        estimates = state.get("estimates", {})
        macros = self._extract_macros(estimates)
        approval = state.get("approval_percentage", 0)
        iterations_used = state.get("current_iteration", 0)

        # Check if max iterations reached without consensus
        if iterations_used >= max_iterations and approval < self.approval_threshold:
            if websocket:
                await websocket.send_json({
                    "type": "max_iterations",
                    "message": f"Analysis complete ({approval}% approval)",
                    "iterations": max_iterations,
                })

            return {
                **macros,
                "estimates": estimates,
                "confidence": state.get("confidence_level"),
                "iterations": max_iterations,
                "approval": approval,
                "assumptions": state.get("assumptions", []),
                "warning": "Did not reach full consensus",
            }

        # Consensus reached
        return {
            **macros,
            "estimates": estimates,
            "confidence": state.get("confidence_level"),
            "iterations": iterations_used,
            "approval": approval,
            "assumptions": state.get("assumptions", []),
        }

    async def estimate_batch(self, descriptions: list[str], max_iterations: int = 3) -> list[Dict]:
        """Estimate nutrition for multiple meals.

        Args:
            descriptions: List of meal descriptions
            max_iterations: Max iterations per meal (lower for batch)

        Returns:
            List of estimate dicts
        """
        results = []
        for description in descriptions:
            result = await self.estimate_meal(
                description=description,
                max_iterations=max_iterations,
            )
            results.append(result)
        return results

    def _extract_macros(self, estimates: Dict[str, float]) -> Dict[str, float]:
        """Extract key macronutrients for display.

        Args:
            estimates: Full nutrient estimates dict

        Returns:
            Dict with calories, protein, carbs, fat
        """
        protein = estimates.get("Protein", 0)
        carbs = estimates.get("Carbohydrates", 0)
        fat = estimates.get("Total Fats", 0)

        # Calculate calories (4 cal/g protein, 4 cal/g carbs, 9 cal/g fat)
        calories = (protein * 4) + (carbs * 4) + (fat * 9)

        return {
            "calories": round(calories),
            "protein": round(protein, 1),
            "carbs": round(carbs, 1),
            "fat": round(fat, 1),
        }


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        workflow = NutritionEstimationWorkflow(approval_threshold=80)
        description = "Grilled salmon with quinoa and roasted vegetables"

        print(f"Estimating nutrition for: {description}\n")

        result = await workflow.estimate_meal(description, max_iterations=3)

        print(f"\n{'='*80}")
        print("FINAL RESULTS")
        print(f"{'='*80}")
        print(f"Iterations used: {result['iterations']}")
        print(f"Approval: {result['approval']}%")
        print(f"Confidence: {result.get('confidence', 'unknown')}")
        print(f"\nMacros:")
        print(f"  Calories: {result.get('calories', 0)}")
        print(f"  Protein: {result.get('protein', 0)}g")
        print(f"  Carbs: {result.get('carbs', 0)}g")
        print(f"  Fat: {result.get('fat', 0)}g")

    asyncio.run(main())
