# Telegram API

## Overview

This is a Telegram API project designed for managing and interacting with various services based on Fast API. 
The application provides endpoints for authentication, group management, word management, level management, and word type management.

## Dependensy

This service provide data from another services: DataServive and AuthService via grpc connection. 

## Features

- **Authentication**: Login, validate tokens.
- **Group Management**: Create, update, retrieve, and delete groups.
- **Level Management**: Create, update, retrieve, and delete levels.
- **Word Management**: Add new words and retrieve words by user.
- **Word Type Management**: Create, update, retrieve, and delete word types.

## Prerequisites

- Python 3.8 or higher
- Use Poetry for a dependency installation from pyproject.toml:
(Install poetry and execute comand "poetry install")

## Environment

For enviroment installetion, you need to create you own .env and .test.env file
In cfg/config.py please write link to your cfg files
For a template use file: .template.env

## Installation

### Clone the Repository

git clone https://github.com/AlenaMeshcheriakova/TelegramAPI.git
cd TelegramAPI

### Starting project

For start up project, use: /src/api/main_service.py
After starting up project you can look on swager: http://localhost:8000/docs

