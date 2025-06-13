# update_mysql Documentation

## Overview

This module provides a command-line tool to update Tushare financial data into a MySQL database. It supports daily, monthly, and yearly data updates, as well as index creation for optimized queries. The script interacts with the Tushare API and manages data ingestion and indexing in a MySQL backend.

## Features

- **Daily, Monthly, Yearly Data Updates:**  
  Update different categories of Tushare data based on frequency.
- **Index Creation:**  
  Automatically create indexes on all relevant tables for faster queries.
- **Configurable Database Connection:**  
  Easily modify database connection parameters.
- **Logging Table:**  
  Ensures a log table exists for tracking update operations.

## File Structure

- `main.py` — Main script for running updates and managing the database.
- `update_apis.json` — Configuration file specifying which APIs to update and their parameters.
- **Dependencies:**  
  - `bageltushare` (custom library for Tushare-MySQL integration)
  - Standard Python libraries: `json`, `time`

## Usage

### 1. Configuration

Edit the following variables in `main.py` if needed:

```python
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "your_password"
DB = "tushare"
TOKEN = "your_tushare_token"
```

Ensure your MySQL server is running and accessible with the above credentials.

### 2. Prepare API Configuration

Create or update `update_apis.json` in the same directory.  
Example structure:

```json
{
  "daily": {
    "api_name_1": {
      "params": {...},
      "fields": [...]
    }
  },
  "monthly": {
    "api_name_2": {
      "params": {...},
      "fields": [...]
    }
  },
  "yearly": {
    "api_name_3": {
      "params": {...},
      "fields": [...]
    }
  }
}
```

### 3. Running the Script

From the `update_mysql` directory, run:

```bash
python main.py
```

You will be prompted to choose the update type:

```
Choose update type:
1. Daily
2. Monthly
3. Yearly
0. Create Indexes
Enter your choice:
```

- Enter `1` for daily updates
- Enter `2` for monthly updates
- Enter `3` for yearly updates
- Enter `0` to create indexes on all tables

### 4. Output

- The script prints progress and timing information to the console.
- Index creation and update operations are logged.

## Functionality Breakdown

- **yearly_update(apis):**  
  Downloads yearly data for each API listed under `"yearly"` in `update_apis.json`.

- **monthly_update(apis):**  
  Updates monthly data for each API listed under `"monthly"`.

- **daily_update(apis):**  
  Updates daily data for each API listed under `"daily"`.

- **create_indexes(apis):**  
  Creates indexes for all tables corresponding to APIs in all categories.

- **main():**  
  Handles user interaction, loads API configuration, and dispatches the selected operation.

## Extending & Customization

- To add new APIs or change parameters, edit `update_apis.json`.
- To change database or Tushare credentials, edit the relevant variables in `main.py`.
- To add new update frequencies or logic, extend the corresponding functions.

## Requirements

- Python 3.x
- MySQL server
- `bageltushare` Python package (must be installed and accessible)
- Valid Tushare API token

## Security Note

**Do not commit your database password or Tushare token to public repositories.**  
Consider using environment variables or a separate configuration file for sensitive information.
