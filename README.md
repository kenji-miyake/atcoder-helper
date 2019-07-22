# atcoder-helper

## Overview

Simple CLI helper tool for AtCoder

## Installation

- `pip install git+https://github.com/kenji-miyake/atcoder-helper`

## Usage

```sh
atcoder-helper [-h] [--contests-dir CONTESTS_DIR] [--template-file TEMPLATE_FILE] contest_id
```

## Example

```sh
vim template.cpp
atcoder-helper gen --template-file template.cpp abc001
cd contests/abc001/A
vim main.cpp
```
