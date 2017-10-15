# Cryptocoin-Market-Toolkit v1.2

A command line tool (python script) to view cryptocoin details. Data is pulled from Coinmarketcap API, more sources will be added soon.

### Features
* Auto updates local cache every 5 mins
* List top coins (sorting option available)
* Search coins (sorting option available)

### What's New
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

### Donate

###### BTC 3BsKLChCTuNk1Shcyya2EvqDH8MTq6p81F
###### LTC LKxHN94vkseoLRikB8nCxT3oUX8h6tcZ5Z
###### ETH 0x44C1c4870c38E3F2f712C1c25d31A57ef59caEca 

License
----
Apache License 2.0