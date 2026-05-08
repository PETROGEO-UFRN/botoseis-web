# Manual run

### Dependencies for manual run

  - [SeismicUnix]() (There is a step to install it bellow)
  - [Docker]() (Necessary for quiky run)
  - [Unix]() Based system (SeismicUnix installationg script only work on [Debia]() based systens)
  - [Python](https://www.python.org/) v3.10.8 or above


### Database

Run a postgres database and set it's connection parameters at `.env` file.


To run the migrations, run on your terminal in the server folder:

```bash
flask db upgrade
```
To create a new migration:
```bash
flask db migrate -m 'Migration Name'
```

### Run the server

Once inside the `server` folder, install its dependencies and run the dev environment as shown below.
```bash
pip3 install -r requirements.txt
```
```bash
flask run
```
