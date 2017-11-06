# Project Dashboard

## Setup
1. Install [Docker](https://www.docker.com)
2. Run `docker-compose up` to start server
3. Run `docker-compose run web python manage.py migrate` to install migrations
4. Run `docker-compose run web python manage.py install_demo` to install demo data
5. Open Browser [localhost:8000](http://localhost:8000)


## ToDo

- [ ] Budget -> list earnings
- [ ] Risk -> display risks
- [ ] Risk -> display issues
- [ ] Risk -> calculate status
- [ ] Display correct project status
- [ ] Progressbar in header
- [ ] Admin UI
