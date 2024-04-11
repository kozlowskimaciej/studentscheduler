#!/bin/sh

command=$1
env=$2

if [ "$command" = "clean" ]; then
    echo "In clean mode."
    docker container prune -f
    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
    exit 0
fi

if [ -z "$env" ]; then
    echo "No environment provided. Please provide a valid environment (dev, prod, test)."
    echo "Usage: ./docker-compose.sh [command] [env]"
    exit 1
fi

if [ "$env" != "dev" ] && [ "$env" != "test" ] && [ "$env" != "prod" ]; then
    echo "Invalid environment provided. Must be 'dev', 'test', or 'prod'."
    exit 1
fi

if [ ! -f "./.env.$env" ]; then
    echo "The config file .env.$env does not exist."
    exit 1
fi

docker_command="docker compose --env-file ./.env.$env -f ./docker/docker-compose.yml"

if [ "$command" = "down" ]; then
    echo "Running docker-compose down -v"
    $docker_command down -v
elif [ "$command" = "run" ]; then
    if [ "$env" = "test" ]; then
        echo "STARTING TEST ENVIRONMENT"
        $docker_command run backend
    else
        echo "STARTING DEV ENVIRONMENT"
        $docker_command up 
    fi
elif [ "$command" = "build"  ]; then
    if [ "$env" = "test" ]; then
        echo "Building the test docker image"
        $docker_command build backend
    else
        echo "Building the docker images for $env environment."
        $docker_command build
    fi
else
    echo "Invalid command. Please provide a valid command (run, build, down, clean)."
    echo "Usage: ./docker-compose.sh [command] [env]"
    exit 1
fi
