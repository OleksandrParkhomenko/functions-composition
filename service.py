from flask import Flask, json, request
from functools import reduce
import functions

app = Flask(__name__)


def get_functions_list(funcs_names):
    funcs = []
    for name in funcs_names:
        try:
            func = getattr(functions, "fun_" + name)
            funcs.append(func)
        except Exception as e:
            print(e)
    return funcs


def composite_functions(*func):
    def compose(f, g):
        return lambda x: f(g(x))

    return reduce(compose, func, lambda x: x)


def get_result(data, rule):
    funcs = get_functions_list(rule)
    funcs.reverse()  # composition should begin from last func
    funcs_composition = composite_functions(*funcs)
    return list(map(funcs_composition, data))


@app.route('/get_result')
def hello():
    body = request.json
    data = body['data']
    rule = body['rule']
    print(type(data))
    print(type(rule))
    result = {
        'result': get_result(data, rule),
    }
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
