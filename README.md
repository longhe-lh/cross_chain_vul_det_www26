# LLM-BridgeGuard

**LLM-BridgeGuard** is a framework for **detecting vulnerabilities in cross-chain bridges** with the help of large language models (LLMs).
 It integrates **business logic graphs**, **code dependency graphs**, and a **dynamic rule base** to provide automated, accurate, and generalizable detection.



## 🔍 What It Does

- Builds a **joint graph (ECBLG)** that links business logic and code logic of cross-chain bridges
- Uses a **dynamic rule base** to capture known and evolving attack patterns
- Applies **LLM-based inference** to detect vulnerabilities with explanations and evidence



## 📂 Project Layout

```
├── dataset/             # Datasets: cross-chain bridge contracts, annotations
├── ecblg_build/         # ECBLG construction (CBLG + CADG → ECBLG)
├── global_config/       # Global configuration (parameters, model settings)
├── llm_teacher/         # LLM Teacher for rule generation & knowledge distillation
├── llm_student/         # LLM Student for vulnerability detection
├── utils/               # Utility functions (logging, preprocessing, evaluation)
├── scripts/             # Helper scripts (build graph, run detection, evaluate)
├── results/             # Detection reports & evaluation outputs
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

------

## 🚀 Quick Start

```
git clone https://github.com/your-org/LLM-BridgeGuard.git
cd LLM-BridgeGuard

pip install -r requirements.txt

# Run detection on a sample bridge contract
python scripts/run_detection.py
```

Results will be stored in `results/`.

------

## 📖 Reference

This project is based on the paper:
 *LLM-BridgeGuard: LLM for Logic and Knowledge-Driven Vulnerability Detection in Cross-Chain Bridge Smart Contracts*
