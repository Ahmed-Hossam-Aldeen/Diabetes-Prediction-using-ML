from PyQt5 import QtWidgets, uic
import sys

from PyQt5.uic.properties import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox

import pickle
import pandas as pd 
import numpy as np

class MainWindow(QtWidgets.QMainWindow):      
    def __init__(self):   
        super(MainWindow, self).__init__()
        uic.loadUi('Diabetes.ui', self)
        self.pred.clicked.connect(self.predictz)
        self.setWindowTitle("Diabetes Predictor")
        self.show() 
        
        
    def predictz(self):
        try:
            float_features = [float(self.glucose.toPlainText()),float(self.insulin.toPlainText()),
                            float(self.bmi.toPlainText()),float(self.age.toPlainText())]

            final_features = [np.array(float_features)] 

            model = pickle.load(open('model.pkl', 'rb'))
            dataset = pd.read_csv('diabetes.csv')
            dataset_X = dataset.iloc[:,[1, 2, 5, 7]].values

            from sklearn.preprocessing import MinMaxScaler
            sc = MinMaxScaler(feature_range = (0,1))
            dataset_scaled = sc.fit_transform(dataset_X)
                

            prediction = model.predict( sc.transform(final_features) )

            if prediction == 1:
                pred = "You may have Diabetes, please consult your Doctor."
            elif prediction == 0:
                pred = "You don't have Diabetes."

            print(pred)
            self.result.setText(pred)
            
        except:
            QMessageBox.about(self, "Error", "Please enter all the required data")
    
app = 0            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()                    