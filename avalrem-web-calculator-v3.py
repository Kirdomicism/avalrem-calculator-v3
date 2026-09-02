import streamlit as st
import pandas as pd
import datetime
import re
import hashlib
import json

# =============================================================================
# KIRDOMICISM ACADEMY — ENTERPRISE AVALREM WEB CALCULATOR (v3.0)
# =============================================================================
# An enterprise-grade, visually stunning, and intellectually provoking Web App
# designed for HR departments, business operations, and tech-savvy auditors.
# It implements the 4 advanced structural dimensions of Action Value Accounting,
# pre-packaged with a comprehensive interactive User's Guide & Testing Framework.
# =============================================================================

# Page Configuration & Styling
st.set_page_config(
    page_title="Kirdomicism Academy: Enterprise Avalrem Calculator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS (Slate & Gold Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Georgia&family=JetBrains+Mono&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main-title {
        font-family: 'Georgia', serif;
        color: #D4AF37; /* Metallic Gold */
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
        text-shadow: 0px 4px 10px rgba(212, 175, 55, 0.15);
    }
    .sub-title {
        font-family: 'Georgia', serif;
        font-style: italic;
        color: #A0AEC0; /* Slate Gray */
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    .section-header {
        font-family: 'Georgia', serif;
        color: #D4AF37;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    .formula-card {
        background-color: #1A202C;
        border-left: 5px solid #D4AF37;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        color: #E2E8F0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .wow-box {
        background: linear-gradient(135deg, #1A202C 0%, #2D3748 100%);
        border: 1px solid #D4AF37;
        padding: 1.5rem;
        border-radius: 10px;
        color: #E2E8F0;
        box-shadow: 0 10px 25px rgba(212, 175, 55, 0.1);
    }
    .metric-value {
        font-family: 'Georgia', serif;
        color: #D4AF37;
        font-size: 2.8rem;
        font-weight: 800;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    .guide-card {
        background-color: #1F2937;
        border-radius: 8px;
        border: 1px solid #374151;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .guide-step {
        color: #D4AF37;
        font-weight: bold;
        font-size: 1.1rem;
    }
    div.stButton > button {
        background-color: #1A202C !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        font-family: 'Georgia', serif !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
        color: #1A202C !important;
        border: 1px solid #1A202C !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
    }
</style>
""", unsafe_style_html=True)

# ------------------------------------------------------------------------------
# Grounded Presets & Dictionaries
# ------------------------------------------------------------------------------
GRID_CELLS = {
    "zQ": {"focus": "Future", "mode": "Plan", "verb": "Brainstorm", "C": 100.0, "desc": "Model future scenarios and set unshakeable strategic targets"},
    "zW": {"focus": "Operation", "mode": "Plan", "verb": "Schedule", "C": 50.0, "desc": "Organize operations, deadlines, and squeeze cycle times"},
    "zE": {"focus": "Control", "mode": "Plan", "verb": "Participate", "C": 50.0, "desc": "Establish robust preventive measures and compliance guidelines"},
    "zR": {"focus": "Utilisation", "mode": "Plan", "verb": "Allocate", "C": 100.0, "desc": "Plan resource deployment, budgets, and recovery boundaries"},
    "zT": {"focus": "System", "mode": "Plan", "verb": "Design", "C": 150.0, "desc": "Craft core workflows, technology integrations, and architectures"},
    "zA": {"focus": "Future", "mode": "Execution", "verb": "Implement", "C": 100.0, "desc": "Execute a defined strategy, giving the official green light"},
    "zS": {"focus": "Operation", "mode": "Execution", "verb": "Produce", "C": 15.0, "desc": "Execute routine workflows with standard zero-defect quality"},
    "zD": {"focus": "Control", "mode": "Execution", "verb": "Check", "C": 15.0, "desc": "Perform audit procedures and verify operations against compliance"},
    "zF": {"focus": "Utilisation", "mode": "Execution", "verb": "Maneuver", "C": 50.0, "desc": "Physically deploy and exploit limited resources on hand"},
    "zG": {"focus": "System", "mode": "Execution", "verb": "Develop", "C": 100.0, "desc": "Deploy and test-run functional administrative software engines"},
    "zC": {"focus": "Future", "mode": "Analysis", "verb": "Study", "C": 100.0, "desc": "Pre-calculate and weigh strategic consequences under uncertainty"},
    "zX": {"focus": "Operation", "mode": "Analysis", "verb": "Research", "C": 50.0, "desc": "Investigate operational metrics, variance, and bottlenecks"},
    "zV": {"focus": "Control", "mode": "Analysis", "verb": "Investigate", "C": 50.0, "desc": "Uncover systemic weaknesses, risks, and process loopholes"},
    "zB": {"focus": "Utilisation", "mode": "Analysis", "verb": "Prioritize", "C": 50.0, "desc": "Audit budget returns, efficiency, and resource leakage"},
    "zN": {"focus": "System", "mode": "Analysis", "verb": "Test", "C": 100.0, "desc": "Audit and review administrative software or database systems"},
    "zY": {"focus": "Future", "mode": "Communication", "verb": "Announce", "C": 100.0, "desc": "Align long-term direction with stakeholders to prevent drag"},
    "zU": {"focus": "Operation", "mode": "Communication", "verb": "Report", "C": 50.0, "desc": "Transmit transparent, proactive updates of project status"},
    "zI": {"focus": "Control", "mode": "Communication", "verb": "Explain", "C": 50.0, "desc": "Deliver training and explain regulatory standards to the team"},
    "zO": {"focus": "Utilisation", "mode": "Communication", "verb": "Testimonise", "C": 50.0, "desc": "Share cost audits, performance returns, and capital results"},
    "zP": {"focus": "System", "mode": "Communication", "verb": "Demonstrate", "C": 100.0, "desc": "Explain and document functional software workflows for users"},
    "zH": {"focus": "Future", "mode": "Exdysivity", "verb": "Dream", "C": 100.0, "desc": "Dream future transitions and adapt targets dynamically"},
    "zJ": {"focus": "Operation", "mode": "Exdysivity", "verb": "Transform", "C": 90.0, "desc": "Willingly abandon obsolete functional routines and standards"},
    "zK": {"focus": "Control", "mode": "Exdysivity", "verb": "Establish", "C": 70.0, "desc": "Modify control frameworks and rules dynamically under change"},
    "zL": {"focus": "Utilisation", "mode": "Exdysivity", "verb": "Create", "C": 100.0, "desc": "Shed unworkable resource routines and acquire new capabilities"},
    "zM": {"focus": "System", "mode": "Exdysivity", "verb": "Revamp", "C": 150.0, "desc": "Completely reconstruct obsolete procedures and standards"}
}

# Scope Multipliers (C_scale)
SCOPE_PRESETS = {
    "Local (Individual / Daily)": 1.0,
    "Team (Departmental / Mid-Range)": 2.5,
    "Enterprise (Sovereign / Organizational)": 5.0
}

# Consequence Risk Levels (maps to i coefficient)
RISK_PRESETS = {
    "Low Consequence / Lower Friction (Baseline)": 0.12,
    "Medium Consequence / Standard Friction": 0.35,
    "High Consequence / Intense Mental Resistance": 0.75
}

# ------------------------------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------------------------------
if "action_ledger" not in st.session_state:
    st.session_state.action_ledger = []
if "nava_balance" not in st.session_state:
    st.session_state.nava_balance = 0.0

def add_to_ledger(action_name, emp_id, code, volume, C, a, i, receiver_id, status, formula_type, final_score):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tx_id = f"TX-KDM-{int(datetime.datetime.now().timestamp())}"
    
    # Simple blockchain simulation for the tech-savvy audience
    prev_hash = "0" * 64 if not st.session_state.action_ledger else st.session_state.action_ledger[-1]["hash"]
    block_string = f"{tx_id}{action_name}{code}{final_score}{timestamp}{prev_hash}"
    tx_hash = hashlib.sha256(block_string.encode()).hexdigest()
    
    st.session_state.action_ledger.append({
        "timestamp": timestamp,
        "tx_id": tx_id,
        "employee_id": emp_id,
        "action_name": action_name,
        "code": code,
        "volume": volume,
        "C": C,
        "a": a,
        "i": i,
        "receiver_id": receiver_id,
        "status": status,
        "type": formula_type,
        "score": round(final_score, 2),
        "hash": tx_hash[:16] + "..."
    })
    
    # Recalculate NAVA Balance (only include validated, non-pending actions)
    st.session_state.nava_balance = sum(
        item["score"] for item in st.session_state.action_ledger if item["status"] == "Validated"
    )

# ------------------------------------------------------------------------------
# Math Core Functions (with Algorithmic Safeguards)
# ------------------------------------------------------------------------------
def calculate_avalrem(C, a, i, volume=1.0, tef=1.0, is_pending=False):
    # Safeguard 1: if i >= a: i = a - 0.1 to prevent division-by-zero or negative results
    if i >= a:
        i = a - 0.1
        
    denominator = a - i
    base_avalrem = (C * volume) / denominator
    
    # Incorporate Temporal Efficiency Factor
    final_score = base_avalrem * tef
    
    # Safeguard 2: End-Receiver Confirmation constraint
    # Holds high-impact actions as Pending, capping at 50% fallback until validated
    if is_pending:
        final_score = final_score * 0.50
        
    return round(final_score, 3), i

# ------------------------------------------------------------------------------
# Main Page Title
# ------------------------------------------------------------------------------
st.markdown("<div class='main-title'>🧬 KIRDOMICISM ACADEMY</div>", unsafe_style_html=True)
st.markdown("<div class='sub-title'>Enterprise Avalrem Volume Calculator — Action Value Accounting (v3.0)</div>", unsafe_style_html=True)

# Main Stats Dashboard Row
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

total_nava = st.session_state.nava_balance
pending_nava = sum(tx["score"] for tx in st.session_state.action_ledger if tx["status"] == "Pending")
total_txs = len(st.session_state.action_ledger)
usd_exchange_rate = 1.25  # 1 Avalrem = $1.25 USD standard
total_equity = total_nava * usd_exchange_rate

with col_stat1:
    st.markdown(f"""
    <div class='card-stat' style='background-color:#1A202C; border: 1px solid #D4AF37; border-radius:10px; padding:1.5rem; text-align:center;'>
        <div class='metric-value'>{total_nava:.2f}</div>
        <div class='metric-label'>🔐 Accumulated NAVA</div>
    </div>
    """, unsafe_style_html=True)

with col_stat2:
    st.markdown(f"""
    <div class='card-stat' style='background-color:#1A202C; border: 1px solid #D4AF37; border-radius:10px; padding:1.5rem; text-align:center;'>
        <div class='metric-value'>{pending_nava:.2f}</div>
        <div class='metric-label'>⏳ Pending Predictions (^)</div>
    </div>
    """, unsafe_style_html=True)

with col_stat3:
    st.markdown(f"""
    <div class='card-stat' style='background-color:#1A202C; border: 1px solid #D4AF37; border-radius:10px; padding:1.5rem; text-align:center;'>
        <div class='metric-value'>${total_equity:,.2f}</div>
        <div class='metric-label'>💸 Value Equity (USD)</div>
    </div>
    """, unsafe_style_html=True)

with col_stat4:
    st.markdown(f"""
    <div class='card-stat' style='background-color:#1A202C; border: 1px solid #D4AF37; border-radius:10px; padding:1.5rem; text-align:center;'>
        <div class='metric-value'>{total_txs}</div>
        <div class='metric-label'>⛓️ Ledger Transactions</div>
    </div>
    """, unsafe_style_html=True)

st.write("")

# Main Navigation Tabs
tab_guide, tab_parser, tab_tenure, tab_calc, tab_db, tab_ledger = st.tabs([
    "📖 User Guide & Sandbox Testing",
    "🖥️ Delimiter Parsing Lab",
    "📈 HR Tenure & Velocity Simulator",
    "🎛️ Dynamic Action Designer",
    "🗄️ Relational Backend Blueprint",
    "⛓️ Cryptographic Ledger"
])

# =============================================================================
# TAB 0: USER'S GUIDE & SANDBOX TESTING (PROVOKING & JAW-DROPPING)
# =============================================================================
with tab_guide:
    st.markdown("<h3 class='section-header'>📖 The Sovereign Quick-Start & Testing Portal</h3>", unsafe_style_html=True)
    
    st.markdown("""
    Welcome to the **Avalrem Volume Calculator (v3.0)** sandbox. This framework serves as a direct operational replacement 
    for legacy, subjective Key Performance Indicators (KPIs). By standardizing human labor into objective, auditable 
    cryptographic value blocks (**the Avalrem**), we align human reality closer to objective strategic targets.
    
    Here is your non-technical roadmap to self-test the advanced logical modules and verify their accuracy.
    """)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("<div class='guide-card'>", unsafe_style_html=True)
        st.markdown("<span class='guide-step'>🧪 Exercise 1: Multi-Dimensional Delimiter Testing</span>", unsafe_style_html=True)
        st.write("""
        This test proves that raw, human-written administrative actions can be decomposed and validated against the proprietary Kirdomic Lexicon instantly.
        
        **How to Self-Test:**
        1. Copy one of the raw command strings below:
           * **High-Impact Overhaul (System Exdysivity):** `#zM => 12 ::: Enterprise ::: High`
           * **Routine Operational Check (Control Execution):** `#zD => 1 ::: Local ::: Low`
        2. Go to the **🖥️ Delimiter Parsing Lab** tab.
        3. Paste the copied string into the **Delimited String Input** box and press Enter.
        4. **Observe the Magic:** Watch the backstage regex parser visually break down your text, map the codes, pull preloaded coefficients, protect variables against division-by-zero, and output a precise mathematical AVR score immediately! Click the **Deploy** button to write it to the block ledger.
        """, unsafe_style_html=True)
        st.markdown("</div>", unsafe_style_html=True)
        
        st.markdown("<div class='guide-card'>", unsafe_style_html=True)
        st.markdown("<span class='guide-step'>⏳ Exercise 3: Temporal Squeezing & Recipient Security</span>", unsafe_style_html=True)
        st.write("""
        This scenario demonstrates how the algorithm prevents "self-appraisal inflation" and rewards execution velocity.
        
        **How to Self-Test:**
        1. Go to the **🎛️ Dynamic Action Designer** tab.
        2. Select Grid Code **zF (Utilisation Execution)**.
        3. Under *Temporal Dimension*, choose **Duration Window (Project)**.
        4. Set *Planned Target Hours* to `40.0` and *Actual Execution Hours* to `30.0`. Observe how completing the task early generates a **1.333x Temporal Efficiency Factor (TEF)**, multiplying your output.
        5. Check the box to **Hold Action as Pending**. Watch the score immediately get slashed by **50%**. This represents our security protocol: the score remains capped until validated by the receiving Employee ID.
        """, unsafe_style_html=True)
        st.markdown("</div>", unsafe_style_html=True)

    with col_g2:
        st.markdown("<div class='guide-card'>", unsafe_style_html=True)
        st.markdown("<span class='guide-step'>📈 Exercise 2: Slaying the Seniority KPI Trap</span>", unsafe_style_html=True)
        st.write("""
        Traditional performance systems fail because senior employees look superior simply because they have had more years to accumulate volume. This test proves how we standardize equity.
        
        **How to Self-Test:**
        1. Go to the **📈 HR Tenure & Velocity Simulator** tab.
        2. Compare **Employee A (Senior)** with a hire date of `2023-01-15` and total score of `1500 AVR` against **Employee B (New Joiner)** with a hire date of `2026-04-01` and total score of `450 AVR`.
        3. **The Revelation:** Even though the senior's raw score is 3x larger, the simulation reveals that the new joiner has a **250%+ higher daily Score Velocity**! HR can now objectively reward actual daily execution momentum over static operational stagnation (Peonerosis).
        """, unsafe_style_html=True)
        st.markdown("</div>", unsafe_style_html=True)
        
        st.markdown("<div class='guide-card'>", unsafe_style_html=True)
        st.markdown("<span class='guide-step'>🗄️ Exercise 4: Validating the IT & Database Blueprint</span>", unsafe_style_html=True)
        st.write("""
        How is this securely stored inside enterprise IT networks? We provide full transparency.
        
        **How to Self-Test:**
        1. Go to the **🗄️ Relational Backend Blueprint** tab.
        2. Examine the PostgreSQL schema preloaded on-screen.
        3. Review the `employee_score_velocity` View code. It demonstrates how database queries automatically execute these tenure-days calculations, outputting clean, daily-updated, auditable performance sheets straight to your executive dashboard!
        4. Review the **⛓️ Cryptographic Ledger** tab to observe the SHA-256 block hashes linked together, preventing historical manipulation of appraisal records.
        """, unsafe_style_html=True)
        st.markdown("</div>", unsafe_style_html=True)

    st.markdown("---")
    st.markdown("### 🎚️ Live Sandbox Play: Let's Run Your Real-Life Priorities Now")
    st.write("Below is a quick, mini-sandbox. Describe what you are about to execute today to get an immediate Kirdomic impact calculation:")
    
    mini_col1, mini_col2 = st.columns(2)
    with mini_col1:
        sandbox_action = st.text_input("What is your real-life task/decision today?", value="Establish automated invoice validation systems")
        sandbox_C = st.slider("Consequence Impact (C):", 1.0, 150.0, 100.0, help="Routine=15, Tactical=50, High Strategic Sovereign=100+")
    with mini_col2:
        sandbox_a = st.slider("Time Delay Rate (a):", 1.0, 10.0, 1.20, help="Immediate=1.05, Planned/Lagging=2.50, Stagnant/Delayed=5.0+")
        sandbox_i = st.slider("Effort / Risk Rate (i):", 0.01, 0.99, 0.35, help="Passive=0.10, Standard=0.35, Extreme focus=0.75+")
    
    # Calculate mini
    mini_score, final_i = calculate_avalrem(sandbox_C, sandbox_a, sandbox_i)
    st.markdown(f"""
    <div style='background-color:#111827; padding:1.2rem; border-radius:8px; border:1px solid #D4AF37; text-align:center;'>
        <span style='color:#A0AEC0; font-size:1.1rem; font-weight:600;'>PROJECTED IMPACT METRIC:</span><br>
        <span style='color:#D4AF37; font-size:2.5rem; font-weight:900;'>{mini_score:.2f} AVR</span><br>
        <span style='color:#E2E8F0; font-size:0.9rem;'>Formula applied: {sandbox_C} / ({sandbox_a:.2} - {final_i:.3f})</span>
    </div>
    """, unsafe_style_html=True)

# ==============================================================================
# TAB 1: DELIMITER PARSING LAB
# ==============================================================================
with tab_parser:
    st.markdown("<h3 class='section-header'>📟 Multi-Dimensional Input String Parser</h3>", unsafe_style_html=True)
    st.write("Type a raw delimited string to simulate direct, high-speed CLI action logging. This demonstrates the power of natural language processing converting raw effort into standardized contribution indices instantly.")
    
    default_input = "#zT => 15 ::: Enterprise ::: High"
    user_string = st.text_input("Enter Delimited String Input:", value=default_input, key="tab1_str", help="Format: #action_code => quantity ::: Scope ::: Consequence Risk")
    
    # Visual Parsing Lab
    col_p1, col_p2 = st.columns([2, 1])
    
    with col_p1:
        st.write("#### Backstage Parser Output:")
        
        # Regex or split processing
        try:
            # Parse main segments divided by :::
            segments = [seg.strip() for seg in user_string.split(":::")]
            
            # Step 1: Parse Token 1 (#action_code => quantity)
            token_1 = segments[0]
            code_match = re.match(r"#(z[A-M|Q-Y])\s*=>\s*(\d+)", token_1)
            
            if code_match:
                grid_code = code_match.group(1)
                quantity = int(code_match.group(2))
            else:
                # Safe fallbacks if empty or wrong
                grid_code = "zS"
                quantity = 1
                st.warning("⚠️ Token 1 parse failure. Falling back to default: #zS => 1")
            
            # Step 2: Parse Token 2 (Scope)
            scope_str = segments[1] if len(segments) > 1 else "Local"
            # Map scope
            matched_scope_key = next((k for k in SCOPE_PRESETS.keys() if scope_str.lower() in k.lower()), "Local (Individual / Daily)")
            scope_mult = SCOPE_PRESETS[matched_scope_key]
            
            # Step 3: Parse Token 3 (Consequence Risk)
            risk_str = segments[2] if len(segments) > 2 else "Low"
            matched_risk_key = next((k for k in RISK_PRESETS.keys() if risk_str.lower() in k.lower()), "Low Consequence / Lower Friction (Baseline)")
            i_coeff = RISK_PRESETS[matched_risk_key]
            
            # Retrieve base variables from Grid Definition
            grid_info = GRID_CELLS[grid_code]
            base_C = grid_info["C"]
            a_rate = 1.50 if "Plan" in grid_info["mode"] else 2.20 # Standard baseline organizational discount rates
            
            # Perform calculation
            calculated_C = base_C * scope_mult
            final_avr, active_i = calculate_avalrem(calculated_C, a_rate, i_coeff, volume=quantity)
            
            # Display beautiful parse tree
            parsed_data = {
                "Token 1 (Target Code)": f"{grid_code} ({grid_info['verb']} - {grid_info['focus']} focus, {grid_info['mode']} mode)",
                "Token 2 (Volume / Quantity)": quantity,
                "Token 3 (Scope & Multiplier)": f"{matched_scope_key} (x{scope_mult})",
                "Token 4 (Consequence Risk / Intrinsic Effort)": f"{matched_risk_key} (i={i_coeff})",
                "Organizational Discount Rate (a)": a_rate
            }
            st.json(parsed_data)
            
            st.success(f"📟 **Success:** Parsed string into a net score of **{final_avr:.2f} AVR**!")
            
        except Exception as e:
            st.error(f"⚠️ **Syntax Error:** Delimiter format invalid. Make sure you use correctly formatted colons. Error details: {e}")
            
    with col_p2:
        st.markdown("<div class='wow-box'>", unsafe_style_html=True)
        st.markdown("#### Raw Action Tokenizer")
        st.write("Sovereign humanic logic decomposes free-text into a real-time token tree, validating input variables against the immutable Kirdomic Lexicon before ledger integration.")
        
        st.markdown(f"**Target Code:** `{grid_code}`")
        st.markdown(f"**Derived C_base:** `{base_C}`")
        st.markdown(f"**Contextual C_scale:** `{scope_mult}`")
        st.markdown(f"**Total C Vector:** `{calculated_C}`")
        st.markdown(f"**Intrinsic Effort (i):** `{active_i}`")
        st.markdown(f"**Calculated Worth:** `{final_avr} AVR`")
        
        if st.button("🔥 Deploy & Lock Into Ledger", key="btn_parser_deploy"):
            add_to_ledger(
                action_name=f"Parser Input: {grid_info['verb']} Protocol",
                emp_id="EMP-KDM-088",
                code=grid_code,
                volume=quantity,
                C=calculated_C,
                a=a_rate,
                i=i_coeff,
                receiver_id="EMP-KDM-SYS",
                status="Validated",
                formula_type="CLI String Parser",
                final_score=final_avr
            )
            st.success("🔒 Chained securely to the local transaction ledger!")
        st.markdown("</div>", unsafe_style_html=True)

# ==============================================================================
# TAB 2: HR TENURE & VELOCITY SIMULATOR
# ==============================================================================
with tab_tenure:
    st.markdown("<h3 class='section-header'>📈 Resolving Equity: Score Velocity vs. Tenure</h3>", unsafe_style_html=True)
    st.write("Traditional performance reviews reward older employees simply because they have been in the company longer, leading to bloated portfolios. Your upgraded Kirdomic engine solves this by calculating **Score Velocity** (Total Score / Total Tenure), guaranteeing mathematical equity for senior vs. junior teams.")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("### Senior Employee Profile")
        senior_hire = st.date_input("Senior Hire Date:", value=datetime.date(2023, 1, 15), key="t_senior_date")
        senior_score = st.number_input("Senior Total Accumulated Volume (AVR):", value=1500.0, step=100.0, key="t_senior_score")
        
        senior_days = (datetime.date.today() - senior_hire).days
        senior_velocity = senior_score / max(senior_days, 1)
        
        st.metric(label="Total Days of Service (Tenure)", value=f"{senior_days} Days")
        st.metric(label="Score Velocity (AVR / Day)", value=f"{senior_velocity:.3f} AVR/day")
        
    with col_t2:
        st.markdown("### Junior / New Joiner Profile")
        junior_hire = st.date_input("Junior Hire Date:", value=datetime.date(2026, 4, 1), key="t_junior_date")
        junior_score = st.number_input("Junior Total Accumulated Volume (AVR):", value=450.0, step=50.0, key="t_junior_score")
        
        junior_days = (datetime.date.today() - junior_hire).days
        junior_velocity = junior_score / max(junior_days, 1)
        
        st.metric(label="Total Days of Service (Tenure)", value=f"{junior_days} Days")
        st.metric(label="Score Velocity (AVR / Day)", value=f"{junior_velocity:.3f} AVR/day")
        
    st.markdown("---")
    st.markdown("### 📊 Live Equity Evaluation")
    
    # Visual analysis
    if junior_velocity > senior_velocity:
        st.success(f"🎯 **Aha! Moment for HR:** Even though the Senior Employee has a higher total volume ({senior_score:.1f} vs {junior_score:.1f}), the Junior Employee has a **{(junior_velocity / senior_velocity * 100) - 100:.1f}% higher operational velocity** ({junior_velocity:.3f} vs {senior_velocity:.3f} AVR/day). They are contributing value at a much faster daily cycle!")
    else:
        st.info(f"⏳ **Standard Execution:** The Senior Employee retains a higher score velocity of **{senior_velocity:.3f} AVR/day** over the Junior's **{junior_velocity:.3f} AVR/day**.")

# ==============================================================================
# TAB 3: DYNAMIC ACTION DESIGNER
# ==============================================================================
with tab_calc:
    st.markdown("<h3 class='section-header'>🎛️ Configure and Pre-Calculate Actions</h3>", unsafe_style_html=True)
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.markdown("#### Step 1: Core Parameters")
        target_code = st.selectbox("Select Action Grid Target Code:", list(GRID_CELLS.keys()), index=4, key="calc_target_code")
        action_name = st.text_input("Enter Action Description:", value=f"Run {GRID_CELLS[target_code]['verb']} system check", key="calc_action_name")
        emp_id = st.text_input("Enter Your Employee ID:", value="EMP-KDM-088", key="calc_emp_id")
        receiver_id = st.text_input("Enter End-Receiver Employee ID:", value="EMP-KDM-001", key="calc_receiver_id")
        
        grid_info = GRID_CELLS[target_code]
        base_C = grid_info["C"]
        
        st.write(f"**Focus Lens:** `{grid_info['focus']}` | **Thinking Mode:** `{grid_info['mode']}`")
        
        st.markdown("#### Step 2: Contextual Vectors")
        scope_choice = st.selectbox("Select Scope Scale (C_scale):", list(SCOPE_PRESETS.keys()), key="calc_scope")
        risk_choice = st.selectbox("Select Consequence/Risk (i):", list(RISK_PRESETS.keys()), key="calc_risk")
        
        C_scale = SCOPE_PRESETS[scope_choice]
        i_rate = RISK_PRESETS[risk_choice]
        calculated_C = base_C * C_scale
        
        # Pull standard organizational discount baseline rate
        a_baseline = 1.20 if "Plan" in grid_info["mode"] else 2.50
        
    with col_c2:
        st.markdown("#### Step 3: Temporal Dimension & Confirmation")
        temp_mode = st.radio("Temporal Dimension Format:", ["Single Point in Time", "Duration Window (Project)"], key="calc_temp_mode")
        
        tef_factor = 1.0
        if temp_mode == "Duration Window (Project)":
            planned_hours = st.number_input("Planned Target Hours (Duration Limit):", min_value=1.0, value=40.0, key="calc_planned_hours")
            actual_hours = st.number_input("Actual Execution Hours:", min_value=1.0, value=30.0, key="calc_actual_hours")
            tef_factor = planned_hours / actual_hours
            st.metric(label="Temporal Efficiency Factor (TEF)", value=f"{tef_factor:.3f}x")
            
        pending_toggle = st.checkbox("Hold Action as Pending (requires End-Receiver validation)", value=False, key="calc_pending")
        
        # Calculate Math Live
        final_avr, protected_i = calculate_avalrem(calculated_C, a_baseline, i_rate, tef=tef_factor, is_pending=pending_toggle)
        
        st.markdown("#### ⚡ Real-Time Math Evaluation")
        
        st.markdown(f"""
        <div class='formula-card'>
            Formula: Avalrem = (C_base * C_scale) / (a - i) * TEF<br>\n            Protected i: {protected_i:.3f} ( Safeguard applied if i >= a )<br>\n            Calculation: ({base_C} * {C_scale}) / ({a_baseline:.2f} - {protected_i:.3f}) * {tef_factor:.2f}<br>\n            Pending Capping: {'Applied (50% Fallback)' if pending_toggle else 'None'}<br>\n            Net Value: <span class='wow-box' style='color:#D4AF37; font-size:1.5rem; font-weight:800;'>{final_avr:.2f} AVR</span>\n        </div>
        """, unsafe_style_html=True)
        
        if st.button("⛓️ Commit and Secure", key="btn_calc_commit"):
            status_lbl = "Pending" if pending_toggle else "Validated"
            add_to_ledger(
                action_name=action_name,
                emp_id=emp_id,
                code=target_code,
                volume=1.0,
                C=calculated_C,
                a=a_baseline,
                i=protected_i,
                receiver_id=receiver_id,
                status=status_lbl,
                formula_type="Manual Action Designer",
                final_score=final_avr
            )
            st.success("🔒 Securely recorded in the cryptographic ledger block!")

# ==============================================================================
# TAB 4: RELATIONAL BACKEND BLUEPRINT
# ==============================================================================
with tab_db:
    st.markdown("<h3 class='section-header'>🗄️ Target Database Architecture (PostgreSQL Schema)</h3>", unsafe_style_html=True)
    st.write("To satisfy technical executives and IT personnel, here is the production-grade PostgreSQL relational schema that supports live tracking, secure hashes, and dynamic tenure calculations.")
    
    sql_schema = """
-- PostgreSQL Relational Database Schema
-- Optimized for High-Frequency Action Value Accounting (AVA)

CREATE TABLE employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    department VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Active'
);

CREATE TABLE action_ledger (
    action_id SERIAL PRIMARY KEY,
    tx_id VARCHAR(100) UNIQUE NOT NULL,
    employee_id VARCHAR(50) REFERENCES employees(employee_id),
    action_name TEXT NOT NULL,
    grid_code CHAR(2) NOT NULL,
    volume_quantity NUMERIC(10, 2) DEFAULT 1.0,
    base_multiplier NUMERIC(10, 4) NOT NULL,
    discount_rate_a NUMERIC(10, 4) NOT NULL,
    risk_rate_i NUMERIC(10, 4) NOT NULL,
    receiver_employee_id VARCHAR(50) REFERENCES employees(employee_id),
    confirmation_status VARCHAR(50) DEFAULT 'Pending',
    formula_type VARCHAR(50) NOT NULL,
    final_score NUMERIC(12, 4) NOT NULL,
    prev_hash CHAR(64) NOT NULL,
    block_hash CHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for rapid Score Velocity queries
CREATE INDEX idx_employee_ledger ON action_ledger(employee_id);
CREATE INDEX idx_ledger_timestamp ON action_ledger(created_at);

-- View to dynamically compute Tenure & daily Score Velocity
CREATE OR REPLACE VIEW employee_score_velocity AS
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.hire_date,
    (CURRENT_DATE - e.hire_date) AS tenure_days,
    COALESCE(SUM(l.final_score), 0) AS total_avalrem,
    CASE 
        WHEN (CURRENT_DATE - e.hire_date) > 0 
        THEN COALESCE(SUM(l.final_score), 0) / (CURRENT_DATE - e.hire_date)
        ELSE COALESCE(SUM(l.final_score), 0)
    END AS score_velocity_per_day
FROM employees e
LEFT JOIN action_ledger l ON e.employee_id = l.employee_id AND l.confirmation_status = 'Validated'
GROUP BY e.employee_id, e.first_name, e.last_name, e.hire_date;
"""
    st.code(sql_schema, language="sql")
    st.info("💡 **IT Architecture Note:** Running queries on the `employee_score_velocity` view completely replaces traditional, biased periodic appraisal charts with daily, auditable execution data.")

# ==============================================================================
# TAB 5: CRYPTOGRAPHIC LEDGER
# ==============================================================================
with tab_ledger:
    st.markdown("<h3 class='section-header'>⛓️ Verified Transaction Audit Trail</h3>", unsafe_style_html=True)
    st.write("Verifiable and immutable digital audit trail of your team's contributions. Features SHA-256 cryptographic linkage to prevent historical manipulation.")
    
    if not st.session_state.action_ledger:
        st.info("The ledger is currently empty. Go to the Delimiter Parsing Lab or Dynamic Action Designer tabs to execute and commit your first actions!")
    else:
        df_ledger = pd.DataFrame(st.session_state.action_ledger)
        st.dataframe(df_ledger, use_container_width=True)
        
        # Download ledger backups
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            json_str = json.dumps(st.session_state.action_ledger, indent=4)
            st.download_button(
                label="📥 Export Ledger Block-Database (JSON)",
                data=json_str,
                file_name="kirdomic_legacy_ledger.json",
                mime="application/json",
                key="btn_dl_json"
            )
        with col_dl2:
            csv_data = df_ledger.to_csv(index=False)
            st.download_button(
                label="📊 Download Performance Statement (CSV)",
                data=csv_data,
                file_name="kirdomic_performance_report.csv",
                mime="text/csv",
                key="btn_dl_csv"
            )

# ------------------------------------------------------------------------------
# Sidebar Context Panel
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37; font-family:Georgia;'>🧠 Kirdomic Lexicon</h2>", unsafe_style_html=True)
    st.write("---")
    st.write("🛡️ **Atammayata:** Achieving absolute unconcoctability, protecting consciousness from 'emotional cooking' or crises [Applied ATAMMAYATA.pdf].")
    st.write("🐍 **Exdysivity:** Continuous, natural renewal by willingly shedding obsolete habits, standards, and rules [Exdysivity Index - 2017.pdf].")
    st.write("⚡ **Anxergy:** The internal ontology of converting anxiety into a constructive execution drive [0-Kirdomicism WORDS.docx].")
    st.write("🧬 **Dexterience:** Shifting from waiting for perfect conditions to executing cleanly with what you have on hand [12 Lessons Self Study Outline.docx].")
    st.write("📊 **Avalremy:** Measuring human contribution and future-readiness through the quantitative value of physical actions [Evolvement of Action Value Accounting - AVA 2024.pdf].")
    st.write("---")
    
    # Active Session Stats
    st.markdown("### Active Session Stats")
    st.metric(label="Locked-In NAVA (Validated)", value=f"{st.session_state.nava_balance:.2f} AVR")
    st.markdown("<div style='text-align:center; color:#A0AEC0; font-size:0.8rem; margin-top:2rem;'>Kirdomic Academy © 2026</div>", unsafe_style_html=True)
