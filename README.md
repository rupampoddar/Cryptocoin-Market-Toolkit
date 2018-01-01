# Cryptocoin-Market-Toolkit v1.3

```
   ______   ____ ___   _______
  / ____/  / __ `__ \ /__  __/
 / /      / / / / / /   / /
/ /____  / / / / / /   / /
\_____/ /_/ /_/ /_/   /_/

Author @xc3p7i0n (twitter.com/xc3p7i0n)
```
A command line tool (python script) to view cryptocoin details. Data is pulled from Coinmarketcap API, more sources _may_ be added soon.

### Features
* Auto updates local cache every 5 mins
* List top coins (sorting option available)
* Search coins (sorting option available)

### What's New
#### v1.3
* Field added - Available Supply
* Sorting option added - supply_asc & supply_desc

#### v1.2
* Sorting option added - % changes in last 1h/24h/7d

#### v1.1
* Local currency support
* Codebase rewritten (modular)

### Requirements
Python libs required
* requests
* tabulate

```sh
$ pip install requests
$ pip install tabulate
```

```sh
$ cd Cryptocoin-Market-Toolkit/
```
### Usage
#### Setup (one time only)

Default Setup (USD Only) 
```sh 
$ chmod +x cmt.py
$ ./cmt.py --setup
```

Setup with local currency support
```sh 
$ chmod +x cmt.py
$ ./cmt.py --setup --localcurrency inr
```

Run program to show help
```sh
$ ./cmt.py
```

List top 50 cryptocoins (sorted by Rank)
```sh
$ ./cmt.py -t 50
```

List top 50 cryptocoins with custom sorting.
Available sorting params (asc=Ascending, desc=Descending): 
* rank
* price
* marketcap
* rank_asc
* rank_desc
* price_asc
* price_desc
* marketcap_asc
* marketcap_desc
* pc1  | pc1_asc  | pc1_desc   (% change in last 1 hour)
* pc24 | pc24_asc | pc24_desc  (% change in last 24 hours)
* pc7  | pc7_asc  | pc7_desc   (% change in last 7 days)
* supply_asc
* supply_desc

```sh
$ ./cmt.py -t 50 -so marketcap_desc
$ ./cmt.py -t 50 -so price_desc
$ ./cmt.py -t 50 -so price_asc
$ ./cmt.py -t 50 -so rank_asc
$ ./cmt.py -t 50 -so pc1_desc
$ ./cmt.py -t 50 -so pc7_desc
```

Search for cryptocoins
```sh
$ ./cmt.py -s bitcoin
```

Search with sorting (same sorting params available)
```sh
$ ./cmt.py -s eth -so marketcap_desc
```

### Todos
* More features (undisclosed （ ^_^）o自自o（^_^ ）)
* Colored output

### Feature Request / Bug Report
DM me on twitter :)

### Donate

###### XRP r4s9nRF26kBuJPjA529mpPwzGR2kJRFoTP
###### BTC 1CowJJXhA9NfB4wCu4pytfyFv6Zy14LD2G
###### ETH 0xCB5132a2cA1AC210e9E32FCC590523768C8b205F

License
----
Apache License 2.0