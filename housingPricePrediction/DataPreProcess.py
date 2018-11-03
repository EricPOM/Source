from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import Transformer.CustomizedTransformer  as ctf
import DataLoader as DL 

#automatically pre-processing data
class DataPreProcess():
	def __init__(self, numericCols, categoricalCols):
		self.numericCols = numericCols
		self.categoricalCols = categoricalCols

	def getProcessedData(self, data):
		pipline = self._buildPipeline()
		return pipline.fit_transform(data)


	def _buildPipeline(self):
		num_pipeline = Pipeline([
		                        ('selector', ctf.DataFrameSelector(self.numericCols)),
		                        ('imputer', SimpleImputer(strategy="median")),
		                        ('std_scaler', MinMaxScaler()),
		                        ])
		cat_pipeline = Pipeline([
		                        ('selector', ctf.DataFrameSelector(self.categoricalCols)),
		                        ('label_binarizer', ctf.CustLabelBinarizer()),
		                        ])
		full_pipeline = FeatureUnion(transformer_list=[
		                        ("num_pipeline", num_pipeline),
		                        ("cat_pipeline", cat_pipeline),
		                        ])
		return full_pipeline


if __name__ == "__main__":
	#testing
	print("here")
	dl = DL.DataLoader()
	train_X, test_X =train_test_split(dl.DataFrame.copy(), test_size=0.3, random_state=42)
	label = train_X["median_house_value"].copy()
	housing = train_X.drop("median_house_value", axis=1) 
	numeric_cols = list(housing.columns.values)
	category_cols = ["ocean_proximity"]
	numeric_cols.remove("ocean_proximity")
	# housing_test = test_X.drop("median_house_value", axis=1) 
	# label_test = test_X["median_house_value"].copy()
	dp = DataPreProcess(numeric_cols, category_cols)

	np = dp.getProcessedData(housing)

	print(np.shape)