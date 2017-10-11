# SSN project

## Introduction
This repo is to manage source code for the SSN project (SNE master).

## Features
 * MAC lookup (both online and offline via the EUI info in the csv Python module)
 * Merge and process data from multiple csv files (with a MAC address column and a column with the BlueBorne vulnerability state, the file name of the csv should be the date of the scan)

## Examples
```bash
./mac_lookup.py -s 10-01-2017.csv -s 10-02-2017.csv -d /tmp/final.csv
```
