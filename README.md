# PyQt5 Chat Application with Exclusive Voice

![Project Banner](https://github.com/your-username/your-repo-name/blob/main/path/to/banner/image.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Setup Backend (Server)](#setup-backend-server)
  - [Setup Frontend (Client)](#setup-frontend-client)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Running the Client](#running-the-client)
- [Message Protocol](#message-protocol)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Introduction

Welcome to the **PyQt5 Chat Application with Exclusive Voice**, a real-time chat platform that seamlessly integrates both text and voice communication. This application ensures that only one user can speak at a time, preventing overlapping audio and fostering organized conversations. Built with Python's PyQt5 for the client and leveraging socket programming for the server, this project offers a robust solution for real-time interactions.

![Chat Interface](https://github.com/your-username/your-repo-name/blob/main/path/to/screenshot/chat_interface.png)

## Features

- **User Authentication:** Securely log in using unique nicknames.
- **Real-time Text Chat:** Instant messaging with all connected users.
- **Exclusive Voice Communication:** Only one user can speak at a time, preventing audio overlap.
- **Online Users List:** View currently connected users with active voice indicators.
- **Responsive GUI:** User-friendly interface built with PyQt5.
- **Error Handling:** Graceful handling of connection issues and other errors.
- **Voice Transmission:** Real-time voice data transmission using `PyAudio`.
- **Threaded Server:** Efficiently manages multiple clients using Python's threading.

## Technologies

### Frontend (Client)

- **Framework:** PyQt5
- **Audio Handling:** PyAudio
- **Networking:** Socket Programming
- **Threading:** Python's `threading` module

### Backend (Server)

- **Runtime:** Python 3.x
- **Networking:** Socket Programming
- **Threading:** Python's `threading` module
- **Data Handling:** Base64 Encoding/Decoding for audio data

## Architecture

The application follows a **Client-Server** architecture:

- **Client:** Built with PyQt5, the client handles the user interface, capturing audio input, displaying messages, and managing user interactions.
- **Server:** Manages multiple client connections, relays messages and audio data between clients, and ensures that only one user can transmit voice at a time.

![Architecture Diagram](https://github.com/your-username/your-repo-name/blob/main/path/to/architecture/diagram.png)

## Prerequisites

- **Python 3.6 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **PyQt5:** For the client GUI
- **PyAudio:** For audio handling in the client
- **Other Python Packages:** As specified in `requirements.txt` for both server and client

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
