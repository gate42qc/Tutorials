# Tutorials

## Setup

In order to run the tutorials, you need to have some libraries installed.
They are specified in `requirements.txt` file.

You can install them by running `pip install -r requirements.txt`.

### Virtualenv

It is generally recommended to run projects in separate virtual environments.
In order to install such environment and make it work with jupyter notebook you can follow [this tutorial](https://medium.com/@eleroy/jupyter-notebook-in-a-virtual-environment-virtualenv-8f3c3448247).

If the method `ipython kernel install --user --name=venv-name` provided in this tutorial doesn't work for you, you can try `python -m ipykernel install --user --name=venv-name`.