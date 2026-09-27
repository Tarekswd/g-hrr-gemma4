"""
AST-based static code analyzer extracting functions, classes, calls, and import relationships.
"""
import ast
import os
from typing import Optional
from .code_graph import CodeGraph, CodeNode

class ASTGraphBuilder:
    def __init__(self):
        self.graph = CodeGraph()

    def parse_python_code(self, file_path: str, code_content: str) -> None:
        try:
            tree = ast.parse(code_content, filename=file_path)
        except SyntaxError:
            return

        module_id = f"mod:{file_path}"
        mod_node = CodeNode(
            id=module_id,
            name=os.path.basename(file_path),
            kind="module",
            file_path=file_path,
            start_line=1,
            end_line=len(code_content.splitlines()),
            code_content=code_content[:500]
        )
        self.graph.add_node(mod_node)

        lines = code_content.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_id = f"{file_path}:{node.name}"
                doc = ast.get_docstring(node)
                class_node = CodeNode(
                    id=class_id,
                    name=node.name,
                    kind="class",
                    file_path=file_path,
                    start_line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    docstring=doc,
                    code_content="\n".join(lines[node.lineno-1 : getattr(node, "end_lineno", node.lineno)])
                )
                self.graph.add_node(class_node)
                self.graph.add_edge(module_id, class_id, "contains")

                for base in node.bases:
                    if isinstance(base, ast.Name):
                        self.graph.add_edge(class_id, f"sym:{base.id}", "inherits")

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_id = f"{file_path}:{node.name}"
                doc = ast.get_docstring(node)
                fn_node = CodeNode(
                    id=fn_id,
                    name=node.name,
                    kind="function",
                    file_path=file_path,
                    start_line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    docstring=doc,
                    code_content="\n".join(lines[node.lineno-1 : getattr(node, "end_lineno", node.lineno)])
                )
                self.graph.add_node(fn_node)
                self.graph.add_edge(module_id, fn_id, "contains")

                # Parse function calls within this function
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            callee_name = child.func.id
                            self.graph.add_edge(fn_id, f"call:{callee_name}", "calls")
                        elif isinstance(child.func, ast.Attribute):
                            callee_name = child.func.attr
                            self.graph.add_edge(fn_id, f"call:{callee_name}", "calls")

    def build_from_files(self, file_dict: dict) -> CodeGraph:
        """file_dict maps file_path -> code_content string"""
        for fpath, content in file_dict.items():
            self.parse_python_code(fpath, content)
        return self.graph
