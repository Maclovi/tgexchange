# Exchange Bot


## Installation

### Requirements

- Python 3.10 or higher
- Redis 7 or higher
- Telegram bot token (from [BotFather](https://t.me/botfather))
### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Maclovi/tgexchange.git 
cd tgexchange
```
### How to start
1. Rename .env.example to .env
2. Fill out the TOKEN
## Usage

Run the bot:
```bash
docker-compose up -d
```
### Commands

- **/start** - Display a welcome message and usage instructions.
- **/rates** - Display all current rates
- **/exchange - Takes 2 currencies and amount

## Example

1. Send the `/start` command to see the welcome message and instructions.
2. Send `/rates` command to see the rates.
3. Send `/exchange usd rub 10` command to see conversion
## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Author

**Sergey** - [GitHub Profile](https://github.com/Maclovi)

---

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/Maclovi/tgloader/issues).
