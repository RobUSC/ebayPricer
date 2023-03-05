# ebayPricer
Specifically created as comic pricing scraper, as I go along I'll make the entries configurable

Based on the tutorial found at:  https://linuxconfig.org/introduction-to-ebay-api-with-python-obtaining-keys-and-accessing-the-sandbox-part-1

To use this repo use a configuration file as recommended on the tutorial with your own values from developer.ebay.com:
```
name: ebay_api_config

# Trading API Sandbox - https://www.x.com/developers/ebay/products/trading-api
api.sandbox.ebay.com:
    compatability: 719
    appid: ENTER_YOUR_APPID_HERE
    certid: ENTER_YOUR_CERTID_HERE
    devid: ENTER_YOUR_DEVID_HERE
    token: ENTER_YOUR_TOKEN_HERE

# Trading API - https://www.x.com/developers/ebay/products/trading-api
api.ebay.com:
    compatability: 719
    appid: ENTER_YOUR_APPID_HERE
    certid: ENTER_YOUR_CERTID_HERE
    devid: ENTER_YOUR_DEVID_HERE
    token: ENTER_YOUR_TOKEN_HERE

# Finding API - https://www.x.com/developers/ebay/products/finding-api
svcs.ebay.com:
    appid: ENTER_YOUR_APPID_HERE
    version: 1.0.0

# Shopping API - https://www.x.com/developers/ebay/products/shopping-api
open.api.ebay.com:
    appid: ENTER_YOUR_APPID_HERE
    version: 671

```

TODO: 
Fix the `X-EBAY-API-IAF-TOKEN` issue with the existing SDK which is required now, but has not been updated in the ebaySDK used. Modified local code by injecting the value into the local SDK file for now:

```    
def build_request_headers(self, verb):
        headers = {
            "X-EBAY-API-VERSION": self.config.get('version', ''),
            "X-EBAY-API-APP-ID": self.config.get('appid', ''),
            "X-EBAY-API-SITE-ID": self.config.get('siteid', ''),
            "X-EBAY-API-CALL-NAME": verb,
            "X-EBAY-API-REQUEST-ENCODING": "XML",
            "X-EBAY-API-IAF-TOKEN": self.config.get('token', ''),
            "Content-Type": "text/xml"
        }
```
