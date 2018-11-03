import logging 
from logging.handlers import TimedRotatingFileHandler

class Logger():
	def __init__(self):
		self.logger = logging.getLogger('app')
		handler = TimedRotatingFileHandler("log/app.log", when="midnight", interval=1)
		handler.suffix ="%d_%m_%Y"
		handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(handler)

	def info(self,msg):
		self.logger.info(msg)
		

	def error(self,msg):
		self.logger.error(msg)

	def warning(self, msg):
		self.logger.warning(msg)

if __name__ == "__main__":
	logger = Logger()
	logger.info("this is info")
	logger.error("this is error")
