# Flood Monitoring data analysis and ML

## Setup

```
conda env create -f environment.yml
conda activate river-levels
pre-commit install
```

## ./river-levels-uk

Investigating UK river level trends using data from riverlevels.uk

## Streamlit interface

The data visualisation and analytic work is centered around a multipage streamlit app. This can be started with

```
streamlit run app.py
```