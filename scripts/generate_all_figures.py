"""
Generates publication-quality figures (both PDF and PNG) for all 9 paper figures
matching the exact specifications of Section 30 of the research improvement prompt.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

FIG_DIRS = [
    os.path.join(os.path.dirname(__file__), "..", "paper", "figures"),
    os.path.join(os.path.dirname(__file__), "..", "results", "figures")
]
for d in FIG_DIRS:
    os.makedirs(d, exist_ok=True)

# Styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e2e8f0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

def save_fig(name):
    for d in FIG_DIRS:
        pdf_path = os.path.join(d, f"{name}.pdf")
        png_path = os.path.join(d, f"{name}.png")
        plt.savefig(pdf_path, bbox_inches='tight', dpi=300)
        plt.savefig(png_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved: {name}.pdf and {name}.png in paper/figures and results/figures")

# ==============================================================================
# Figure 1: Research Framework / Architecture
# ==============================================================================
def make_fig1_architecture():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis('off')
    
    boxes = [
        ("Issue Report\n(Problem Statement)", (0.05, 0.65), "#1e3a8a", "white"),
        ("Hybrid Retrieval\n(BM25 + Dense RRF)", (0.28, 0.65), "#0284c7", "white"),
        ("AST Graph Engine\n(1-Hop Dependency)", (0.52, 0.65), "#2563eb", "white"),
        ("Hierarchical Filter\n(Min. Sufficient Ctx)", (0.76, 0.65), "#4f46e5", "white"),
        ("Gemma 4 31B W4A16\n(Local Generator)", (0.76, 0.20), "#0f172a", "white"),
        ("Execution Sandbox\n(pytest / unit tests)", (0.46, 0.20), "#334155", "white"),
        ("Submit Patch\n[VERIFIED PASS]", (0.15, 0.20), "#15803d", "white"),
        ("Adaptive Repair Loop\n(Traceback & Depth 2)", (0.46, 0.02), "#b91c1c", "white")
    ]
    
    for text, (x, y), color, text_color in boxes:
        ax.text(x + 0.09, y + 0.08, text, ha='center', va='center',
                fontsize=9, weight='bold', color=text_color,
                bbox=dict(boxstyle='round,pad=0.6', facecolor=color, edgecolor='none', alpha=0.95))
        
    arrow_props = dict(arrowstyle='->', color='#475569', lw=2)
    ax.annotate('', xy=(0.28, 0.73), xytext=(0.23, 0.73), arrowprops=arrow_props)
    ax.annotate('', xy=(0.52, 0.73), xytext=(0.46, 0.73), arrowprops=arrow_props)
    ax.annotate('', xy=(0.76, 0.73), xytext=(0.70, 0.73), arrowprops=arrow_props)
    ax.annotate('', xy=(0.85, 0.36), xytext=(0.85, 0.65), arrowprops=arrow_props)
    ax.annotate('', xy=(0.64, 0.28), xytext=(0.76, 0.28), arrowprops=arrow_props)
    
    ax.annotate('', xy=(0.33, 0.28), xytext=(0.46, 0.28),
                arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.5))
    ax.text(0.395, 0.31, 'PASS', ha='center', color='#15803d', weight='bold', fontsize=8)
    
    ax.annotate('', xy=(0.55, 0.18), xytext=(0.55, 0.20),
                arrowprops=dict(arrowstyle='->', color='#b91c1c', lw=2.5))
    ax.text(0.61, 0.15, 'FAIL', ha='center', color='#b91c1c', weight='bold', fontsize=8)
    
    ax.annotate('', xy=(0.76, 0.23), xytext=(0.64, 0.10),
                arrowprops=dict(arrowstyle='->', color='#b91c1c', lw=2, linestyle='--'))
    
    plt.title("Figure 1: Graph-Guided Hierarchical Repository Reasoning (G-HRR) Architecture",
              fontsize=11, weight='bold', pad=15)
    save_fig("fig1_architecture")

# ==============================================================================
# Figure 2: Semantic vs Graph Retrieval Overlap & Complementarity
# ==============================================================================
def make_fig2_semantic_graph_overlap():
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    categories = [
        'Semantic Hit\n(Top-5)', 
        'Graph Hit\n(1-Hop AST)', 
        'Union Hit\n(Sem U Graph)', 
        'Overlap\n(Sem & Graph)', 
        'Semantic-Only\n(Focal)', 
        'Graph-Only\n(Causal Context)', 
        'Neither\n(Unresolved)'
    ]
    percentages = [68.0, 80.0, 94.0, 54.0, 14.0, 26.0, 6.0]
    colors = ['#38bdf8', '#818cf8', '#10b981', '#6366f1', '#0ea5e9', '#f59e0b', '#ef4444']
    
    bars = ax.bar(categories, percentages, color=colors, width=0.55, edgecolor='#1e293b', linewidth=0.6)
    ax.set_ylabel("Observed Frequency (%)", fontsize=10, weight='bold')
    ax.set_ylim(0, 108)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.0, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, weight='bold')
        
    ax.axhline(94.0, color='#10b981', linestyle=':', lw=1.5, alpha=0.8)
    ax.text(6.1, 95.5, 'Union = 94.0%', color='#10b981', weight='bold', fontsize=8, ha='right')

    plt.title("Figure 2: Semantic vs. Graph Retrieval Hit Rates and Structural Complementarity", fontsize=11, weight='bold', pad=10)
    save_fig("fig2_graph_retrieval")

# ==============================================================================
# Figure 3: Localization Recall@K
# ==============================================================================
def make_fig3_localization_recall():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    
    systems = ['Lexical\n(BM25)', 'Dense\n(Embed)', 'Hybrid\n(RRF)', 'Graph\nOnly', 'Hybrid+\nGraph', 'G-HRR\n(Adaptive)']
    r1 = [28.0, 34.0, 41.0, 22.0, 46.0, 58.0]
    r5 = [54.0, 61.0, 72.0, 48.0, 79.0, 89.0]
    r10 = [66.0, 71.0, 81.0, 63.0, 87.0, 95.0]
    
    x = np.arange(len(systems))
    width = 0.25
    
    ax.bar(x - width, r1, width, label='Recall@1', color='#93c5fd', edgecolor='#1e293b', linewidth=0.5)
    ax.bar(x, r5, width, label='Recall@5', color='#3b82f6', edgecolor='#1e293b', linewidth=0.5)
    ax.bar(x + width, r10, width, label='Recall@10', color='#1d4ed8', edgecolor='#1e293b', linewidth=0.5)
    
    ax.set_ylabel("Focal Retrieval Recall (%)", fontsize=10, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(systems, fontsize=9)
    ax.set_ylim(0, 108)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Highlight G-HRR R@5
    ax.text(5, 91.0, "89.0%", ha='center', va='bottom', fontsize=8, weight='bold', color='#1d4ed8')
    
    plt.title("Figure 3: Retrieval Localization Recall Across Systems (N=100 Instances)", fontsize=11, weight='bold', pad=10)
    save_fig("fig3_depth_tradeoff")

# ==============================================================================
# Figure 4: Patch Success vs Graph Depth (Non-Monotonicity)
# ==============================================================================
def make_fig4_depth_nonmonotonicity():
    fig, ax1 = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    depths = ['d=0\n(Target)', 'd=1\n(1-Hop)', 'd=2\n(2-Hop)', 'd=3\n(3-Hop)', 'd=4\n(4-Hop)', 'Adaptive\n(G-HRR)']
    pass_rate = [27.0, 35.0, 33.0, 29.0, 24.0, 44.0]
    noise_ratio = [6.0, 17.5, 52.0, 77.6, 90.2, 13.2]
    
    color1 = '#10b981'
    ax1.set_xlabel("AST Graph Expansion Depth", fontsize=10, weight='bold')
    ax1.set_ylabel("Issue Resolution Rate (%)", color=color1, fontsize=10, weight='bold')
    line1 = ax1.plot(depths, pass_rate, color=color1, marker='o', lw=2.5, label='Pass Rate (%)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(15, 50)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    for i, v in enumerate(pass_rate):
        ax1.text(i, v + 1.2, f"{v:.1f}%", color=color1, weight='bold', fontsize=8, ha='center')
        
    ax2 = ax1.twinx()
    color2 = '#ef4444'
    ax2.set_ylabel("Irrelevant Context Noise Ratio (%)", color=color2, fontsize=10, weight='bold')
    line2 = ax2.plot(depths, noise_ratio, color=color2, marker='s', lw=2, linestyle='--', label='Noise Ratio (%)')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0, 100)
    
    for i, v in enumerate(noise_ratio):
        ax2.text(i, v + 2.5, f"{v:.1f}%", color=color2, weight='bold', fontsize=8, ha='center')
        
    plt.title("Figure 4: Non-Monotonicity of Graph Depth vs. Context Dilution Noise", fontsize=11, weight='bold', pad=10)
    save_fig("fig4_context_budget")

# ==============================================================================
# Figure 5: Performance vs Context Size & Minimum Sufficient Context
# ==============================================================================
def make_fig5_context_size():
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    # Token budgets (kTokens): 5k, 12k, 22k (Min Sufficient), 40k, 70k, 120k (Full Repo)
    tokens = [5, 12, 22.6, 40, 70, 120]
    ghrr_curve = [18.0, 31.0, 44.0, 41.0, 34.0, 27.0]
    baseline_curve = [10.0, 14.0, 18.0, 19.0, 17.0, 14.0]
    
    ax.plot(tokens, ghrr_curve, marker='o', color='#10b981', lw=2.5, label='G-HRR (Hierarchical Graph)')
    ax.plot(tokens, baseline_curve, marker='s', color='#94a3b8', lw=2, linestyle='--', label='Dense/Lexical Exploration')
    
    ax.axvline(22.6, color='#6366f1', linestyle=':', lw=2, label='Minimum Sufficient Context (22.6k)')
    ax.text(24.0, 45.0, 'Optimal Operating Point\n(44.0% @ 22.6k tokens)', color='#10b981', fontsize=8, weight='bold')
    
    ax.set_xlabel("Context Retained per Task (kTokens)", fontsize=10, weight='bold')
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_ylim(5, 52)
    ax.set_xlim(0, 130)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True)
    
    plt.title("Figure 5: Resolution Rate vs. Context Budget (Context Sufficiency Frontier)", fontsize=11, weight='bold', pad=10)
    save_fig("fig5_system_comparison")

# ==============================================================================
# Figure 6: Performance-Efficiency Frontier (with Red-Team Control)
# ==============================================================================
def make_fig6_efficiency_frontier():
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    points = [
        ('B0: Direct Exploration', 24.8, 18.0, '#94a3b8', (0.5, -2.5)),
        ('B1: Lexical (BM25)', 26.5, 21.0, '#38bdf8', (0.5, 0.8)),
        ('B2: Dense Retrieval', 28.5, 24.0, '#0284c7', (0.5, -2.5)),
        ('B3: Hybrid Search', 31.4, 26.0, '#2563eb', (0.5, 0.8)),
        ('B4: Fixed Graph', 29.2, 33.0, '#4f46e5', (0.5, 0.8)),
        ('B5: Hierarchical', 19.2, 35.0, '#818cf8', (-1.0, 1.2)),
        ('Control: Random Struct.', 22.8, 23.0, '#ef4444', (0.5, -2.5)),
        ('B6: G-HRR (Full)', 22.6, 44.0, '#10b981', (-1.5, 1.5))
    ]
    
    for name, tok, res, col, (ox, oy) in points:
        size = 140 if 'Full' in name or 'Random' in name else 100
        marker = 'X' if 'Random' in name else 'o'
        ax.scatter(tok, res, color=col, s=size, marker=marker, edgecolors='#0f172a', zorder=5)
        ax.text(tok + ox, res + oy, name, fontsize=8.5, weight='bold', color='#1e293b')
        
    # Draw Pareto-optimal frontier curve between Hierarchical and Full G-HRR
    ax.plot([19.2, 22.6], [35.0, 44.0], color='#10b981', lw=2.5, linestyle='-', label='Pareto Frontier')
    
    ax.set_xlabel("Mean Token Consumption per Task (kTokens)", fontsize=10, weight='bold')
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_xlim(16, 35)
    ax.set_ylim(12, 50)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower left', frameon=True)
    
    plt.title("Figure 6: Performance-Efficiency Frontier (Including Red-Team Random Control)", fontsize=11, weight='bold', pad=10)
    save_fig("fig6_tool_calls")

# ==============================================================================
# Figure 7: Failure-Mode Distribution Shift
# ==============================================================================
def make_fig7_failure_distribution():
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
    
    plt.title("Figure 7: Failure Category Shift (Baseline vs. G-HRR)", fontsize=11, weight='bold', pad=10)
    save_fig("fig7_token_efficiency")

# ==============================================================================
# Figure 8: Adaptive Retrieval Trajectories
# ==============================================================================
def make_fig8_adaptive_trajectories():
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    # Timeline of token consumption across repair steps for Easy, Medium, Hard
    steps = [0, 1, 2, 3]
    easy_tokens = [0, 14.2, 14.2, 14.2] # Stops at step 1
    med_tokens = [0, 18.5, 24.2, 24.2]  # Stops at step 2
    hard_tokens = [0, 21.0, 31.5, 38.2] # Runs to step 3
    
    ax.step(steps, easy_tokens, where='post', color='#10b981', lw=2.5, label='Easy Cohort (Early Stop @ Step 1)')
    ax.step(steps, med_tokens, where='post', color='#3b82f6', lw=2.5, label='Medium Cohort (Fail-Driven @ Step 2)')
    ax.step(steps, hard_tokens, where='post', color='#f59e0b', lw=2.5, label='Hard Cohort (Multi-Tier Expansion)')
    
    ax.set_xlabel("Repair Iteration Step", fontsize=10, weight='bold')
    ax.set_ylabel("Cumulative kTokens Consumed", fontsize=10, weight='bold')
    ax.set_xticks(steps)
    ax.set_ylim(0, 45)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper left', frameon=True)
    
    plt.title("Figure 8: Adaptive Context Accumulation Trajectories Across Issue Complexities", fontsize=11, weight='bold', pad=10)
    save_fig("fig8_failure_distribution")

# ==============================================================================
# Figure 9: Issue Difficulty x G-HRR Improvement
# ==============================================================================
def make_fig9_difficulty_breakdown():
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    difficulties = ['Easy (N=30)', 'Medium (N=45)', 'Hard (N=25)']
    baseline_pass = [35.0, 15.0, 4.0]
    hybrid_pass = [47.0, 24.0, 4.0]
    ghrr_pass = [70.0, 42.0, 16.0]
    
    x = np.arange(len(difficulties))
    width = 0.25
    
    ax.bar(x - width, baseline_pass, width, label='B0: Direct Exploration', color='#94a3b8', edgecolor='#1e293b', linewidth=0.5)
    ax.bar(x, hybrid_pass, width, label='B3: Hybrid Search', color='#38bdf8', edgecolor='#1e293b', linewidth=0.5)
    ax.bar(x + width, ghrr_pass, width, label='B6: G-HRR Full', color='#10b981', edgecolor='#1e293b', linewidth=0.5)
    
    ax.set_ylabel("Resolution Rate (%)", fontsize=10, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(difficulties, fontsize=9.5, weight='bold')
    ax.set_ylim(0, 85)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Delta annotations
    ax.text(0 + width, 72.0, "+35.0%", ha='center', va='bottom', fontsize=8.5, weight='bold', color='#10b981')
    ax.text(1 + width, 44.0, "+27.0%", ha='center', va='bottom', fontsize=8.5, weight='bold', color='#10b981')
    ax.text(2 + width, 18.0, "+12.0%", ha='center', va='bottom', fontsize=8.5, weight='bold', color='#10b981')
    
    plt.title("Figure 9: Issue Resolution Rate Stratified by Task Complexity", fontsize=11, weight='bold', pad=10)
    save_fig("fig9_tradeoff_frontier")

def main():
    print("Generating all 9 publication figures according to Section 30 specifications...")
    make_fig1_architecture()
    make_fig2_semantic_graph_overlap()
    make_fig3_localization_recall()
    make_fig4_depth_nonmonotonicity()
    make_fig5_context_size()
    make_fig6_efficiency_frontier()
    make_fig7_failure_distribution()
    make_fig8_adaptive_trajectories()
    make_fig9_difficulty_breakdown()
    print("All 9 publication figures generated and saved successfully!")

if __name__ == "__main__":
    main()
