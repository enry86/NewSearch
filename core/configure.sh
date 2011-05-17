#!/bin/bash

#Db configuration variables
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER="newsearch"
DB_PSWD="newsearch"
DB_NAME="enrico"

# Folders Configuration

echo "Creating files folders..."
mkdir files
mkdir files/calais_res
mkdir files/html_proc
mkdir files/test_out
mkdir files/test_graph

echo "Setup DB..."
mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password=$DB_PSWD $DB_NAME < conf/mysql.sql

echo "Configuration Complete"
