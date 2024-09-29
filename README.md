<h1 align="center">Perfect Sound Server</h1>
<p align="center">A Backend Service for Perfect Sound</p>
<p align="center">
	<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Miltonbhowmick/perfectsound-server"> 
</p>

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)

## About

Perfect sound is a music playing website where users buy new subscription and download musics. Each subscription has a large amount of credits. Users only download musics until they have credits.

## Features

- Playing music.
- Bottom Player playing music along with Playing list music.
- Subscription plan for a certain amount of time.
  
## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed:

- Docker
- Python 3.9+
- Setup Stripe Account for test API keys. Please check `.env.example`

### Installation

1. Clone the repository:
   `git clone https://github.com/Miltonbhowmick/perfectsound-server.git`
2. Navigate to the project directory:
	`cd perfectsound-server`
3. Pull containers of docker:
  `docker-compose pull`
4. Start the development server:
 	`docker-compose up server`  
5. Open your web browser and access django admin of the application at http://localhost:8000/admin. [Please check the terminal which port is running for django]

## License
This project is licensed under the [MIT License](./LICENSE) - see the [LICENSE](./LICENSE) file for details.

