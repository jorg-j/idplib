# IDP Python Utilities

The purpose of this library is to provide useful tools to support IDP based processes


## Install

```
pip install IDPlib
```

## Usage

Useage will be broken down into a few concepts. General and tool specific.

### General

ValueUtils 

#### Normalisers
```
from idplib import ValueUtils

# Takes a digit as a string and returns a string 
# Removes spaces, hyphens, comma, dollar sign
# Or you can submit your own pattern to normalise, this allows you to handle for specific cases

result = ValueUtils.Normalise.digit('$5')
>>> '5'

result = ValueUtils.Normalise.digit('5%', pattern=r"[ -\$,%]")
>>> '5'

# Safely round numbers as python can incorrectly round floating point digits

result = ValueUtils.Normalise.safe_round(1.515)
>>> 1.52

result = ValueUtils.Normalise.safe_round(1.5155, decimal_places=3)
>>> 1.5

# Dates

# To Convert a string into a date. Handles most non American formats

result = ValueUtils.Normalise.Date.from_string('1/5/2024')
>>> datetime.datetime(2024, 5,1, 0, 0)

# Get the tax year from a date given the tax year starts July 1

result = ValueUtils.Normalise.Date.tax_year('1/8/2024')
>>> 2025

```
