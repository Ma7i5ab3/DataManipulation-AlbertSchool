# Data

## Lesson files (made up for teaching)

| File | Content |
|---|---|
| `orders.tsv` | 3 orders; tab-separated, latin-1, ids with leading zeros, one empty total |
| `orders.xlsx` | Sheets `Orders` and `Refunds` |
| `orders.json` | 2 orders with a nested `customer` dict and a list of `items` |

## Practice files (real data, downloaded on 7 November 2026)

| File | Source | Licence |
|---|---|---|
| `velib_stations.csv` | Paris Open Data, *Vélib - Vélos et bornes - Disponibilité temps réel* (`velib-disponibilite-en-temps-reel`), CSV export as published (`;` separator, UTF-8) | ODbL |
| `paris_roadworks.xlsx` | Paris Open Data, *Travaux perturbants la circulation* (`chantiers-perturbants`), Excel export; geometry columns left out | ODbL |
| `pandas_issues.json` | GitHub REST API, the 100 most recent issues and pull requests of `pandas-dev/pandas`; kept fields: number, title, state, is_pull_request, created_at, closed_at, comments, user (login, type), labels (name) | GitHub API data |

The practice files are a snapshot: re-downloading them later gives different numbers.
