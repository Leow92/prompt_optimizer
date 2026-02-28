import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .optimizer import LeoOptimizer, OpenAIProvider, GroqProvider, AnthropicProvider, GeminiProvider, MistralProvider
from .evaluator import BatchEvaluator
import os
import json
import difflib
from rich.text import Text
from rich.columns import Columns

app = typer.Typer(help="Leo Prompt Optimizer CLI")
console = Console()

def generate_diff_view(original: str, optimized: str):
    """
    Creates a Rich-formatted side-by-side comparison.
    """
    def color_text(text, color):
        return f"[{color}]{text}[/{color}]"

    # Split into lines for comparison
    orig_lines = original.splitlines()
    opt_lines = optimized.splitlines()

    # Create two Rich Panels to represent the 'Before' and 'After'
    orig_display = Text()
    opt_display = Text()

    # Use difflib to find changes
    d = difflib.Differ()
    diff = list(d.compare(orig_lines, opt_lines))

    for line in diff:
        if line.startswith('  '): # Unchanged
            orig_display.append(line[2:] + "\n")
            opt_display.append(line[2:] + "\n")
        elif line.startswith('- '): # Removed from original
            orig_display.append(line[2:] + "\n", style="bold red")
        elif line.startswith('+ '): # Added to optimized
            opt_display.append(line[2:] + "\n", style="bold green")

    return (
        Panel(orig_display, title="[red]Original Draft", border_style="red"),
        Panel(opt_display, title="[green]Optimized Prompt", border_style="green")
    )

@app.command()
def optimize(
    prompt_file: str = typer.Option(..., help="Path to text file containing prompt draft"),
    provider_name: str = typer.Option("openai", help="Provider to use: 'openai', 'groq', 'gemini', 'anthropic' or 'mistral'"), # Added this
    tests: str = typer.Option(None, help="Path to JSON file with test cases"),
    model: str = typer.Option(None, help="Model override (e.g. 'llama3-70b-8192')"),
    output: str = "optimized_prompt.txt"
):
    """
    Optimizes a prompt and optionally evaluates it against test cases.
    """
    with open(prompt_file, "r") as f:
        draft = f.read()

    # 1. Dynamic Provider Initialization
    if provider_name.lower() == "openai":
        provider = OpenAIProvider()
        default_model = model or "gpt-5-2025-08-07"
    elif provider_name.lower() == "groq":
        provider = GroqProvider()
        default_model = model or "openai/gpt-oss-20b"
    elif provider_name.lower() == "anthropic":
        provider = AnthropicProvider()
        default_model = model or "claude-3-5-sonnet-20240620"
    elif provider_name.lower() == "mistral":
        provider = MistralProvider()
        default_model = model or "mistral-medium-2508"
    elif provider_name.lower() == "gemini":
        provider = GeminiProvider()
        default_model = model or "gemini-3-flash-preview"
    else:
        raise typer.BadParameter(f"Unsupported provider: {provider_name}")

    optimizer = LeoOptimizer(provider, default_model=default_model)
    
    with console.status("[bold green]Optimizing prompt..."):
        optimized = optimizer.optimize(draft)
    
    with open(output, "w") as f:
        f.write(optimized)
    
    # console.print(Panel(optimized, title="Optimized Prompt", border_style="green"))

    # 2. Optional Evaluation
    if tests and os.path.exists(tests):
        with open(tests, "r") as f:
            test_cases = json.load(f)
        
        evaluator = BatchEvaluator(provider, optimizer.env, judge_model=default_model)
        
        with console.status(f"[bold blue]Running {len(test_cases)} evaluations..."):
            summary_obj = evaluator.run_batch(draft, optimized, test_cases)
        
        # Display the side-by-side diff
        diff_panels = generate_diff_view(draft, optimized)
        console.print(Columns(diff_panels, expand=True))

        # Use the new helper method to print the table
        console.print(summary_obj.to_rich_table())

# At the bottom of cli.py
def main():
    app()

if __name__ == "__main__":
    main()