# cave-link-client

Python script to download data from the Cave-Link API and write it to a CSV file

## Without Poetry

### Installation

Clone the repository:

```shell
git clone https://github.com/vuilleumierc/cave-link-client.git
cd cave-link-client
```

Create a venv and install the project:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### Usage

```shell
cavelink-get --station 106 --group 0 --length 10 --output cavelink.csv
```

### Help

```shell
poetry run cavelink-get --help
```

## With Poetry

### Requirements

[Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

### Installation

```shell
git clone https://github.com/vuilleumierc/cave-link-client.git
cd cave-link-client
poetry install
```

### Usage

```shell
poetry run cavelink-get --station 106 --group 0 --length 10 --output cavelink.csv
```

### Help

```shell
poetry run cavelink-get --help
```
