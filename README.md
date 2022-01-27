# Flood Monitoring data analysis and ML

## Setup

```
conda env create -f environment.yml
conda activate river-levels
pre-commit install
```

## ./river-levels-uk

Investigating UK river level trends using data from riverlevels.uk

## River level DVC pipeline
```
    +-------------------+    
    | download_stations |    
    +-------------------+    
              *              
              *              
              *              
+--------------------------+ 
| cache_catchment_readings | 
+--------------------------+ 
```

The cache_catchment_readings maintains a cache of catchment data as a dvc checkpoint file. This means that data is not overwritten upon rerunning the pipeline, but instead new readings are appended to it.

To run the pipeline and cache the latest readings for the selected catchments, run:

```
dvc exp run
```

If you want to clear this data cache and start again, you can reset the checkpoint files with:

```
dvc exp run --reset
```

## Streamlit interface

The data visualisation and analytic work is centered around a multipage streamlit app. This can be started with

```
streamlit run app.py
```