wedding list
=========

## Overview

**wedding list** is a working progress web app I've built for testing purposes. 

## How to use?
## With Docker
You will need on your machine Docker version 19.03.12 or plus,
and also docker-compose version 1.26.2 or plus installed on your machine.

```
docker-compose -f dev.yml up 
```

You might need to run it twice the first time in order to let the database container
create and initialize the database.

If you want to get inside the container and debug the app with pdb, 
you can do the following:

1) Enter the container:

`docker container exec -ti weddinglistbackend bash`

2) Run django development server using port 8080

`python manage.py runserver 0.0.0.0:8080`


3) I have created a Django management command "prepare" to add fake data to 
the database, this will be added automatically, but if you want to try it out
just run:

`python manage.py prepare`

4) You are ready to go, just go to your localhost at http://localhost/
and you will see the app running.

## TODO
- missing tests
- missing CI
- would be nice to split FE from BE completely.

## Contributing


## Notes

During the development of this project I tried to follow domain driven design
principles, so it has a lot of DDD on it.

## License

Copyright ©‎ 2020, [ottotech](https://ottotech.site/)

Released under MIT license, see [LICENSE](https://github.com/ottotech/godic/blob/master/LICENSE.md) for details.