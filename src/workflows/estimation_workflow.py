"""Simple estimation and verification workflow."""

from src.agents.input_agent import InputAgent
from src.agents.input_critic import InputCritic
from src.config.settings import settings


class EstimationWorkflow:
    """Workflow for estimating and verifying nutrition."""

    def __init__(self):
        self.estimator = InputAgent()
        self.critic = InputCritic()

    async def run(self, description: str, max_iterations: int = 5) -> dict:
        """Run estimation workflow.

        Args:
            description: Meal description
            max_iterations: Max negotiation rounds

        Returns:
            Final estimates dict
        """
        print(f"\nEstimating nutrition for: {description}\n")

        feedback = None
        estimates = None

        for iteration in range(1, max_iterations + 1):
            print(f"Iteration {iteration}/{max_iterations}")

            # Get estimates
            print("  Estimator working...")
            estimates = await self.estimator.estimate(description, feedback)
            print(f"  Got {len(estimates)} nutrient estimates")

            # Verify estimates
            print("  Critic verifying...")
            verification = await self.critic.verify(description, estimates)
            approval = verification["approval_percentage"]
            print(f"  Approval: {approval}%")

            # Check if approved
            if verification["approved"] or approval >= settings.approval_threshold:
                print(f"\nConsensus reached! ({approval}% approval)")
                return {
                    "estimates": estimates,
                    "iterations": iteration,
                    "approval": approval,
                }

            # Prepare feedback for next iteration
            feedback = verification["feedback"]
            print(f"  Feedback: {feedback}\n")

        # Max iterations reached
        print(f"\nMax iterations reached. Final approval: {approval}%")
        return {
            "estimates": estimates,
            "iterations": max_iterations,
            "approval": approval,
        }
