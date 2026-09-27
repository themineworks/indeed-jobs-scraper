# Indeed Jobs Scraper: Extract Jobs, Salaries & Descriptions

Scrape public Indeed job listings by keyword and location: title, company, location, salary, job type, posted date, full description and apply URL. Eight country sites. No login, no API key, pay per job.

**Run it on Apify:** [apify.com/themineworks/indeed-scraper](https://apify.com/themineworks/indeed-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/indeed-scraper](https://themineworks.com/actors/indeed-scraper/)

**Price:** $4.80 per 1,000 jobs on Apify's free plan, down to $3.00 on higher plans, plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Keyword and location search across 8 country sites (US, GB, CA, IN, AU, DE, FR, NL)
* Salary text as published, job type and remote flag
* Posted date and full job description
* Direct apply URL for every posting
* No login and no cookies: reads public search pages

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/indeed-scraper").call(run_input={
    "query": "software engineer",
    "location": "New York"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/indeed-scraper').call({
    "query": "software engineer",
    "location": "New York"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~indeed-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "software engineer", "location": "New York"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 indeed_jobs_scraper.py --token YOUR_APIFY_TOKEN --query "software engineer" --location "New York"
node indeed_jobs_scraper.mjs --token YOUR_APIFY_TOKEN --query "software engineer" --location "New York"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `query` (required) | string |  | Job title, skill, or keyword to search for (Indeed's 'what' field), for example "software engineer" or… |
| `location` | string |  | City, state, ZIP, or 'Remote' (Indeed's 'where' field), for example "Austin, TX" or "10001" |
| `country` | string | `"US"` | Which Indeed country site (ccTLD) to search, for example uk.indeed.com for GB |
| `maxResults` | integer | `45` | Maximum number of job listings to return |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `job_id` | string | Indeed job key (unique job ID) |
| `job_url` | string | Canonical Indeed job posting URL |
| `title` | string | Job title |
| `company` | string | Company name |
| `location` | string | Job location |
| `remote` | boolean | Whether the job is flagged remote |
| `salary` | string | Salary text as shown on Indeed (for example '$105,000, $125,000 a year') |
| `job_type` | string | Employment type (Full-time, Part-time, Contract, etc.) |
| `posted` | string | Relative posting time (for example '3 days ago', 'Just posted') |
| `posted_date` | string | Absolute posting date as ISO timestamp when available |
| `description` | string | Job description snippet (plain text) |
| `company_rating` | number | Company star rating on Indeed if shown |
| `company_review_count` | number | Number of company reviews if shown |
| `urgently_hiring` | boolean | Indeed 'Urgently hiring' flag |
| `sponsored` | boolean | Whether the listing is a sponsored/promoted result |
| `search_query` | string | The query this job was found under |
| `search_location` | string | The location this job was found under |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/indeed-scraper
```

## FAQ

### Do I need an Indeed login?

No. The actor reads public Indeed search pages only. No account, no cookies, no API key.

### Which countries does it cover?

Eight Indeed country sites: US, GB, CA, IN, AU, DE, FR and NL. Set the country input to pick one.

### What does it cost?

You pay per job returned and nothing for a search that finds none. Indeed hard-blocks datacenter traffic, so it runs on residential proxy, which is why it is priced above the lighter boards.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Foundit Jobs Scraper](https://themineworks.com/actors/foundit-jobs-scraper/): Foundit.in (Monster India): 20 fields, monitor mode
* [Hirist Jobs Scraper](https://themineworks.com/actors/hirist-jobs-scraper/): India IT jobs across 147 locations, 19 fields
* [Naukri Jobs Scraper](https://themineworks.com/actors/naukri-jobs/): India's largest job board structured as clean JSON

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
