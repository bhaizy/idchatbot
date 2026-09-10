<h1 align="center">──「 𝗜𝗗 𝗖𝗛𝗔𝗧𝗕𝗢𝗧 」──</h1>

<p align="center">
  <b>An Advanced, Asynchronous Telegram AI Chatbot powered by Google Gemini and Pyrogram</b>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11"></a>
  <a href="https://docs.pyrogram.org/"><img src="https://img.shields.io/badge/Pyrogram-v2.0.106-blue?style=for-the-badge&logo=telegram" alt="Pyrogram"></a>
  <a href="https://www.mongodb.com/"><img src="https://img.shields.io/badge/MongoDB-Motor%20Async-green?style=for-the-badge&logo=mongodb" alt="MongoDB"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge&logo=google" alt="Google Gemini"></a>
  <a href="https://dashboard.heroku.com/new?template=https://github.com/yourusername/idchatbot"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku" alt="Deploy to Heroku"></a>
</p>

---

## 🌟 Key Features

- 🤖 **Google Gemini AI Engine**: Intelligent, context-aware conversations powered by Google's generative models (`gemini-pro`).
- 💬 **Multi-Turn Chat History**: Retains conversational context per user/chat for coherent long discussions.
- 👥 **Group & DM Support**: Works seamlessly in both private direct messages and group chats.
- 🎛️ **Group Chatbot Toggle**: Admins can easily enable or disable AI auto-replies in groups (`/chatbot on` / `/chatbot off`).
- 📢 **Broadcast System**: Broadcast text, media, or pinned messages across all registered users and chats with detailed delivery stats.
- 📊 **Real-Time Analytics & Stats**: View total users, total groups, system uptime, and database metrics.
- ⚡ **Asynchronous Architecture**: Fully asynchronous I/O using Pyrogram v2, Motor (async MongoDB), and aiohttp for ultra-fast response times.
- 🔒 **Role-Based Access Control**: Protected owner/admin commands to ensure bot security.
- 🐳 **Docker & Heroku Ready**: Pre-configured `Procfile`, `Dockerfile`, `heroku.yml`, and `app.json` for one-click deployments.

---

## 🚀 One-Click Deploy to Heroku

Deploying your own instance of **ID Chatbot** to Heroku is quick and simple:

[![Deploy](https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku)](https://dashboard.heroku.com/new?template=https://github.com/yourusername/idchatbot)

> [!NOTE]
> Make sure you enable the `worker` dyno in your Heroku app's **Resources** tab after deploying.

---

## 🛠️ Environment Variables

Configure the following environment variables in your `.env` file or hosting service dashboard:

| Variable | Type | Required | Default | Description |
| :--- | :---: | :---: | :---: | :--- |
| `BOT_TOKEN` | String | **Yes** | — | Telegram Bot token obtained from [@BotFather](https://t.me/BotFather) |
| `API_ID` | Integer | **Yes** | — | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | String | **Yes** | — | Telegram API Hash from [my.telegram.org](https://my.telegram.org) |
| `MONGO_URL` | String | **Yes** | — | MongoDB connection URI string (e.g. MongoDB Atlas) |
| `OWNER_ID` | Integer | **Yes** | — | Telegram numeric User ID of the bot owner |
| `GEMINI_API_KEY` | String | **Yes** | — | Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/) |
| `BOT_NAME` | String | No | `ID Chatbot` | Display name of the bot |
| `BOT_USERNAME` | String | No | `None` | Telegram username of the bot (without `@`) |
| `SUPPORT_GROUP` | String | No | `None` | Telegram link or username for the support group |
| `SUPPORT_CHANNEL` | String | No | `None` | Telegram link or username for the updates channel |

---

## 📖 Commands List

### 👤 User & Group Commands

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `/start` | None | Start the bot and receive a welcome message with quick actions |
| `/help` | None | View help documentation and list of available commands |
| `/ping` | None | Check the bot latency and system status |
| `/chatbot` | `on` / `off` | Toggle AI chatbot mode in the current group chat (Admins only) |
| `/clear` | None | Clear conversational history / context with the AI |

### 👑 Owner & Admin Commands

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `/stats` | None | View total registered users, active chats, server uptime, and database stats |
| `/broadcast` | `<message>` / Reply | Broadcast a message or media to all users and group chats |
| `/bchat` | `<message>` / Reply | Broadcast exclusively to registered group chats |
| `/buser` | `<message>` / Reply | Broadcast exclusively to private chat users |
| `/users` | None | View detailed count and list of active bot users |
| `/chats` | None | View detailed count and list of active connected groups |

---

## 🔑 How to Obtain Credentials

### 1. Telegram `API_ID` & `API_HASH`
1. Log in with your Telegram phone number at [https://my.telegram.org](https://my.telegram.org).
2. Navigate to **API Development Tools**.
3. Fill out the application form (Title and Short Name).
4. Copy your `api_id` (numeric) and `api_hash` (alphanumeric string).

### 2. Telegram `BOT_TOKEN`
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the on-screen instructions.
3. Choose a name and unique username ending in `bot`.
4. Copy the HTTP API token provided by BotFather.

### 3. Telegram `OWNER_ID`
1. Message [@userinfobot](https://t.me/userinfobot) or [@MissRose_bot](https://t.me/MissRose_bot) (send `/id`).
2. Copy your numeric user ID (e.g., `123456789`).

### 4. MongoDB `MONGO_URL`
1. Create a free account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a free shared cluster (M0 sandbox).
3. Under **Database Access**, create a user with read/write permissions.
4. Under **Network Access**, add IP address `0.0.0.0/0` (allow access from anywhere).
5. Go to **Clusters** > **Connect** > **Drivers** > Select Python driver.
6. Copy the connection string format:
   ```text
   mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
   ```
   *(Replace `<username>` and `<password>` with your database user credentials)*.

### 5. Google Gemini `GEMINI_API_KEY`
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click on **Get API Key** and generate a new key for your project.
4. Copy the generated API key.

---

## 💻 Manual Deployment & Installation

### Option 1: Local / VPS Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/idchatbot.git
   cd idchatbot
   ```

2. **Set up a Python Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -U pip
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   ```bash
   cp sample.env .env
   # Edit .env with your favorite editor (e.g., nano, vim, or code)
   nano .env
   ```

5. **Run the Bot**:
   ```bash
   python3 -m bot
   ```

---

### Option 2: Docker Deployment

1. **Build Docker Image**:
   ```bash
   docker build -t idchatbot .
   ```

2. **Run Docker Container**:
   ```bash
   docker run -d --name idchatbot --env-file .env idchatbot
   ```

---

## 📁 Project Structure

```text
idchatbot/
├── bot/
│   ├── __init__.py           # Bot client & DB initialization
│   ├── config.py             # Config variables & environment loaders
│   ├── database/             # MongoDB async models (users, chats, settings)
│   │   ├── chats_db.py
│   │   ├── settings_db.py
│   │   └── users_db.py
│   ├── helpers/              # Decorators, utility helpers, keyboards
│   │   ├── decorators.py
│   │   └── utils.py
│   └── plugins/              # Message handlers, commands & AI logic
│       ├── admin.py
│       ├── broadcast.py
│       ├── chatbot.py
│       └── start.py
├── .gitignore                # Git ignored patterns
├── Dockerfile                # Docker image definition
├── Procfile                  # Heroku worker process definition
├── README.md                 # Project documentation
├── app.json                  # Heroku one-click deploy manifest
├── heroku.yml                # Heroku container build configuration
├── requirements.txt          # Python dependencies
├── runtime.txt               # Heroku Python runtime version
└── sample.env                # Environment template
```

---

## 🤝 Credits & Acknowledgements

- [Pyrogram](https://github.com/pyrogram/pyrogram) — Elegant, modern Telegram MTProto API framework for Python.
- [Google Generative AI](https://github.com/google/generative-ai-python) — Next-generation generative AI SDK from Google.
- [Motor](https://github.com/mongodb/motor) — Asynchronous Python driver for MongoDB.
- [Heroku](https://www.heroku.com/) — Cloud platform for effortless bot deployment.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/yourusername"><b>ID Chatbot Team</b></a>
</p>
