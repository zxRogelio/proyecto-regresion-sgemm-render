
from sklearn.base import BaseEstimator, TransformerMixin

class ColumnIndexSelector(BaseEstimator, TransformerMixin):
    """Selecciona columnas por índice después del preprocesamiento.

    Importante: el constructor NO modifica el parámetro indices.
    Esto permite que scikit-learn pueda clonar el transformador durante cross_validate.
    """
    def __init__(self, indices=None):
        self.indices = indices

    def fit(self, X, y=None):
        self.indices_ = list(self.indices) if self.indices is not None else None
        return self

    def transform(self, X):
        indices = self.indices_ if hasattr(self, "indices_") else list(self.indices)
        if hasattr(X, "iloc"):
            return X.iloc[:, indices]
        return X[:, indices]
