# PyQt5 Chat Application with Exclusive Voice



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

![Chat Interface](https://github.com/freeb5d/chatroom/blob/main/client.jpg)

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
```

### Setup Backend (Server)

1. **Navigate to the `server` Directory:**

    ```bash
    cd server
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Server Settings:**

    - Open `server.py` and ensure the `HOST` and `PORT` variables are set correctly. By default, it uses `localhost`.
    - Alternatively, you can use environment variables or a `config.py` file for configuration.

### Setup Frontend (Client)

1. **Open a New Terminal and Navigate to the `client` Directory:**

    ```bash
    cd client
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Client Settings:**

    - Open `client.py` and ensure the `SERVER_HOST` and `SERVER_PORT` variables match the server's IP address and port. By default, it uses `localhost`.
    - You can also set these via environment variables or a configuration file.

## Configuration

### Server Configuration (`server/server.py`)

```python
HOST = 'localhost'  # Server's IP address
PORT = 5050         # Port number
```

### Client Configuration (`client/client.py`)

```python
# Server configuration
SERVER_HOST = 'localhost'  # Update to server's IP if accessing remotely
SERVER_PORT = 5050         # Port number
```

**Note:** Ensure that the server's IP address and port are correctly configured in both the server and client. If accessing the server remotely, replace `'localhost'` with the server's public IP address in the client configuration.

## Usage

### Running the Server

1. **Ensure You Are in the `server` Directory and the Virtual Environment is Activated.**

2. **Start the Server:**

    ```bash
    python server.py
    ```

    - The server will start and listen for incoming client connections on the specified `HOST` and `PORT`.
    - You should see output indicating that the server has started, e.g., `Chat server started on localhost:5050`.

### Running the Client

1. **Ensure You Are in the `client` Directory and the Virtual Environment is Activated.**

2. **Start the Client Application:**

    ```bash
    python client.py
    ```

    - A PyQt5 GUI window will appear.
    - Enter a unique nickname in the provided input field.
    - Click the **Connect** button to establish a connection with the server.

## Message Protocol

While this application uses socket programming for real-time communication, here's an overview of the key message protocols used between the client and server:

| **Message Type**       | **Format**                         | **Description**                                       |
| ---------------------- | ---------------------------------- | ----------------------------------------------------- |
| **User Registration**  | `<nickname>\n`                     | Sent by the client immediately after connecting to register a unique nickname. |
| **User List Update**   | `USERLIST:<user1>,<user2>,...\n`    | Sent by the server to update the list of online users. |
| **Status Update**      | `STATUS:<START/STOP>:<nickname>\n` | Indicates a user has started or stopped talking.       |
| **Text Message**       | `MSG:<message>\n`                   | Sent by the client to broadcast a text message.        |
| **Voice Data**         | `VOICE:<base64_encoded_audio>\n`    | Sent by the client to transmit voice data.             |
| **Server Message**     | `SERVER:<message>\n`                | General messages from the server (e.g., user joined).  |
| **Busy Status**        | `STATUS:BUSY\n`                     | Sent by the server to a client if someone else is currently talking. |

## Contributing

Contributions are welcome! To ensure a smooth collaboration, please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

    ```bash
    git checkout -b feature/YourFeature
    ```

3. **Commit Your Changes**

    ```bash
    git commit -m "Add some feature"
    ```

4. **Push to the Branch**

    ```bash
    git push origin feature/YourFeature
    ```

5. **Open a Pull Request**

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](https://github.com/freeb5d/chatroom/blob/main/LICENSE).

## Contact

- **Author:** kaveh T

- **GitHub:** [freeb5d](https://github.com/freeb5d)

## Acknowledgements

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Shields.io for Badges](https://shields.io/)
- [Base64 Encoding in Python](https://docs.python.org/3/library/base64.html)
