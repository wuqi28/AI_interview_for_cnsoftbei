from flask import jsonify


def R(code, message, data):
    result_data = {
        'code': code,
        'message': message,
        'data': data
    }
    # 返回 JSON 数据
    return jsonify(result_data)
