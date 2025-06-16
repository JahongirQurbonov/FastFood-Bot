#!/bin/bash

# PostgreSQL o'rnatish (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL ishga tushirish
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Database yaratish
sudo -u postgres psql -c "CREATE DATABASE fastfood_bot;"
sudo -u postgres psql -c "CREATE USER botuser WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fastfood_bot TO botuser;"

echo "✅ Database tayyor!"
