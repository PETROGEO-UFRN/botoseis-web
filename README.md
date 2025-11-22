# CloudSeis

CloudSeis is a cloud-based seismic data processing software based on the desktop app [BotoSeis](https://github.com/botoseis/BotoSeis)
<br />
CloudSeis is mainly a wrapper for [SeismicUnix](https://github.com/JohnWStockwellJr/SeisUnix) allowing usage through API and web UI, adding tooling for store, track and organize data processing steps.

![Workspace main screen with sample workflow](
  ./docs/assets/home_screen.png
)

## Getting Started

### Requirements
  - Docker
  - Docker Compose
  - Unix based system
  - Make


### Running local demo

Go to root and run the Makefile for local-demo. It will make available the necessery services for end user.
```bash
make local-demo
```
The program workspace can be access through [`http://localhost:4173/`](http://localhost:4173/)

By default, local demo mode will accept login with e-mail password `root@admin.com`. This setup is for fast local-demo only and should not be used on a production server.


</br>
</br>

For automate tests, make the test database available by runing:
```bash
make test
``` 

For managing or making new programs available, run the admin dashboard:
```bash
make adm
```


Each service can be run and managed individualy with docker-compose.

To manully run any instance without docker, check each service `README.md` on each service folder.


# Architeture

### Tech Stack

  - [Python](https://www.python.org/) *running v3.12*
  - [Flask](https://flask.palletsprojects.com/en/stable/)
  - [Bokeh](https://bokeh.org/)
  - [Numpy](https://numpy.org/)
  - [SQLAlchemy](https://www.sqlalchemy.org/)
  - [Typescript](https://www.typescriptlang.org/) *running v22.18, v16 or above should work*
  - [React](https://react.dev/) *managed by [Vite](https://vite.dev/)*
  - [Docker](https://www.docker.com/)
  - [Docker Compose](https://docs.docker.com/compose/)
  - [SeismicUnix](https://wiki.seismic-unix.org/start) *pre loaded scripts*

### Services

![High level architecture diagram](
  ./docs/assets/architecture.png
)

The project is divided in 4 services:
 - API <br />
   Base API that handle every persistent storage on the aplication
 - Admin Client <br />
   Web interface that provides management of the programs available for the end user. The admin can create, delete and modify programs information. It will reflect in the end user view. 
 - Workspace <br />
   The end user view. Where the avarage end user must interact with it's workflows, files and history information
 - Data-view <br />
   Vizualization web interface. Usualy it opens as result of some action at the Workspace, displaying visualization tools for the selected data or for the resulting data of some process.

### Database diagram

![Database diagram, simplified version](
  ./docs/assets/database_simplified_diagram.png
)
Database diagram simplified for easier understanding of data flow. <br />
Mostly every table have a column to identify who can access and modify each row.