# Student Scheduler

## How to start
```bash
./docker-compose.sh run ENV
```

Replace `ENV` with the name of the environment you want to use. The available environments are:
- `dev`: For development. This environment uses the settings in the .env.dev file.
- `test`: For testing. This environment uses the settings in the .env.test file.
- `prod`: For production. This environment uses the settings in the .env.prod file.

For example, to start the application in the development environment, you would run:
```bash
./docker-compose.sh run dev
```

## Building the application
```bash
./docker-compose.sh build ENV
```
Replace `ENV` with the name of the environment you want to use. The available environments are `dev`, `test`, and `prod`.

For example, to build the application in the development environment, you would run:
```bash
./docker-compose.sh build dev
```

## Stop and remove containers
```bash
./docker-compose.sh down ENV
```
Replace `ENV` with the name of the environment you want to stop and remove. The available environments are `dev`, `test`, and `prod`.

For example, to stop and remove the application in the development environment, you would run:
```bash
./docker-compose.sh down dev
```

## Clean up Docker
```bash
./docker-compose.sh clean
```
This command will remove all unused containers, networks, and dangling images.