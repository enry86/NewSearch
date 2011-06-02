#!/bin/bash
source conf/db_settings.sh

# Folders Configuration

echo "Creating files folders..."
mkdir files
mkdir files/calais_res
mkdir files/html_proc
mkdir files/test_out
mkdir files/test_graph

echo "Setup DB..."
mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password=$DB_PSWD < conf/mysql.sql

echo "Configuration Complete"
