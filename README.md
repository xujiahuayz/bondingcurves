# SOK: Decentralized exchanges (DEX) with automated market maker (AMM) protocols

This is an exploration of the different automated market making algorithms in DeFi.

## Table Of Contents

- [Table of Contents](#table-of-contents)
- [Setup](#setup)
- [Conservation function, slippage and divergence loss plots](#Conservation-function,-slippage-and-divergence-loss-plots)
- [Contirbuting](#contributing)

## Setup

We recommend you use `pyenv` to manage your python versions.

We have used **python 3.9.1** in this repo.

On how to use `pyenv`, see [here](https://realpython.com/intro-to-pyenv/).

We also advise you to use **venv** module to manage the per project python dependencies.

For example, once you have installed the **3.9.1** python version with `pyenv`, execute this

```bash
python -m venv ~/.v/uclamm
```

This command will create a `uclamm` python virutal environment. Now you are ready to install the dependencies required for this project.

Activate the environment

```bash
source ~/.v/uclamm/bin/activate
```

Now, install the dependencies

```bash
pip install -r requirements.txt
```

## Conservation function, slippage and divergence loss plots

To plot all of these, run

```bash
python -m amms.analysis
```

from the root of this workspace. Note that it takes some time to plot all of these.

## Contributing

You must follow our code style if you want to make a pull request. We are using `pre-commit` to maintain our code style and formatting (**flake8** and **black**). To activate the pre-commit hooks, run

```bash
pre-commit install
```

in the root of this workspace. This will enable automatic linting and formatting on commits, so that you don't to worry about it.