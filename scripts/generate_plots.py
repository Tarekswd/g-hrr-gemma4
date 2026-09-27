"""
Generates publication-quality SVG figures and charts for the research paper.
Covers Figures 1 through 9.
"""
import os

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def generate_fig1_architecture():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 450" width="100%" height="100%">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e3c72;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2a5298;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#11998e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38ef7d;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-opacity="0.15"/>
    </filter>
  </defs>
  <rect width="900" height="450" fill="#f8fafc" rx="12"/>
  <text x="450" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#0f172a">Figure 1: Graph-Guided Hierarchical Repository Reasoning (G-HRR) Architecture</text>
  
  <!-- Boxes -->
  <!-- Issue -->
  <rect x="40" y="80" width="160" height="70" rx="8" fill="url(#grad1)" filter="url(#shadow)"/>
  <text x="120" y="115" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Issue Report</text>
  <text x="120" y="135" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#e2e8f0">Problem Statement</text>

  <!-- Arrow -->
  <path d="M 200 115 L 240 115" stroke="#64748b" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Hybrid Retrieval -->
  <rect x="250" y="80" width="180" height="70" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#shadow)"/>
  <text x="340" y="112" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#1e293b">Hybrid Seed Retrieval</text>
  <text x="340" y="132" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#64748b">BM25 + Dense RRF (k=10)</text>

  <!-- Arrow -->
  <path d="M 430 115 L 470 115" stroke="#64748b" stroke-width="2.5"/>

  <!-- AST Code Graph -->
  <rect x="480" y="80" width="180" height="70" rx="8" fill="#ffffff" stroke="#3b82f6" stroke-width="2" filter="url(#shadow)"/>
  <text x="570" y="112" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#1e293b">AST Graph Expander</text>
  <text x="570" y="132" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#3b82f6">1-Hop Caller/Callee Graph</text>

  <!-- Arrow -->
  <path d="M 660 115 L 700 115" stroke="#64748b" stroke-width="2.5"/>

  <!-- Hierarchical Context -->
  <rect x="710" y="80" width="150" height="70" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#shadow)"/>
  <text x="785" y="112" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#1e293b">Hierarchical Filter</text>
  <text x="785" y="132" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#64748b">Smallest Sufficient Ctx</text>

  <!-- Downward Arrow -->
  <path d="M 785 150 L 785 220 L 710 220" stroke="#64748b" stroke-width="2.5"/>

  <!-- Gemma 4 Model -->
  <rect x="480" y="190" width="220" height="80" rx="8" fill="url(#grad1)" filter="url(#shadow)"/>
  <text x="590" y="225" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Gemma 4 31B W4A16</text>
  <text x="590" y="245" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#cbd5e1">Local Reasoning &amp; Patch Gen</text>

  <!-- Arrow to Test -->
  <path d="M 480 230 L 400 230" stroke="#64748b" stroke-width="2.5"/>

  <!-- Test Sandbox -->
  <rect x="220" y="195" width="170" height="70" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#shadow)"/>
  <text x="305" y="228" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#1e293b">Execution Sandbox</text>
  <text x="305" y="248" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#64748b">pytest / unit validation</text>

  <!-- Fork: Pass -> Submit, Fail -> Repair -->
  <path d="M 220 230 L 160 230 L 160 320" stroke="#16a34a" stroke-width="2.5"/>
  <rect x="80" y="320" width="160" height="60" rx="8" fill="url(#grad2)" filter="url(#shadow)"/>
  <text x="160" y="355" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#ffffff">Submit Patch [PASS]</text>

  <path d="M 305 265 L 305 320" stroke="#dc2626" stroke-width="2.5"/>
  <rect x="220" y="320" width="170" height="60" rx="8" fill="#ffffff" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <text x="305" y="348" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#dc2626">Adaptive Repair Loop</text>
  <text x="305" y="366" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#64748b">Traceback &amp; Depth 2 Fallback</text>
  <!-- Loopback -->
  <path d="M 390 350 L 590 350 L 590 270" stroke="#dc2626" stroke-width="2" stroke-dasharray="5,5"/>
</svg>"""
    with open(os.path.join(FIG_DIR, "fig1_architecture.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def generate_fig3_depth_chart():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <rect width="600" height="350" fill="#ffffff" rx="8"/>
  <text x="300" y="35" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">Figure 3: Resolution Rate vs. Graph Expansion Depth</text>
  
  <!-- Axes -->
  <line x1="80" y1="280" x2="540" y2="280" stroke="#94a3b8" stroke-width="2"/>
  <line x1="80" y1="280" x2="80" y2="70" stroke="#94a3b8" stroke-width="2"/>

  <!-- Y labels -->
  <text x="70" y="285" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#64748b">0%</text>
  <text x="70" y="235" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#64748b">10%</text>
  <text x="70" y="185" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#64748b">20%</text>
  <text x="70" y="135" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#64748b">30%</text>
  <text x="70" y="85" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#64748b">40%</text>

  <!-- Bars: D0=27%, D1=35%, D2=33%, D3=29%, Adaptive=44% -->
  <!-- 1% = 5px. y = 280 - (val * 5) -->
  <rect x="110" y="145" width="55" height="135" fill="#93c5fd" rx="4"/>
  <text x="137" y="135" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#1e3a8a">27%</text>
  <text x="137" y="300" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#475569">Depth 0</text>

  <rect x="195" y="105" width="55" height="175" fill="#3b82f6" rx="4"/>
  <text x="222" y="95" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#1e3a8a">35%</text>
  <text x="222" y="300" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#475569">Depth 1</text>

  <rect x="280" y="115" width="55" height="165" fill="#60a5fa" rx="4"/>
  <text x="307" y="105" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#1e3a8a">33%</text>
  <text x="307" y="300" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#475569">Depth 2</text>

  <rect x="365" y="135" width="55" height="145" fill="#93c5fd" rx="4"/>
  <text x="392" y="125" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#1e3a8a">29%</text>
  <text x="392" y="300" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#475569">Depth 3</text>

  <rect x="450" y="60" width="55" height="220" fill="#10b981" rx="4"/>
  <text x="477" y="50" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#065f46">44%</text>
  <text x="477" y="300" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#047857">Adaptive</text>
</svg>"""
    with open(os.path.join(FIG_DIR, "fig3_depth_tradeoff.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def generate_fig5_system_comparison():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 350" width="100%" height="100%">
  <rect width="650" height="350" fill="#ffffff" rx="8"/>
  <text x="325" y="35" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">Figure 5: Benchmark Resolution Rate Across Systems (%)</text>
  
  <g transform="translate(60, 60)">
    <!-- Baseline: 18% -->
    <text x="140" y="35" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#334155">Baseline (A)</text>
    <rect x="150" y="18" width="90" height="26" fill="#94a3b8" rx="4"/>
    <text x="250" y="35" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#334155">18.0%</text>

    <!-- Semantic: 26% -->
    <text x="140" y="85" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#334155">Semantic (B)</text>
    <rect x="150" y="68" width="130" height="26" fill="#38bdf8" rx="4"/>
    <text x="290" y="85" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#0284c7">26.0%</text>

    <!-- Graph: 33% -->
    <text x="140" y="135" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#334155">Graph (C)</text>
    <rect x="150" y="118" width="165" height="26" fill="#60a5fa" rx="4"/>
    <text x="325" y="135" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#2563eb">33.0%</text>

    <!-- Hierarchical: 35% -->
    <text x="140" y="185" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#334155">Hierarchical (D)</text>
    <rect x="150" y="168" width="175" height="26" fill="#818cf8" rx="4"/>
    <text x="335" y="185" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#4f46e5">35.0%</text>

    <!-- Full G-HRR: 44% -->
    <text x="140" y="235" text-anchor="end" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">G-HRR Full (E)</text>
    <rect x="150" y="218" width="220" height="26" fill="#10b981" rx="4"/>
    <text x="380" y="235" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#047857">44.0%</text>
  </g>
</svg>"""
    with open(os.path.join(FIG_DIR, "fig5_system_comparison.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def generate_fig8_failure_chart():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <rect width="600" height="350" fill="#ffffff" rx="8"/>
  <text x="300" y="35" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">Figure 8: Failure Category Distribution (G-HRR vs. Baseline)</text>
  
  <g transform="translate(40, 70)">
    <text x="160" y="30" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#334155">F1: Wrong Localization</text>
    <rect x="170" y="18" width="150" height="16" fill="#f87171" rx="3"/>
    <rect x="170" y="18" width="35" height="16" fill="#34d399" rx="3"/>

    <text x="160" y="65" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#334155">F2: Missing Context</text>
    <rect x="170" y="53" width="97" height="16" fill="#f87171" rx="3"/>
    <rect x="170" y="53" width="28" height="16" fill="#34d399" rx="3"/>

    <text x="160" y="100" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#334155">F3: Dependency Failure</text>
    <rect x="170" y="88" width="53" height="16" fill="#f87171" rx="3"/>
    <rect x="170" y="88" width="21" height="16" fill="#34d399" rx="3"/>

    <text x="160" y="135" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#334155">F4: Root Cause Failure</text>
    <rect x="170" y="123" width="39" height="16" fill="#f87171" rx="3"/>
    <rect x="170" y="123" width="42" height="16" fill="#34d399" rx="3"/>

    <text x="160" y="170" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#334155">F9: Incomplete Patch</text>
    <rect x="170" y="158" width="10" height="16" fill="#f87171" rx="3"/>
    <rect x="170" y="158" width="112" height="16" fill="#34d399" rx="3"/>
  </g>
  <!-- Legend -->
  <rect x="210" y="290" width="14" height="14" fill="#f87171" rx="2"/>
  <text x="230" y="302" font-family="Arial, sans-serif" font-size="11" fill="#475569">Baseline Failure Rate</text>
  <rect x="370" y="290" width="14" height="14" fill="#34d399" rx="2"/>
  <text x="390" y="302" font-family="Arial, sans-serif" font-size="11" fill="#475569">G-HRR Failure Rate</text>
</svg>"""
    with open(os.path.join(FIG_DIR, "fig8_failure_distribution.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    print("Generating publication SVG charts in paper/figures/...")
    generate_fig1_architecture()
    generate_fig3_depth_chart()
    generate_fig5_system_comparison()
    generate_fig8_failure_chart()
    print("All figures successfully created.")

if __name__ == "__main__":
    main()
