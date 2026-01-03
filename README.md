# AvicBotIRC

A modern, asynchronous IRC bot written in Python 3.12+. Originally created in 2015, this bot has been completely rewritten for 2026 with contemporary best practices.

## Features

- **Asynchronous I/O**: Built on Python's `asyncio` for efficient, non-blocking network operations
- **Language Code Lookups**: Query 150+ ISO 639 language codes (e.g., `!lang en?`)
- **Wikimedia Tool Integration**: Quick links to Global User Contributions and CentralAuth pages
- **Configurable**: All settings via environment variables for flexible deployment
- **Comprehensive Logging**: Built-in logging for debugging and monitoring
- **Conversational Triggers**: Fun responses when the bot's name is mentioned

## Requirements

- Python 3.10 or higher (tested on 3.12)
- No external dependencies (uses only Python standard library)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Avicennasis/AvicBotIRC.git
   cd AvicBotIRC
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Run the bot:
   ```bash
   python avicbotirc.py
   ```

## Configuration

Configure the bot using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `AVICBOT_NICK` | Bot's IRC nickname | `AvicBot` |
| `AVICBOT_SERVER` | IRC server hostname | `irc.libera.chat` |
| `AVICBOT_PORT` | IRC server port | `6667` |
| `AVICBOT_CHANNELS` | Comma-separated channels | `#avicbot` |
| `AVICBOT_MASTER` | Owner's nickname | `Avicennasis` |
| `AVICBOT_USERNAME` | IRC username | `AvicBot` |
| `AVICBOT_REALNAME` | IRC "real name" | `Avicennasis` |
| `AVICBOT_PASSWORD` | NickServ password | *(none)* |
| `AVICBOT_BUFFER_SIZE` | Socket buffer size | `10240` |

### Example

```bash
export AVICBOT_NICK="MyBot"
export AVICBOT_SERVER="irc.libera.chat"
export AVICBOT_CHANNELS="#mychannel,#anotherchannel"
export AVICBOT_MASTER="MyNick"
python avicbotirc.py
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!commands` | List available commands | `!commands` |
| `!say <text>` | Bot echoes the text | `!say Hello world` |
| `!lang <code>?` | Look up a language code | `!lang ja?` |
| `!guc <username>` | Global User Contributions link | `!guc Example` |
| `!cauth <username>` | CentralAuth page link | `!cauth Example` |
| `!link <path>` | Custom link builder | `!link docs` |
| `!sing` | Bot sings a song | `!sing` |
| `!random` | Random number (guaranteed fair) | `!random` |
| `!die <botname>` | Disconnect the bot | `!die AvicBot` |

## Conversational Triggers

When you mention the bot's name along with certain words, it responds:

- "hello AvicBot" → "Hi"
- "AvicBot dance" → "\*dances\*"
- "goodbye AvicBot" → "I'll miss you"
- "AvicBot master" → "Avicennasis is my master"

## Project Structure

```
AvicBotIRC/
├── avicbotirc.py    # Main bot implementation
├── README.md        # This file
├── LICENSE          # MIT License
└── restart.sh       # Optional restart script
```

## Changelog

### 2026 Rewrite
- Complete rewrite using Python 3.12+ and asyncio
- Replaced 280+ if-statements with efficient dictionary lookups
- Added comprehensive inline documentation
- Environment variable configuration
- Updated default server to Libera.Chat (Freenode no longer exists)
- Added proper error handling and logging
- Class-based architecture with `IRCBot`

### 2015 Original
- Initial release for Freenode IRC
- Basic command support
- Language code lookups

## License

MIT License - Copyright (c) 2015-2026 Léon "Avic" Simmons

See [LICENSE](LICENSE) for full text.

## Author

**Léon "Avic" Simmons** ([@Avicennasis](https://github.com/Avicennasis))
