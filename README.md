# molecule-parser
Parse chemical formulas.

## Requirements
- [poetry](https://python-poetry.org/docs/#installation)
- Python >= 3.9

## Example
1. Set up virtual environment

   ```sh
   $ poetry install
   ```
3. Enter virtual environment

   ```sh
   $ poetry shell
   ```
5. Parse formulas:
    ```python
    >>> from molecule_parser import parse_molecule
    >>> parse_molecule("Mg(OH)2")
    {'Mg': 1, 'O': 2, 'H': 2}
    ```
    
## Running tests
```sh
$ poetry run pytest
```

## Additional notes
I also used this challenge as an opportunity to play with the [SLY](https://github.com/dabeaz/sly) library.
Though I did not manage to come up with a complete grammar (nested groups of atoms is missing).
In case you want to have a look, check out the `sly` branch.
