import config.config as config
import web.telegram as telegram
from coordinator import coordinator as coordinator

print('Starting mercari-watchdog...')

cfg = config.load()

telegram_client = telegram.new_telegram_client(cfg.telegram_token, cfg.telegram_chat_id, cfg.download_photos)

coordinator.start(cfg.searches, cfg.delay, cfg.msg_tpl, cfg.change_rate, telegram_client)
