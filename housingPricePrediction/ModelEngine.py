from sklearn.externals import joblib 
#mport ConfigManager as cm
#to validate model
#Learning Curve / validation Curve ...
class ModelEngine():
	def exportML(self, model, path):
		try:
			jobLib.dump(model, path)
		except Exception as e:
			print("Error : ", str(e))

	def loadML(self, path):
		try:
			return joblib.load(path)
		except Exception as e:
			print("Error : ", str(e))