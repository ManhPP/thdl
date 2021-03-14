from flask import Flask, request, jsonify
from matching import StringMatching

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/search', methods=['GET', 'POST'])
def search():
    product = request.args.get('product', '')
    r = StringMatching.find(product)
    return jsonify({"sp": r[1].loc[r[0]]["product"]})


if __name__ == '__main__':
    app.run()
