from django.http import JsonResponse


class httpCode(object):
    ok = 200
    paramserror = 400
    # 未授权
    unauth = 401
    # 方法错误
    methoderror = 405
    # 服务器内部错误
    servererror = 500


def result(code=httpCode.ok,message='',data=None,kwargs=None):
    json_dic={'code': code, 'message': message, 'data': data}

    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dic.update(json_dic)

    return JsonResponse(json_dic)


def ok():
    return result()


def para_error(message='',data=None):
    """
    参数错误
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.paramserror,message,data)


def unauth(message='',data=None):
    """
    未授权
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.unauth,message,data)


def method_erroe(message='', data=None):
    """
    方法错误
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.methoderror,message,data)


def server_erroe(message='', data=None):
    return result(httpCode.servererror,message,data)
