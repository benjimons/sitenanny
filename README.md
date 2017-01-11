# sitenanny
This script uses linkchecker to monitor a given domain and detect new offsite domain links. It can send email alerts when a new domain is detected on a given site.

## Requirements 
- Python 2.7
- Linkchecker - https://wummel.github.io/linkchecker/

##Usage 
```
Usage:  ./nannydata.py -t domain -s <domain name> -f <output filename>
        -t domain (future use)
        -s domain name you wish to scan
        -f output file, this is overwritten each run
        
Example:
        ./nannydata.py -t domain -s example.com -f example.com.file

```
