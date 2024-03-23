### Getting started
#### Run the API locally
You may [install pixi](https://pixi.sh/latest/#installation) and subsequently run `pixi install` in the root folder to install all dependencies.

Subsequently, you currently have to run `pixi run pip_install_e` to install `banking_api` as a python package via `pip install -e .` into the pixi environment.

Finally, you can simply `pixi run api` to launch the api locally.

#### Contribute to the API development
Assuming you [installed pre-commit](https://pre-commit.com/#installation), run `pre-commit install` and subsequently `pre-commit run --all-files`.

Depending on your IDE preferences, you may need to select pixi as python interpreter and configure test discoverage. 
If you use VS Code, you can leverage the `.vscode` configurations automatically.

You are ready to contribute! :)
