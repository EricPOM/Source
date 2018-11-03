from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelBinarizer 

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, col_names):
        self.col_names = col_names
    
    def fit(self, X, y=None):
        pass
    
    def transform(self, X, y=None):
        return X[self.col_names].values
    
    def fit_transform(self, X, y=None):
        return self.transform(X)


class CustLabelBinarizer(LabelBinarizer):
    def fit(self, X, y=None):
        pass
    
    def transform(self, X, y=None):
        return LabelBinarizer().fit(X).transform(X)
    
    def fit_transform(self, X, y=None):
         return self.transform(X)