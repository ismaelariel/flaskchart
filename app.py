from flask import Flask, request, render_template, render_template_string
import matplotlib.pyplot as plt
from flask_plots import Plots
from io import BytesIO
import seaborn as sbn
import pandas as pd
import numpy as np
import base64
import os


app = Flask(__name__)
plots = Plots(app)


machine = pd.read_csv('static/One_year_compiled.csv')
machine_index = pd.read_csv('static/One_year_compiled.csv', index_col=0)


@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')

    return ''


@app.route('/state', methods=['GET'])
def state_world():
    chart00 = get_plot_00()
    chart01 = get_plot_01()
    chart02 = get_plot_02()

    if request.method == 'GET':
        return render_template_string(
                """
                <link rel="stylesheet" href="{{url_for('static', filename='css/index.css')}}" />
                {% from 'plots/utils.html' import render_img %}
                <div class="div_charts_container">
                    {{ render_img(data=chart00, alt_img='my_img') }}
                    {{ render_img(data=chart01, alt_img='my_img') }}
                    {{ render_img(data=chart02, alt_img='my_img') }}
                <div/>
                """,
                chart00=chart00,
                chart01=chart01,
                chart02=chart02
            )

    return ''


def get_plot_00():
    fig, ax = plt.subplots()
    mask = np.tril(machine.corr())
    sbn.heatmap(machine.corr(), vmin=-1, vmax=1, cmap='coolwarm', mask=mask)
    data = plots.get_data(fig)

    return data


def get_plot_01():
    position = machine['pCut::CTRL_Position_controller::Actual_position']

    fig, ax = plt.subplots()
    ax.plot(position)
    ax.set_title("Actual Position")
    data = plots.get_data(fig)

    return data


def get_plot_02():
    speed = machine['pCut::CTRL_Position_controller::Actual_speed']

    fig, ax = plt.subplots()
    ax.plot(speed)
    ax.set_title("Actual Speed")
    data = plots.get_data(fig)

    return data


if __name__ == '__main__':
    app.run()
