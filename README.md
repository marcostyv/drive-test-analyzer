# Drive Test Analyzer

Python tool and local web app to analyse 4G/5G drive test logs: data cleaning, radio KPI analysis (RSRP, RSRQ, SNR, CQI), coverage maps and automated reporting.

> Work in progress. Write your own description here at the end of week 1.

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data
Real 5G/LTE traces from an Irish mobile operator, collected with G-NetTrack Pro:
D. Raca, D. Leahy, C.J. Sreenan and J.J. Quinlan. *Beyond Throughput, The Next Generation: A 5G Dataset with Channel and Context Metrics.* ACM MMSys 2020. — https://github.com/uccmisl/5gdataset

The data is not included in this repository. Download it and extract it into `data/raw/`.
