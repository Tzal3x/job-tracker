# job-tracker
A program that tracks applications by scrapping your personal data from popular job hiring platforms and exports them to a file of your choice (e.g. csv).

## Installation
*Python 3.8.10*
`pip install -r requirements`

Create manually a `.env.yaml` file containing the fields bellow:
```yaml
LinkedIn:
  username: "<your LinkedIn email>"
  password: "<your LinkedIn password>"
```

## Run
`python main.py`

### Example Output CSV
| url	| company_name | linkedin_status | title | location | 
| --- | ------------ | --------------- | ----- | -------- |
| linkedin.com/jobs/view/... |	Tra-ated | Applied 3d ago |	Backend Engineer |Rome (On-site) |
| linkedin.com/jobs/view/... |	Doulras LLC| Applied 5d ago	| Software Engineer (Back-end) | Barcelona (Remote) |
| linkedin.com/jobs/view/... |	Ten-rains | Application viewed 5d ago |	MongoDB / Elasticsearch (Semopr) | Rome (Remote) |
| linkedin.com/jobs/view/... |	UDWDcoMinds	 | Application viewed 5d ago |	Junior System Engineer | Athens (Hybrid) |
| linkedin.com/jobs/view/... |	Greed Associates | Application viewed 3d ago |	Python Web Developer | European Union (Remote) |
