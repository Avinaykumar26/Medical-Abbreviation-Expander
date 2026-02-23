# 🧠 Medical Abbreviation Expander

> **A Smart NLP Tool to Decode and Analyze Medical Abbreviations in Clinical Text**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-2.2%2B-orange)](https://www.sbert.net/)

---

## 👤 Author

**A VINAY KUMAR**

- GitHub: [@Avinaykumar26](https://github.com/Avinaykumar26)
- Email: [avinaykumar2004@gmail.com](mailto:avinaykumar2004@gmail.com)
- working link :- https://medical-abbreviation-expander-projwila.streamlit.app/
- ( copy past this in browser and view the app )

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Docker](#-docker-deployment)
- [Evaluation](#-evaluation--metrics)
- [Data Files](#-data-files)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## Overview

The **Medical Abbreviation Expander** is an AI-powered Streamlit application that automatically detects and expands medical abbreviations found in clinical text. It is designed to improve readability and reduce ambiguity in medical notes, discharge summaries, and other healthcare documents.

The tool supports two modes of operation:

| Mode | Description |
|------|-------------|
| **Rule-Based Lookup** | Fast dictionary-based resolution using a curated CSV of medical abbreviations |
| **Contextual Embeddings** | Uses Sentence Transformers (`all-MiniLM-L6-v2`) to disambiguate abbreviations with multiple possible expansions based on surrounding context |

Additionally, the app includes a built-in **Evaluation Dashboard** with Precision & Accuracy metrics, bar charts, and trend-over-time visualizations — all computed automatically against a ground truth dataset.

---

## ✨ Features

- 🔍 **Auto-Detect Abbreviations** — Identifies all-caps tokens (2–5 characters) in clinical text
- 📖 **Rule-Based Expansion** — Resolves unambiguous abbreviations using a CSV dictionary
- 🤖 **Contextual Disambiguation** — Leverages sentence embeddings (cosine similarity) for multi-candidate abbreviations
- 📝 **Annotated Text View** — Displays expanded abbreviations inline with hover-over confidence scores
- 💾 **Download Expanded Text** — Export the annotated clinical note as a `.txt` file
- 📊 **Evaluation Dashboard** — Live Precision & Accuracy metrics with bar charts and trend graphs
- 📁 **Analytics Logging** — Auto-saves every analysis run to `data/analysis_data.csv`
- 📎 **File Upload Support** — Upload `.txt` files directly into the app
- 🐳 **Docker Ready** — Includes a `Dockerfile` for one-command containerized deployment
- 🧪 **Unit Tests** — Pytest-based test suite for the resolver module

---

## 🎬 Demo

After launching the app, paste a clinical note or upload a `.txt` file:

```
Pt c/o SOB and elevated BP. Hx of HTN and DM. Echo shows RA enlargement.
Rx: ACE inhibitor.
```

The app will:
1. Detect abbreviations: `SOB`, `BP`, `HTN`, `DM`, `RA`
2. Expand each one with confidence scores
3. Display annotated text with inline expansions
4. Show evaluation metrics (if ground truth is available)

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Interactive web UI |
| [Pandas](https://pandas.pydata.org/) | Data handling and CSV I/O |
| [Sentence Transformers](https://www.sbert.net/) | Contextual embedding-based disambiguation |
| [PyTorch](https://pytorch.org/) | Backend for transformer models |
| [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) | Data visualization and charts |
| [spaCy](https://spacy.io/) | NLP utilities |
| [Pytest](https://pytest.org/) | Unit testing framework |

---

## 📁 Project Structure

```
Medical-Abbreviation-Expander/
│
├── app/
│   ├── main.py                    # Streamlit main app + evaluation dashboard
│   └── utils.py                   # Helper functions (find abbreviations, highlight)
│
├── models/
│   ├── resolver.py                # Rule-based abbreviation resolver (CSV lookup)
│   └── embed_disambiguator.py     # Embedding model for contextual disambiguation
│
├── data/
│   ├── abbreviations.csv          # Base abbreviation dictionary (abbr → expansion)
│   ├── ground_truth.csv           # Ground truth labels for evaluation
│   ├── sample_notes.txt           # Sample clinical note for testing
│
├── notebooks/
│   └── abbreviation_analysis.ipynb  # Jupyter notebook for in-depth analysis
│
├── tests/
│   └── test_resolver.py           # Unit tests for the resolver module
│
├── Dockerfile                     # Docker containerization config
├── requirements.txt               # Python dependencies
├── LICENSE                        # Apache 2.0 License
├── .gitignore                     # Git ignore rules
└── README.md                      # Project documentation (you are here)
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+** installed on your system
- **pip** package manager
- (Optional) **Docker** for containerized deployment

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Tarunyl/Medical-Abbreviation-Expander.git
cd Medical-Abbreviation-Expander
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv .venv
```

**Activate it:**

| OS | Command |
|---|---|
| Windows | `.venv\Scripts\activate` |
| macOS / Linux | `source .venv/bin/activate` |

### Step 3 — Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** On first run with embeddings enabled, the `all-MiniLM-L6-v2` model (~80 MB) will be automatically downloaded.

---

## 📖 Usage

### Running the Streamlit App

```bash
streamlit run app/main.py
```

Or, if `streamlit` is not in your PATH:

```bash
python -m streamlit run app/main.py
```

Then open your browser at:

```
http://localhost:8501
```

### App Workflow

1. **Paste** a clinical note in the text area, or **upload** a `.txt` file
2. *(Optional)* Enable **contextual disambiguation** via the sidebar checkbox
3. Click **🔍 Expand Abbreviations**
4. View the expansion table, annotated text, and evaluation metrics
5. **Download** the expanded text as a `.txt` file

---

## 🐳 Docker Deployment

Build and run the app in a Docker container:

```bash
# Build the image
docker build -t medical-abbr-expander .

# Run the container
docker run -p 8501:8501 medical-abbr-expander
```

Access the app at `http://localhost:8501`.

---

## ☁️ Streamlit Cloud Deployment

The easiest way to host this app for free is via **[Streamlit Community Cloud](https://streamlit.io/cloud)**:

1. **Push** your code to a GitHub repository.
2. Log in to [Streamlit Cloud](https://share.streamlit.io/).
3. Click **New app**, then select your repository, branch, and main file path: `app/main.py`.
4. Click **Deploy!**

> **Note:** Streamlit Cloud will automatically detect `requirements.txt` and install all dependencies. First-time deployment may take 2-3 minutes as it downloads the embedding models.

---

## 📈 Evaluation & Metrics

### In-App Evaluation

The app automatically evaluates predictions against `data/ground_truth.csv` after each expansion run. It displays:

- **Precision** — Fraction of correctly expanded abbreviations
- **Accuracy** — Overall correctness score
- **Bar Chart** — Correct vs. Incorrect predictions (color-coded)
- **Trend Chart** — Precision & Accuracy over time across multiple runs

### Jupyter Notebooks

A notebook is included for deeper analysis:

```bash
jupyter notebook
```

| Notebook | Description |
|---|---|
| `notebooks/abbreviation_analysis.ipynb` | Extended analysis of abbreviation patterns, confidence, and distributions |

---

## 📂 Data Files

| File | Format | Description |
|---|---|---|
| `abbreviations.csv` | `abbr, expansion, notes` | Dictionary of medical abbreviations. Use `\|` to separate multiple expansions. |
| `ground_truth.csv` | `abbr, true_expansion` | Ground truth labels for evaluation |
| `sample_notes.txt` | Plain text | Sample clinical note for quick testing |
| `analysis_data.csv` | Auto-generated | Logged results from each app run |
| `evaluation_results.csv` | Auto-generated | Detailed evaluation output |

### Adding New Abbreviations

Edit `data/abbreviations.csv` to add new entries:

```csv
abbr,expansion,notes
ECG,Electrocardiogram,diagnostic test
ICU,Intensive Care Unit,hospital unit
PRN,As Needed,medication frequency
```

For ambiguous abbreviations with multiple meanings, separate expansions with `|`:

```csv
MS,Multiple Sclerosis|Mitral Stenosis,ambiguous
```

---

## 🧪 Testing

Run the test suite with Pytest:

```bash
pytest tests/ -v
```

The tests verify:
- ✅ Unambiguous abbreviation lookup and resolution
- ✅ Ambiguous abbreviation handling with confidence scoring
- ✅ Resolver returns correct data types

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Commit** your changes: `git commit -m "Add my feature"`
4. **Push** to the branch: `git push origin feature/my-feature`
5. **Open** a Pull Request

### Ideas for Contributions

- 📚 Expand the `abbreviations.csv` dictionary with more medical terms
- 🌐 Add multilingual abbreviation support
- 🧠 Integrate a biomedical language model (e.g., BioBERT, PubMedBERT)
- 📊 Add more evaluation metrics (F1-score, recall)
- 🎨 Improve the Streamlit UI/UX

---


## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the healthcare community
</p>
