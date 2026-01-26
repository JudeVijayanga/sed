
# Troubleshooting

## ModuleNotFoundError

```bash
pip install -e .
```

Empty Output Folder

## Possible issues:

- wrong working directory

- missing or incorrect file paths

- no write permissions

```
import os
print(os.getcwd())
```

## Empty Plots

- flux file contains zeros or NaNs

- try plotting raw flux first

## Wrong Redshift Correction

Make sure spectrum.py matches:

```
suppliments/output.txt
```