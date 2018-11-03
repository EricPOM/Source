import configparser 
import datetime
from pathlib import Path

#application configuration
class ConfigManager():
	"""docstring for ClassName"""
	def __init__(self):
		self.configPath = "appConfig.ini" 
		self.config = configparser.ConfigParser();
		file = Path(self.configPath)
		if file.is_file():
			print("loading configuration file")
			self._setupConfig()

	@property
	def Config(self):
		return self.config

	#configuration creation & update	
	#customize it according to different requirment 
	def generateConfig(self):
		now = datetime.datetime.now()
		self.config["DEFAULT"] = { "AppName":"housing prices prediction",
								   "Version": "1.1",
								   "Owner" : "YX",
								   "Crated Date": "03/02/2018",
								   "Last Updated Date": now.strftime("%m/%d/%Y")
								  }
		#init applcaition setting
		self.config["APPSETTING"] = {}						 	 
		self.config["APPSETTING"]["FILE_PATH"] = './FlatFile/housing.csv' 


		self._output()

	def _output(self):
		try:
			with open(self.configPath, 'w') as configFile:
				self.config.write(configFile)
		except IOError:
			print("wirting config file failed")
		except Exception as e:
			print("Error: ", str(e))

	#setup existing configuration 
	def _setupConfig(self):
		self.config.read(self.configPath)

if __name__ =="__main__":
	cf = ConfigManager()
	#cf.generateConfig()
	#testing
	print(cf.Config["APPSETTING"]["FILE_PATH"])
