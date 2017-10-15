# Cryptocoin-Market-Toolkit v1.1

A command line tool (python script) to view cryptocoin details. Data is pulled from Coinmarketcap API, more sources will be added soon.

### Features
  - Auto updates local cache every 5 mins
  - List top coins (sorting option available)
  - Search coins (sorting option available)

### What's New in v1.1
- Local currency support
- Codebase rewritten (modular)

### Usage
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
Setup (one time only)
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
$ ./cmt.py --top 50
```

List top 50 cryptocoins with custom sorting.
Available sorting params:
* rank
* price
* marketcap
* rank_asc
* rank_desc
* price_asc
* price_desc
* marketcap_asc
* marketcap_desc

```sh
$ ./cmt.py --top 50 --sortorder marketcap_desc
$ ./cmt.py --top 50 --sortorder price_desc
$ ./cmt.py --top 50 --sortorder price_asc
$ ./cmt.py --top 50 --sortorder rank_asc
```

Search for cryptocoins
```sh
$ ./cmt.py --search bitcoin
```
Search with sorting (same sorting params available)
```sh
S ./cmt.py --search eth --sortorder marketcap_desc
```

### Todos

 - More features (undisclosed （ ^_^）o自自o（^_^ ）)
 - Colored output

### Donate

###### BTC 3BsKLChCTuNk1Shcyya2EvqDH8MTq6p81F
###### LTC LKxHN94vkseoLRikB8nCxT3oUX8h6tcZ5Z
###### ETH 0x44C1c4870c38E3F2f712C1c25d31A57ef59caEca 

License
----
Apache License 2.0