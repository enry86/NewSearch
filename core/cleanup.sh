#!/bin/bash
source conf/db_settings.sh

# Removing directories
rm -rf files

# Cleanup DB
mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password=$DB_PSWD $DB_NAME < conf/clean_db.sql

