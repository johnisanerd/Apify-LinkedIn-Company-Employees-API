# 👥 LinkedIn Company Employees API: Company Employee List from Python and MCP

> Get a company employee list from LinkedIn as JSON: name, job title, location and public profile URL for the people who work at a company, each checked against their own public profile.

- Actor: [LinkedIn Company Employees API on Apify](https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3)
- Input schema: [input parameters](https://apify.com/johnvc/linkedin-company-employees-api/input-schema?fpr=9n7kx3)
- Get a free API token: [apify.com](https://apify.com?fpr=9n7kx3)

This repo is a Python and MCP quick-start for the **LinkedIn Company Employees API** on Apify. Give it company names or LinkedIn company URLs and it returns a list of employees at each company, one row per person, with name, job title, headline, location and profile URL. By default it opens each person's public profile and keeps only the people who show a current role at the company, so a LinkedIn employee list from this API leaves out the people who have moved on. It needs no LinkedIn login, cookie or seat. Expect a partial list: the API can only find people whose public profiles show up in search results, which in testing was roughly 10 to 45% of a small company, 7 to 19% of a mid-size one and under 1% of a very large one. A fresh run with profile checks takes about 3 to 10 minutes per company.

Responsible use: the API returns only what LinkedIn shows signed-out visitors and collects no contact details such as emails or phone numbers, and you are responsible for using the data lawfully.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The **LinkedIn Company Employees API** turns a company name or a LinkedIn company URL into a company employee list. You pass `companies` (up to 50 per run) and can narrow the list with `titleKeywords` such as "engineer" or "head of" and `locations` such as "New York". Each row carries `fullName`, `currentTitle`, `headline`, `location`, `profileUrl` and `companyName`, plus `verified` and `matchReason`, which record whether the person's public profile shows a current role at the company, and `foundBy`, the public search that found them. For talent mapping, a recruiter can pass Datadog's LinkedIn URL with `titleKeywords: ["engineer"]` and `locations: ["New York"]` and get the engineers there who are confirmed as current staff, with title and location. The run's `RUN_SUMMARY` record compares what was found with LinkedIn's own employee count, so you always know how much of the company a run reached. The default run in this repo asks for three people at one small company and costs well under a cent; a fresh verified run takes 3 to 10 minutes per company, and results served from the shared cache come back much faster.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-LinkedIn-Company-Employees-API.git
   cd Apify-LinkedIn-Company-Employees-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python linkedin-company-employees-api-example.py
   ```

The script starts one run for Firecrawl with `maxResultsPerCompany: 3`, prints the run id, waits for the run to finish, then prints each person and the company's coverage line from `RUN_SUMMARY`. To try another input, replace `RUN_INPUT` at the top of the script with any JSON input from this README; the optional knobs are already there as comments.

The script starts a run and then reads the dataset instead of making one synchronous call on purpose. Apify's synchronous run endpoints stop waiting after 300 seconds, and a verified run for one company can take longer than that.

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python linkedin-company-employees-api-example.py
```

## Why Use This LinkedIn Company Employees API?

### No LinkedIn login, cookie or seat

The API reads only what LinkedIn shows a signed-out visitor. There is no field for an account, a password or a session cookie, so no LinkedIn account is ever at risk, and anyone with a free Apify token can run it.

### Each person checked against their public profile

With `verifyEmployment` on (the default), the API opens each person's public profile and keeps them only if it shows a current role at the company you asked about. A person whose profile shows another employer, or whose own headline says "Former" or "Retired", is dropped and never charged.

### Rows you can audit

`matchReason` says how employment was decided and `foundBy` records the exact public search that found each person (or `company-page` for people listed on the company's own page), so any list can be checked and reproduced.

### Coverage in every run

Every run writes `RUN_SUMMARY` with the people found and verified per company, LinkedIn's own employee count and the coverage ratio between the two.

### Pay per person, never per search

Search requests and profile page reads are never charged on their own. You pay one small event per person delivered, plus one per stored row and one per run start (see [Pricing](#pricing)).

## Get a company employee list from LinkedIn

Paste company names straight from a CRM or a spreadsheet, or use LinkedIn company URLs. A URL is exact. A name is matched to its LinkedIn company page first, and a name that cannot be matched with confidence returns a `CompanyNotFound` error row instead of another company's people, so you can retry with the URL. One run takes up to 50 companies and returns a list of employees at each one:

```json
{
  "companies": [
    "https://www.linkedin.com/company/stripe",
    "Datadog",
    "https://www.linkedin.com/company/vercel"
  ],
  "maxResultsPerCompany": 25
}
```

Each person comes back once per company with their name, title or headline, location and profile URL. Download the dataset as JSON, CSV or Excel, or open the run's **Employees** view for a flat LinkedIn employee list (name, title, company, location, verified, profile URL).

## How to find employees of a company

By hand, you would open the company's LinkedIn page and scroll its People tab while signed in, or search the web for `site:linkedin.com/in "Company Name"` and open the profiles one at a time. The API runs those public searches for you, across about a dozen role slices for a company of up to 500 people and about 30 above that, then opens each profile and keeps only current employees.

To search employees of a company by role or by place, add `titleKeywords` and `locations`. Both narrow the list and add searches that surface more people: each title keyword is its own search, which reaches people that a plain company search ranks too deep to find, and every search names the place. For a large company, raise `maxSearchQueriesPerCompany` (up to 100) to reach more of it.

## Talent mapping: see who works on a competitor's team

Talent mapping means charting who holds which roles at the companies you hire from, before you start sourcing. If you are comparing talent mapping tools or software, this one is a pay-per-person API you can call from a script, a spreadsheet workflow or an AI agent. One function in one city at a competitor:

```json
{
  "companies": ["https://www.linkedin.com/company/datadog"],
  "titleKeywords": ["engineer"],
  "locations": ["New York"],
  "maxResultsPerCompany": 30,
  "verifyEmployment": true
}
```

Each verified row gives the person's title or headline, location and how the match was made. Work history appears only on the few profiles that show it to signed-out visitors, so read the result as a map of who is on the team now, not of where they came from. A large company returns a slice of its staff; titles and cities pick which slice.

## Account mapping: the decision makers at each target account

In sales, account mapping means listing the people who make or shape buying decisions at each target account. Pass your accounts and the seniority words you care about:

```json
{
  "companies": ["Ramp", "Deel", "Vercel"],
  "titleKeywords": ["vp", "head of", "director"],
  "maxResultsPerCompany": 15,
  "verifyEmployment": true
}
```

Seniority comes from title words only, because LinkedIn's internal seniority and function filters are not public. Title keywords match anywhere on a person's public page, so scan the titles in the result before you hand the list to outreach. The API returns no reporting lines and no emails.

## CRM hygiene: confirm your contacts still work at the account

Contact records go stale as people change jobs. List who works at each account now, then match the result against your CRM by `profileUrl` or `slug`:

```json
{
  "companies": [
    "https://www.linkedin.com/company/stripe",
    "https://www.linkedin.com/company/microsoft"
  ],
  "titleKeywords": ["procurement", "accounts payable"],
  "maxResultsPerCompany": 30,
  "verifyEmployment": true
}
```

A contact who appears in the list is confirmed as current staff. A contact who is missing may simply not be indexed by search, so a missing name is not proof that the person left. There is no contact-list input: the API takes companies, not people.

## Features

### Core Capabilities
- A company employee list for up to 50 companies per run, from LinkedIn company URLs or plain company names
- Narrow by `titleKeywords` (up to 20) and `locations` (up to 10); both also add searches that surface more people
- `verifyEmployment` on by default; off for a faster, search-level list
- Up to 1,000 people per company with `maxResultsPerCompany`, and up to 100 search slices per company with `maxSearchQueriesPerCompany`
- A shared cache for recent profiles, company pages and searches, with `maxAgeDays` to tighten it or switch it off
- Datasets download as JSON, CSV or Excel, with a ready-made Employees view
- Works as an MCP tool in Claude, Cursor and ChatGPT (see the install sections below); an n8n community node is open source on GitHub (see Use from n8n)

### Data Quality
- `verified` and `matchReason` on every employee row; people whose profile shows no current role at the company are never returned
- `foundBy` on every employee row, so each person can be traced to the search that found them
- People whose own headline says "Former" or "Retired" are dropped
- `fromCache` and `fetched_at` show whether a row came from the shared cache and when it was fetched
- A company that cannot be matched or searched produces an error row (`CompanyNotFound`, `CompanyPageUnavailable`, `SearchUnavailable` or `InvalidInput`), never a person charge
- `RUN_SUMMARY` reports found, verified, LinkedIn's employee count and coverage for every company

It pairs with the rest of the LinkedIn suite: the [LinkedIn Company API](https://apify.com/johnvc/linkedin-company-api?fpr=9n7kx3) for company size, industry and headquarters ([Python example repo](https://github.com/johnisanerd/Apify-LinkedIn-Company-API)), the [LinkedIn Profile API](https://apify.com/johnvc/linkedin-profile-api?fpr=9n7kx3) for full profiles from URLs you already have ([Python example repo](https://github.com/johnisanerd/Apify-LinkedIn-Profile-API)), and the [LinkedIn People Search API](https://apify.com/johnvc/linkedin-people-search-api?fpr=9n7kx3) to find people by name, job title, school or location across every company.

## Coverage, speed and limits

- **Partial coverage.** The API finds people through public search results, so it returns the people search engines have indexed, not a full headcount. In testing that was roughly 10 to 45% of a small company, 7 to 19% of a mid-size one and under 1% of a very large one. Check `coverage` in `RUN_SUMMARY` for every run.
- **Speed.** A fresh verified run takes about 3 to 10 minutes per company. Rows served from the shared cache, and runs with `verifyEmployment` off, finish much sooner.
- **Long runs.** Apify's synchronous run endpoints give up after 300 seconds, so for verified runs start a run, wait for it to finish, then read the dataset. The Python client does this with `start()` and `wait_for_finish()` (see the example script); over plain HTTP, use the asynchronous Run Actor endpoint described in the [Apify API reference](https://docs.apify.com/api/v2) and fetch the dataset items once the run has succeeded.
- **Fields can be empty.** LinkedIn hides much of a profile from signed-out visitors. `currentTitle` and `headline` are left out when neither the profile nor the search result shows them, and work history (`positions`) is rare. Fields with no value are left out of the row; only `verified` is always present (`null` when the profile was not checked), so read every other field as optional.
- **Not available.** Emails, phone numbers, reporting lines, LinkedIn's internal seniority and function filters, and former employees.

## Pricing

The API is priced per event. At the time of writing (2026-10-03) every event costs $0.00001; check the Pricing tab on the [Actor page](https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3) for current rates.

| Event | When it is charged |
|---|---|
| Actor start | Once per run |
| Dataset item | Once per row stored, error rows included |
| Employee found | Once per person delivered from search alone (checks off, a per-company limit reached, or the profile could not be opened) |
| Employee verified | Once per person whose public profile confirms a current role; replaces the found charge, so a person is never charged both |

The default run in this repo (three verified people) comes to 7 events, or $0.00007. A run that returns 100 verified people at one company comes to 201 events, about $0.002. People dropped as former employees produce no row and no charge. You can set a maximum cost per run in the Apify Console, or pass `max_total_charge_usd` to `start()` in Python; the run stops cleanly when it reaches the cap, and a very small cap also means fewer searches per company.

## Usage Examples

### Basic Example

The default run in the example script:

```json
{
  "companies": ["https://www.linkedin.com/company/firecrawl"],
  "maxResultsPerCompany": 3
}
```

### Advanced Example

Engineers and recruiters at two companies in Dublin, using every input parameter:

```json
{
  "companies": ["https://www.linkedin.com/company/stripe", "Intercom"],
  "titleKeywords": ["engineer", "recruiter"],
  "locations": ["Dublin"],
  "maxResultsPerCompany": 50,
  "verifyEmployment": true,
  "maxSearchQueriesPerCompany": 40,
  "maxAgeDays": 1
}
```

### Fast list without profile checks

With `verifyEmployment` off the API skips the profile pages and returns only people whose search result lists the company as their experience. Rows have `verified` set to `null`, `matchReason` set to `search-experience` and no `location`, and some of those people may have left since. In testing, a run like this for one company finished in under a minute.

```json
{
  "companies": ["https://www.linkedin.com/company/supabase"],
  "maxResultsPerCompany": 30,
  "verifyEmployment": false
}
```

### From an AI agent over MCP

When an assistant calls the API, pass a company name and keep the cap small, because a verified run takes minutes:

```json
{
  "companies": ["Notion"],
  "titleKeywords": ["engineer"],
  "maxResultsPerCompany": 10
}
```

## Input Parameters

Only `companies` is required. Everything else narrows or limits the run.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `companies` | array of string | YES | prefilled `["https://www.linkedin.com/company/apify"]` | LinkedIn company URLs (`https://www.linkedin.com/company/microsoft`) or company names (`Microsoft`), 1 to 50 per run. A URL is exact; a name is matched to its LinkedIn company page first. |
| `titleKeywords` | array of string | no | empty | Return only people whose public page mentions one of these job titles, such as `engineer`, `sales` or `head of marketing`. Each keyword is also its own search. Empty searches built-in role slices, more of them for larger companies. Up to 20. |
| `locations` | array of string | no | empty | Return only people in these cities, regions or countries, such as `Dublin` or `United States`. Every search names the place, and people whose public profile shows a different location are left out. Up to 10. |
| `maxResultsPerCompany` | integer | no | `100` | Stop after delivering this many people for each company, 1 to 1,000. You are charged only for people actually returned. |
| `verifyEmployment` | boolean | no | `true` | Open each person's public profile and confirm a current role at the company. `false` returns a faster, search-level list (name, headline, profile URL). |
| `maxSearchQueriesPerCompany` | integer | no | `40` | Cap on the public search slices per company, 1 to 100. Each slice returns about ten people, so more slices reach more of a large company. The run also scales the slices down when its budget is small. |
| `maxAgeDays` | integer | no | per record type | Serve results fetched within this many days from the shared cache, 0 to 90. `0` always fetches fresh. Left empty, the cache keeps profiles up to 7 days, company pages up to 30 days and searches up to 1 day. |

## Output Format

The examples below use a synthetic person ("Jane Doe") and a made-up company. A verified row:

```json
{
  "result_type": "employee",
  "companyName": "Example Company",
  "companySlug": "example-company",
  "companyUrl": "https://www.linkedin.com/company/example-company",
  "profileUrl": "https://www.linkedin.com/in/example-profile",
  "slug": "example-profile",
  "fullName": "Jane Doe",
  "headline": "Senior Software Engineer at Example Company",
  "location": "Dublin, County Dublin, Ireland",
  "currentTitle": "Senior Software Engineer",
  "currentCompany": "Example Company",
  "verified": true,
  "matchReason": "current-position",
  "foundBy": "site:linkedin.com/in \"Example Company\" engineer",
  "fromCache": false,
  "fetched_at": "2026-10-03T11:07:28Z",
  "about": "Backend engineer working on data pipelines.",
  "education": [
    {
      "organizationName": "Example University",
      "organizationUrl": "https://www.linkedin.com/school/example-university/",
      "startDate": "2012",
      "endDate": "2016"
    }
  ],
  "followers": 1250,
  "connections": 500,
  "memberId": "000000000"
}
```

A found row, from a run with `verifyEmployment` off:

```json
{
  "result_type": "employee",
  "companyName": "Example Company",
  "companySlug": "example-company",
  "companyUrl": "https://www.linkedin.com/company/example-company",
  "profileUrl": "https://www.linkedin.com/in/example-profile",
  "slug": "example-profile",
  "fullName": "Jane Doe",
  "headline": "Senior Software Engineer at Example Company",
  "currentTitle": "Senior Software Engineer",
  "verified": null,
  "matchReason": "search-experience",
  "foundBy": "site:linkedin.com/in \"Example Company\"",
  "fromCache": false,
  "fetched_at": "2026-10-03T11:07:28Z"
}
```

An error row, which is never charged as a person:

```json
{
  "result_type": "error",
  "error_type": "CompanyNotFound",
  "error_message": "No LinkedIn company page matches this name. Try the company's LinkedIn URL instead.",
  "requestedCompany": "Example Company That Does Not Exist",
  "fetched_at": "2026-10-03T11:07:28Z"
}
```

The `RUN_SUMMARY` record in the run's key-value store, trimmed to the coverage fields:

```json
{
  "companies": [
    {
      "requestedCompany": "https://www.linkedin.com/company/example-company",
      "companyName": "Example Company",
      "companySlug": "example-company",
      "employeesInLinkedin": 58,
      "found": 3,
      "verified": 3,
      "coverage": 0.0517,
      "stoppedReason": "maxResultsPerCompany reached"
    }
  ],
  "employeesFound": 3,
  "employeesVerified": 3,
  "companiesResolved": 1
}
```

Fields you will use most:

| Field | Rows | Description |
|---|---|---|
| `result_type` | all | `employee` for a person, `error` for a company that could not be matched or searched. |
| `fullName`, `headline` | employee | The person's name and professional headline, from the public profile or search result. |
| `currentTitle`, `currentCompany` | employee | The current role's title and employer. For a verified person, the role at the company you asked about. Left out when not shown. |
| `location` | employee | City or area from the public profile. Present when the profile was opened. |
| `profileUrl`, `slug` | employee | Canonical public profile URL with tracking parameters removed, and its last part, a stable key for deduplication and CRM matching. |
| `companyName`, `companySlug`, `companyUrl` | employee | The company this person was found for, from its LinkedIn company page. |
| `verified` | employee | `true` when the public profile confirms a current role at the company; `null` when the profile was not opened or could not be opened. `false` does not occur. |
| `matchReason` | employee | `current-position` or `current-company` (a current role links the company's page), `company-name` (the employer's name matches, a weaker match), `profile-unavailable`, or `search-experience` (not opened; the search result lists the company as the person's experience). |
| `foundBy` | employee | The public search that found the person, or `company-page` for people listed on the company's own LinkedIn page. |
| `fromCache` | employee | `true` when the row's data came from the shared cache instead of being fetched during this run. |
| `fetched_at` | all | When the row's data was fetched (ISO 8601, UTC); for a cached row, the original fetch time. |
| `about`, `education`, `followers`, `connections`, `photoUrl`, `memberId` | verified | Public profile details on verified rows, when the profile shows them. Connection counts above 500 show as 500. |
| `positions` | verified | Work history (title, company, dates, location, current flag) on the rare profiles that show it to signed-out visitors. |
| `requestedCompany`, `error_type`, `error_message` | error | The `companies` entry the error is about, the error kind and a plain-words reason. |

<!-- ask-ai:start -->
## 🤖 Ask an AI assistant about this Actor

Open a ready-to-send prompt about the LinkedIn Company Employees API in the AI of your choice:

- 💬 [ChatGPT](https://chatgpt.com/?q=How%20do%20I%20use%20the%20LinkedIn%20Company%20Employees%20API%20by%20johnvc%20on%20Apify%20%28https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3%29?%20Show%20me%20input%20examples%2C%20output%20fields%2C%20common%20use%20cases%2C%20and%20how%20to%20integrate%20it%20into%20a%20workflow.)
- 🧠 [Claude](https://claude.ai/new?q=How%20do%20I%20use%20the%20LinkedIn%20Company%20Employees%20API%20by%20johnvc%20on%20Apify%20%28https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3%29?%20Show%20me%20input%20examples%2C%20output%20fields%2C%20common%20use%20cases%2C%20and%20how%20to%20integrate%20it%20into%20a%20workflow.)
- 🔍 [Perplexity](https://www.perplexity.ai/search?q=How%20do%20I%20use%20the%20LinkedIn%20Company%20Employees%20API%20by%20johnvc%20on%20Apify%20%28https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3%29?%20Show%20me%20input%20examples%2C%20output%20fields%2C%20common%20use%20cases%2C%20and%20how%20to%20integrate%20it%20into%20a%20workflow.)
- 🅒 [Copilot](https://copilot.microsoft.com/?q=How%20do%20I%20use%20the%20LinkedIn%20Company%20Employees%20API%20by%20johnvc%20on%20Apify%20%28https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3%29?%20Show%20me%20input%20examples%2C%20output%20fields%2C%20common%20use%20cases%2C%20and%20how%20to%20integrate%20it%20into%20a%20workflow.)
<!-- ask-ai:end -->

## People also search for

### How can I find a list of employees at a company?

Add the company's LinkedIn URL or name to `companies` and run the API. It searches for the company's people, opens each public profile, and returns the ones whose profile shows a current role there, with name, title, location and profile URL. The result is a partial list: only people whose public profiles appear in search results can be found, and `RUN_SUMMARY` tells you what share of LinkedIn's employee count a run reached.

### How do I find out who works at a company?

The manual route is a web search for `site:linkedin.com/in "Company Name"`, then opening each profile to check it is current. The API runs those searches across role slices for you, checks every profile, and drops anyone who has moved on.

### How can I verify that someone currently works for a company?

The API checks every person it finds against their public profile and returns them only when the profile shows a current role at the company you asked about. `verified` is `true` for those rows, and `matchReason` says how the match was made (`current-position`, `current-company` or the weaker `company-name`). It takes companies, not people, so it lists who works at an account; it is not a background check or an employment verification service.

### Can I find company employees without a LinkedIn account?

Yes. The API reads only LinkedIn's public pages, the same ones a signed-out visitor sees. It never asks for an account, a password or a session cookie.

### Can I filter LinkedIn employees by job title, location or seniority?

Yes, by title words and places. `titleKeywords` narrows the list to job titles such as `engineer`, `recruiter`, `director` or `head of`, and `locations` keeps only people in the cities, regions or countries you name. LinkedIn's internal seniority and function codes are not public, so seniority comes from title words.

### Is there a way to export a company's LinkedIn employee list?

Yes. Every run writes a dataset you can download as JSON, CSV or Excel from the Apify Console or read from Python, as the example script does. The **Employees** view gives a flat table of name, title, company, location, verified and profile URL.

### Are there free tools to find a company's employees on LinkedIn?

If you are looking for a free LinkedIn scraper for this job: Apify's free plan includes monthly platform credit, which covers small runs like the default one in this repo many times over, and free-plan accounts have a monthly cap on how many people this API returns. A paid Apify plan lifts that cap.

### How can I see all the employees of a company on LinkedIn?

Not all of them, from public pages. The API returns the people search engines have indexed: in testing roughly 10 to 45% of a small company, 7 to 19% of a mid-size one and under 1% of a very large one. Add `titleKeywords` and `locations`, or raise `maxSearchQueriesPerCompany`, to reach more people at a large company, and check `coverage` in `RUN_SUMMARY`.

### Is there a way to find out how many employees a company has?

`RUN_SUMMARY` shows the employee count LinkedIn lists for each company (`employeesInLinkedin`). For company size, industry and headquarters as their own rows, use the [LinkedIn Company API](https://apify.com/johnvc/linkedin-company-api?fpr=9n7kx3).

### Will LinkedIn ban you for scraping?

This API uses no LinkedIn account, so there is no account for LinkedIn to restrict. It reads only the public pages a signed-out visitor can see.

### Can ChatGPT or Claude list a company's employees?

Yes, once the API is connected as an MCP tool. Use the install sections below for [Claude Code](https://claude.ai/referral/uIlpa7nPLg) (free trial), [Claude Cowork](https://claude.ai/referral/uIlpa7nPLg) (free trial), Claude on the web, Cursor or ChatGPT, then ask in plain language, for example "list the engineers at Notion". If you were looking for a LinkedIn scraper MCP server, this one runs on the hosted Apify MCP server and needs no LinkedIn login. Keep `maxResultsPerCompany` small in agent calls, because a verified run takes minutes.

### Is this a LinkedIn employee scraper or an API?

This repo teaches the **LinkedIn Company Employees API** on Apify. People also search for "linkedin employee scraper", "linkedin company employees scraper" or "scrape linkedin company employees"; the same Actor covers that need and returns structured JSON you can call from Python or over MCP.

### What is the difference between verified and found?

A verified person's public profile shows a current role at the company. A found person comes from search results without that check, because `verifyEmployment` was off, a per-company limit was reached or the profile could not be opened, and only when the search result lists the company as their experience. Each person is charged once, as found or as verified, never both.

### How do I use the company employee list API from Python?

Clone this repo, run `uv sync`, put your Apify token in `.env`, and run `uv run python linkedin-company-employees-api-example.py`. The script shows the whole pattern: start a run with a `run_input` dictionary, wait for it to finish, read the default dataset, then read `RUN_SUMMARY` from the default key-value store.

### Can I run it on a schedule?

Yes. Save your input as a task in the Apify Console and schedule it monthly. Compare runs by `slug` to spot new names; a person missing from a later run may simply not have been found that time, so absence is not proof that they left.

## Use from n8n

An n8n community node for this API is open source on GitHub: [n8n-nodes-linkedin-company-employees-api](https://github.com/johnisanerd/n8n-nodes-linkedin-company-employees-api). It is not on npm yet. Once it is published, it installs on a self-hosted n8n from **Settings > Community Nodes** as `n8n-nodes-linkedin-company-employees-api`, with your Apify API token as the credential.

---

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the LinkedIn Company Employees API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the LinkedIn Company Employees API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

---

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the LinkedIn Company Employees API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

---

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/linkedin-company-employees-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api`, using OAuth when prompted.
5. Ask Claude to run the LinkedIn Company Employees API.

Open Claude on the web: https://claude.ai

---

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the LinkedIn Company Employees API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

---

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-company-employees-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

## 🌐 About Alpha OSINT

This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.
See the [LinkedIn Company Employees API source page](https://www.alphaosint.com/sources/linkedin-company-employees-api/) for related tools and use cases.
For support or requests for this actor, please start a ticket [directly on our support page](https://apify.com/johnvc/linkedin-company-employees-api/issues/open?fpr=9n7kx3).

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the LinkedIn Company Employees API to power your talent mapping, account mapping and CRM hygiene workflows with reliable, structured results.*

Last Updated: 2026.10.03
