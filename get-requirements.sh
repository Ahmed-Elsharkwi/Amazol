#!/bin/bash

# Update package index
sudo apt update

# Install MySQL server
sudo apt install -y mysql-server=8.0.39-0ubuntu0.22.04.1
sudo apt install mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
echo "[client]
user=root
password=your_password
" > ~/.my.cnf
chmod 600 ~/.my.cnf

# Secure MySQL installation (optional, uncomment if needed)
# sudo mysql_secure_installation

# Run the SQL file
# Replace '/path/to/your/file.sql' with the actual path to your SQL file
SQL_FILE="setup_mysql_dev.sql"
if [ -f "$SQL_FILE" ]; then
    sudo mysql -u root -p'root' < "$SQL_FILE"
else
    echo "SQL file not found: $SQL_FILE"
fi
sudo apt install python3-pip
pip install -r requirements.txt
sudo pip3 install pyOpenSSL --upgrade
