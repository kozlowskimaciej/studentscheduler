#!/bin/sh

while getopts e: flag
do
    case "${flag}" in
        e) env=${OPTARG};;
    esac
done

shift $((OPTIND -1))

if [ -z "$env" ]; then
    echo "No environment provided. Defaulting to dev."
    env="dev"
fi

if [ ! -f "./.env.$env" ]; then
    echo "The file .env.$env does not exist."
    exit 1
fi

if [ "$1" = "clean" ]; then
    echo "In clean mode."
    docker container prune -f
    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
elif [ "$1" = "down" ]; then
    echo "Running docker-compose down -v"
    docker-compose --env-file ./.env.$env -f ./docker/docker-compose.yml down -v
else
    echo "Running docker-compose with env file .env.$env"
    docker-compose --env-file ./.env.$env -f ./docker/docker-compose.yml up ${@:2}
fi