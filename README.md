# atcoder-helper

## Overview

Simple CLI helper tool for AtCoder

## Installation

- `pip install git+https://github.com/kenji-miyake/atcoder-helper`

## Usage

```sh
atcoder-helper gen [--contests-dir CONTESTS_DIR] [--template-file TEMPLATE_FILE] contest_id [alphabets [alphabets ...]]
```

## Example

```sh
vim template.cpp
atcoder-helper gen --template-file template.cpp abc001 A B
cd contests/abc001/A
vim main.cpp
```
