from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

import json
import requests
import os

app = Flask(__name__)

import os

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

## Get connection details for APIs
# titanic_staging_app_url = os.environ['TITANIC_STAGING_URL'] # change to your app name
titanic_prod_app_url = os.environ["TITANIC_PROD_URL"]  # change to your app name


class MyForm(FlaskForm):
    pclass = StringField(
        "pclass",
        validators=[DataRequired()],
        render_kw={"placeholder": "Write a number..."},
    )
    sex = StringField(
        "sex", validators=[DataRequired()], render_kw={"placeholder": "female/male"}
    )
    age = StringField(
        "age",
        validators=[DataRequired()],
        render_kw={"placeholder": "Write a number..."},
    )
    sibsp = StringField(
        "sibsp",
        validators=[DataRequired()],
        render_kw={"placeholder": "Write a number..."},
    )
    # sex = SelectField(choices=[('female', 'male')])


@app.route("/", methods=["GET", "POST"])
def dataprediction():
    form = MyForm()

    if form.validate_on_submit():
        print("Validated.")
        age_content = form.age.data
        pclass = form.pclass.data
        sibsp = form.sibsp.data

        data = {
            "pclass": form.pclass.data,
            "sex": form.sex.data,
            "age": form.age.data,
            "sibsp": form.sibsp.data,
            "parch": 0,
            "fare": 7.25,
            "embarked": "S",
            "name": "Dr. D",
            "ticket": "Some 1234",
            "cabin": "KingPing",
            "passengerid": 123,
        }

        headers = {"Content-Type": "application/json"}

        # sample data
        sample_data = {
            "pclass": 1,
            "sex": "female",
            "age": 4.0,
            "sibsp": 1,
            "parch": 0,
            "fare": 7.25,
            "embarked": "S",
            "name": "Dr. D",
            "ticket": "Some 1234",
            "cabin": "KingPing",
            "passengerid": 123,
        }

        print(data)

        data_to_api = json.dumps(data)

        send_request_deployed = requests.request(
            "POST", titanic_prod_app_url, headers=headers, data=data_to_api
        )

        print(send_request_deployed)
        api_response = send_request_deployed.json()
        print("API Response:")
        print(api_response)

        prediction = send_request_deployed.json()

        return render_template(
            "index.html",
            form=form,
            data=data,
            api_status=send_request_deployed,
            api_response=api_response,
            prediction=prediction,
        )

    else:
        print("Form not validated.")
        return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
