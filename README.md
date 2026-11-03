# Drive Test Analyzer

This repo is a Streamlit application which analyses drive-tests from the dataset "Raca et al., MMSys 2020, Cork, Ireland" [https://github.com/uccmisl/5gdataset](url), showing graphs, histograms and a map that highlights colour-codes RSRP coverage (Excellent/Good/Fair/Poor) along the routes.


It takes a CSV file and prepares it by modifying some data types and cleaning out-of-range values, such as RSRP (3GPP reporting range). Thus, each CSV is prepared for data analysis, calculation and graphics.
The app loads all CSVs in the folder (83 files, ~188k samples) into a single dataset. There are also other functionalities such as filtering (by service, mobility or RAT) and overview of radio KPI distributions.

This app was built with Python, pandas and Streamlit.



## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data
Real 5G/LTE traces from an Irish mobile operator, collected with G-NetTrack Pro:
D. Raca, D. Leahy, C.J. Sreenan and J.J. Quinlan. *Beyond Throughput, The Next Generation: A 5G Dataset with Channel and Context Metrics.* ACM MMSys 2020. — https://github.com/uccmisl/5gdataset

The data is not included in this repository. Download it and extract it into `data/raw/`.
