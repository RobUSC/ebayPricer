# ebayPricer
Specifically created as comic pricing scraper, as I go along I'll make the entries configurable

Based on the tutorial found at:  https://linuxconfig.org/introduction-to-ebay-api-with-python-obtaining-keys-and-accessing-the-sandbox-part-1

Uses OAuth token to auithenticate with eBay APIs, this is performed with an override of the eBaySDK Shopping Connection class.

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
Integrate with MongoDB for better reflection on processed data (highs/lows/outliers)
Refine eBay matched item filtering (e.g non exact matches)
Filter clickbait titles like "CGC IT!" or "Homages"
