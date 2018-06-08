# solr-fstats - Solr fields statistics

solr-fstats is a commandline command (Python3 program) that extracts some statistics regarding field coverage from a Solr index. It prints the output as pure CSV data (all values are quoted) to stdout.

## Usage

```
solr-fstats
    required arguments:
        -core CORE  Solr core to use (default: None)

    optional arguments:
        -h, --help  show this help message and exit
        -host HOST  hostname or IP address of the Solr instance to use (default:localhost)
        -port PORT  port of the Solr instance to use (default: 8983)
```

* example:
    ```
    solr-fstats -host [HOSTNAME OF YOUR SOLR INSTANCE] -core [YOUR SOLR CORE] > [OUTPUT STATISTICS DOCUMENT]
    ```

### Note

Currently, concrete fields that are included into a definition of a dynamic field are not part of the field statistics, i.e., only static fields will be evaluated right now.

## Requirements

* [requests](http://docs.python-requests.org/en/master/)
* [sortedcontainers](http://www.grantjenks.com/docs/sortedcontainers/)

### Install requirements

1. (optionally) install [pip](https://pip.pypa.io/) for Python 3.x:

    sudo apt-get install python3-pip

2. install requirements with pip:

    sudo -H pip3 install -r requirements.txt

## Run

* install requirements
* clone this git repo or just download the [solr_fstats.py](solr_fstats/solr_fstats.py) file
* run ./solr_fstats.py
* for a hackish way to use solr_fstats system-wide, copy to /usr/local/bin

### Install system-wide via pip

* via pip:
    ```
    sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF SOLR-FSTATS]
    ```
    (which provides you ```solr-fstats``` as a system-wide commandline command)

## Description

(of the column headers of a resulting statistic)

### ... in English

#### field_name
* the field (path) of this statistic line

#### existing
* number of records that contain this field (path), i.e., field coverage

#### existing_percentage
* ^ percentage of 'existing'
* (existing / Total Records * 100)

#### notexisting
* number of records that do not contain this field (path)

#### notexisting_percentage
* ^ percentage of 'notexisting'
* (not existing / Total Records * 100)

### ... in German

Erklärung der Spaltenköpfe

#### field_name
* Der Pfad zu den analysierten Werten

#### existing
* gibt an, wieviele Felder diesen Pfades existieren.

#### existing_percentage
* existing in Prozent
* existing / Total Records * 100

#### notexisting
* gibt an, wieviele Rekords nicht über diesen Pfad verfügen

#### notexisting_percentage
* notexisting in Prozent
* notexisting / Total Records * 100)
