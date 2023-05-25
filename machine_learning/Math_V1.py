import scipy
import joblib
import numpy as np
import pandas as pd
import mysql.connector
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from scipy.signal import savgol_filter


class DataProcessor:
    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database

    def connect_to_database(self):
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host,
                                      database=self.database)
        cursor = cnx.cursor()
        return cnx, cursor

    def retrieve_data(self, cursor):
        query = "SELECT * FROM account_scandata"
        cursor.execute(query)
        db_rows = cursor.fetchall()
        cursor.close()
        return db_rows

    def retrieve_data_for_prediction(self, cursor, scan_id):
        query = f"SELECT * FROM account_scandata WHERE scan_connection_id='{scan_id}'"
        cursor.execute(query)
        db_rows = cursor.fetchall()
        cursor.close()
        return db_rows

    def sample_data(self, db_rows):
        data = [(int(row[2]), row[1]) for row in db_rows]
        column_names = ['Sample'] + [i[0] for i in data[:700]]
        n = len(db_rows)
        step = 700
        start = 0
        filters = []
        while start < n:
            end = min(start + step, n)
            filters.append((start, end))
            start = end
        rows = [
            [count] + [i[0] for i in data[i:j]]
            for count, (i, j) in enumerate(filters, start=1)
        ]
        df = pd.DataFrame(rows, columns=column_names)
        latest_sample = list(df.iloc[-1, :].values)
        return [latest_sample[1:]]

    def preprocess_data(self, db_rows):
        data = [(int(row[2]), row[1]) for row in db_rows]
        column_names = ['Sample'] + [i[0] for i in data[:700]]
        n = len(db_rows)
        step = 700
        start = 0
        filters = []
        while start < n:
            end = min(start + step, n)
            filters.append((start, end))
            start = end
        rows = [
            [count] + [i[1] for i in data[i:j]]
            for count, (i, j) in enumerate(filters, start=1)
        ]
        df = pd.DataFrame(rows, columns=column_names)
        y = df.iloc[:, 1:].values
        smoothed_y = savgol_filter(y, window_length=15, polyorder=2, deriv=1)
        n_train = int(0.8 * len(df))
        X_train, y_train = smoothed_y[:n_train], df.iloc[:n_train, 0].values
        X_test, y_test = smoothed_y[n_train:], df.iloc[n_train:, 0].values
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, y_train, X_test_scaled, y_test


class ModelTrainer:
    def __init__(self, X_train_scaled, y_train):
        self.X_train_scaled = X_train_scaled
        self.y_train = y_train

    def train_model(self):
        model = Pipeline([
            ('svr', SVR())
        ])
        param_grid = {
            'svr__C': np.logspace(-3, 3, 7),
        }
        grid = GridSearchCV(model, param_grid=param_grid, cv=5)
        grid.fit(self.X_train_scaled, self.y_train)
        train_score = grid.score(self.X_train_scaled, self.y_train)
        return grid, train_score

    def save_model(self, grid):
        joblib.dump(grid, r'C:\Users\saad\Desktop\qt-web\machine_learning\gs_object.pkl')

    def load_model(self):
        return joblib.load(r"C:\Users\saad\Desktop\qt-web\machine_learning\gs_object.pkl")


class SavGolFilter:
    def __init__(self, unprocessed_energy_data, excel_file_path):
        self.d = unprocessed_energy_data
        self.bv = pd.read_excel(excel_file_path, sheet_name='B vectors')
        self.weights = self.bv.drop(['Factor ', ' B0'], axis=1).iloc[0].values
        self.bias = self.bv[' B0'].iloc[0]
        self.sav_gol_window_arg = 15

    def get_prediction(self, vals):
        x1 = scipy.signal.savgol_filter(vals, window_length=self.sav_gol_window_arg, polyorder=3, deriv=1,
                                        mode='constant')
        window = int((self.sav_gol_window_arg - 1) / 2)
        return np.dot(x1[window:(-1 * window)], self.weights) + self.bias

    def process_data(self):
        tuples_list = [(1100 + i * 2, self.d[i]) for i in range(len(self.d))]
        df = pd.DataFrame(tuples_list, columns=['A', 'B'])
        vals = pd.Series(df['B'].values, index=df['A'])
        return self.get_prediction(vals)
