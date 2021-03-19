import sys, getopt, csv
import pandas as pd
import json
from prettyprinter import pprint
from flask import Flask, request, jsonify
import os, shutil

app = Flask(__name__)

@app.route("/rollback", methods=['POST'])
def rollback():
    if os.path.isfile('export.json.back'):
        os.remove('export.json')
        os.rename('export.json.back', 'export.json')
        return jsonify({
            'status': 'success'
        })

    else:
        return jsonify({
            'status': 'failed',
            'message': '롤백할 파일이 존재하지 않습니다.'
        })

@app.route("/upload", methods=['POST'])
def goMain():

    try:

        if os.path.isfile('export.json'):
            shutil.copy('./export.json', './export.json.back')

        file = request.files['file']
        filename = file.filename
        file.save('./'+filename)

        main([
            '',
            filename
        ])

    except (IOError, FileExistsError, ValueError):
        return jsonify({
            'status': 'failed',
            'message': '파일이 잘못되었습니다.',
        })

    return jsonify({
        'status': 'success',
        'message': '적용되었습니다.'
    })


def main(argv):

    FILE_NAME = argv[0]
    EXCEL_FILE_NAME = ""
    SAVE_JSON_FILE = "export.json"

    if len(argv) < 2:
        print('invalid arguments :: <excel file name> <save json file name?>')

    if len(argv) > 2:
        SAVE_JSON_FILE = argv[2]

    EXCEL_FILE_NAME = argv[1]

    origin = pd.read_excel(EXCEL_FILE_NAME, sheet_name=None)

    categoryTag = origin['카테고리']
    priceTag = origin['가격대']
    cardData = origin['상품리스트']

    data = {
        'categoryTag': json.loads(categoryTag.to_json(orient='records')),
        'priceTag': json.loads(priceTag.to_json(orient='records')),
        'cardData': json.loads(cardData.to_json(orient='records'))
    }

    with open(SAVE_JSON_FILE, "w", encoding='UTF-8') as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
