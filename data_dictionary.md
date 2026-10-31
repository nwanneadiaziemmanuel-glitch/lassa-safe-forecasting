# Data dictionary

| Field | Type | Meaning |
|---|---|---|
| `week_start_date` | date | Start date of epidemiological reporting week |
| `week_end_date` | date | End date of epidemiological reporting week |
| `epi_year` | integer | Epidemiological year |
| `epi_week` | integer | Epidemiological week |
| `suspected_cases` | integer | Reported suspected Lassa cases |
| `confirmed_cases` | integer | Reported laboratory-confirmed cases; primary target |
| `probable_cases` | integer | Reported probable cases |
| `deaths` | integer | Reported deaths |
| `extraction_method` | categorical | Automated/manual/mixed extraction label |
| `extraction_timestamp` | datetime | Time the source table was extracted/compiled |
| `report_pdf_url` | URL | Source report reference where available |

## Integrity checks used

- no missing values in supplied analytical fields
- no duplicate weeks
- seven-day spacing between weekly start dates
- no negative case/death counts
- confirmed cases do not exceed suspected cases
- probable cases do not exceed suspected cases
- deaths do not exceed confirmed + probable cases

These checks test table consistency; they do not establish epidemiological completeness.
