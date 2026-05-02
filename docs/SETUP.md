# Element of the Day Setup Guide

Display a periodic table element that changes daily.

## Overview

The Element of the Day plugin selects a periodic table element based on the day of the year (day_of_year mod 118), cycling through all 118 elements. It fetches element details from the PubChem REST API. No API key required.

- API reference: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

### Prerequisites

No API key required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Element of the Day**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `element_of_day` plugin variables:
   ```
   {{{ element_of_day.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `element_of_day.element_name` | Element name | `Hydrogen` |
| `element_of_day.symbol` | Element symbol | `H` |
| `element_of_day.atomic_number` | Atomic number | `1` |
| `element_of_day.atomic_weight` | Standard atomic weight | `1.008` |
| `element_of_day.category` | Element category (e.g. nonmetal, noble gas) | `nonmetal` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to refresh (once per day is sufficient). | `3600` |

## Troubleshooting

- **Wrong element** — the element cycles daily by day of year; this is by design.

