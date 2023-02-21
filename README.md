# job-tracker ✍️ 
A program that tracks applications by scrapping your personal data from popular job hiring platforms and exports them to a file of your choice (e.g. csv).

## The problem
Nowadays it is not uncommon to apply to dozens or even hundreds job postings. It would be useful for job seekers to keep track of their applications, and make simple data analysis on that data. Writing down what's the status of the application, what was said during the interviews and other useful information. 

## The solution
✅ The aim of this program is to save time of the job seeker by scraping and saving to a file the information of his/her applications so more time can be focused on doing things that would increase the probability of getting an offer.

_⚠️ The scrapping is **not** 100% accurate: (e.g. some job titles or the working model remote/hybrid/on-site) might be left out blank etc._
Despite the persisting problems, the program can still be useful by saving time for the user, even if the data need some manual fine-tuning.

Please pay attention to open issues to find some detected bugs or other misbehaviours. 

☕ Feel free to contribute by opening a pull-request for the open issues or create one yourself :)

## Installation
*Python 3.8.10*
`pip install -r requirements`

(Optional) Create manually a YAML file containing the fields bellow:
```yaml
LinkedIn:
  username: "<your LinkedIn email>"
  password: "<your LinkedIn password>"
  
<other platform of your choice>:
  username: "<platform email>"
  password: "<platform password>"
```
This is used so that the scrapper can login to the platform of choice.
If this file is not provided it's ok. You can still pass the username and password using the command line arguments. 

## Run
Execute the following `python main.py --help` for a detailed description of the programs options and example runs.

## Example Output CSV of parsing linkedin data
| url	| company_name | linkedin_status | title | location | 
| --- | ------------ | --------------- | ----- | -------- |
| linkedin.com/jobs/view/... |	Tra-ated | Applied 3d ago |	Backend Engineer |Rome (On-site) |
| linkedin.com/jobs/view/... |	Doulras LLC| Applied 5d ago	| Software Engineer (Back-end) | Barcelona (Remote) |
| linkedin.com/jobs/view/... |	Ten-rains | Application viewed 5d ago |	MongoDB / Elasticsearch (Semopr) | Rome (Remote) |
| linkedin.com/jobs/view/... |	UDWDcoMinds	 | Application viewed 5d ago |	Junior System Engineer | Athens (Hybrid) |
| linkedin.com/jobs/view/... |	Greed Associates | Application viewed 3d ago |	Python Web Developer | European Union (Remote) |
