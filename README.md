[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/jolsfd/inzidenz-ampel)
[![License](https://img.shields.io/github/license/jolsfd/inzidenz-ampel.svg)](https://github.com/jolsfd/inzidenz-ampel/blob/main/LICENSE)

# Inzidenz-Ampel

The program uses the API of the RKI to determine the incidence value of a district in Germany. The value describes the new infections per 100,000 inhabitants in one week. 

## Setup

You need Python installed. You can download it [here](https://www.python.org/downloads/).

Clone Repository or download on the [releases page](https://github.com/jolsfd/inzidenz-ampel/releases/latest):

```bash
git clone https://github.com/jolsfd/inzidenz-ampel.git
```

Install requirements:

```bash
pip install -r requirements.txt
```

You need to configure the OBJECT_ID in `incidence.py` for your district. You can get the OBJECT_ID 
[here](https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0).

```python
# Example for Berlin Mitte

OBJECT_ID = "413"
```

## Run 

```
python incidence.py
```

## License

Released under the terms of the [MIT License](https://github.com/jolsfd/inzidenz-ampel/blob/main/LICENSE).