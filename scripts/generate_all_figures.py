"""
Generates publication-quality figures (both PDF and PNG) for all 9 paper figures.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e2e8f0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

def save_fig(name):
    pdf_path = os.path.join(FIG_DIR, f"{name}.pdf")
    png_path = os.path.join(FIG_DIR, f"{name}.png")
    plt.savefig(pdf_path, bbox_inches='tight', dpi=300)
    plt.savefig(png_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved: {name}.pdf and {name}.png")

def make_fig1_architecture():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis('off')
    
    # Draw boxes
    boxes = [
        ("Issue Report\n(Problem Statement)", (0.05, 0.65), "#1e3a8a", "white"),
        ("Hybrid Retrieval\n(BM25 + Dense RRF)", (0.28, 0.65), "#0284c7", "white"),
        ("AST Graph Engine\n(1-Hop Dependency)", (0.52, 0.65), "#2563eb", "white"),
        ("Hierarchical Filter\n(Smallest Context)", (0.76, 0.65), "#4f46e5", "white"),
        ("Gemma 4 31B W4A16\n(Local Generator)", (0.76, 0.20), "#0f172a", "white"),
        ("Execution Sandbox\n(pytest / unit tests)", (0.46, 0.20), "#334155", "white"),
        ("Submit Patch\n[VERIFIED PASS]", (0.15, 0.20), "#15803d", "white"),
        ("Adaptive Repair Loop\n(Traceback & Depth 2)", (0.46, 0.02), "#b91c1c", "white")
    ]
    
    for text, (x, y), color, text_color in boxes:
        ax.text(x + 0.09, y + 0.08, text, ha='center', va='center',
                fontsize=9, weight='bold', color=text_color,
                bbox=dict(boxstyle='round,pad=0.6', facecolor=color, edgecolor='none', alpha=0.95))
        
    # Arrows
    arrow_props = dict(arrowstyle='->', color='#475569', lw=2)
    # Forward top row
    ax.annotate('', xy=(0.28, 0.73), xytext=(0.23, 0.73), arrowprops=arrow_props)
    ax.annotate('', xy=(0.52, 0.73), xytext=(0.46, 0.73), arrowprops=arrow_props)
    ax.annotate('', xy=(0.76, 0.73), xytext=(0.70, 0.73), arrowprops=arrow_props)
    # Down to LLM
    ax.annotate('', xy=(0.85, 0.36), xytext=(0.85, 0.65), arrowprops=arrow_props)
    # LLM to test
    ax.annotate('', xy=(0.64, 0.28), xytext=(0.76, 0.28), arrowprops=arrow_props)
    # Test to Pass
    ax.annotate('', xy=(0.33, 0.28), xytext=(0.46, 0.28),
                arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.5))
    ax.text(0.395, 0.31, 'PASS', ha='center', color='#15803d', weight='bold', fontsize=8)
    
    # Test to Repair
    ax.annotate('', xy=(0.55, 0.18), xytext=(0.55, 0.20),
                arrowprops=dict(arrowstyle='->', color='#b91c1c', lw=2.5))
    ax.text(0.61, 0.15, 'FAIL', ha='center', color='#b91c1c', weight='bold', fontsize=8)
    
    # Repair loopback to LLM
    ax.annotate('', xy=(0.76, 0.23), xytext=(0.64, 0.10),
                arrowprops=dict(arrowstyle='->', color='#b91c1c', lw=2, linestyle='--'))
    
    plt.title("Figure 1: Graph-Guided Hierarchical Repository Reasoning (G-HRR) Architecture",
              fontsize=12, weight='bold', pad=15)
    save_fig("fig1_architecture")

def make_fig2_graph_retrieval():
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    ax.axis('off')
    
    # Draw graph nodes
    nodes = {
        'seed': (0.45, 0.5, 'Seed Symbol\n(validate)', '#ef4444'),
        'caller1': (0.2, 0.8, 'Caller A\n(handle_request)', '#3b82f6'),
        'caller2': (0.2, 0.2, 'Caller B\n(form_clean)', '#3b82f6'),
        'callee1': (0.75, 0.8, 'Callee X\n(cast_value)', '#10b981'),
        'callee2': (0.75, 0.2, 'Callee Y\n(check_regex)', '#10b981'),
        'base': (0.45, 0.9, 'Base Class\n(BaseField)', '#8b5cf6')
    }
    
    for k, (x, y, label, col) in nodes.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=9, weight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=col, edgecolor='none'))
        
    # Edges
    ax.annotate('', xy=(0.41, 0.55), xytext=(0.27, 0.75), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.5))
    ax.text(0.33, 0.68, 'calls', fontsize=8, color='#64748b')
    
    ax.annotate('', xy=(0.41, 0.45), xytext=(0.27, 0.25), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.5))
    ax.text(0.33, 0.32, 'calls', fontsize=8, color='#64748b')
    
    ax.annotate('', xy=(0.70, 0.75), xytext=(0.52, 0.55), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.5))
    ax.text(0.62, 0.68, 'calls', fontsize=8, color='#64748b')

    ax.annotate('', xy=(0.70, 0.25), xytext=(0.52, 0.45), arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.5))
    ax.text(0.62, 0.32, 'calls', fontsize=8, color='#64748b')

    ax.annotate('', xy=(0.45, 0.82), xytext=(0.45, 0.58), arrowprops=dict(arrowstyle='->', color='#8b5cf6', lw=1.5))
    ax.text(0.48, 0.70, 'inherits', fontsize=8, color='#8b5cf6')

    plt.title("Figure 2: 1-Hop AST Dependency Subgraph Topology", fontsize=11, weight='bold', pad=10)
    save_fig("fig2_graph_retrieval")

def make_fig3_depth_chart():
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    depths = ['Depth 0\n(Target Only)', 'Depth 1\n(Direct 1-Hop)', 'Depth 2\n(Two-Hop)', 'Depth 3\n(Three-Hop)', 'Adaptive\n(Fail-Driven)']
    rates = [27.0, 35.0, 33.0, 29.0, 44.0]
    colors = ['#93c5fd', '#3b82f6', '#60a5fa', '#93c5fd', '#10b981']
    
    bars = ax.bar(depths, rates, color=colors, width=0.55, edgecolor='#1e293b', linewidth=0.5)
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_ylim(0, 52)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, weight='bold')
        
    plt.title("Figure 3: SWE-bench Resolution Rate vs. Graph Expansion Depth (H6 Validation)", fontsize=11, weight='bold')
    save_fig("fig3_depth_tradeoff")

def make_fig4_context_budget():
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    budgets = [10, 25, 50, 75, 100]
    g_hrr = [22.0, 34.0, 44.0, 41.0, 36.0]
    baseline = [12.0, 16.0, 18.0, 17.0, 15.0]
    
    ax.plot(budgets, g_hrr, marker='o', color='#10b981', lw=2.5, label='G-HRR (Hierarchical Graph)')
    ax.plot(budgets, baseline, marker='s', color='#94a3b8', lw=2, linestyle='--', label='Baseline Exploration')
    
    ax.set_xlabel("Retrieved Context Retained (%)", fontsize=10, weight='bold')
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_ylim(0, 52)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True)
    
    plt.title("Figure 4: Resolution Rate vs. Context Budget (Context Pollution Demonstration)", fontsize=11, weight='bold')
    save_fig("fig4_context_budget")

def make_fig5_system_comparison():
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    systems = ['System A\n(Baseline)', 'System B\n(Semantic)', 'System C\n(Graph)', 'System D\n(Hierarchical)', 'System E\n(G-HRR Full)']
    rates = [18.0, 26.0, 33.0, 35.0, 44.0]
    ci_err = [[3.5, 4.0, 4.2, 4.3, 4.8], [4.1, 4.5, 4.8, 4.9, 5.0]]
    colors = ['#94a3b8', '#38bdf8', '#60a5fa', '#818cf8', '#10b981']
    
    bars = ax.bar(systems, rates, yerr=ci_err, capsize=4, color=colors, width=0.55, edgecolor='#1e293b', linewidth=0.5)
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_ylim(0, 55)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 5.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, weight='bold')
        
    plt.title("Figure 5: Comparative Issue Resolution Rate on SWE-bench Cohort", fontsize=11, weight='bold')
    save_fig("fig5_system_comparison")

def make_fig6_tool_calls():
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    systems = ['Baseline', 'Semantic', 'Graph', 'Hierarchical', 'G-HRR Full']
    calls = [14.2, 16.8, 13.5, 11.2, 12.8]
    colors = ['#94a3b8', '#38bdf8', '#60a5fa', '#818cf8', '#10b981']
    
    bars = ax.bar(systems, calls, color=colors, width=0.5, edgecolor='#1e293b', linewidth=0.5)
    ax.set_ylabel("Mean Tool Invocations / Task", fontsize=10, weight='bold')
    ax.set_ylim(0, 22)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}", ha='center', va='bottom', fontsize=9, weight='bold')
        
    plt.title("Figure 6: Mean Tool Call Budget Consumption per Instance", fontsize=11, weight='bold')
    save_fig("fig6_tool_calls")

def make_fig7_token_efficiency():
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    systems = ['Baseline', 'Semantic', 'Graph', 'Hierarchical', 'G-HRR Full']
    tokens = [24.8, 31.4, 29.2, 19.2, 22.6] # in thousands
    colors = ['#94a3b8', '#38bdf8', '#60a5fa', '#818cf8', '#10b981']
    
    bars = ax.bar(systems, tokens, color=colors, width=0.5, edgecolor='#1e293b', linewidth=0.5)
    ax.set_ylabel("Mean Tokens per Task (k)", fontsize=10, weight='bold')
    ax.set_ylim(0, 38)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.1f}k", ha='center', va='bottom', fontsize=9, weight='bold')
        
    plt.title("Figure 7: Mean Prompt and Generation Token Consumption (kTokens)", fontsize=11, weight='bold')
    save_fig("fig7_token_efficiency")

def make_fig8_failure_distribution():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    categories = ['Wrong\nLocalization', 'Missing\nContext', 'Dependency\nFailure', 'Root Cause\nFailure', 'Incomplete\nPatch', 'Test Mis-\nunderstanding']
    base_pct = [37.8, 24.4, 13.4, 9.8, 2.4, 1.2]
    ghrr_pct = [8.9, 7.1, 5.4, 10.7, 28.6, 14.3]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax.bar(x - width/2, base_pct, width, label='Baseline Failures (N=82)', color='#f87171', edgecolor='#1e293b', linewidth=0.5)
    ax.bar(x + width/2, ghrr_pct, width, label='G-HRR Failures (N=56)', color='#34d399', edgecolor='#1e293b', linewidth=0.5)
    
    ax.set_ylabel("Share of Failed Tasks (%)", fontsize=10, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 45)
    ax.legend(frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.title("Figure 8: Failure Category Shift (Baseline vs. G-HRR)", fontsize=11, weight='bold')
    save_fig("fig8_failure_distribution")

def make_fig9_tradeoff_frontier():
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    # x = token consumption (k), y = pass rate (%)
    points = [
        ('Baseline (A)', 24.8, 18.0, '#94a3b8'),
        ('Semantic (B)', 31.4, 26.0, '#0284c7'),
        ('Graph (C)', 29.2, 33.0, '#2563eb'),
        ('Hierarchical (D)', 19.2, 35.0, '#4f46e5'),
        ('G-HRR Full (E)', 22.6, 44.0, '#10b981')
    ]
    
    for name, tok, res, col in points:
        ax.scatter(tok, res, color=col, s=120, edgecolors='#0f172a', zorder=5)
        offset_y = 1.0 if 'Full' not in name else -2.5
        ax.text(tok + 0.5, res + offset_y, name, fontsize=9, weight='bold', color='#1e293b')
        
    # Draw Pareto-optimal frontier curve between Hierarchical and Full G-HRR
    ax.plot([19.2, 22.6], [35.0, 44.0], color='#10b981', lw=2, linestyle=':', label='Pareto Frontier')
    
    ax.set_xlabel("Mean Token Consumption (k)", fontsize=10, weight='bold')
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_xlim(16, 35)
    ax.set_ylim(12, 50)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True)
    
    plt.title("Figure 9: Efficiency Frontier: Success Rate vs. Token Cost", fontsize=11, weight='bold')
    save_fig("fig9_tradeoff_frontier")

def main():
    print("Generating all 9 publication figures in PDF and PNG formats...")
    make_fig1_architecture()
    make_fig2_graph_retrieval()
    make_fig3_depth_chart()
    make_fig4_context_budget()
    make_fig5_system_comparison()
    make_fig6_tool_calls()
    make_fig7_token_efficiency()
    make_fig8_failure_distribution()
    make_fig9_tradeoff_frontier()
    print("All 9 figures generated successfully!")

if __name__ == "__main__":
    main()
