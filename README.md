# Django Real-Time Chat App

A real-time chat application built with **Django** and **Django Channels**. Users can sign up, log in, join chat rooms and exchange messages instantly over **WebSockets**. Every message is saved in the database, so the conversation is still there after a page refresh.

![Chat preview](docs/preview.png)

## Features

- Real-time messaging with WebSockets (no page refresh needed)
- Multiple chat rooms: open `/chat/<room-name>/` and start talking
- User signup, login and logout using Django's built-in authentication
- Authenticated WebSocket connections: anonymous users are rejected
- Message history is stored in the database and loaded when a room is opened
- Every message shows the sender's username
- WhatsApp-style chat interface (your messages on the right, others on the left)
- Django admin panel to view and manage messages

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django 5.2 |
| Real-time | Django Channels, WebSocket |
| ASGI server | Daphne |
| Channel layer | InMemoryChannelLayer (development) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |

## Architecture

![Architecture](docs/architecture.png)

**How a message travels:**

1. The browser opens a WebSocket connection to `/ws/chat/<room-name>/`.
2. Daphne receives it and `ProtocolTypeRouter` sends it to the WebSocket branch.
3. `AuthMiddlewareStack` identifies the logged-in user and `URLRouter` finds `ChatConsumer`.
4. When a user sends a message, the consumer saves it in the database.
5. The consumer broadcasts it to the room's channel group with `group_send`.
6. Every consumer in that group pushes the message to its own browser instantly.

## Project Structure

```
django-realtime-chat/
├── config/
│   ├── asgi.py            # HTTP + WebSocket routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── chat/
│   ├── migrations/
│   ├── templates/
│   │   ├── chat/
│   │   │   ├── index.html     # enter a room name
│   │   │   └── room.html      # chat room page
│   │   └── registration/
│   │       ├── login.html
│   │       └── signup.html
│   ├── admin.py
│   ├── consumers.py       # WebSocket consumer (ChatConsumer)
│   ├── models.py          # Message model
│   ├── routing.py         # WebSocket URL routes
│   ├── urls.py
│   └── views.py
├── docs/
│   ├── architecture.png
│   └── preview.png
├── manage.py
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/faizanjutt473/django-realtime-chat.git
cd django-realtime-chat
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django channels daphne
```

### 4. Set up the database

```bash
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```

The terminal should show `Starting ASGI/Daphne version ...`. If you see the plain `Starting development server` message instead, make sure `'daphne'` is the **first** entry in `INSTALLED_APPS`.

### 6. Use the app

1. Open `http://127.0.0.1:8000/accounts/signup/` and create an account.
2. Log in. You will be taken to `http://127.0.0.1:8000/chat/`.
3. Enter a room name (for example `lobby`).
4. Open the same room in another browser or an incognito window with a second user and start chatting.

Optional: create an admin user to view messages at `/admin/`:

```bash
python manage.py createsuperuser
```

## Key Files Explained

| File | Purpose |
|------|---------|
| `config/asgi.py` | Routes HTTP traffic to Django and WebSocket traffic to Channels |
| `chat/routing.py` | Maps `ws/chat/<room_name>/` to `ChatConsumer` |
| `chat/consumers.py` | Handles connect, receive, broadcast and saving messages |
| `chat/models.py` | `Message` model: room, user, content, timestamp |
| `chat/views.py` | Room pages, chat history and signup (login protected) |

## Limitations and Future Improvements

- `InMemoryChannelLayer` works for a single process. For production use `channels-redis`.
- For HTTPS deployment, the WebSocket URL must change from `ws://` to `wss://`.
- Room names with spaces or special characters are not handled yet.
- Ideas: online users list, typing indicator, message timestamps, private (one-to-one) chats.

## Author

**Muhammad Faizan Farooq**
GitHub: [faizanjutt473](https://github.com/faizanjutt473)

## License

This project is open source and available for learning purposes.
