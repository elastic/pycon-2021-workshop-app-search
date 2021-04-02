# Searchable Django Applications with Elastic App Search (PyCon US 2021)

## What to do before the Workshop?

- Fork / Clone the repository

  - `$ git clone https://github.com/elastic/pycon-2021-workshop-app-search`
  - `$ cd pycon-2021-workshop-app-search` 

- Create a virtual environment and install all
  dependencies in `requirements.txt`:
  
  - `$ python -m venv venv`
  - `$ source venv/bin/activate`
  - `$ (venv) python -m pip install -r requirements.txt`

- [Start an Enterprise Search instance](#starting-an-enterprise-search-instance). There are two
  options here:
  - Create an Elastic Cloud account (comes with a 14 day free trial no credit card required)
  - Install `docker-compose` and use `docker-compose up` to start an Enterprise Search instance locally

- Update the `url` and `private_key` values in `config.yml` 
  per the instructions for starting the Enterprise Search instance below.

- Make sure at least `examples/example_1_making_requests.py`
  is able to run completely. You should see the message
  `Everything worked! :-)` in your terminal. All examples are
  meant to be run via `python examples/example_N_...py` or
  via the "Run" functionality in your IDE.

## Starting an Enterprise Search instance

### Elastic Cloud

- Create an [Elastic Cloud account](https://www.elastic.co/cloud)
- Create a new Deployment using the "Enterprise Search" template
- Select a cloud provider and region and select `Create Deployment`.
  The instance will be provisioned and available in a few minutes
- Click `Launch` or `Copy Endpoint` in the new deployment overview
  and copy the URL (minus the `/login` path). The result should look like
  approximately this: `https://(deployment name)-1a6dc7.ent.us-west1.gcp.cloud.es.io`
- Open `config.yml` and set `url` field to be `"https://(deployment name)-1a6dc7.ent.us-west1.gcp.cloud.es.io"`
  and run the script and ensure it passes without error.
- Select `Launch App Search`, from here you'll be placed in a getting started
  screen. You can follow these steps if you'd like otherwise you can
  select `Skip Onboarding` in the top.
- That's it, you're now in App Search!  

### Docker Compose

- Download and install [docker-compose](https://docs.docker.com/compose)
- With an open terminal in the cloned git repository run `docker-compose up`.
  Wait for all services to 
- You should be able to connect to `http://localhost:3002` in a browser
- Open `config.yml` and set `url` field to be `"http://localhost:3002"`
  and run the script and ensure it passes without error.
- The username will be `enterprise_search` and the password will be `changeme`.
- Select `Launch App Search`, from here you'll be placed in a getting started
  screen. You can follow these steps if you'd like otherwise you can
  select `Skip Onboarding` in the top.
- That's it, you're now in App Search!  

### Finding your Private Key

- When in App Search, navigate to the `Credentials` tab
- Click the `Copy to Clipboard` button next to the Private Key
- Paste the value into the `private_key` field in `config.yml`

## Getting Started with the Django App

### Setup

- Ensure your virtualenv is activated and `requirements.txt` is installed
- Change directory into `django/`
- Run `python manage.py migrations` to create `db.sqlite3`
- Run `python manage.py runserver` to start the server on `http://localhost:8000`.
  Don't use these exact configurations in production!
- Access [`http://localhost:8000/reset`](http://localhost:8000/reset) to load data into the Django database

### URLs of Interest

- [`http://localhost:8000/<park-id>`](http://localhost:8000/park-acadia) Shows a park by ID within the Django database
- [`http://localhost:8000/search`](http://localhost:8000/search) Has the Reference UI configured for App Search
- [`http://localhost:8000/remove-park`](http://localhost:8000/remove-park) Removes `park-acadia` from the Django database, see how signals keep App Search up to date.
- [`http://localhost:8000/add-park`](http://localhost:8000/add-park) Adds `park-acadia` from the Django database, see how signals keep App Search up to date.
- [`http://localhost:8000/remove-m2m`](http://localhost:8000/remove-m2m) Removes the state `Tennessee` from `park-great-smoky-mountains`, see how signals keep App Search up to date.
- [`http://localhost:8000/add-m2m`](http://localhost:8000/add-m2m) Adds the state `Tennessee` to `park-great-smoky-mountains`, see how signals keep App Search up to date.
- [`http://localhost:8000/reset`](http://localhost:8000/reset) Resets the Django database to its original set of data (takes a while because we're not using background tasks)
- [`http://localhost:8000/run-task`](http://localhost:8000/run-task)
  Runs the background task to index documents from the database into a new source engine and update a meta engine.

### Indexing Models into App Search

See `django/parks/models.py` for the signals approach to indexing documents in App Search.
See `django/parks/tasks.py` for the tasks approach to indexing documents in App Search.

When doing this in real life I recommend using background tasks
for signal handlers to avoid blocking web requests.

### Reference UI

The [Reference UI](https://github.com/elastic/app-search-reference-ui-react) has been generated and the production compressed JS and CSS are stored in `django/static/`.
When you're creating your own Reference UI you should not copy these and instead follow the instructions
on the Reference UI repository.
