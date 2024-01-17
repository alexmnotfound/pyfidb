# Crypto DB Data

## Overview
The Crypto DB Data Project is a Python-based application designed to fetch, process, 
and store cryptocurrency data from the Binance API into a local MySQL database. 
It allows users to download Open, High, Low, Close, and Volume (OHLC) data for 
specified cryptocurrencies and intervals and provides functionalities to check 
existing data in the database.


## Features
* Fetch and store OHLC data from the Binance API.
* Create and manage tables in a MySQL database for different cryptocurrencies and intervals.
* Check existing tables in the database and display their date ranges.

### Downloading Data
* Select the 'Download' option.
* The script will download data based on the parameters specified in download_params.json.
* Data will be stored in respective tables in the MySQL database.

### Checking Database Tables
* Select the 'Check' option.
* Enter a specific symbol to check tables related to that symbol or press Enter to check all tables.
* The script will display the names of the tables and their date ranges.


---

## How to run it

### DB Config
1. Create a DB `config.py` file in the parent folder with the following info:
```python
# Database Configuration
DB_CONFIG = {
    'host': 'YOUR_HOST',
    'user': 'YOUR_USER',
    'passwd': 'YOUR_PASSWORD',
    'database': 'YOUR_DATABASE_NAME'
}
```

### Run script
I personally recommend it to run it in a virtual environment, as follows:
1. Open a command prompt or terminal window.
2. Navigate to the directory where you want to create the virtual environment. You can use the `cd` command to change directories.
3. Enter the following command to create a new virtual environment: `python3 -m venv myenv`, replacing "myenv" with the name you want to give to your virtual environment.
4. Activate the virtual environment by entering the following command (Linux environments): `source myenv/bin/activate`
5. Once the virtual environment is activated, you can install Python packages using `pip` as usual. For example, to install the all the packages, 
you can enter the following command: `pip3 install -r requirements.txt`
6. Assuming you're on the project's folder, now you can run `python3 main.py`
7. When you're done using the virtual environment, you can deactivate it by entering the following command: `deactivate`


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

---