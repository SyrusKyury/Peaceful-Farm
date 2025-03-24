# Peaceful Farm

![Peaceful-Farm-Logo](docs/logo.png)

## Introduction
**Peaceful Farm** is an Exploit Manager specifically designed for Attack-Defense CTF (Capture The Flag) competitions. It consists of two key components:

- **Peaceful Farm Server**: Collects flags from clients and submits them to the game server. It also provides a web interface with detailed statistics and real-time updates.
- **Peaceful Farm Client**: Executes attacks on adversaries' services, retrieves flags, and sends them back to the Peaceful Farm Server.

## Features
- Web interface with detailed statistics and attack performance charts
- Timed flag submission system synchronized with competition rounds
- Automatic generation of multithreaded Python clients for parallel exploits
- Backup flag submission: If the server is unreachable, clients store stolen flags for future submission
- CSV report generation for easy data analysis
- API route and web interface protection via authentication
- Management of request concurrency to optimize performance
- Feedback on failed attack attempts
- Real-time logging via the web interface's console
- Submission Server emulation for testing exploits
- [Simple plugin system](web/app/plugins/README.md) for easy system updates and extensions
- GUI-based application setup for ease of configuration
- Support for running exploits in Python, PHP, and JavaScript

## Architecture
![Architecture](docs/architecture.png)

## Requirements

### Server
- Docker
- Docker Compose

### Client
- Python 3

## Getting Started

### Setting up the Server
To start using **Peaceful Farm**, first launch the server using one of the following commands in the project directory:

```bash
docker-compose up -d --build
```

or

```bash
docker compose up -d --build
```

Your server is now ready to use!

### Setting up the Client
The client can be downloaded from your **Peaceful Farm Server** by visiting the index page.

To use the client, simply define your exploit in the *exploit* function. The client will automatically execute this function against each opposing team in parallel, collecting flags and sending them to your **Peaceful Farm Server**.

The *exploit* function takes two parameters:

- **target_ip**: The IP address of the target machine.
- **exploit_data**: A storage container for any reusable data required for future exploitations.

For example, when exploiting a Flask web application that leaks a secret token, you wouldn’t want to repeatedly steal the token every time the exploit runs. Instead, store and reuse the token in *exploit_data*, which helps maintain stealth and efficiency.

### Screenshots

#### Login Screen
![Login Screen of Peaceful Farm](docs/login.png)

#### Dashboard Overview
![Dashboard of Peaceful Farm](docs/dashboard.png)

#### Information Page
![Information Page of Peaceful Farm](docs/info.png)

#### Settings Page
![Settings Page of Peaceful Farm](docs/settings.png)