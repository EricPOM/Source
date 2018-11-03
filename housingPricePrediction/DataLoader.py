import pandas as pd
import ConfigManager 

#loading data 
class DataLoader():
	def __init__(self):
		self.configMgt = ConfigManager.ConfigManager()
		self.df = self._loadData()

	@property
	def DataFrame(self):
		#print(self.df.head())
		return self.df

	def _loadData(self):
		try:
			print(self.configMgt.Config["APPSETTING"]["FILE_PATH"])
			return pd.read_csv(self.configMgt.Config["APPSETTING"]["FILE_PATH"])
		except Exception as e:
			print("Error: ", str(e))


if __name__ == "__main__":
	#dl = DataLoader()
	#print(dl.DataFrame.head())






