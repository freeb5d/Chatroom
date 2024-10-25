import sys
import socket
import threading
import base64
import pyaudio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QListWidget,
    QLabel, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

# Server configuration
SERVER_HOST = 'localhost'  # Updated server IP address
SERVER_PORT = 5050             # Updated port number

# Voice configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class Communicate(QObject):
    message_received = pyqtSignal(str)
    userlist_updated = pyqtSignal(list)
    status_updated = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Chat Client with Exclusive Voice")
        self.setGeometry(100, 100, 800, 600)
        self.nickname = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm = Communicate()
        self.comm.message_received.connect(self.display_message)
        self.comm.userlist_updated.connect(self.update_users_list_display)
        self.comm.status_updated.connect(self.handle_status_update)
        self.comm.error_occurred.connect(self.handle_error)
        self.init_ui()
        self.connected = False
        self.listening = False
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.voice_thread = None
        self.play_stream = None
        self.play_lock = threading.Lock()
        self.currently_talking_user = None  # Track the current talker

    def init_ui(self):
        """
        Initialize the GUI components.
        """
        main_layout = QHBoxLayout()
        
        # Left side: Chat and controls
        chat_layout = QVBoxLayout()
        
        # Nickname input
        nickname_layout = QHBoxLayout()
        self.nickname_input = QLineEdit()
        self.nickname_input.setPlaceholderText("Enter your nickname")
        nickname_layout.addWidget(QLabel("Nickname:"))
        nickname_layout.addWidget(self.nickname_input)
        chat_layout.addLayout(nickname_layout)

        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        chat_layout.addWidget(self.connect_button)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chat_layout.addWidget(self.chat_display)

        # Message input and controls
        message_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        self.message_input.setDisabled(True)
        message_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.setDisabled(True)
        self.send_button.clicked.connect(self.send_message)
        message_layout.addWidget(self.send_button)

        # Voice (Talk) button
        self.talk_button = QPushButton("🎤 Talk")
        self.talk_button.setDisabled(True)
        self.talk_button.setCheckable(True)
        self.talk_button.clicked.connect(self.toggle_talking)
        message_layout.addWidget(self.talk_button)

        chat_layout.addLayout(message_layout)
        main_layout.addLayout(chat_layout, 3)  # Allocate more space to chat

        # Right side: Online users
        users_layout = QVBoxLayout()
        users_label = QLabel("Online Users:")
        users_layout.addWidget(users_label)
        self.users_list = QListWidget()
        self.users_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        users_layout.addWidget(self.users_list)
        main_layout.addLayout(users_layout, 1)  # Allocate less space to users

        self.setLayout(main_layout)

    def connect_to_server(self):
        """
        Connect to the chat server with the provided nickname.
        """
        if self.connected:
            QMessageBox.warning(self, "Already Connected", "You are already connected to the server.")
            return

        self.nickname = self.nickname_input.text().strip()
        if not self.nickname:
            QMessageBox.warning(self, "Input Error", "Please enter a nickname.")
            return

        try:
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.socket.sendall((self.nickname + '\n').encode('utf-8'))
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", f"Could not connect to server: {e}")
            return

        self.connected = True
        self.connect_button.setDisabled(True)
        self.nickname_input.setDisabled(True)
        self.message_input.setDisabled(False)
        self.send_button.setDisabled(False)
        self.talk_button.setDisabled(False)
        self.chat_display.append("Connected to the server.")

        # Start the listening thread
        listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        listen_thread.start()

    def listen_for_messages(self):
        """
        Listen for incoming messages from the server.
        """
        buffer = ""
        try:
            while True:
                data = self.socket.recv(4096)
                if not data:
                    break  # Server closed connection
                buffer += data.decode('utf-8', errors='ignore')
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    message = message.strip()
                    if not message:
                        continue
                    if message.startswith("USERLIST:"):
                        users = message[len("USERLIST:"):].split(',')
                        self.comm.userlist_updated.emit(users)
                    elif message.startswith("STATUS:"):
                        parts = message.split(':', 2)
                        if len(parts) == 3:
                            _, action, user = parts
                            self.comm.status_updated.emit(action, user)
                    elif message.startswith("VOICE:") or message.startswith("MSG:") or message.startswith("SERVER:"):
                        self.comm.message_received.emit(message)
        except Exception as e:
            self.comm.error_occurred.emit(f"Error receiving messages: {e}")
        finally:
            self.socket.close()
            self.connected = False
            self.comm.message_received.emit("Disconnected from the server.")
            self.comm.error_occurred.emit("Disconnected from the server.")

    def display_message(self, message):
        """
        Display received text or handle voice messages.
        """
        if message.startswith("VOICE:"):
            # Handle incoming voice data
            encoded_data = message[len("VOICE:"):].strip()
            try:
                audio_data = base64.b64decode(encoded_data)
                self.play_audio(audio_data)
            except Exception as e:
                print(f"Error decoding audio data: {e}")
        elif message.startswith("MSG:"):
            # Display the message in chat
            display_message = message[len("MSG:"):].strip()
            self.chat_display.append(display_message)
        elif message.startswith("SERVER:"):
            # Display server messages (like user joining or leaving)
            display_message = message[len("SERVER:"):].strip()
            self.chat_display.append(display_message)
        elif message == "Disconnected from the server.":
            self.chat_display.append(message)
            QMessageBox.information(self, "Disconnected", message)

    def send_message(self):
        """
        Send a text message to the server.
        """
        if not self.connected:
            QMessageBox.warning(self, "Not Connected", "You are not connected to any server.")
            return

        message = self.message_input.text().strip()
        if message:
            try:
                self.socket.sendall(f"MSG:{message}\n".encode('utf-8'))
                # Remove the local append to prevent duplication
                # Messages are displayed when received from the server
                self.message_input.clear()
            except Exception as e:
                QMessageBox.critical(self, "Send Failed", f"Could not send message: {e}")

    def toggle_talking(self):
        """
        Toggle the talking state: start or stop sending voice data.
        """
        if self.talk_button.isChecked():
            # Attempt to start talking
            self.socket.sendall(f"STATUS:START:{self.nickname}\n".encode('utf-8'))
        else:
            # Stop talking
            self.socket.sendall(f"STATUS:STOP:{self.nickname}\n".encode('utf-8'))
            self.stop_sending_voice()

    def send_status_start(self):
        """
        Start sending voice data.
        """
        self.talk_button.setText("🎤 Stop Talking")
        self.start_sending_voice()

    def send_status_stop(self):
        """
        Stop sending voice data.
        """
        self.talk_button.setText("🎤 Talk")
        self.stop_sending_voice()

    def handle_status_update(self, action, user):
        """
        Handle user status updates to enforce exclusive talking.
        """
        if action == "START":
            if self.currently_talking_user is None:
                self.currently_talking_user = user
                if user == self.nickname:
                    # You are the talker
                    self.send_status_start()
                else:
                    # Another user is talking; disable your Talk button
                    self.talk_button.setDisabled(True)
                self.update_users_list_display(self.current_users())
            else:
                if user != self.nickname:
                    # Someone else started talking; ensure your Talk button is disabled
                    self.talk_button.setDisabled(True)
        elif action == "STOP":
            if self.currently_talking_user == user:
                self.currently_talking_user = None
                if user == self.nickname:
                    # You stopped talking
                    self.send_status_stop()
                # Re-enable Talk button for all users
                self.talk_button.setDisabled(False)
                self.update_users_list_display(self.current_users())
        elif action == "BUSY":
            # Received BUSY status when trying to start talking
            self.talk_button.setChecked(False)
            self.talk_button.setText("🎤 Talk")
            QMessageBox.information(self, "Mic Busy", f"Someone else is currently talking. Please wait until they finish.")

    def start_sending_voice(self):
        """
        Start capturing and sending voice data.
        """
        self.stream = self.pyaudio_instance.open(format=FORMAT,
                                                 channels=CHANNELS,
                                                 rate=RATE,
                                                 input=True,
                                                 frames_per_buffer=CHUNK)
        self.listening = True
        self.voice_thread = threading.Thread(target=self.capture_and_send_voice, daemon=True)
        self.voice_thread.start()

    def capture_and_send_voice(self):
        """
        Capture audio from the microphone and send it to the server.
        """
        try:
            while self.listening:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                encoded_data = base64.b64encode(data).decode('utf-8')
                voice_message = f"VOICE:{encoded_data}\n"
                self.socket.sendall(voice_message.encode('utf-8'))
        except Exception as e:
            self.comm.error_occurred.emit(f"Error capturing/sending voice: {e}")

    def stop_sending_voice(self):
        """
        Stop capturing and sending voice data.
        """
        self.listening = False
        if self.voice_thread is not None:
            self.voice_thread.join()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def play_audio(self, audio_data):
        """
        Play received audio data.
        """
        try:
            if self.play_stream is None:
                self.play_stream = self.pyaudio_instance.open(format=FORMAT,
                                                               channels=CHANNELS,
                                                               rate=RATE,
                                                               output=True,
                                                               frames_per_buffer=CHUNK)
            self.play_stream.write(audio_data)
        except Exception as e:
            print(f"Error playing audio data: {e}")

    def update_users_list_display(self, users):
        """
        Refresh the users list widget, adding mic emojis on the left where necessary.
        """
        self.users_list.clear()
        for user in users:
            display_name = user
            if user == self.currently_talking_user:
                display_name = "🎤 " + user
            self.users_list.addItem(display_name)

    def handle_error(self, error_message):
        """
        Handle errors by displaying them in the chat and optionally showing a message box.
        """
        print(error_message)
        if "Disconnected" in error_message:
            QMessageBox.information(self, "Disconnected", error_message)
        else:
            self.chat_display.append(f"Error: {error_message}")

    def current_users(self):
        """
        Retrieve the current list of users from the users_list widget.
        """
        return [self.users_list.item(i).text().replace("🎤 ", "") for i in range(self.users_list.count())]

    def closeEvent(self, event):
        """
        Handle the window close event to ensure resources are cleaned up.
        """
        if self.connected:
            if self.talk_button.isChecked():
                self.talk_button.setChecked(False)
                self.toggle_talking()
            try:
                self.socket.close()
            except:
                pass
        if self.play_stream is not None:
            self.play_stream.stop_stream()
            self.play_stream.close()
        self.pyaudio_instance.terminate()
        event.accept()

def main():
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
