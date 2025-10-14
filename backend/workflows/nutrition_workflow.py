"""Comprehensive nutrition estimation workflow with iterative refinement."""

from typing import Dict, Optional

from agents.nutrition_estimator import NutritionEstimatorAgent
from agents.nutrition_verifier import NutritionVerifierAgent


class NutritionEstimationWorkflow:
    """
    Workflow that coordinates estimator and verifier agents to produce
    accurate nutritional estimates through iterative refinement.
    """

    def __init__(self, approval_threshold: int = 80):
        """
        Initialize workflow with agents.

        Args:
            approval_threshold: Minimum approval percentage to accept estimates (default: 80%)
        """
        self.estimator = NutritionEstimatorAgent()
        self.verifier = NutritionVerifierAgent()
        self.approval_threshold = approval_threshold

    async def estimate_meal(
        self,
        description: str,
        websocket=None,
        max_iterations: int = 3,
    ) -> Dict:
        """
        Estimate nutrition for a meal with iterative refinement.

        Args:
            description: Natural language meal description
            websocket: Optional WebSocket for streaming progress
            max_iterations: Maximum refinement iterations

        Returns:
            Dict containing final estimates and metadata
        """
        feedback = None
        estimates = None
        verification = None

        # Notify start
        if websocket:
            await websocket.send_json(
                {
                    "type": "workflow_start",
                    "description": description,
                    "max_iterations": max_iterations,
                }
            )

        for iteration in range(1, max_iterations + 1):
            # Send iteration update
            if websocket:
                await websocket.send_json(
                    {
                        "type": "iteration",
                        "iteration": iteration,
                        "max": max_iterations,
                    }
                )

            # Step 1: Estimator generates/refines estimates
            if websocket:
                await websocket.send_json(
                    {
                        "type": "status",
                        "status": "estimating",
                        "message": f"Analyzing meal (iteration {iteration})...",
                    }
                )

            estimates = await self.estimator.estimate(description, feedback)

            if "error" in estimates:
                if websocket:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "error": estimates["error"],
                        }
                    )
                return estimates

            # Extract macros for display
            macros = self.estimator.extract_macros(estimates.get("estimates", {}))

            if websocket:
                await websocket.send_json(
                    {
                        "type": "estimates",
                        "macros": macros,
                        "confidence": estimates.get("confidence_level"),
                        "reasoning": estimates.get("reasoning"),
                        "full_count": len(estimates.get("estimates", {})),
                    }
                )

            # Step 2: Verifier checks estimates
            if websocket:
                await websocket.send_json(
                    {
                        "type": "status",
                        "status": "verifying",
                        "message": "Verifying accuracy...",
                    }
                )

            verification = await self.verifier.verify(description, estimates)

            if "error" in verification:
                if websocket:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "error": verification["error"],
                        }
                    )
                # Return estimates even if verification failed
                return {
                    **macros,
                    "estimates": estimates.get("estimates", {}),
                    "confidence": estimates.get("confidence_level"),
                    "iterations": iteration,
                    "approval": 0,
                    "warning": "Verification failed",
                }

            approval = verification.get("approval_percentage", 0)
            issues = verification.get("issues_found", [])

            if websocket:
                await websocket.send_json(
                    {
                        "type": "verification",
                        "approval": approval,
                        "issues_count": len(issues),
                        "issues": issues[:3],  # Send top 3 issues
                    }
                )

            # Step 3: Check if consensus reached
            if verification.get("approved") or approval >= self.approval_threshold:
                if websocket:
                    await websocket.send_json(
                        {
                            "type": "consensus",
                            "message": f"Consensus reached! ({approval}% approval)",
                            "iterations": iteration,
                        }
                    )

                return {
                    **macros,
                    "estimates": estimates.get("estimates", {}),
                    "confidence": estimates.get("confidence_level"),
                    "iterations": iteration,
                    "approval": approval,
                    "assumptions": estimates.get("assumptions", []),
                }

            # Prepare feedback for next iteration
            feedback = verification.get("feedback")

            if websocket:
                await websocket.send_json(
                    {
                        "type": "refining",
                        "message": f"Refining estimates based on feedback... ({approval}% approval)",
                    }
                )

        # Max iterations reached - return best estimates
        if websocket:
            await websocket.send_json(
                {
                    "type": "max_iterations",
                    "message": f"Analysis complete ({approval}% approval)",
                    "iterations": max_iterations,
                }
            )

        return {
            **macros,
            "estimates": estimates.get("estimates", {}),
            "confidence": estimates.get("confidence_level"),
            "iterations": max_iterations,
            "approval": approval,
            "assumptions": estimates.get("assumptions", []),
            "warning": "Did not reach full consensus",
        }

    async def estimate_batch(self, descriptions: list[str], max_iterations: int = 3) -> list[Dict]:
        """
        Estimate nutrition for multiple meals.

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
