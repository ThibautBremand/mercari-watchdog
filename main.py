import config.config as config
from coordinator import coordinator as coordinator

print('Starting mercari-watchdog...')

cfg = config.load()

coordinator.start(cfg.searches, cfg.delay, cfg.msg_tpl, cfg.telegram_token, cfg.telegram_chat_id)
