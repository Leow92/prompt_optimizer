import json
import tiktoken  # Use tiktoken for accurate local token counting
from typing import List, Dict
import re
from rich.table import Table
import ast

class EvaluationResult:
    def __init__(self, data: Dict):
        self.data = data

    def __str__(self):
        """Standard Python print() output (Plain Text/ASCII)"""
        m = self.data.get("metrics", {})
        return (
            f"\n{'='*20} EVALUATION RESULT {'='*20}\n"
            f"⭐ Score: {self.data.get('g_eval_score')}/5 | ✅ Schema: {self.data.get('schema_adherence')}\n"
            f"📉 Tokens: {m.get('token_efficiency_pct')}% reduction\n"
            f"📝 Reasoning: {self.data.get('reasoning')}\n"
            f"{'='*57}"
        )

    def to_rich_table(self, title="Evaluation Result") -> Table:
        """Helper for the CLI to get a beautiful Rich Table"""
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold white")
        table.add_column("Status", justify="center")

        d = self.data
        m = d.get("metrics", {})
        eff = m.get("token_efficiency_pct", 0)
        schema = d.get("schema_adherence", "")
        halluc = d.get("hallucination_risk", "")

        table.add_row("G-Eval Score", f"{d.get('g_eval_score')}/5", "💎")
        table.add_row("Schema Adherence", schema, "✅" if schema == "Pass" else "❌")
        table.add_row("Token Efficiency", f"{eff}%", "✅" if eff > 0 else "⚠️")
        table.add_row("Original Tokens", str(m.get("original_tokens")), "")
        table.add_row("Optimized Tokens", str(m.get("optimized_tokens")), "")
        table.add_row("Hallucination Risk", halluc, "✅" if halluc != "High" else "⚠️")
        table.add_row("Reasoning", d.get("reasoning", ""), "📝")
        return table

class BatchResult:
    def __init__(self, summary: Dict):
        self.summary = summary

    def __str__(self):
        """Standard Python print() output (Plain Text/ASCII)"""
        s = self.summary
        return (
            f"Batch ({s['total_runs']} runs): {s['avg_g_eval']}/5 Score | "
            f"{s['token_reduction_pct']}% Efficiency | "
            f"Hallucinations: {s['hallucination_incidents']}/{s['total_runs']} "
            f"({s['hallucination_accuracy']:.1f}% clean)"
        )

    def to_rich_table(self, title="Optimization Performance Report") -> Table:
        """Helper for the CLI to get a beautiful Rich Table"""
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold white")
        table.add_column("Status", justify="center")

        s = self.summary
        eff = s['token_reduction_pct']
        halluc_acc = s['hallucination_accuracy']
        table.add_row("Total Runs", str(s['total_runs']), "🔢")
        table.add_row("Token Efficiency", f"{eff}%", "✅" if eff > 0 else "⚠️")
        table.add_row("Avg G-Eval (1-5)", f"{s['avg_g_eval']:.2f}", "💎")
        table.add_row("Schema Pass Rate", f"{s['schema_pass_rate']:.1f}%", "✅")
        table.add_row("Hallucinations", f"{s['hallucination_incidents']}/{s['total_runs']}", "🛡️")
        table.add_row("Hallucination Accuracy", f"{halluc_acc:.1f}%", "✅" if halluc_acc >= 90 else "⚠️")
        return table

class PromptEvaluator:
    def __init__(self, provider, jinja_env, judge_model):
        self.provider = provider
        self.env = jinja_env
        self.judge_model = judge_model
        # Use o200k_base or cl100k_base for OpenAI/Groq models
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def evaluate(self, original_prompt: str, optimized_prompt: str, test_input: str) -> Dict:
        # 1. Generate Outputs
        out_old = self.provider.complete([{"role": "user", "content": f"{original_prompt}\n{test_input}"}], self.judge_model)
        out_new = self.provider.complete([{"role": "user", "content": f"{optimized_prompt}\n{test_input}"}], self.judge_model)

        # 2. Calculate Token Efficiency (Local Python Calculation)
        tokens_old = self._count_tokens(original_prompt)
        tokens_new = self._count_tokens(optimized_prompt)
        efficiency = ((tokens_old - tokens_new) / tokens_old) * 100

        # 3. Render Judge Template
        template = self.env.get_template('judge_v0.1.j2')
        judge_content = template.render(
            original_prompt=original_prompt,
            optimized_prompt=optimized_prompt,
            test_input=test_input,
            output_a=out_old,
            output_b=out_new
        )

        # 4. Get Judge Verdict
        raw_verdict = self.provider.complete([{"role": "user", "content": judge_content}], self.judge_model)
        clean_verdict = re.sub(r'^```json\s*|```\s*$', '', raw_verdict.strip(), flags=re.MULTILINE)

        try:
            verdict = json.loads(clean_verdict)
        except json.JSONDecodeError:
            try:
                verdict = ast.literal_eval(clean_verdict)
            except (ValueError, SyntaxError):
                print(f"Failed to parse JSON. Raw output was: {raw_verdict}")
                raise

        # 5. Merge Data
        verdict["metrics"] = {
            "token_efficiency_pct": round(efficiency, 2),
            "original_tokens": tokens_old,
            "optimized_tokens": tokens_new
        }
        
        return EvaluationResult(verdict)

class BatchEvaluator:
    def __init__(self, provider, jinja_env, judge_model):
        self.provider = provider
        self.env = jinja_env
        self.judge_model = judge_model
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _token_count(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def run_batch(self, original_prompt: str, optimized_prompt: str, test_cases: List[str]) -> Dict:
        results = []
        
        # Calculate prompt-level efficiency once
        orig_tokens = self._token_count(original_prompt)
        opt_tokens = self._token_count(optimized_prompt)
        efficiency_gain = ((orig_tokens - opt_tokens) / orig_tokens) * 100

        for test_input in test_cases:
            # 1. Generate outputs from both prompts
            out_old = self.provider.complete([{"role": "user", "content": f"{original_prompt}\nInput: {test_input}"}], self.judge_model)
            out_new = self.provider.complete([{"role": "user", "content": f"{optimized_prompt}\nInput: {test_input}"}], self.judge_model)

            # 2. Render and run judge
            judge_tmpl = self.env.get_template('judge_v0.1.j2')
            judge_query = judge_tmpl.render(
                original_prompt=original_prompt,
                optimized_prompt=optimized_prompt,
                test_input=test_input,
                output_a=out_old,
                output_b=out_new
            )

            raw_verdict = self.provider.complete([{"role": "user", "content": judge_query}], self.judge_model)
            clean_verdict = re.sub(r'^```json\s*|```\s*$', '', raw_verdict.strip(), flags=re.MULTILINE)
            
            try:
                verdict = json.loads(clean_verdict)
            except json.JSONDecodeError:
                try:
                    verdict = ast.literal_eval(clean_verdict)
                except (ValueError, SyntaxError):
                    print(f"Failed to parse JSON. Raw output was: {raw_verdict}")
                    raise
            
            results.append(verdict)

        # 3. Aggregate Summary
        summary = {
            "total_runs": len(results),
            "token_reduction_pct": round(efficiency_gain, 2),
            "avg_g_eval": sum(r['g_eval_score'] for r in results) / len(results),
            "schema_pass_rate": (sum(1 for r in results if r['schema_adherence'] == "Pass") / len(results)) * 100,
            "hallucination_incidents": sum(1 for r in results if r['hallucination_risk'] == "High"),
            "hallucination_accuracy": (1 - sum(1 for r in results if r['hallucination_risk'] == "High") / len(results)) * 100,
            "individual_runs": results
        }
        return BatchResult(summary)