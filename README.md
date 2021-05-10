# DevOps Apprenticeship: Project Exercise

## Getting started

### Installing Poetry
Installation instructions can be found [`https://python-poetry.org/docs/%23installation`](here).

### Environment variables

you will need to take a copy of .env-template and call .env to which you will then need to provide values for  
TRELLO_KEY  
TRELLO_TOKEN  

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ poetry install
```
### On Windows (Using Git Bash)
```bash
$ poetry install
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

Your app should now be running in daemon mode:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Run using vagrant

If you havent already you will want to install vagrant details found [`https://www.vagrantup.com/docs/installation`](here)

Using a terminal you should change directory to this project and run the following

```vagrant up```

vagrant will begin to build your app using gunicorn rather than flask, once the build scripts stop providing feedback you
can now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Run using docker

### Development 
### build
```docker build --target development --tag todo-app:dev . ```
### run
```docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/,target=/todo_app todo-app:dev```

### Production 
### build
```docker build --target production --tag todo-app:prod . ```
### run
```docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/,target=/todo_app todo-app:prod```

### Run using docker compose (with image build) 
```docker compose up --build```