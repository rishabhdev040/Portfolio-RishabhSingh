# Customer Segmentation with K-Means

This project explores customer purchasing behavior and groups customers into segments using K-Means clustering.

## Workflow

- Inspected the customer dataset with Pandas, including summary statistics, column types, missing values, and categorical value counts.
- Removed rows containing missing values and created derived features such as customer age, total children, and total spend across product categories.
- Encoded categorical education and marital-status fields.
- Selected the six clustering features: `Age`, `Income`, `NumWebPurchases`, `NumStorePurchases`, `NumWebVisitsMonth`, and `Total_spend`.
- Standardized the features with `StandardScaler`.
- Compared K-Means inertia for cluster counts from 2 through 9, then fitted a five-cluster model.
- Saved the fitted K-Means model and scaler for reuse by the Streamlit application.

## Files

- `customer_segementation(kmeans).ipynb` — exploratory analysis, feature preparation, scaling, elbow-method inspection, and K-Means clustering.
- `main.py` — Streamlit interface for entering customer attributes and predicting a cluster.
- `kmeans_model.pkl` — trained K-Means model.
- `scaler.pkl` — fitted feature scaler used before prediction.
- `requirements.txt` — Python dependencies.

## Setup

Use Python 3.10 or newer and install the dependencies:

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
streamlit run main.py
```

The model and scaler files must remain beside `main.py` in the project directory (or update the paths in `main.py`).

## Input features

The application accepts age, income, total spend, online purchases, in-store purchases, and monthly web visits. Inputs are transformed with the saved scaler before the saved K-Means model predicts a cluster.

## Notes

The notebook expects the source dataset file `customer_segmentation.csv`, which is not included here. The serialized model artifacts are included so the Streamlit prediction interface can use the trained pipeline without retraining.
