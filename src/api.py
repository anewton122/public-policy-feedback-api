"""
FastAPI application for querying public policy survey responses.

The API reads a synthetic dataset of survey responses with realistic demographic
distributions and exposes endpoints to compute overall support rates, filter
support by demographic attributes, and aggregate support by a chosen field.

Endpoints:

* `GET /support` — Return the overall support rate and total count of respondents.
* `GET /support_by` — Filter the dataset by optional demographic parameters and
  return the support rate and count for the filtered group.
* `GET /grouped` — Group the dataset by a specified categorical field and
  return support rates for each group.

The dataset is loaded into memory at startup for efficient queries.  See
README.md for full project context and usage examples.
"""

from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query
import pandas as pd


# Read the synthetic survey data at startup
DATA_PATH = "data/policy_survey_data.csv"
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    # Provide a helpful error if the data file is missing
    raise RuntimeError(
        f"Expected data file at '{DATA_PATH}'. Please generate the dataset and place it in the data directory."
    )

app = FastAPI(
    title="Public Policy Feedback API",
    description="API for summarising support for a policy across demographic groups.",
    version="0.1.0",
)


def calculate_support_rate(sub_df: pd.DataFrame) -> float:
    """Compute the support rate (mean) for the policy within a DataFrame.

    Returns 0.0 if the DataFrame is empty to avoid division by zero.
    """
    if sub_df.empty:
        return 0.0
    return float(sub_df["policy_support"].mean())


@app.get("/support")
def overall_support() -> Dict[str, Any]:
    """Return the overall support rate and total respondent count."""
    rate = calculate_support_rate(df)
    return {"count": int(len(df)), "support_rate": round(rate, 3)}


@app.get("/support_by")
def support_by(
    gender: Optional[str] = Query(None, description="Filter by gender"),
    race: Optional[str] = Query(None, description="Filter by race"),
    age_group: Optional[str] = Query(None, description="Filter by age group"),
    education: Optional[str] = Query(None, description="Filter by education level"),
    income: Optional[str] = Query(None, description="Filter by income category"),
) -> Dict[str, Any]:
    """Return support rate for respondents matching the given filters.

    The function filters the global DataFrame based on any provided query
    parameters.  If no rows match the filters, a 404 is returned.
    """
    sub_df = df.copy()
    # Apply filters one by one
    if gender:
        sub_df = sub_df[sub_df["gender"].str.casefold() == gender.casefold()]
    if race:
        sub_df = sub_df[sub_df["race"].str.casefold() == race.casefold()]
    if age_group:
        sub_df = sub_df[sub_df["age_group"].str.casefold() == age_group.casefold()]
    if education:
        sub_df = sub_df[sub_df["education"].str.casefold() == education.casefold()]
    if income:
        sub_df = sub_df[sub_df["income"].str.casefold() == income.casefold()]

    if sub_df.empty:
        raise HTTPException(status_code=404, detail="No respondents match the given filters.")
    rate = calculate_support_rate(sub_df)
    return {"count": int(len(sub_df)), "support_rate": round(rate, 3)}


@app.get("/grouped")
def support_grouped(group_by: str = Query(..., description="Column to group by")) -> List[Dict[str, Any]]:
    """Return support rates aggregated by the specified column.

    The group_by parameter must correspond to a categorical column in the
    dataset.  The endpoint returns a list of objects with the group value,
    respondent count and support rate.  Invalid group names return 400.
    """
    valid_columns = {"gender", "race", "age_group", "education", "income"}
    if group_by not in valid_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid group_by '{group_by}'. Must be one of {sorted(valid_columns)}.",
        )

    grouped_df = (
        df.groupby(group_by)["policy_support"]
        .agg(["count", "mean"])
        .reset_index()
        .rename(columns={"mean": "support_rate"})
    )
    # Round support rates for readability
    grouped_df["support_rate"] = grouped_df["support_rate"].round(3)
    return grouped_df.to_dict(orient="records")
