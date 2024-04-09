# Student Scheduler

## How to start
```bash
./docker-compose.sh -e ENV up
```

Replace `ENV` with the name of the environment you want to use. The available environments are:
- `dev`: For development. This environment uses the settings in the .env.dev file.
- `prod`: For development. This environment uses the settings in the .env.prod file.

For example, to start the application in the development environment, you would run:
```bash
./docker-compose.sh -e dev up
```

## Stop and remove containers
```bash
./docker-compose.sh -e ENV down
```
Remove containers, networks and volumes