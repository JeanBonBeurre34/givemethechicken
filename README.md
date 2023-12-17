# givemethechicken

## Description
This project is a Python-based server that simulates a Unix file system. It allows clients to connect via a network and execute basic Unix-like commands such as **ls**, **touch**, **mkdir**, **cd**, **echo**, and **cat**. The server is designed to handle multiple client connections simultaneously, providing each client with its own isolated file system environment.

## Features
* Simulated Unix file system commands (ls, touch, echo, cat, mkdir, cd).
* Multi-threaded server handling multiple clients at once.
* Dockerized application for easy deployment.
* Automated Docker image build and push to Docker Hub using GitHub Actions.

## Getting Started

### Prerequisites
* Python 3.9 or later.
* Docker (for running within a container).
* Git (for version control)

### Installation
**Clone the repository**
```bash
git clone https://github.com/JeanBonBeurre34/givemethechicken
```

**Running locally using python**
```bash
python givemethechicken.py
```

**Build and running using docker**
Build your docker container locally
```bash
docker build -t givemethechicken:latest .
```

**run the container locally**
Run the container locally and expose the port 9999.
```bash
docker run -d -p 9999:9999 givemethechicken:latest
```
The container will start in daemon mode and expose the port 9999 to connect on.

**check the running container**
Check to get the running container
```bash
docker ps
```
