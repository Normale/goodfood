import anthropic
import json
from typing import Dict, List, Any
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

# Initialize Anthropic client and Rich console
client = anthropic.Anthropic()
console = Console()

NUTRIENTS_LIST = """
### MACRONUTRIENTS
- Carbohydrates (g)
- Protein (g)
- Total Fats (g)
- Alpha-linolenic acid (g)
- Linoleic acid (g)
- EPA+DHA (mg)
- Soluble Fiber (g)
- Insoluble Fiber (g)
- Water (ml)

### VITAMINS
- Vitamin C (mg)
- Vitamin B1 Thiamine (mg)
- Vitamin B2 Riboflavin (mg)
- Vitamin B3 Niacin (mg)
- Vitamin B5 Pantothenic acid (mg)
- Vitamin B6 Pyridoxine (mg)
- Vitamin B7 Biotin (mcg)
- Vitamin B9 Folate (mcg DFE)
- Vitamin B12 (mcg)
- Vitamin A (mcg RAE)
- Vitamin D (mcg)
- Vitamin E (mg)
- Vitamin K (mcg)

### MINERALS
- Calcium (mg)
- Phosphorus (mg)
- Magnesium (mg)
- Potassium (mg)
- Sodium (mg)
- Chloride (mg)
- Iron (mg)
- Zinc (mg)
- Copper (mcg)
- Selenium (mcg)
- Manganese (mg)
- Iodine (mcg)
- Chromium (mcg)
- Molybdenum (mcg)

### ESSENTIAL AMINO ACIDS
- Leucine (g)
- Lysine (g)
- Valine (g)
- Isoleucine (g)
- Threonine (g)
- Methionine (g)
- Phenylalanine (g)
- Histidine (g)
- Tryptophan (g)

### BENEFICIAL COMPOUNDS
- Choline (mg)
- Taurine (mg)
- CoQ10 (mg)
- Alpha-lipoic acid (mg)
- Beta-glucan (g)
- Resistant starch (g)

### PHYTONUTRIENTS
- Beta-carotene (mg)
- Lycopene (mg)
- Lutein (mg)
- Zeaxanthin (mg)
- Total polyphenols (mg)
- Quercetin (mg)
- Sulforaphane (mg)
- Allicin (mg)
- Curcumin (mg)
"""


class NutritionEstimatorAgent:
    """Agent that estimates nutritional values from ingredients"""

    def __init__(self):
        self.role = "Nutritional Estimator"

    def estimate(self, ingredients: List[str], feedback: str = None) -> Dict[str, Any]:
        """Estimate nutritional values for given ingredients"""

        prompt = f"""You are a nutritional expert tasked with estimating the nutritional content of a dish.

Ingredients:
{json.dumps(ingredients, indent=2)}

{f"Previous feedback from verifier: {feedback}" if feedback else ""}

Analyze these ingredients and provide a detailed estimate of ALL the following nutrients:
{NUTRIENTS_LIST}

Instructions:
1. Consider typical serving sizes and preparation methods
2. Account for nutrient interactions (e.g., cooking reduces some vitamins)
3. Be specific about quantities - estimate the total amount in the dish
4. For nutrients that are trace/negligible, still provide a number (can be 0 or very small)
5. If you revised estimates based on feedback, explain what you changed and why

Respond ONLY with valid JSON in this format:
{{
    "estimates": {{
        "Carbohydrates (g)": <number>,
        "Protein (g)": <number>,
        ... (all nutrients)
    }},
    "reasoning": "Brief explanation of your estimation approach and any changes made",
    "confidence_level": "high/medium/low",
    "assumptions": ["assumption 1", "assumption 2", ...]
}}"""

        # Display outgoing message
        feedback_display = feedback if feedback else "None - Initial estimation"
        console.print(
            Panel(
                f"[bold cyan]Analyzing ingredients...[/bold cyan]\n\n"
                f"Ingredients: {', '.join(ingredients)}\n\n"
                f"[dim]Feedback from verifier:[/dim]\n{feedback_display}",
                title="[bold cyan]🧪 ESTIMATOR → API[/bold cyan]",
                border_style="cyan",
            )
        )

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            # Display incoming response
            estimates_preview = json.dumps(result.get("estimates", {}), indent=2)
            console.print(
                Panel(
                    f"[bold cyan]Confidence: {result.get('confidence_level', 'unknown')}[/bold cyan]\n\n"
                    f"[bold]Reasoning:[/bold]\n{result.get('reasoning', 'N/A')}\n\n"
                    f"[bold]Assumptions:[/bold]\n"
                    + "\n".join(f"  • {a}" for a in result.get("assumptions", []))
                    + "\n\n"
                    f"[bold]Estimates ({len(result.get('estimates', {}))} nutrients):[/bold]\n"
                    f"[dim]{estimates_preview[:500]}{'...' if len(estimates_preview) > 500 else ''}[/dim]",
                    title="[bold cyan]🧪 API → ESTIMATOR[/bold cyan]",
                    border_style="cyan",
                )
            )

            return result
        except:
            console.print(
                Panel(
                    f"[bold red]Failed to parse response[/bold red]",
                    title="[bold red]🧪 ESTIMATOR ERROR[/bold red]",
                    border_style="red",
                )
            )
            return {"error": "Failed to parse response", "raw": response_text}


class NutritionVerifierAgent:
    """Agent that verifies and challenges nutritional estimates"""

    def __init__(self):
        self.role = "Nutritional Verifier"

    def verify(
        self, ingredients: List[str], estimates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify estimates and provide detailed feedback"""

        prompt = f"""You are a nutritional fact-checker. Your job is to verify estimates and provide feedback.

Ingredients:
{json.dumps(ingredients, indent=2)}

Estimates to verify:
{json.dumps(estimates, indent=2)}

Your task:
1. Check each nutrient estimate for accuracy based on the ingredients
2. Identify specific values that seem significantly off
3. Consider:
   - Typical nutrient profiles of each ingredient
   - Realistic portion sizes
   - Bioavailability and cooking losses
   - Nutrient interactions
4. Be specific about what's wrong and what the values should be closer to
5. **IMPORTANT: Accept estimates that are within ±20-25% of expected values as correct**
6. Only flag issues when values are significantly off (more than 25% deviation)
7. Be reasonable and not overly critical - small variations are acceptable

Respond ONLY with valid JSON in this format:
{{
    "approved": true/false,
    "issues_found": [
        {{
            "nutrient": "Vitamin C (mg)",
            "estimated_value": 45,
            "issue": "Too low - oranges alone provide ~70mg per fruit",
            "suggested_value": 85,
            "severity": "high/medium/low"
        }}
    ],
    "overall_feedback": "Summary of main issues (or confirmation if estimates look good)",
    "approval_percentage": <0-100, percentage of estimates that seem correct>
}}"""

        # Display outgoing message
        estimates_sample = dict(list(estimates.get("estimates", {}).items())[:5])
        console.print(
            Panel(
                f"[bold magenta]Verifying estimates...[/bold magenta]\n\n"
                f"Checking {len(estimates.get('estimates', {}))} nutrients\n"
                f"Acceptance range: ±20-25%\n\n"
                f"[dim]Sample of estimates being verified:[/dim]\n"
                f"[dim]{json.dumps(estimates_sample, indent=2)}...[/dim]",
                title="[bold magenta]🔍 VERIFIER → API[/bold magenta]",
                border_style="magenta",
            )
        )

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        try:
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            # Display incoming response
            approval_pct = result.get("approval_percentage", 0)
            issues_found = result.get("issues_found", [])
            issues_count = len(issues_found)

            status_color = (
                "green"
                if approval_pct >= 80
                else "yellow"
                if approval_pct >= 60
                else "red"
            )

            issues_text = ""
            if issues_found:
                issues_text = "\n\n[bold]Issues found:[/bold]\n"
                for idx, issue in enumerate(issues_found[:8], 1):
                    severity_color = (
                        "red"
                        if issue.get("severity") == "high"
                        else "yellow"
                        if issue.get("severity") == "medium"
                        else "blue"
                    )
                    issues_text += f"[{severity_color}]{idx}. {issue['nutrient']}:[/{severity_color}] {issue['issue']}\n"
                    issues_text += f"   Estimated: {issue.get('estimated_value')}, Suggested: {issue.get('suggested_value')}\n"

            console.print(
                Panel(
                    f"[bold {status_color}]Approval: {approval_pct}%[/bold {status_color}]\n"
                    f"Issues found: {issues_count}\n\n"
                    f"[bold]Overall Feedback:[/bold]\n{result.get('overall_feedback', 'N/A')}"
                    f"{issues_text}",
                    title=f"[bold magenta]🔍 API → VERIFIER[/bold magenta]",
                    border_style="magenta",
                )
            )

            return result
        except:
            console.print(
                Panel(
                    f"[bold red]Failed to parse response[/bold red]",
                    title="[bold red]🔍 VERIFIER ERROR[/bold red]",
                    border_style="red",
                )
            )
            return {"error": "Failed to parse response", "raw": response_text}


def estimate_dish_nutrition(
    ingredients: List[str], max_iterations: int = 5, approval_threshold: int = 80
):
    """
    Main function that coordinates both agents to estimate nutrition

    Args:
        ingredients: List of ingredients with quantities
        max_iterations: Maximum number of estimation rounds
        approval_threshold: Percentage of estimates that must be approved to stop (default: 80%)

    Returns:
        Final agreed-upon nutritional estimates
    """
    estimator = NutritionEstimatorAgent()
    verifier = NutritionVerifierAgent()

    console.print(
        Panel(
            f"[bold yellow]Starting nutritional estimation[/bold yellow]\n\n"
            f"Ingredients: {', '.join(ingredients)}\n"
            f"Max iterations: {max_iterations}\n"
            f"Approval threshold: {approval_threshold}%",
            title="[bold yellow]🔬 PIPELINE START[/bold yellow]",
            border_style="yellow",
        )
    )

    feedback = None

    for iteration in range(1, max_iterations + 1):
        console.print(f"\n[bold white]{'=' * 80}[/bold white]")
        console.print(
            f"[bold white]ITERATION {iteration}/{max_iterations}[/bold white]"
        )
        console.print(f"[bold white]{'=' * 80}[/bold white]\n")

        # Estimator makes/revises estimates
        estimates = estimator.estimate(ingredients, feedback)

        if "error" in estimates:
            console.print(
                Panel(
                    f"[bold red]Estimator error: {estimates['error']}[/bold red]",
                    border_style="red",
                )
            )
            continue

        # Verifier checks estimates
        verification = verifier.verify(ingredients, estimates)

        if "error" in verification:
            console.print(
                Panel(
                    f"[bold red]Verifier error: {verification['error']}[/bold red]",
                    border_style="red",
                )
            )
            continue

        approval_pct = verification.get("approval_percentage", 0)
        issues_found = verification.get("issues_found", [])

        # Display ALL nutrients from current estimates
        console.print(
            f"\n[bold green]📊 ALL CURRENT ESTIMATES ({len(estimates.get('estimates', {}))} nutrients):[/bold green]"
        )
        all_estimates = estimates.get("estimates", {})

        # Group nutrients by category for better readability
        macro_nutrients = [
            "Carbohydrates (g)",
            "Protein (g)",
            "Total Fats (g)",
            "Alpha-linolenic acid (g)",
            "Linoleic acid (g)",
            "EPA+DHA (mg)",
            "Soluble Fiber (g)",
            "Insoluble Fiber (g)",
            "Water (ml)",
        ]
        vitamins = [k for k in all_estimates.keys() if "Vitamin" in k]
        minerals = [
            "Calcium (mg)",
            "Phosphorus (mg)",
            "Magnesium (mg)",
            "Potassium (mg)",
            "Sodium (mg)",
            "Chloride (mg)",
            "Iron (mg)",
            "Zinc (mg)",
            "Copper (mcg)",
            "Selenium (mcg)",
            "Manganese (mg)",
            "Iodine (mcg)",
            "Chromium (mcg)",
            "Molybdenum (mcg)",
        ]
        amino_acids = [
            k
            for k in all_estimates.keys()
            if k
            in [
                "Leucine (g)",
                "Lysine (g)",
                "Valine (g)",
                "Isoleucine (g)",
                "Threonine (g)",
                "Methionine (g)",
                "Phenylalanine (g)",
                "Histidine (g)",
                "Tryptophan (g)",
            ]
        ]
        other = [
            k
            for k in all_estimates.keys()
            if k not in macro_nutrients + vitamins + minerals + amino_acids
        ]

        # Print macronutrients
        console.print("[bold cyan]Macronutrients:[/bold cyan]")
        for nutrient in macro_nutrients:
            if nutrient in all_estimates:
                console.print(f"  {nutrient}: {all_estimates[nutrient]}")

        # Print vitamins
        console.print("\n[bold cyan]Vitamins:[/bold cyan]")
        for nutrient in vitamins:
            console.print(f"  {nutrient}: {all_estimates[nutrient]}")

        # Print minerals
        console.print("\n[bold cyan]Minerals:[/bold cyan]")
        for nutrient in minerals:
            if nutrient in all_estimates:
                console.print(f"  {nutrient}: {all_estimates[nutrient]}")

        # Print amino acids
        if amino_acids:
            console.print("\n[bold cyan]Essential Amino Acids:[/bold cyan]")
            for nutrient in amino_acids:
                console.print(f"  {nutrient}: {all_estimates[nutrient]}")

        # Print other nutrients
        if other:
            console.print("\n[bold cyan]Other Nutrients:[/bold cyan]")
            for nutrient in other:
                console.print(f"  {nutrient}: {all_estimates[nutrient]}")

        # Display issues if any
        if issues_found:
            console.print(
                f"\n[bold yellow]Issues to address ({len(issues_found)}):[/bold yellow]"
            )
            for idx, issue in enumerate(issues_found[:5], 1):
                severity_color = (
                    "red"
                    if issue.get("severity") == "high"
                    else "yellow"
                    if issue.get("severity") == "medium"
                    else "blue"
                )
                console.print(
                    f"  [{severity_color}]{idx}. {issue['nutrient']}:[/{severity_color}] "
                    f"{issue['issue']}"
                )

        # Check if we've reached agreement
        if verification.get("approved") or approval_pct >= approval_threshold:
            console.print(f"\n")
            console.print(
                Panel(
                    f"[bold green]Consensus reached! ({approval_pct}% approval)[/bold green]\n\n"
                    f"Iterations used: {iteration}/{max_iterations}\n"
                    f"Final confidence: {estimates.get('confidence_level', 'unknown')}",
                    title="[bold green]✅ SUCCESS[/bold green]",
                    border_style="green",
                )
            )
            return {
                "final_estimates": estimates["estimates"],
                "iterations": iteration,
                "confidence": estimates.get("confidence_level"),
                "assumptions": estimates.get("assumptions", []),
                "final_approval": approval_pct,
            }

        # Prepare feedback for next iteration
        feedback = f"""
        Approval: {approval_pct}%
        Overall feedback: {verification.get("overall_feedback", "")}

        Specific issues to address:
        {json.dumps(verification.get("issues_found", []), indent=2)}
        """

        console.print(
            Panel(
                f"[bold yellow]Moving to next iteration...[/bold yellow]\n"
                f"Current approval: {approval_pct}% (target: {approval_threshold}%)",
                border_style="yellow",
            )
        )

    console.print(f"\n")
    console.print(
        Panel(
            f"[bold yellow]Maximum iterations reached[/bold yellow]\n\n"
            f"Final approval: {approval_pct}%\n"
            f"Status: Partial consensus",
            title="[bold yellow]⚠️  PARTIAL SUCCESS[/bold yellow]",
            border_style="yellow",
        )
    )

    return {
        "final_estimates": estimates["estimates"],
        "iterations": max_iterations,
        "confidence": estimates.get("confidence_level"),
        "assumptions": estimates.get("assumptions", []),
        "final_approval": approval_pct,
        "warning": "Did not reach full consensus",
    }


# Example usage
if __name__ == "__main__":
    # Example dish
    ingredients = [
        "400 g makaronu, suchego, typu tagliatelle",
        "100 g cebuli, przekrojonej na pół",
        "2 ząbki czosnku",
        "30 g masła",
        "400 g kurek, świeżych, oczyszczonych",
        "3/4 łyżeczki soli",
        "woda, osolona, do ugotowania makaronu",
        "150 g śmietany, min. 30% tłuszczu",
        "1 łyżka mąki pszennej",
        "1/2 łyżeczki pieprzu czarnego, mielonego",
        "1/4 łyżeczki gałki muszkatołowej, mielonej (opcjonalnie)",
        "tymianek, świeży, tylko liście, do posypania",
        "natka pietruszki, świeża, posiekana, do posypania",
    ]

    ingredients = ["Chef Select Pizza Salami, 400 g, Lidl, produkt chłodzony"]
    result = estimate_dish_nutrition(
        ingredients=ingredients,
        max_iterations=5,
        approval_threshold=80,  # Changed from 90 to 80 to be less strict
    )

    console.print("\n")
    console.print(
        Panel(
            f"[bold blue]Final Results[/bold blue]\n\n"
            f"Iterations needed: {result['iterations']}\n"
            f"Final approval: {result['final_approval']}%\n"
            f"Confidence: {result['confidence']}\n"
            f"Total nutrients tracked: {len(result['final_estimates'])}",
            title="[bold blue]📋 FINAL NUTRITIONAL PROFILE[/bold blue]",
            border_style="blue",
        )
    )

    if result:
        console.print("\n[bold blue]Key nutrients:[/bold blue]")
        key_nutrients = [
            "Protein (g)",
            "Carbohydrates (g)",
            "Total Fats (g)",
            "Vitamin C (mg)",
            "Iron (mg)",
            "Calcium (mg)",
        ]

        for nutrient in key_nutrients:
            value = result["final_estimates"].get(nutrient, "N/A")
            console.print(f"  [cyan]{nutrient}:[/cyan] {value}")

        console.print(
            f"\n[dim]💾 Complete data available in result['final_estimates'][/dim]"
        )
        console.print(
            f"[dim]All {len(result['final_estimates'])} nutrients tracked successfully[/dim]"
        )
