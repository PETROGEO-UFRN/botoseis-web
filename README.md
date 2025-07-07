# CloudSeis

CloudSeis is a cloud-based seismic data processing software based on the desktop app [BotoSeis](https://github.com/botoseis/BotoSeis)
<br />
CloudSeis is mainly a wrapper for [SeismicUnix](https://github.com/JohnWStockwellJr/SeisUnix) allowing usage through API and web UI, adding tooling for store, track and organize data processing steps.

![Database diagram, simplified version](
  ./docs/assets/home_screen.png
)

## Getting Started

### Dependencies

 - Main dependencies:
    - [SeismicUnix]() (There is a step to install it bellow)
    - [Docker]() (Necessary for quiky run)
    - [Unix]() Based system (SeismicUnix installationg script only work on [Debia]() based systens)
 - Opcional dependancies, for manual run only (docker handle they)
    - [Python](https://www.python.org/) v3.10.8 or above
    - [Node.js](https://nodejs.org/en) v16 or above
    - [yarn](https://yarnpkg.com/) v1.22.19 or above

#### Installing seismic unix

run the command line bellow on visit the oficial guide to manual install
```bash
bash -c "$(wget -qO- https://gist.githubusercontent.com/botoseis/4ca681cb9ef706c1b8410153c6199cf2/raw/b16ad754839d1ca3657d8e8396db14f5ba791e6b/install_seismic_unix.sh)"
```

### Quicky start
   >  Requires **docker-compose**

Go to root and run the Makefile. It will make available the necessery services for end user.
```bash
make
```


For automate tests, make the test database available by runing:
```bash
make test
``` 

For manage or make new programs available, run the admin dashboard:
```bash
make adm
```


Each service can be run and managed individualy with docker-compose.

To manully run any instance without docker, check each folder `README.md`.


# Architeture

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