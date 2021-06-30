from flask import Flask, jsonify, render_template, request
from data_processing import DataProcessing


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calc')
def hello():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    threshold = request.args.get('threshold')
    # modified = data_processing.call(start_date, end_date)
    return render_template('result.html', calculated_c=c)

if __name__ == "__main__":
    dp = DataProcessing(
        csv_path='./nhk_news_covid19_prefectures_daily_data.csv',
        start='2021/1/16', end='2021/5/12', threshold='10000000')
    dp.txt_output()
    dp.hsm_program()
    # app.run(debug=True)
