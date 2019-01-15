from flask import Flask,render_template,url_for,request
import pandas as pd
import numpy as np
from sklearn import linear_model
import csv

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html') 

@app.route('/mlmodel',methods=['POST'])
def mlmodel():
	if request.method == 'POST':
		comment=request.form.get('comment')
		v= float(comment)
		if v<=0:
			return render_template('novalue.html') 
		if v>0:	
			df= pd.read_csv("G:/project/New folder/student_scores.csv")
			x_parameter = []
			y_parameter = []
			for Hours,Scores in zip(df['Hours'],df['Scores']):
		        	x_parameter.append([float(Hours)])
		        	y_parameter.append(float(Scores))
			#print(x_parameter)
			#print(y_parameter)
			regr = linear_model.LinearRegression()
			regr.fit (x_parameter,y_parameter)
			print ('Coefficients: ', regr.coef_)
			print ('Intercept: ',regr.intercept_)
			#predict_value=float(input("Enter the Hours for which you want to know Scores: "))

			predict_value=v
			predict_outcome = regr.predict([[predict_value]])
			with open('G:/project/New folder/student_scores.csv', mode='a',newline='') as student_scores:
		        	student_scores_w = csv.writer(student_scores, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		        	student_scores_w.writerow([predict_value, int(predict_outcome[0])])
			print(predict_outcome)
			return render_template('res.html',result=round(float(predict_outcome[0]),3)) 

if __name__ == '__main__':
	app.run(debug=True)
