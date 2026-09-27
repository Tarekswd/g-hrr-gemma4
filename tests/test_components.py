"""
Unit test suite verifying all research modules and empirical statistical pipelines.
"""
import unittest
import os
import sys

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.retrieval.bm25 import BM25Retriever
from src.retrieval.semantic_search import DenseCodeRetriever
from src.retrieval.hybrid_search import HybridCodeSearcher
from src.graph.code_graph import CodeGraph, CodeNode
from src.graph.ast_graph_builder import ASTGraphBuilder
from src.graph.graph_expansion import GraphExpander
from src.reasoning.hierarchical_context import HierarchicalContextBuilder
from src.reasoning.confidence_heuristic import ConfidenceHeuristic
from src.validation.failure_parser import FailureParser
from src.evaluation.metrics import BenchmarkMetrics
from src.evaluation.failure_classifier import FailureClassifier
from src.evaluation.statistical_tests import StatisticalAnalysis
from src.experiments.experiment_runner import BenchmarkCohortGenerator, ExperimentRunner

class TestResearchComponents(unittest.TestCase):
    def test_bm25_retriever(self):
        docs = [
            {"id": "doc1", "text": "def validate_user(user_id): pass"},
            {"id": "doc2", "text": "def format_currency(val): pass"},
            {"id": "doc3", "text": "class UserValidator(Validator): pass"}
        ]
        retriever = BM25Retriever()
        retriever.index(docs)
        results = retriever.retrieve("validate user", top_k=2)
        self.assertEqual(len(results), 2)
        top_doc, score = results[0]
        self.assertIn("validate", top_doc["text"])

    def test_hybrid_searcher(self):
        docs = [
            {"id": "f1", "text": "def compute_loss(y_true, y_pred): return mse(y_true, y_pred)"},
            {"id": "f2", "text": "def render_html_template(context): return template.render(context)"}
        ]
        searcher = HybridCodeSearcher()
        searcher.index(docs)
        results = searcher.retrieve("compute loss mse", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0]["id"], "f1")

    def test_ast_graph_and_expansion(self):
        sample_code = """
import os

class ModelField:
    def validate(self, value):
        if value is None:
            raise ValueError("Null value")
        return True

def handle_request(field, val):
    field.validate(val)
"""
        builder = ASTGraphBuilder()
        builder.parse_python_code("django/models.py", sample_code)
        graph = builder.graph

        self.assertIn("django/models.py:ModelField", graph.nodes)
        self.assertIn("django/models.py:validate", graph.nodes)
        self.assertIn("django/models.py:handle_request", graph.nodes)

        expander = GraphExpander(graph)
        expanded = expander.expand(["django/models.py:validate"], depth=1)
        self.assertTrue(len(expanded) >= 1)

    def test_hierarchical_context_builder(self):
        builder = HierarchicalContextBuilder(token_budget=5000)
        focal_node = CodeNode(
            id="node1",
            name="validate",
            kind="function",
            file_path="app/views.py",
            start_line=10,
            end_line=20,
            docstring="Validates input",
            code_content="def validate(x): return x > 0"
        )
        ctx = builder.build_context(
            repo_summary="Core Web Service",
            focal_nodes=[focal_node],
            neighbor_nodes=[]
        )
        self.assertIn("LEVEL 1: REPOSITORY ARCHITECTURE", ctx["prompt_text"])
        self.assertIn("def validate(x)", ctx["prompt_text"])
        self.assertTrue(ctx["estimated_tokens"] > 0)

    def test_confidence_heuristic(self):
        heuristic = ConfidenceHeuristic()
        score_pass = heuristic.compute_heuristic(
            test_passed=True,
            lines_changed=10,
            files_changed=1,
            syntax_valid=True,
            test_coverage_matches=True
        )
        score_fail = heuristic.compute_heuristic(
            test_passed=False,
            lines_changed=10,
            files_changed=1,
            syntax_valid=True,
            test_coverage_matches=False
        )
        self.assertGreater(score_pass, 0.7)
        self.assertLessEqual(score_fail, 0.35)

    def test_failure_parser(self):
        trace = """
Traceback (most recent call last):
  File "django/core/handlers/base.py", line 124, in get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "django/views/generic.py", line 45, in dispatch
    return super().dispatch(request, *args, **kwargs)
AttributeError: 'NoneType' object has no attribute 'status_code'
FAILED tests/test_handlers.py::test_null_handler - AttributeError
"""
        parser = FailureParser()
        parsed = parser.parse_traceback(trace)
        self.assertTrue(parsed["has_failure"])
        self.assertEqual(parsed["exception_type"], "AttributeError")
        self.assertEqual(parsed["faulting_file"], "django/views/generic.py")
        self.assertEqual(parsed["faulting_line"], 45)

    def test_statistical_analysis(self):
        # 44 passes out of 100
        outcomes_hrr = [1] * 44 + [0] * 56
        # 18 passes out of 100
        outcomes_base = [1] * 18 + [0] * 82

        mean, lower, upper = StatisticalAnalysis.bootstrap_ci(outcomes_hrr)
        self.assertAlmostEqual(mean, 44.0, delta=1.0)
        self.assertTrue(lower < mean < upper)

        mcnemar = StatisticalAnalysis.mcnemar_test(outcomes_base, outcomes_hrr)
        self.assertGreater(mcnemar["chi2"], 0.0)
        self.assertLess(mcnemar["p_value"], 0.05)

    def test_experiment_runner(self):
        tasks = BenchmarkCohortGenerator.generate_cohort(n_tasks=5, seed=42)
        runner = ExperimentRunner(seed=42)
        results = runner.run_system_evaluation("adaptive_full", tasks)
        self.assertEqual(len(results), 5)
        summary = BenchmarkMetrics.calculate_summary(results)
        self.assertIn("pass_rate", summary)

if __name__ == "__main__":
    unittest.main()
