from sklearn.model_selection import train_test_split
import ModelEngine as mlEngine
import DataLoader as dataLoader
import DataPreProcess as preproc
import ConfigManager as cmfmagt
import Logger as lgr 
def app_main():
	try:
		logger = lgr.Logger()
		print("--------application starting--------------")
		logger.info("--------application starting--------------")
		print("--------loading data----------------------")
		logger.info("--------loading data----------------------")
		dl = dataLoader.DataLoader()
		train_X, test_X =train_test_split(dl.DataFrame.copy(), test_size=0.3, random_state=42)
		# label = train_X["median_house_value"].copy()
		# housing = train_X.drop("median_house_value", axis=1) 
		housing = test_X.drop("median_house_value", axis=1) 
		#label_test = test_X["median_house_value"].copy()
		numeric_cols = list(housing.columns.values)
		category_cols = ["ocean_proximity"]
		numeric_cols.remove("ocean_proximity")
		dp = preproc.DataPreProcess(numeric_cols, category_cols)
		print("--------processing data-------------------")
		dataProcessed = dp.getProcessedData(housing)
		print(dataProcessed.shape)
		configMagt = cmfmagt.ConfigManager()
		engine = mlEngine.ModelEngine()
		print("------------loading model------------------")
		bestModel = engine.loadML(configMagt.config["APPSETTING"]["ml_path"])
		result = bestModel.predict(dataProcessed)
		print(result.shape)
	except Exception as e:
		print("Error : ", str(e))	

if __name__ == "__main__":
	app_main()