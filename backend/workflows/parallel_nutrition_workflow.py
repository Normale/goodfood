"""Parallel Nutrition Workflow - Processes ingredients in parallel with estimator-validator loops."""

from typing import Any, Dict, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableParallel

from agents.preprocessing_agent import PreprocessingAgent
from agents.ingredient_estimator import IngredientEstimator
from agents.ingredient_validator import IngredientValidator
from config.nutrients import NUTRIENTS
from config.settings import settings


# State schemas
class IngredientSubgraphState(TypedDict, total=False):
    """State for individual ingredient estimation subgraph (estimator ↔ validator loop)."""

    ingredient_name: str
    amount: str
    notes: Optional[str]
    round: int
    max_rounds: int

    # Estimator outputs
    estimates: Optional[Dict[str, float]]
    reasoning: Optional[str]
    confidence_level: Optional[str]

    # Validator outputs
    approved: bool
    feedback: Optional[str]
    issues_found: int


class ParallelNutritionState(TypedDict, total=False):
    """State for the main parallel nutrition workflow."""

    # Input
    description: str
    max_rounds: int  # Max rounds per ingredient in estimator-validator loop

    # Preprocessing outputs
    ingredients: List[Dict[str, Any]]  # List of {name, amount, notes}
    cooking_process: Dict[str, Any]
    meal_category: str
    preprocessing_reasoning: str

    # Coordinator outputs (after parallel execution)
    ingredient_results: Dict[str, Dict[str, Any]]  # Key: ingredient name, Value: full results

    # Merge outputs
    estimates_sum: Dict[str, float]  # Summed nutrients from all ingredients

    # Final analysis outputs
    final_estimates: Dict[str, float]  # After accounting for interactions and cooking process
    interaction_reasoning: str
    process_impact_reasoning: str


def create_ingredient_subgraph(
    estimator: IngredientEstimator,
    validator: IngredientValidator,
    max_rounds: int = 3
):
    """Create a subgraph for estimating and validating a single ingredient.

    This creates an estimator ↔ validator loop similar to the joke ↔ jury example.

    Args:
        estimator: Ingredient estimator agent
        validator: Ingredient validator agent
        max_rounds: Maximum rounds of estimation-validation loop

    Returns:
        Compiled StateGraph for single ingredient processing
    """
    graph = StateGraph(IngredientSubgraphState)

    def estimator_node(state: IngredientSubgraphState) -> IngredientSubgraphState:
        """Run ingredient estimator."""
        round_num = state.get("round", 0)

        # If max rounds reached, just return current state
        if round_num >= max_rounds:
            state["approved"] = True  # Force approval to exit loop
            return state

        # Run estimation
        import asyncio
        result = asyncio.run(estimator.estimate(
            ingredient_name=state["ingredient_name"],
            amount=state["amount"],
            notes=state.get("notes")
        ))

        state["estimates"] = result["estimates"]
        state["reasoning"] = result["reasoning"]
        state["confidence_level"] = result["confidence_level"]
        state["round"] = round_num + 1

        return state

    def validator_node(state: IngredientSubgraphState) -> IngredientSubgraphState:
        """Run ingredient validator."""
        estimates = state.get("estimates", {})

        # Run validation
        import asyncio
        result = asyncio.run(validator.validate(
            ingredient_name=state["ingredient_name"],
            amount=state["amount"],
            estimates=estimates
        ))

        state["approved"] = result["approved"]
        state["feedback"] = result.get("feedback")
        state["issues_found"] = result.get("issues_found", 0)

        return state

    # Add nodes
    graph.add_node("estimator", estimator_node)
    graph.add_node("validator", validator_node)

    # Set entry point
    graph.set_entry_point("estimator")

    # Add edges: estimator → validator → (estimator or END)
    graph.add_edge("estimator", "validator")
    graph.add_conditional_edges(
        "validator",
        lambda s: "END" if s.get("approved", False) else "estimator",
        {
            "estimator": "estimator",
            "END": END,
        },
    )

    return graph.compile()


class ParallelNutritionWorkflow:
    """Workflow that processes ingredients in parallel with individual estimator-validator loops."""

    def __init__(self, max_rounds_per_ingredient: int = 3):
        """Initialize workflow.

        Args:
            max_rounds_per_ingredient: Max rounds for each ingredient's estimator-validator loop
        """
        self.preprocessing_agent = PreprocessingAgent()
        self.ingredient_estimator = IngredientEstimator()
        self.ingredient_validator = IngredientValidator()
        self.max_rounds = max_rounds_per_ingredient
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the main workflow graph.

        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(ParallelNutritionState)

        # Add nodes
        workflow.add_node("preprocessing", self.preprocessing_agent)
        workflow.add_node("coordinator", self._coordinator_node)
        workflow.add_node("merge", self._merge_node)
        workflow.add_node("interaction_analysis", self._interaction_analysis_node)

        # Set entry point
        workflow.set_entry_point("preprocessing")

        # Add edges
        workflow.add_edge("preprocessing", "coordinator")
        workflow.add_edge("coordinator", "merge")
        workflow.add_edge("merge", "interaction_analysis")
        workflow.add_edge("interaction_analysis", END)

        return workflow.compile()

    def _coordinator_node(self, state: ParallelNutritionState) -> ParallelNutritionState:
        """Coordinator node that spawns parallel ingredient subgraphs.

        This is similar to the runners_node in the parallel example.
        """
        ingredients = state.get("ingredients", [])

        if not ingredients:
            # No ingredients to process
            state["ingredient_results"] = {}
            return state

        # Create a subgraph for each ingredient
        subgraphs = {}
        for ing in ingredients:
            ing_name = ing["name"]
            # Create compiled subgraph for this ingredient
            subgraph = create_ingredient_subgraph(
                self.ingredient_estimator,
                self.ingredient_validator,
                max_rounds=self.max_rounds
            )

            # Wrap the subgraph invocation in a lambda that captures the ingredient data
            def make_runner(ingredient_data):
                def runner(input_state):
                    # Initialize state for this ingredient's subgraph
                    ing_state: IngredientSubgraphState = {
                        "ingredient_name": ingredient_data["name"],
                        "amount": ingredient_data["amount"],
                        "notes": ingredient_data.get("notes"),
                        "round": 0,
                        "max_rounds": self.max_rounds,
                        "approved": False,
                    }
                    # Run the subgraph
                    result = subgraph.invoke(ing_state)
                    return result
                return runner

            subgraphs[ing_name] = make_runner(ing)

        # Run all subgraphs in parallel
        parallel = RunnableParallel(**subgraphs)
        results = parallel.invoke({})

        # Store results in state
        state["ingredient_results"] = results

        return state

    def _merge_node(self, state: ParallelNutritionState) -> ParallelNutritionState:
        """Merge node that sums up nutrients from all ingredients."""
        ingredient_results = state.get("ingredient_results", {})

        # Initialize sum dictionary
        estimates_sum = {nutrient: 0.0 for nutrient in NUTRIENTS.keys()}

        # Sum up all nutrients
        for ing_name, result in ingredient_results.items():
            estimates = result.get("estimates", {})
            for nutrient, value in estimates.items():
                if nutrient in estimates_sum:
                    estimates_sum[nutrient] += value

        state["estimates_sum"] = estimates_sum

        return state

    def _interaction_analysis_node(self, state: ParallelNutritionState) -> ParallelNutritionState:
        """Analyze nutrient interactions and cooking process impact.

        This node uses an LLM to:
        1. Identify which nutrients have interactions with other ingredients
        2. Account for cooking process impact (e.g., vitamin loss from baking)
        3. Produce final adjusted estimates
        """
        from langchain_anthropic import ChatAnthropic
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import JsonOutputParser
        from pydantic import BaseModel, Field

        class InteractionAnalysisResult(BaseModel):
            """Result of interaction and cooking process analysis."""
            final_estimates: Dict[str, float] = Field(description="Final adjusted nutrient estimates")
            interaction_reasoning: str = Field(description="Explanation of nutrient interactions")
            process_impact_reasoning: str = Field(description="Explanation of cooking process impact")

        llm = ChatAnthropic(
            model=settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.3,
        )

        parser = JsonOutputParser(pydantic_object=InteractionAnalysisResult)

        prompt = PromptTemplate(
            template="""You are a nutritional biochemist expert. Analyze nutrient interactions and cooking process impacts.

Meal description: {description}

Ingredients:
{ingredients_list}

Cooking process:
Method: {cooking_method}
Temperature: {cooking_temp}
Duration: {cooking_duration}
Known impacts: {cooking_impacts}

Current nutrient estimates (sum of all ingredients):
{estimates_json}

Your task (use chain of thought reasoning):
1. Identify nutrient interactions between ingredients:
   - Vitamin absorption enhanced/inhibited by other nutrients
   - Mineral bioavailability changes
   - Protein/amino acid combinations
   - Fat-soluble vitamin absorption

2. Account for cooking process impacts:
   - Heat-sensitive vitamins (C, B vitamins) - losses
   - Fat content changes (absorbed oil, rendered fat)
   - Protein denaturation effects
   - Mineral retention/loss

3. Calculate final adjusted estimates for ALL nutrients

4. Explain your reasoning step by step

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=[
                "description",
                "ingredients_list",
                "cooking_method",
                "cooking_temp",
                "cooking_duration",
                "cooking_impacts",
                "estimates_json"
            ],
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | llm | parser

        # Prepare inputs
        ingredients = state.get("ingredients", [])
        ingredients_list = "\n".join([
            f"- {ing['name']}: {ing['amount']}" + (f" ({ing.get('notes')})" if ing.get("notes") else "")
            for ing in ingredients
        ])

        cooking_process = state.get("cooking_process", {})
        estimates_sum = state.get("estimates_sum", {})

        import json
        estimates_json = json.dumps(estimates_sum, indent=2)

        try:
            # Invoke the chain
            result = chain.invoke({
                "description": state.get("description", ""),
                "ingredients_list": ingredients_list,
                "cooking_method": cooking_process.get("method", "unknown"),
                "cooking_temp": cooking_process.get("temperature", "unknown"),
                "cooking_duration": cooking_process.get("duration", "unknown"),
                "cooking_impacts": ", ".join(cooking_process.get("nutrient_impact", [])),
                "estimates_json": estimates_json,
            })

            state["final_estimates"] = result["final_estimates"]
            state["interaction_reasoning"] = result["interaction_reasoning"]
            state["process_impact_reasoning"] = result["process_impact_reasoning"]

        except Exception as e:
            print(f"Error during interaction analysis: {e}")
            # Fall back to sum estimates
            state["final_estimates"] = state.get("estimates_sum", {})
            state["interaction_reasoning"] = f"Error occurred: {str(e)}"
            state["process_impact_reasoning"] = "No adjustments made due to error"

        return state

    async def estimate_meal(
        self,
        description: str,
        websocket=None,
        max_rounds_per_ingredient: int = 3,
    ) -> Dict:
        """Estimate nutrition for a meal using parallel ingredient processing.

        Args:
            description: Natural language meal description
            websocket: Optional WebSocket for streaming progress
            max_rounds_per_ingredient: Max rounds for each ingredient's validation loop

        Returns:
            Dict containing final estimates and metadata
        """
        # Initialize state
        state: ParallelNutritionState = {
            "description": description,
            "max_rounds": max_rounds_per_ingredient,
        }

        # Notify start
        if websocket:
            await websocket.send_json({
                "type": "workflow_start",
                "description": description,
                "stage": "preprocessing",
            })

        # Stream through the graph
        async for event in self.graph.astream(state, stream_mode="updates"):
            for node_name, node_state in event.items():
                # After preprocessing
                if node_name == "preprocessing":
                    ingredients = node_state.get("ingredients", [])
                    cooking_process = node_state.get("cooking_process", {})

                    if websocket:
                        await websocket.send_json({
                            "type": "preprocessing_complete",
                            "ingredients_count": len(ingredients),
                            "cooking_method": cooking_process.get("method", "unknown"),
                            "meal_category": node_state.get("meal_category", "unknown"),
                        })

                # After coordinator (parallel execution)
                elif node_name == "coordinator":
                    ingredient_results = node_state.get("ingredient_results", {})

                    if websocket:
                        await websocket.send_json({
                            "type": "parallel_estimation_complete",
                            "ingredients_processed": len(ingredient_results),
                        })

                # After merge
                elif node_name == "merge":
                    estimates_sum = node_state.get("estimates_sum", {})

                    if websocket:
                        # Extract macros for display
                        macros = self._extract_macros(estimates_sum)
                        await websocket.send_json({
                            "type": "merge_complete",
                            "macros": macros,
                        })

                # After interaction analysis
                elif node_name == "interaction_analysis":
                    final_estimates = node_state.get("final_estimates", {})

                    if websocket:
                        # Extract macros for display
                        macros = self._extract_macros(final_estimates)
                        await websocket.send_json({
                            "type": "final_analysis_complete",
                            "macros": macros,
                        })

                # Update state reference
                state = node_state

        # Prepare final result
        final_estimates = state.get("final_estimates", {})
        macros = self._extract_macros(final_estimates)

        return {
            **macros,
            "estimates": final_estimates,
            "estimates_sum": state.get("estimates_sum", {}),
            "ingredient_results": state.get("ingredient_results", {}),
            "cooking_process": state.get("cooking_process", {}),
            "interaction_reasoning": state.get("interaction_reasoning", ""),
            "process_impact_reasoning": state.get("process_impact_reasoning", ""),
        }

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
        workflow = ParallelNutritionWorkflow(max_rounds_per_ingredient=3)
        description = "Pancakes"

        print(f"Estimating nutrition for: {description}\n")

        result = await workflow.estimate_meal(description, max_rounds_per_ingredient=3)

        print(f"\n{'='*80}")
        print("FINAL RESULTS")
        print(f"{'='*80}")
        print(f"\nMacros:")
        print(f"  Calories: {result.get('calories', 0)}")
        print(f"  Protein: {result.get('protein', 0)}g")
        print(f"  Carbs: {result.get('carbs', 0)}g")
        print(f"  Fat: {result.get('fat', 0)}g")
        print(f"\nInteraction Analysis:")
        print(f"  {result.get('interaction_reasoning', 'N/A')}")
        print(f"\nCooking Process Impact:")
        print(f"  {result.get('process_impact_reasoning', 'N/A')}")

    asyncio.run(main())
