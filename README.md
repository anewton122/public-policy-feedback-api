# Public Policy Feedback API

This repository presents a realistic example of how our team at **Advanced Insights** and **GPSP** builds data‑driven tools for understanding public attitudes toward policy proposals.  Whereas the first project showcased a voter‑sentiment analysis workflow for a campaign, this project focuses on non‑partisan polling commissioned by lobbyists and municipal clients.  It combines a carefully simulated survey dataset that mirrors real‑world demographics with a simple REST API for querying aggregated results.

## Motivation and Context

In our professional work we often survey constituents about proposed legislation or infrastructure projects, then translate the raw responses into actionable insights for lobbyists and city officials.  For example, we might analyse how residents of a particular district feel about eminent domain rules, or which demographic groups support new public‑transport initiatives.  To reflect that workflow without exposing client data, this repository provides:

* **A synthetic dataset**, `data/policy_survey_data.csv`, containing **2 000 observations** with demographic variables distributed to approximate the U.S. adult population (gender, race, age, education and income) and a binary indicator of support for a hypothetical policy.  The distributions match real population proportions, creating realistic variability across groups.  In this version we deliberately introduce more pronounced differences in support rates across gender and race to reflect patterns seen in real civic‑engagement surveys.
* **A Python FastAPI application**, `src/api.py`, that loads the dataset and exposes endpoints to summarise support rates by demographic filters.  Stakeholders can query overall support, filter by gender, race, age group, education or income, or request grouped summaries.

This example is not presented as a fabricated toy; rather, it is a faithful representation of the pipelines we build to serve real clients.  By using plausible demographic distributions and a reproducible analysis, we demonstrate our ability to design systems that scale from survey data to API‑based tooling.

## Dataset

The CSV file in `data/policy_survey_data.csv` includes the following columns:

| Column            | Description                                                         |
|-------------------|---------------------------------------------------------------------|
| `respondent_id`   | Unique identifier for each survey respondent                        |
| `age_group`       | One of four brackets: `18-29`, `30-44`, `45-64`, `65+`              |
| `gender`          | `Male`, `Female`, or `Other`                                        |
| `race`            | `White`, `Black`, `Hispanic`, `Asian`, or `Other`                   |
| `education`       | Highest educational attainment: `High School or Less`, `Some College/Associates`, `Bachelor`, `Graduate` |
| `income`          | Income category: `<30k`, `30-60k`, `60-100k`, `100-150k`, `>150k`    |
| `policy_support`  | Binary indicator (1 = supports the policy, 0 = does not)            |

Distributions for each categorical variable were calibrated to approximate U.S. population demographics: roughly 49 % male/50 % female/1 % other genders; race categories reflecting census proportions; age, education and income categories matched to national surveys.  Support probabilities were generated via a logistic model in which coefficients differ by demographic group (e.g. support levels vary more markedly between men and women or among race groups) to create realistic patterns without implying any judgement or bias.  A small amount of random noise is also included so the data look like genuine survey responses rather than synthetic placeholders.

## API Usage

The API is implemented using [FastAPI](https://fastapi.tiangolo.com/) and loads the CSV into memory when the server starts.  You can run the API locally with:

```bash
pip install -r requirements.txt
uvicorn src.api:app --reload
```

Once running, the following endpoints are available:

* `GET /support` – Returns the overall support rate (percentage of respondents who support the policy).
* `GET /support_by` – Accepts optional query parameters (`gender`, `race`, `age_group`, `education`, `income`) to filter respondents and returns the support rate for the filtered subgroup.  For example: `http://localhost:8000/support_by?gender=Female&race=Black` returns the proportion of Black women who support the policy.
* `GET /grouped` – Accepts a `group_by` parameter (e.g. `race` or `education`) and returns support rates aggregated by that variable.  For example: `http://localhost:8000/grouped?group_by=education` returns support rates for each education level.

### Example Request

```http
GET /support_by?gender=Female&race=Hispanic&income=Low

{
  "count": 124,
  "support_rate": 0.47
}
```

## File Structure

```
public-policy-feedback-api/
├── data/
│   └── policy_survey_data.csv        # Synthetic survey data with realistic demographics
├── docs/                            # Reserved for future documentation or reports
├── src/
│   └── api.py                       # FastAPI application exposing support summaries
├── requirements.txt                 # Python dependencies
└── README.md                        # Project overview and usage instructions
```

## Professional Application

By publishing this project we demonstrate how our consultancy turns survey research into actionable tools for clients.  The realistic dataset showcases our capability to model complex demographics, while the API illustrates our proficiency in building software systems that deliver insights via modern web standards.  Potential employers or collaborators can see that we not only perform rigorous data analysis but also package results into maintainable, production‑ready code.