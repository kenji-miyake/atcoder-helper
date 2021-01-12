# atcoder-helper

## Overview

Simple CLI helper tool for AtCoder

## Installation

- `pip install git+https://github.com/kenji-miyake/atcoder-helper`

## Usage

```sh
atcoder-helper gen [--contests-dir CONTESTS_DIR] [--template-file TEMPLATE_FILE] contest_id [alphabets [alphabets ...]]
```

To use command-line completion, please follow the instructions in [argcomplete](https://github.com/kislyuk/argcomplete).

If you're using fish-shell, please run the following command.

```sh
register-python-argcomplete --shell fish atcoder-helper | source
```

## Example

```sh
# Create your template file
vim template.cpp

# Create contest workspace
atcoder-helper gen --template-file template.cpp abc001 A B

# Start coding
vim contests/abc001/A/main.cpp
```
