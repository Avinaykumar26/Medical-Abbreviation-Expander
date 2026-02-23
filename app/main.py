import sys
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure repo root is on sys.path so local imports like `models.*` work
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from models.resolver import AbbreviationResolver
from models.embed_disambiguator import EmbedDisambiguator
from app.utils import find_abbreviations, highlight_expansions

# --- Page Config & Styling ---
st.set_page_config(
    page_title="Medical Abbreviation Expander",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/brain.png", width=80)
    st.title("Settings & Info")
    
    use_embeddings = st.checkbox(
        "Enable Contextual Disambiguation", 
        value=False,
        help="Uses Sentence-Transformers to pick the best expansion based on surrounding text."
    )
    
    st.divider()
    st.info("""
    **How it works:**
    1. Detects acronyms (2-5 caps).
    2. Looks up meanings in `abbreviations.csv`.
    3. (Optional) Uses AI to disambiguate.
    """)
    
    if st.button("Clear Analytics Log"):
        log_path = os.path.join(ROOT, "data", "analysis_data.csv")
        if os.path.exists(log_path):
            os.remove(log_path)
            st.success("Log cleared!")

# --- Initialize Resolver ---
@st.cache_resource
def get_resolver():
    return AbbreviationResolver()

@st.cache_resource
def get_disambiguator():
    return EmbedDisambiguator()

resolver = get_resolver()
disamb = None
if use_embeddings:
    with st.spinner("Loading AI model..."):
        disamb = get_disambiguator()

# --- Main UI ---
st.title("🧠 Medical Abbreviation Expander + Evaluator")
st.markdown("---")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("Input Clinical Text")
    text_input = st.text_area("Paste clinical note text here", height=250, placeholder="e.g., Pt c/o SOB and elevated BP. Hx of HTN and DM.")
    uploaded = st.file_uploader("Or upload a .txt file", type=['txt'])
    if uploaded and not text_input:
        text_input = uploaded.read().decode('utf-8')

with col_b:
    st.subheader("Results & Actions")
    process_btn = st.button("🔍 Expand Abbreviations")
    
    if process_btn:
        if not text_input:
            st.warning("Please provide text or upload a file.")
        else:
            with st.spinner("Processing text..."):
                abbrs = find_abbreviations(text_input)
                expansions = {}

                for abbr in abbrs:
                    candidates = resolver.lookup(abbr)
                    if not candidates:
                        expansions[abbr] = (f"[UNKNOWN]", 0.0)
                        continue
                    
                    if len(candidates) == 1 or not use_embeddings:
                        chosen, conf = resolver.resolve(abbr, context=text_input)
                        expansions[abbr] = (chosen, conf)
                    else:
                        # Extract basic context (approximate sentence)
                        sentences = text_input.replace('\n', ' ').split('.')
                        context_sentence = next((s for s in sentences if abbr in s), text_input)
                        chosen, sim = disamb.choose_candidate(candidates, context_sentence)
                        expansions[abbr] = (chosen, float(sim))

                # --- Visual Display ---
                st.success(f"Detected {len(abbrs)} abbreviations!")
                
                rows = [{"abbr": a, "expansion": e[0], "confidence": round(e[1], 3)} for a, e in expansions.items()]
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

                # Annotated text
                annotated = highlight_expansions(text_input, expansions)
                st.markdown("### Annotated Text")
                st.markdown(f'<div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">{annotated}</div>', unsafe_allow_html=True)

                # Download
                out_text = text_input
                for a, (exp, _) in expansions.items():
                    out_text = out_text.replace(a, f"{a} ({exp})")
                st.download_button("💾 Download Expanded Text", data=out_text, file_name="expanded_note.txt")

                # --- Logging ---
                try:
                    data_dir = os.path.join(ROOT, "data")
                    os.makedirs(data_dir, exist_ok=True)
                    log_path = os.path.join(data_dir, "analysis_data.csv")

                    log_df = pd.DataFrame(rows)
                    log_df["text_length"] = len(text_input)
                    log_df["use_embeddings"] = use_embeddings
                    log_df["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
                        old = pd.read_csv(log_path)
                        # Harmonize older/mixed logs if they exist
                        if 'Abbreviation' in old.columns:
                            old['abbr'] = old['abbr'].fillna(old['Abbreviation'])
                        if 'Expansion' in old.columns:
                            old['expansion'] = old['expansion'].fillna(old['Expansion'])
                        
                        # Keep only standard columns to avoid growth
                        standard_cols = ['abbr', 'expansion', 'confidence', 'text_length', 'use_embeddings', 'timestamp']
                        old = old[[c for c in standard_cols if c in old.columns]]
                        
                        new = pd.concat([old, log_df], ignore_index=True)
                    else:
                        new = log_df

                    new.to_csv(log_path, index=False)
                except Exception as e:
                    st.error(f"Error saving logs: {e}")

# --- Evaluation Section ---
st.markdown("---")
st.header("📊 Performance Dashboard")

truth_path = os.path.join(ROOT, "data", "ground_truth.csv")
log_path = os.path.join(ROOT, "data", "analysis_data.csv")

if os.path.exists(truth_path) and os.path.exists(log_path):
    try:
        preds = pd.read_csv(log_path)
        
        # Harmonize columns for eval
        if 'Abbreviation' in preds.columns:
            preds['abbr'] = preds['abbr'].fillna(preds['Abbreviation'])
        if 'Expansion' in preds.columns:
            preds['expansion'] = preds['expansion'].fillna(preds['Expansion'])
            
        truth = pd.read_csv(truth_path)
        
        # Ensure we don't have duplicate 'abbr' columns before merging
        preds = preds.loc[:, ~preds.columns.duplicated()]
        
        merged = pd.merge(preds, truth, on="abbr", how="inner")
        if not merged.empty:
            merged["correct"] = merged.apply(
                lambda x: 1 if str(x["expansion"]).strip().lower() == str(x["true_expansion"]).strip().lower() else 0, axis=1
            )

            precision = merged["correct"].sum() / len(merged)
            accuracy = precision # Simple accuracy: correct / total samples
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Precision", f"{precision:.2%}")
            m2.metric("Accuracy", f"{accuracy:.2%}")
            m3.metric("Samples", len(merged))
            m4.metric("Correct", merged["correct"].sum())

            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Results Distribution")
                fig, ax = plt.subplots(figsize=(8, 5))
                counts = merged["correct"].value_counts().sort_index()
                labels = ["Incorrect", "Correct"] if len(counts) == 2 else (["Correct"] if 1 in counts.index else ["Incorrect"])
                sns.barplot(x=labels, y=counts.values, palette=["#ff6b6b", "#51cf66"], ax=ax)
                ax.set_ylabel("Count")
                st.pyplot(fig)

            with c2:
                st.subheader("Trend Over Time")
                # Group by run (timestamp)
                if "timestamp" in merged.columns:
                    merged["timestamp"] = pd.to_datetime(merged["timestamp"])
                    trend = merged.groupby("timestamp")["correct"].mean().reset_index()
                    fig2, ax2 = plt.subplots(figsize=(8, 5))
                    ax2.plot(trend["timestamp"], trend["correct"], marker='o', linestyle='-', color='#4dabf7')
                    ax2.set_ylim(-0.1, 1.1)
                    ax2.set_title("Accuracy per Run")
                    plt.xticks(rotation=45)
                    st.pyplot(fig2)
        else:
            st.info("No matching samples in logs for evaluation against ground truth.")
    except Exception as e:
        st.error(f"Evaluation error: {e}")
else:
    st.info("💡 Evaluation will appear here once you've run some expansions and `ground_truth.csv` is present in the `data/` folder.")
