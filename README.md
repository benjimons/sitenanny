# sitenanny
This script uses linkchecker to monitor a given domain and detect new offsite domain links. It can send email alerts when a new domain is detected on a given site.

## Requirements 
- Python 2.7
- Linkchecker - https://wummel.github.io/linkchecker/

##Usage 
```
Usage:  ./nannydata.py -t domain -s <domain name> -f <input filename>
        -t domain (future use)
        -s domain name you have scanned
        -f input linkchecker file
                example output from this command would be the input file:
                linkchecker --user-agent="github.com/benjimons/sitenanny" -t30 -q -ocsv -Fcsv -v http://www.example.com
Example:
        ./nannydata.py -t domain -s example.com -f example.com.log

```
