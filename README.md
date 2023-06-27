# last_cassandra_repair_time_script
A small script used to find out how many days have passed since the last repair command was executed using the log file. 
The script also creates a .prom file to be scraped by node exporter and be sent to Prometheus so it can be displayed in Grafana. 
