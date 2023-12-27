# Python database handling for Finance

---

![img.png](img.png)

---

## Overview

### Functionality
* **Input**: Accept a list of up to 4 cryptocurrency tickers.
* **Input**: Accept multiple timeframes (1w, 1d, 4h, 1h, 15min) in a single execution.
* **Input**: Date range in 'YYYY-MM-DD' format, considering time for intervals less than a day.
* **Database**: Connect to a local MySQL database to check/create tables and manage OHLC data.
* **Data Source**: Use Binance API v3 klines for crypto OHLC data.
* **Error Handling**: Print to console and log errors to a file as necessary.

### Database Schema
* Each table corresponds to a specific ticker and timeframe.
* Columns: Open, High, Low, Close, Volume, and Date (as primary key).

### Script Design
* Object-Oriented Programming approach for scalability and maintainability.
* Separate classes/modules for database interaction, API communication, and core logic.

### Development Environment
* Python (latest stable version).
* Libraries: requests for API calls, pandas for data handling, mysql-connector-python for database interaction.
* Ensure compatibility with common Python conventions and best practices.

### Binance API Integration
* Modify the existing historicData and historicDataFull functions to fit the new script structure.
* No API key required for public data endpoints.

### Date and Time Handling
* Enhance dateToMs function for better error handling and flexibility.
* Ensure accurate conversion and handling of dates and times, especially for intervals less than one day.

### Error Handling and Logging
* Implement robust error handling to capture and log exceptions, especially for API and database interactions.
* Include detailed logs for troubleshooting and auditing purposes.

---

## Next Steps
### Database Setup:
* Decide on the MySQL database setup (locally/remote, credentials).
* Finalize table naming conventions.

### Script Development:
* Start developing the core modules (database, API, main logic).
* Integrate your existing functions into the new structure.

### Testing and Validation:
* Test the script with various tickers and timeframes.
* Validate the data accuracy and error handling capabilities.

### Iteration and Feedback:
* Regularly review the script's performance and functionality.
* Iterate based on feedback and any additional requirements.
