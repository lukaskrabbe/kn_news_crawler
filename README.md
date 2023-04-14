# Kieler Nachrichten News Crawler (KN-News-Crawler)

This is a simple news crawler that crawls news from the E-Paper Website of Kieler Nachrichten.

## Structure

The project is structured as follows:
```
.
├── Dockerfile
├── Makefile
├── README.md
├── data
│        ├── logs
│        │       ├── 05_04_2023
│        │       │       ├── kn-data-prep.log
│        │       │       └── kn-data-upload.log
│        │       ├── 19_03_2023
│        │       │       ├── kn-data-consumer.log
│        │       │       └── kn-data-prep.log
│        │       ├── 20_03_2023
│        │       │      ├── kn-data-consumer.log
│        │       │      └── kn-data-prep.log
│        │       └── 21_03_2023
│        │            ├── kn-data-prep.log
│        │           └── kn-data-upload.log
│        ├── prep
│        │        ├── 19_03_2023_979736
│        │        │      ├── EIDOS21059162_7aaf27b8-c4b5-11ed-a678-30d01d2dc779.json
│        │        │      └── ...
│        │        └── 20_03_2023_979762
│        │            ├── EIDOS133139_aa780d2a-c64a-11ed-9f13-8ba62d7fb9c4.json
│        │            └── ...
│        └── raw
│            ├── 19_03_2023_979736
│            │        ├── EIDOS21059162_7aaf27b8-c4b5-11ed-a678-30d01d2dc779.json
│            │        └── ...
│            └── 20_03_2023_979762
│                ├── EIDOS133139_aa780d2a-c64a-11ed-9f13-8ba62d7fb9c4.json
│                └── ...
├── requirements.in
├── requirements.txt
├── secrets
│        ├── KN_USER_SECRET.json
│        └── MONGO_USER_SECRET.json
├── src
│        ├── __init__.py
│        ├── analytics
│        │       ├── general_overview.ipynb
│        │       ├── political_overview.ipynb
│        │       ├── text_analyse.ipynb
│        │       └── text_clustering.ipynb
│        ├── helpers
│        │       ├── __init__.py
│        │       ├── log.py
│        │       └── secrets.py
│        ├── kn
│        │       ├── __init__.py
│        │       ├── __pycache__
│        │       │       ├── __init__.cpython-310.pyc
│        │       │       ├── download.cpython-310.pyc
│        │       │       ├── login.cpython-310.pyc
│        │       │       └── prep.cpython-310.pyc
│        │       ├── download.py
│        │       ├── login.py
│        │       └── prep.py
│        ├── kn_data_consumer.py
│        ├── kn_data_prep.py
│        └── kn_data_upload.py
└── tests
    └── main_test.py

```
Where:
* src/ contains all src files
* src/analytic/ contains all files for the analytics (Jupyter Notebooks)
* src/helpers/ contains all helper files, e.g. for logging and secret loading
* src/kn/ contains all files used for communication with the E-Paper Website
* src/kn_data_consumer.py is the main file for the data downlaod
* src/kn_data_prep.py is the main file for the data preparation
* src/kn_data_upload.py is the main file for the data upload to MongoDB


## Usage


### Data Download


### Data Preparation


### Data Upload


## Authors

* **Lukas Krabbe** - *Initial work* - [Lukas Krabbe](mailto:mail@l-krabbe.de)