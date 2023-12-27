# Helpers functionalities

---

## Set up MySQL on Ubuntu:

### Step 1: Update Package Index
First, update the package index on your Ubuntu system. Open a terminal and execute the following command:
```bash
sudo apt update
```

### Step 2: Install MySQL Server
Install the MySQL package using the following command:
```bash
sudo apt install mysql-server
```
This command installs the latest MySQL server package available in your Ubuntu's repositories.

### Step 3: Secure MySQL Installation
After the installation is complete, it’s recommended to run a security script that comes pre-installed with MySQL. This script removes some insecure default settings and locks down access to the database system. Start the script with:
```bash
sudo mysql_secure_installation
```

This script will prompt you to configure options like password validation policy, setting a root password, removing anonymous users, disabling remote root login, and removing the test database. Follow the prompts to make your MySQL installation more secure.

### Step 4: Check MySQL Service Status
* Check if the MySQL service is running: `sudo systemctl status mysql.service`
* If it’s not running, you can start it with: `sudo systemctl start mysql`
* To enable MySQL to start on boot, use: `sudo systemctl enable mysql`

### Step 5: Log into MySQL
To interact with the MySQL server from the terminal, log in as the root (or admin) user:
```bash
sudo mysql -u root -p
```
If you have set a password for the root during the secure installation, you will be prompted to enter it. If not, just pressing Enter should log you in.

### Step 6: (Optional) Creating a New Database and User
You might want to create a separate database and user for your application. In the MySQL shell, you can do this with:

```sql
CREATE DATABASE my_database;
CREATE USER 'my_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON my_database.* TO 'my_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
Replace my_database, my_user, and password with your desired database name, username, and password.

### Step 7: Install MySQL Connector for Python
Finally, ensure that the MySQL connector for Python is installed, as it is necessary for your Python application to communicate with the MySQL server:
```bash
pip install mysql-connector-python
```

**Note**: 
These instructions are for Ubuntu's command line interface. Ensure your system has administrative privileges to perform these operations. Also, the MySQL version installed will depend on the specific version of Ubuntu and its repositories. For the most recent features or specific versions, you might need to add the official MySQL APT repository.



