# Clinical Trials DBMS/SE Project

The Drug Testing Management System is designed to support the full lifecycle of clinical trials, from patient recruitment to data analysis. The system's primary goals are to ensure regulatory compliance, improve data accuracy, streamline patient management, and facilitate communicatiion among stakeholders. It support various phases of clinical trials and integrates with laboratory systems for efficient data exchange.

### Setup:
```
source .venv/bin/activate
```
`mysql` or `mariadb`
```
create database proj;
use proj;
source db.sql;
source pop.sql;
```

### To Run:
```
streamlit run frontend.py
```
