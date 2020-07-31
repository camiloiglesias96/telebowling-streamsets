# Telebowling Data Streamsets

Sistema de transmisión de datos telemetricos para sistemass de bowling Brunswick que permitira
aplicar tecnicas posteriores de BI (Business Intelligence) para asi ofrecer a nuestros clientes
un control remoto de sus establecimientos

# Instalación

``` 
Clone the project

    git clone https://github.com/camiloiglesias96/telebowling-streamsets.git

Install all dependencies

    pipenv install

Run virtual environment

    pipenv shell

Run migrations

    pipenv run python scripts\migrate.py

Make the initial data installation

    pipenv run python scripts\install.py
```

