# Table of Contents

   1. [Description](#description)
   2. [Notes for Reviewers](#notes-for-reviewers)
   3. [Getting Started](#getting-started)
      1. [Prerequisites](#prerequisites)
      2. [Local Development](#local-development)
      3. [Docker](#docker)

## Description

This module converts flat CSV data into a nested JSON hierarchy based on up to  
three levels and an `item_id`. It handles validation rules such as required  
fields and disallows skipped hierarchy levels. Designed for clean API  
integration, it returns structured output.

## Getting Started

### Prerequisites

- Python 3.13  
- [`uv`](https://github.com/astral-sh/uv) (install with `pip install uv`)  
- [`just`](https://github.com/casey/just) (optional but recommended)  
- Docker (optional, for containerized runs)

You can run the project locally with Python and `uv`, or use Docker if you  
prefer a containerized environment. `just` is used to simplify common commands  
for both setups.

To install dependencies and run application:

```shell
just prod-sync
just run
```

### Local Development

```shell
just dev-sync
just dev
```

### Tests

To run tests:

```shell
just test
```

### Docker

Application can be run inside docker:

```shell
just docker
```

## Notes for Reviewers

### Task 1

Regarding the code: I think it's pretty solid and built the right way –
modular, separated concerns, easy to follow. In a real production setup,
we'd wrap it with all the usual trimmings: a proper CI/CD pipeline
kicking off tests and deployments, structured logging piped somewhere
useful (like Splunk/Datadog), better error handling and alerting,
monitoring dashboards, the works.

For this exercise though, I included the basics – Docker to run it, a
Justfile for common commands, and README – enough to show it works and
how you'd integrate it. I skipped stuff like API versioning or complex
routing since the requirement was just to hit `localhost:8080` directly.
Kept it lean to focus on the core task.

### Tasks 2

#### On a high level, how would you design a data model/schema in a database, e.g. PostgreSQL or BigQuery, to support the above forecast validation?

I've split the schema into distinct tables to keep data types separate. I have a
forecasts table for weekly predictions, an actual table for historical sales and
unit costs, and a price log table that records all price change events with  
timestamps. The validation_runs table holds the details of each experiment’s  
training and test periods and links to both forecasts and metrics via a unique  
run ID. This modular design not only makes it easier to version and compare  
different model experiments but also scales efficiently using PostgreSQL for  
transactional work and BigQuery for large-scale analytics.

#### How would you make sure that we can Store the outputs of several validation rounds, i.e. successively rolled windows in the rolling validation strategy? Store the outputs of several model experiments?

I ensure proper tracking by assigning a unique run_id to every validation
round, which represents a specific train/test window in the rolling validation
strategy. Each forecast and its evaluation metrics are linked to this run_id,
allowing us to trace back and compare results across time. Additionally, an
experiment_id is used to differentiate outputs from various model experiments.
This approach provides a clear separation of results for each validation round
and experiment, making performance comparisons straightforward.

#### How would you design a pipeline that allows for running parameterized validation?

A parameterized validation pipeline can be implemented using orchestration
tools like Airflow or Prefect, which allow you to pass in dynamic parameters
such as training and testing windows, as well as model configurations. This
setup automatically slices the data, executes the model training, and
evaluates the forecasts. It provides a repeatable and flexible process that
can easily adapt to different scenarios by simply changing the input
parameters. This ensures consistent and robust validation cycles for our
forecasting models.

#### Some features that act like an event log, like price, will need to be "gridded" to the relevant date. What method would you use to join it into the relevant time window?

For gridding event log features like price, I use an as-of join to match each
calendar week with the latest price event that occurred on or before the week’s
start. This ensures that every time window is assigned the appropriate price
value. Technically, this can be implemented using SQL lateral joins or window
functions to efficiently retrieve the latest event. This approach ensures
accurate alignment of event data with the respective forecast periods.

#### Some features that are unknown in the future, like cost, will need to be filled in for future dates. What method would you use to forward fill them into future time windows?

For features like cost that are unknown in the future, I use forward filling
to extend the last known value into future time windows. This can be
implemented with SQL window functions such as LAST_VALUE() OVER (PARTITION BY
product_id ORDER BY calendar_week) with the appropriate settings, or using
pandas’ ffill() method during data preprocessing. This technique carries
forward the most recent observation, ensuring that future periods have a valid
cost value. It’s a straightforward method to handle missing future data,
especially when I assume the cost remains stable until updated.
