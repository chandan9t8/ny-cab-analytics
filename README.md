# ny-cab-analytics
### Introduction
The main aim of the project was to analyse and create a pipeline for the NYC Yellow taxi trip data.
[Data source](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

### Project Stucture
- `./main/expt.ipynb` : jupyter notebook where all the experimentation resides
- `./ny-data-pipeline/` : directory where all the code in the mage(orchestrator) resides.

### Techstack used
- Google Compute Engine for creating a virtual machine.
- Google Cloud Storage for storing the data
- Mage to create ETL pipelines
- BigQuery as data warehouse for storing fact and dimensional tables
- Looker Studio for creating a dashboard with important KPIs for stakeholder consumption.

### Dashboard
Below are the snapshots of the dashboard generated using the fact tables in bigquery
![rev](dashboard/revKPI)

![trip](dashboard/tripKPI)

Click [here](https://lookerstudio.google.com/reporting/24cca208-4879-493e-8c4e-c28c17b4f7ff) to view the dashboard on looker.
