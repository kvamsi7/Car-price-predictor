from flask import Flask, render_template,request,jsonify
from flask_cors import CORS, cross_origin
import numpy as np
from datetime import date
import pickle


app = Flask(__name__)# initializing a flask app

@app.route('/') # route to display the home page
@cross_origin()
def index():
    return render_template('index.html')

@app.route("/predict",methods=['POST']) # route to show the predictions in a wen GUI
@cross_origin()
def predict():
    if request.method == 'POST':
        try:
            Fuel_Type_Diesel = 0
            if request.method == 'POST':
                year = int(request.form['year'])
                Present_Price = float(request.form['present_price'])
                Kms_Driven = int(request.form['km_driven'])
                Kms_Driven2 = np.log(Kms_Driven)
                Owner = int(request.form['owners'])
                Fuel_Type_Petrol = request.form['fuel_type']
                if (Fuel_Type_Petrol == 'Petrol'):
                    Fuel_Type_Petrol = 1
                    Fuel_Type_Diesel = 0
                else:
                    Fuel_Type_Petrol = 0
                    Fuel_Type_Diesel = 1
                current_year = date.today().year
                year = current_year - year

                Seller_Type_Individual = request.form['select_type_buyer']
                if (Seller_Type_Individual == 'Individual'):
                    Seller_Type_Individual = 1
                else:
                    Seller_Type_Individual = 0
                Transmission_Mannual = request.form['transmission_manual']
                if (Transmission_Mannual == 'Mannual'):
                    Transmission_Mannual = 1
                else:
                    Transmission_Mannual = 0

                model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
                prediction = model.predict(
                    [[Present_Price, Kms_Driven2, Owner, year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                      Seller_Type_Individual, Transmission_Mannual]])
                output = round(prediction[0], 2)

                if output < 0:
                    return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
                else:
                    return render_template('index.html',
                                           prediction_text="You Can Sell The Car at the Price of {} lakhs".format(
                                               output))
        except Exception as e:
            print('The Exception message is : ', e)
            return "Something is wrong."
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)