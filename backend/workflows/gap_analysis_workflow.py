"""Nutrient Gap Analysis Workflow - Analyzes daily nutrition gaps and suggests meals."""

from typing import Any, Dict, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config.nutrition_goals import NUTRITION_GOALS, get_priority_weight
from config.settings import settings
from utils.logger import get_logger


class GapAnalysisState(TypedDict, total=False):
    """State for the gap analysis workflow."""

    # Input
    meals: List[Dict[str, Any]]  # List of meals with detailed_nutrients

    # Aggregation outputs
    total_nutrients: Dict[str, float]  # Summed nutrients from all meals

    # Gap calculation outputs
    nutrient_gaps: List[Dict[str, Any]]  # List of gaps with priority scores
    top_gaps: List[Dict[str, Any]]  # Top 5 gaps for frontend

    # Meal suggestion outputs
    meal_suggestions: List[Dict[str, Any]]  # List of meal suggestions


class NutrientGap(BaseModel):
    """Model for a nutrient gap."""
    nutrient: str = Field(description="Nutrient name")
    current: float = Field(description="Current amount consumed")
    target: float = Field(description="Target daily amount")
    deficit: float = Field(description="Amount needed (target - current)")
    percentage: float = Field(description="Percentage of target achieved")
    priority: str = Field(description="Priority level: high, medium, or low")
    unit: str = Field(description="Unit of measurement")


class MealSuggestion(BaseModel):
    """Model for a meal suggestion."""
    meal: str = Field(description="Short meal title (max 8 words)")
    reasoning: str = Field(description="Brief reason why this meal helps (max 15 words)")


class GapPrioritizationResult(BaseModel):
    """Result of gap prioritization analysis."""
    important_gaps: List[str] = Field(description="List of most important nutrient names")
    nutrient_groupings: Dict[str, List[str]] = Field(
        description="Groups of nutrients found in similar foods"
    )
    reasoning: str = Field(description="Step-by-step reasoning for prioritization")


class MealSuggestionResult(BaseModel):
    """Result of meal suggestion analysis."""
    suggestions: List[MealSuggestion] = Field(
        description="List of 3-5 meal suggestions",
        min_items=3,
        max_items=5
    )


class GapAnalysisWorkflow:
    """Workflow that analyzes nutrient gaps and suggests meals."""

    def __init__(self):
        """Initialize workflow."""
        self.logger = get_logger()
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the gap analysis workflow graph.

        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(GapAnalysisState)

        # Add nodes
        workflow.add_node("aggregate_meals", self._aggregate_meals_node)
        workflow.add_node("calculate_gaps", self._calculate_gaps_node)
        workflow.add_node("prioritize_gaps", self._prioritize_gaps_node)
        workflow.add_node("suggest_meals", self._suggest_meals_node)

        # Set entry point
        workflow.set_entry_point("aggregate_meals")

        # Add edges
        workflow.add_edge("aggregate_meals", "calculate_gaps")
        workflow.add_edge("calculate_gaps", "prioritize_gaps")
        workflow.add_edge("prioritize_gaps", "suggest_meals")
        workflow.add_edge("suggest_meals", END)

        return workflow.compile()

    def _aggregate_meals_node(self, state: GapAnalysisState) -> GapAnalysisState:
        """Aggregate nutrients from all meals.

        Args:
            state: Current workflow state

        Returns:
            Updated state with total_nutrients
        """
        meals = state.get("meals", [])

        # Initialize totals
        total_nutrients: Dict[str, float] = {}

        # Sum up all nutrients from meals
        for meal in meals:
            detailed_nutrients = meal.get("detailed_nutrients", {})
            for nutrient_name, value in detailed_nutrients.items():
                if nutrient_name not in total_nutrients:
                    total_nutrients[nutrient_name] = 0.0
                total_nutrients[nutrient_name] += float(value)

        state["total_nutrients"] = total_nutrients

        self.logger.log_interaction(
            agent_name="aggregate_meals",
            prompt="Aggregate all meal nutrients",
            response=f"Aggregated {len(total_nutrients)} nutrients from {len(meals)} meals",
            metadata={"meal_count": len(meals), "nutrient_count": len(total_nutrients)}
        )

        return state

    def _calculate_gaps_node(self, state: GapAnalysisState) -> GapAnalysisState:
        """Calculate nutrient gaps compared to daily goals.

        Args:
            state: Current workflow state

        Returns:
            Updated state with nutrient_gaps and top_gaps
        """
        total_nutrients = state.get("total_nutrients", {})

        # Calculate gaps for all nutrients in goals
        gaps = []

        for nutrient_name, goal_data in NUTRITION_GOALS.items():
            target = goal_data.get("target", 0)
            unit = goal_data.get("unit", "")
            priority = goal_data.get("priority", "medium")

            # Get current amount (0 if not consumed)
            current = total_nutrients.get(nutrient_name, 0.0)

            # Calculate deficit and percentage
            deficit = max(0, target - current)
            percentage = (current / target * 100) if target > 0 else 100

            # Only include gaps below 100%
            if percentage < 100:
                priority_weight = get_priority_weight(nutrient_name)

                # Calculate importance score (lower percentage + higher priority = higher score)
                importance_score = (100 - percentage) * priority_weight

                gap = {
                    "nutrient": nutrient_name,
                    "current": round(current, 2),
                    "target": target,
                    "deficit": round(deficit, 2),
                    "percentage": round(percentage, 1),
                    "priority": priority,
                    "unit": unit,
                    "importance_score": importance_score,
                }
                gaps.append(gap)

        # Sort by importance score (descending)
        gaps.sort(key=lambda x: x["importance_score"], reverse=True)

        # Get top 5 gaps for frontend
        top_gaps = []
        for gap in gaps[:5]:
            # Format for TopNutrientGaps component
            # Map nutrient name to frontend ID format
            nutrient_id = gap["nutrient"].lower().replace(" ", "_").replace("+", "_").replace("-", "_")

            top_gaps.append({
                "id": nutrient_id,
                "name": gap["nutrient"],
                "current": gap["current"],
                "target": gap["target"],
                "deficit": gap["deficit"],
                "percentage": gap["percentage"],
                "unit": gap["unit"],
            })

        state["nutrient_gaps"] = gaps
        state["top_gaps"] = top_gaps

        self.logger.log_interaction(
            agent_name="calculate_gaps",
            prompt="Calculate nutrient gaps",
            response=f"Found {len(gaps)} nutrient gaps, top 5 selected",
            metadata={
                "total_gaps": len(gaps),
                "top_gap": gaps[0]["nutrient"] if gaps else "none"
            }
        )

        return state

    def _prioritize_gaps_node(self, state: GapAnalysisState) -> GapAnalysisState:
        """Use LLM to prioritize gaps and group nutrients by food sources.

        Args:
            state: Current workflow state

        Returns:
            Updated state with prioritization reasoning
        """
        gaps = state.get("nutrient_gaps", [])

        if not gaps:
            # No gaps to prioritize
            return state

        # Create LLM chain for gap prioritization
        llm = ChatAnthropic(
            model=settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.3,
            max_tokens=2048,
        )

        parser = JsonOutputParser(pydantic_object=GapPrioritizationResult)

        prompt = PromptTemplate(
            template="""You are a nutrition expert analyzing daily nutrient gaps.

Current nutrient gaps (sorted by importance):
{gaps_json}

Your task:
1. Identify the MOST IMPORTANT gaps to address:
   - Prioritize essential nutrients (vitamins, minerals, essential fatty acids)
   - High-priority deficiencies (marked as "high" priority)
   - Large percentage deficiencies (below 50% of target)
   - Less important: polyphenols, non-essential compounds

2. Group nutrients that are commonly found in similar foods:
   - Example: "Vitamin D, Omega-3, Calcium" -> Found in fatty fish, fortified dairy
   - Example: "Vitamin C, Fiber, Potassium" -> Found in fruits and vegetables
   - Example: "Iron, Zinc, B12" -> Found in red meat, legumes
   - Try to maximize coverage of multiple deficiencies with single food groups

3. Explain your step-by-step reasoning

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["gaps_json"],
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | llm | parser

        # Prepare gaps summary (top 15 for analysis)
        gaps_summary = []
        for gap in gaps[:15]:
            gaps_summary.append({
                "nutrient": gap["nutrient"],
                "current": gap["current"],
                "target": gap["target"],
                "percentage": gap["percentage"],
                "priority": gap["priority"],
                "deficit": gap["deficit"],
                "unit": gap["unit"],
            })

        import json
        gaps_json = json.dumps(gaps_summary, indent=2)

        try:
            prompt_inputs = {"gaps_json": gaps_json}
            prompt_text = prompt.format(**prompt_inputs)

            result = chain.invoke(prompt_inputs)

            # Store prioritization results in state for meal suggestion
            state["gap_prioritization"] = result

            self.logger.log_interaction(
                agent_name="prioritize_gaps",
                prompt=prompt_text,
                response=json.dumps(result, indent=2),
                metadata={
                    "gaps_analyzed": len(gaps_summary),
                    "important_gaps_count": len(result.get("important_gaps", [])),
                }
            )

        except Exception as e:
            print(f"Error during gap prioritization: {e}")
            # Continue without prioritization
            state["gap_prioritization"] = {
                "important_gaps": [gap["nutrient"] for gap in gaps[:5]],
                "nutrient_groupings": {},
                "reasoning": f"Error occurred: {str(e)}"
            }

        return state

    def _suggest_meals_node(self, state: GapAnalysisState) -> GapAnalysisState:
        """Generate meal suggestions based on prioritized gaps.

        Args:
            state: Current workflow state

        Returns:
            Updated state with meal_suggestions
        """
        gaps = state.get("nutrient_gaps", [])
        prioritization = state.get("gap_prioritization", {})
        total_nutrients = state.get("total_nutrients", {})

        if not gaps:
            # No gaps, no suggestions needed
            state["meal_suggestions"] = []
            return state

        # Create LLM chain for meal suggestions
        llm = ChatAnthropic(
            model=settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.5,  # Slightly higher for creative meal ideas
            max_tokens=1024,
        )

        parser = JsonOutputParser(pydantic_object=MealSuggestionResult)

        prompt = PromptTemplate(
            template="""You are a nutrition expert suggesting meals to fill nutrient gaps.

Important nutrient gaps to address:
{important_gaps}

Nutrient groupings (nutrients found in similar foods):
{nutrient_groupings}

Current nutrient status (top 10 deficiencies):
{top_deficiencies}

Your task:
Generate 3-5 meal suggestions that:
1. Address the most important nutrient gaps (essential nutrients, vitamins, minerals)
2. Cover multiple deficiencies with single meals when possible
3. Are practical and realistic meal options
4. Focus on whole foods and common ingredients

For each meal suggestion:
- meal: Short, specific meal title (max 8 words). Example: "Salmon with quinoa and broccoli"
- reasoning: Brief explanation of key nutrients covered (max 15 words). Example: "High in omega-3, vitamin D, and fiber"

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["important_gaps", "nutrient_groupings", "top_deficiencies"],
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | llm | parser

        # Prepare inputs
        important_gaps = prioritization.get("important_gaps", [])
        nutrient_groupings = prioritization.get("nutrient_groupings", {})

        # Format important gaps
        important_gaps_text = "\n".join([f"- {gap}" for gap in important_gaps[:10]])

        # Format nutrient groupings
        groupings_text = "\n".join([
            f"- {group_name}: {', '.join(nutrients)}"
            for group_name, nutrients in nutrient_groupings.items()
        ]) if nutrient_groupings else "No groupings available"

        # Format top deficiencies
        deficiencies_text = "\n".join([
            f"- {gap['nutrient']}: {gap['percentage']:.1f}% of target ({gap['current']}/{gap['target']} {gap['unit']})"
            for gap in gaps[:10]
        ])

        import json

        try:
            prompt_inputs = {
                "important_gaps": important_gaps_text,
                "nutrient_groupings": groupings_text,
                "top_deficiencies": deficiencies_text,
            }
            prompt_text = prompt.format(**prompt_inputs)

            result = chain.invoke(prompt_inputs)

            # Format suggestions for frontend
            suggestions = []
            for suggestion in result.get("suggestions", [])[:5]:
                suggestions.append({
                    "meal": suggestion.get("meal", ""),
                    "reasoning": suggestion.get("reasoning", ""),
                })

            state["meal_suggestions"] = suggestions

            self.logger.log_interaction(
                agent_name="suggest_meals",
                prompt=prompt_text,
                response=json.dumps(result, indent=2),
                metadata={
                    "suggestions_count": len(suggestions),
                    "gaps_addressed": len(important_gaps),
                }
            )

        except Exception as e:
            print(f"Error during meal suggestion: {e}")
            # Provide fallback suggestions
            state["meal_suggestions"] = [
                {
                    "meal": "Mixed berry smoothie with spinach",
                    "reasoning": "High in vitamins, antioxidants, and fiber",
                },
                {
                    "meal": "Salmon with quinoa and vegetables",
                    "reasoning": "Rich in omega-3, protein, and essential minerals",
                },
                {
                    "meal": "Lentil soup with whole grain bread",
                    "reasoning": "Excellent source of fiber, iron, and B vitamins",
                },
            ]

        return state

    async def analyze_gaps(
        self,
        meals: List[Dict[str, Any]],
        websocket=None,
    ) -> Dict:
        """Analyze nutrient gaps and generate meal suggestions.

        Args:
            meals: List of meals with detailed_nutrients
            websocket: Optional WebSocket for streaming progress

        Returns:
            Dict containing gap analysis results
        """
        # Initialize state
        state: GapAnalysisState = {
            "meals": meals,
        }

        # Notify start
        if websocket:
            await websocket.send_json({
                "type": "gap_analysis_start",
                "meal_count": len(meals),
            })

        # Stream through the graph
        async for event in self.graph.astream(state, stream_mode="updates"):
            for node_name, node_state in event.items():
                # Send progress updates
                if websocket:
                    if node_name == "aggregate_meals":
                        await websocket.send_json({
                            "type": "gap_analysis_status",
                            "status": "aggregating",
                            "message": f"Aggregating nutrients from {len(meals)} meals...",
                        })
                    elif node_name == "calculate_gaps":
                        gaps_count = len(node_state.get("nutrient_gaps", []))
                        await websocket.send_json({
                            "type": "gap_analysis_status",
                            "status": "calculating",
                            "message": f"Found {gaps_count} nutrient gaps...",
                        })
                    elif node_name == "prioritize_gaps":
                        await websocket.send_json({
                            "type": "gap_analysis_status",
                            "status": "prioritizing",
                            "message": "Prioritizing important gaps...",
                        })
                    elif node_name == "suggest_meals":
                        suggestions_count = len(node_state.get("meal_suggestions", []))
                        await websocket.send_json({
                            "type": "gap_analysis_status",
                            "status": "suggesting",
                            "message": f"Generated {suggestions_count} meal suggestions...",
                        })

                # Update state reference
                state = node_state

        # Prepare final result
        return {
            "total_nutrients": state.get("total_nutrients", {}),
            "nutrient_gaps": state.get("nutrient_gaps", []),
            "top_gaps": state.get("top_gaps", []),
            "meal_suggestions": state.get("meal_suggestions", []),
            "gap_prioritization": state.get("gap_prioritization", {}),
        }


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        workflow = GapAnalysisWorkflow()

        # Sample meals
        meals = [
            {
                "description": "Oatmeal with berries",
                "detailed_nutrients": {
                    "Protein": 12,
                    "Carbohydrates": 68,
                    "Total Fats": 14,
                    "Fiber": 8,
                    "Vitamin C": 15,
                    "Iron": 2,
                },
            },
            {
                "description": "Chicken salad",
                "detailed_nutrients": {
                    "Protein": 42,
                    "Carbohydrates": 45,
                    "Total Fats": 22,
                    "Fiber": 6,
                    "Vitamin A": 500,
                    "Calcium": 150,
                },
            },
        ]

        print(f"Analyzing gaps for {len(meals)} meals...\n")

        result = await workflow.analyze_gaps(meals)

        print(f"\n{'='*80}")
        print("GAP ANALYSIS RESULTS")
        print(f"{'='*80}")
        print(f"\nTop 5 Nutrient Gaps:")
        for gap in result.get("top_gaps", []):
            print(f"  {gap['name']}: {gap['percentage']:.1f}% ({gap['current']}/{gap['target']} {gap['unit']})")

        print(f"\nMeal Suggestions:")
        for i, suggestion in enumerate(result.get("meal_suggestions", []), 1):
            print(f"  {i}. {suggestion['meal']}")
            print(f"     → {suggestion['reasoning']}")

    asyncio.run(main())
