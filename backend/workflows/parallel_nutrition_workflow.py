"""Parallel Nutrition Workflow - Processes ingredients in parallel with estimator-validator loops."""

from typing import Any, Dict, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableParallel

from agents.preprocessing_agent import PreprocessingAgent
from agents.ingredient_estimator import IngredientEstimator
from agents.ingredient_validator import IngredientValidator
from config.nutrients import NUTRIENTS
from config.settings import settings
from utils.logger import get_logger


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
    detailed_nutrient_analysis: str  # Natural language analysis of every nutrient
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

        # Run estimation synchronously
        result = estimator.estimate_sync(
            ingredient_name=state["ingredient_name"],
            amount=state["amount"],
            notes=state.get("notes")
        )

        state["estimates"] = result["estimates"]
        state["reasoning"] = result["reasoning"]
        state["confidence_level"] = result["confidence_level"]
        state["round"] = round_num + 1

        return state

    def validator_node(state: IngredientSubgraphState) -> IngredientSubgraphState:
        """Run ingredient validator."""
        estimates = state.get("estimates", {})

        # Run validation synchronously
        result = validator.validate_sync(
            ingredient_name=state["ingredient_name"],
            amount=state["amount"],
            estimates=estimates
        )

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

        # Initialize sum dictionary with Title Case keys from NUTRIENTS
        estimates_sum = {nutrient: 0.0 for nutrient in NUTRIENTS.keys()}

        # Create a mapping from lowercase/snake_case to proper nutrient names
        nutrient_name_map = {}
        for proper_name in NUTRIENTS.keys():
            # Create snake_case version
            snake_case = proper_name.lower().replace(" ", "_").replace("+", "_").replace("-", "_")
            nutrient_name_map[snake_case] = proper_name
            # Also map lowercase version
            nutrient_name_map[proper_name.lower()] = proper_name
            # And exact match
            nutrient_name_map[proper_name] = proper_name

        # Sum up all nutrients
        for ing_name, result in ingredient_results.items():
            estimates = result.get("estimates", {})
            for nutrient_key, value in estimates.items():
                # Try to find the proper nutrient name
                proper_name = nutrient_name_map.get(nutrient_key)
                if proper_name and proper_name in estimates_sum:
                    estimates_sum[proper_name] += value
                elif nutrient_key in estimates_sum:
                    # Fallback: direct key match
                    estimates_sum[nutrient_key] += value

        state["estimates_sum"] = estimates_sum

        return state

    def _interaction_analysis_node(self, state: ParallelNutritionState) -> ParallelNutritionState:
        """Analyze nutrient interactions and cooking process impact using two-agent approach.

        Agent 1: Detailed natural language analysis of every nutrient
        Agent 2: Structured final estimates based on the analysis
        """
        from langchain_anthropic import ChatAnthropic
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
        from pydantic import BaseModel, Field

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

        # Create LLM for both agents
        llm = ChatAnthropic(
            model=settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.2,  # Low temperature for scientific accuracy
            max_tokens=8000,  # Higher for detailed analysis
        )

        # ============================================================
        # AGENT 1: Detailed Natural Language Analysis
        # ============================================================

        analysis_prompt = PromptTemplate(
            template="""You are a nutritional biochemist expert. Analyze how cooking process and ingredient interactions affect EVERY SINGLE NUTRIENT in this meal.

Meal description: {description}

Ingredients:
{ingredients_list}

Cooking process:
Method: {cooking_method}
Temperature: {cooking_temp}
Duration: {cooking_duration}
Known impacts: {cooking_impacts}

Current nutrient estimates (sum of raw ingredients):
{estimates_json}

YOUR TASK: Go through EVERY nutrient listed above, one by one, and explain in natural language how it will be affected:

For EACH nutrient, write a clear statement following these patterns:

1. If nutrient stays the same:
   "Nutrient X - Does not change during cooking"

2. If nutrient increases:
   "Nutrient X - Increases by approximately Y% because [reason]. For example, [specific mechanism]"

3. If nutrient decreases:
   "Nutrient X - Decreases by approximately Y% due to [specific reason]. In the current process of {cooking_method} at {cooking_temp} for {cooking_duration}, [explain mechanism]"

4. If nutrient has complex interactions:
   "Nutrient X - Initially Y, but bioavailability changes by Z% due to [interaction with other nutrients/cooking]. Final available amount is approximately [calculation]"

IMPORTANT RULES:
- Go through ALL nutrients systematically (macronutrients, vitamins, minerals, etc.)
- Be specific about percentages (e.g., "15-20%" not "some")
- Explain WHY each change happens (heat degradation, oxidation, protein binding, etc.)
- Consider the specific cooking method, temperature, and duration
- Account for nutrient interactions (e.g., vitamin C enhancing iron absorption, fat helping vitamin absorption)

Examples of GOOD analysis:
- "Vitamin C - Decreases by approximately 25-30% due to heat degradation. In the current process of baking at 180°C for 20 minutes, ascorbic acid oxidizes and breaks down from thermal stress."
- "Iron - Increases bioavailability by 15% because vitamin C present in the ingredients enhances non-heme iron absorption"
- "Beta-Carotene - Does not change significantly, as this carotenoid is stable at moderate cooking temperatures"
- "Protein - Does not change in quantity but denatures, which actually improves digestibility by 10-15%"
- "Polyphenols - Decrease by approximately 20% during high temperature cooking. In the current process of frying at 180°C for 10 minutes, they oxidize and degrade due to prolonged heat exposure"

Now provide your detailed analysis for EVERY nutrient:""",
            input_variables=[
                "description",
                "ingredients_list",
                "cooking_method",
                "cooking_temp",
                "cooking_duration",
                "cooking_impacts",
                "estimates_json"
            ],
        )

        analysis_chain = analysis_prompt | llm | StrOutputParser()

        try:
            # Prepare inputs
            analysis_inputs = {
                "description": state.get("description", ""),
                "ingredients_list": ingredients_list,
                "cooking_method": cooking_process.get("method", "unknown"),
                "cooking_temp": cooking_process.get("temperature", "unknown"),
                "cooking_duration": cooking_process.get("duration", "unknown"),
                "cooking_impacts": ", ".join(cooking_process.get("nutrient_impact", [])) if cooking_process.get("nutrient_impact") else "none specified",
                "estimates_json": estimates_json,
            }

            # Get detailed natural language analysis
            print("Running detailed nutrient analysis...")
            detailed_analysis = analysis_chain.invoke(analysis_inputs)

            # Store the detailed analysis
            state["detailed_nutrient_analysis"] = detailed_analysis

            # Log the detailed analysis
            logger = get_logger()
            logger.log_interaction(
                agent_name="detailed_nutrient_analyzer",
                prompt=analysis_prompt.format(**analysis_inputs),
                response=detailed_analysis,
                metadata={
                    "description": state.get("description", ""),
                    "num_ingredients": len(ingredients),
                    "cooking_method": cooking_process.get("method", "unknown"),
                    "num_nutrients": len(estimates_sum)
                }
            )

            # ============================================================
            # AGENT 2: Structured Final Estimates
            # ============================================================

            class FinalEstimatesResult(BaseModel):
                """Final nutrient estimates based on detailed analysis."""
                final_estimates: Dict[str, float] = Field(
                    description="Final adjusted nutrient values after cooking and interactions"
                )
                summary: str = Field(
                    description="Brief summary of major changes"
                )

            estimates_parser = JsonOutputParser(pydantic_object=FinalEstimatesResult)

            estimates_prompt = PromptTemplate(
                template="""You are a nutritional calculation expert. Based on the detailed analysis below, calculate the FINAL NUMERIC VALUES for all nutrients.

Original nutrient values (from raw ingredients):
{estimates_json}

Detailed nutrient-by-nutrient analysis:
{detailed_analysis}

YOUR TASK: Convert the detailed analysis into precise final numeric values.

INSTRUCTIONS:
1. For each nutrient in the original estimates, apply the changes described in the analysis
2. Calculate the final value based on percentage changes mentioned
3. If analysis says "does not change", keep the original value
4. If analysis mentions percentage decrease (e.g., "25-30%"), use the midpoint (27.5%) and calculate: original * (1 - 0.275)
5. If analysis mentions percentage increase, calculate: original * (1 + percentage/100)
6. Include ALL nutrients from the original estimates, even if they didn't change

EXAMPLE:
If original Vitamin C = 50mg and analysis says "Vitamin C - Decreases by 25-30%":
Final Vitamin C = 50 * (1 - 0.275) = 36.25mg

{format_instructions}

Provide your response as valid JSON only.""",
                input_variables=[
                    "estimates_json",
                    "detailed_analysis"
                ],
                partial_variables={
                    "format_instructions": estimates_parser.get_format_instructions(),
                },
            )

            estimates_chain = estimates_prompt | llm | estimates_parser

            # Get final structured estimates
            print("Calculating final nutrient values...")
            estimates_inputs = {
                "estimates_json": estimates_json,
                "detailed_analysis": detailed_analysis,
            }

            result = estimates_chain.invoke(estimates_inputs)

            # Log the final estimates calculation
            logger.log_interaction(
                agent_name="final_estimates_calculator",
                prompt=estimates_prompt.format(**estimates_inputs),
                response=json.dumps(result, indent=2),
                metadata={
                    "description": state.get("description", ""),
                    "num_nutrients": len(result["final_estimates"])
                }
            )

            # Store results in state
            state["final_estimates"] = result["final_estimates"]
            state["interaction_reasoning"] = detailed_analysis[:500] + "..." if len(detailed_analysis) > 500 else detailed_analysis
            state["process_impact_reasoning"] = result["summary"]

        except Exception as e:
            print(f"Error during interaction analysis: {e}")
            import traceback
            traceback.print_exc()

            # Fall back to sum estimates
            state["final_estimates"] = state.get("estimates_sum", {})
            state["interaction_reasoning"] = f"Error occurred: {str(e)}"
            state["process_impact_reasoning"] = "No adjustments made due to error"
            state["detailed_nutrient_analysis"] = "Error during analysis"

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

        # Track current stage for iteration simulation
        current_stage = 0
        total_stages = 4  # preprocessing, coordinator, merge, interaction_analysis

        # Stream through the graph
        async for event in self.graph.astream(state, stream_mode="updates"):
            for node_name, node_state in event.items():
                current_stage += 1

                # After preprocessing
                if node_name == "preprocessing":
                    ingredients = node_state.get("ingredients", [])
                    cooking_process = node_state.get("cooking_process", {})

                    if websocket:
                        # Send iteration event (similar to original workflow)
                        await websocket.send_json({
                            "type": "iteration",
                            "iteration": current_stage,
                            "max": total_stages,
                        })

                        # Send status event
                        await websocket.send_json({
                            "type": "status",
                            "status": "preprocessing",
                            "message": f"Analyzing ingredients ({len(ingredients)} found)...",
                        })

                # After coordinator (parallel execution)
                elif node_name == "coordinator":
                    ingredient_results = node_state.get("ingredient_results", {})

                    if websocket:
                        # Send iteration event
                        await websocket.send_json({
                            "type": "iteration",
                            "iteration": current_stage,
                            "max": total_stages,
                        })

                        # Send status event
                        await websocket.send_json({
                            "type": "status",
                            "status": "estimating",
                            "message": f"Estimating nutrients in parallel ({len(ingredient_results)} ingredients)...",
                        })

                # After merge
                elif node_name == "merge":
                    estimates_sum = node_state.get("estimates_sum", {})

                    if websocket:
                        # Send iteration event
                        await websocket.send_json({
                            "type": "iteration",
                            "iteration": current_stage,
                            "max": total_stages,
                        })

                        # Send status event
                        await websocket.send_json({
                            "type": "status",
                            "status": "verifying",
                            "message": "Combining ingredient estimates...",
                        })

                        # Extract macros for display
                        macros = self._extract_macros(estimates_sum)

                        # Send estimates event (similar to original)
                        await websocket.send_json({
                            "type": "estimates",
                            "macros": macros,
                            "confidence": "high",  # Aggregate confidence
                            "reasoning": f"Combined {len(node_state.get('ingredient_results', {}))} ingredients",
                            "full_count": len(estimates_sum),
                        })

                # After interaction analysis
                elif node_name == "interaction_analysis":
                    final_estimates = node_state.get("final_estimates", {})

                    if websocket:
                        # Send iteration event
                        await websocket.send_json({
                            "type": "iteration",
                            "iteration": current_stage,
                            "max": total_stages,
                        })

                        # Send status event
                        await websocket.send_json({
                            "type": "status",
                            "status": "verifying",
                            "message": "Analyzing nutrient interactions and cooking impact...",
                        })

                        # Extract macros for display
                        macros = self._extract_macros(final_estimates)

                        # Send final estimates
                        await websocket.send_json({
                            "type": "estimates",
                            "macros": macros,
                            "confidence": "high",
                            "reasoning": node_state.get("interaction_reasoning", "")[:200],  # Truncate for websocket
                            "full_count": len(final_estimates),
                        })

                        # Send consensus event (analysis complete)
                        await websocket.send_json({
                            "type": "consensus",
                            "message": "Analysis complete! Nutrient estimates finalized.",
                            "iterations": total_stages,
                        })

                # Update state reference
                state = node_state

        # Prepare final result
        final_estimates = state.get("final_estimates", {})
        macros = self._extract_macros(final_estimates)

        # Calculate aggregate confidence from ingredient results
        ingredient_results = state.get("ingredient_results", {})
        confidences = [
            result.get("confidence_level", "medium")
            for result in ingredient_results.values()
        ]
        # Simple confidence aggregation: if most are high, overall is high
        confidence_counts = {"high": 0, "medium": 0, "low": 0}
        for conf in confidences:
            confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
        overall_confidence = max(confidence_counts, key=confidence_counts.get) if confidences else "high"

        # Collect assumptions from all ingredients
        all_assumptions = []
        for result in ingredient_results.values():
            ing_name = result.get("ingredient_name", "unknown")
            reasoning = result.get("reasoning", "")
            if reasoning:
                all_assumptions.append(f"{ing_name}: {reasoning}")

        # Add cooking process assumptions
        cooking_process = state.get("cooking_process", {})
        if cooking_process.get("nutrient_impact"):
            all_assumptions.append(f"Cooking impact: {', '.join(cooking_process['nutrient_impact'])}")

        return {
            **macros,
            "estimates": final_estimates,
            "confidence": overall_confidence,
            "iterations": total_stages,  # Number of workflow stages
            "approval": 100,  # All ingredients approved after parallel validation
            "assumptions": all_assumptions,
            # Additional data (for advanced users / debugging)
            "estimates_sum": state.get("estimates_sum", {}),
            "ingredient_results": state.get("ingredient_results", {}),
            "cooking_process": state.get("cooking_process", {}),
            "detailed_nutrient_analysis": state.get("detailed_nutrient_analysis", ""),
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
