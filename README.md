# DNS-Client
A simple Python script that implements the `dnspython` library to perform DNS lookups (A, AAAA, and CNAME) using Google's public DNS server (`8.8.8.8`).  
It prints out detailed header, question, and answer section information.


Make sure you have **Python 3** installed.
Install the required dependency:

`pip install dnspython`

Run the script from the terminal:

`python dnsclient.py <hostname> <query_type>`

Example:

`python dns_query.py google.com A`
