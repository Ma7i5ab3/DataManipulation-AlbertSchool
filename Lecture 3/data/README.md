# Practice data: `taxis_dirty.csv`

6,483 rows × 15 columns. Built by `make_taxis_dirty.py` (seeded, reproducible) from the
seaborn sample dataset `taxis` (6,433 NYC taxi rides, March 2019, derived from NYC TLC trip records).

## Problems already in the real data
| Dimension | Problem | Rows |
|---|---|---|
| Missing | `payment` NaN | 44 |
| Missing | `pickup_zone` / `pickup_borough` NaN | 27 |
| Missing | `dropoff_zone` / `dropoff_borough` NaN | 46 |
| Accuracy | `passengers == 0` | 97 |
| Accuracy | `distance == 0` | 52 |
| Consistency | pickup outside March 2019 | 1 |

(Counts include the copies added by the duplication step.)

## Problems added by the script
| Dimension | Problem | Rows |
|---|---|---|
| Inconsistency | `payment` spelled `Cash`, `CASH`, ` cash`, `Credit card`, `credit card ` (trailing space), `CREDIT CARD` | 121 in the final file (120 + 1 copied by duplication) |
| Inconsistency | `pickup_borough == "manhattan"` (lower case) | 25 |
| Missing (disguised) | `payment == "unknown"` | 30 |
| Accuracy | negative `fare` | 8 |
| Accuracy | `passengers == 9` | 5 |
| Consistency | `dropoff` before `pickup` (times swapped) | 6 |
| Duplication | exact copies of a row | 40 |
| Duplication | same `ride_id`, different `tip` and `total` | 10 |

Key numbers: `df.duplicated().sum()` = 40 · `df.duplicated(subset="ride_id").sum()` = 50 ·
`df["payment"].nunique()` = 9 → 3 after `.str.strip().str.lower()`.
