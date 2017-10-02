# Cryptocoin-Market-Toolkit

A command line tool (python script) to view cryptocoin details. Data is pulled from Coinmarketcap API, more sources will be added soon.

### Features
  - List top coins (sort by rank|price|marketcap)
  - Search coins (sort by rank|price|marketcap)

### Usage
Python libs required
* requests
```sh
$ cd Cryptocoin-Market-Toolkit/
```
Setup local database (one time only)
```sh
$ chmod +x db_setup.py
$ ./db_setup.py
```

Run program to show help
```sh
$ chmod +x program.py
$ ./program.py
```

Update local database 
```sh
$ ./program.py --update
```

List top 50 cryptocoins (sorted by Rank)
```sh
$ ./program.py --top 50
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
$ ./program.py --top 50 --sortorder marketcap_desc
$ ./program.py --top 50 --sortorder price_desc
$ ./program.py --top 50 --sortorder price_asc
$ ./program.py --top 50 --sortorder rank_asc
```

Search for cryptocoins
```sh
$ ./program.py --search bitcoin
```
Search with sorting (same sorting params available)
```sh
S ./program.py --search eth --sortorder marketcap_desc
```

### Todos

 - More features (undisclosed （ ^_^）o自自o（^_^ ）)
 - Colored output
 - Local currency support

### Donate

###### BTC 3BsKLChCTuNk1Shcyya2EvqDH8MTq6p81F
###### LTC LKxHN94vkseoLRikB8nCxT3oUX8h6tcZ5Z
###### ETH 0x44C1c4870c38E3F2f712C1c25d31A57ef59caEca 

License
----
Apache License 2.0