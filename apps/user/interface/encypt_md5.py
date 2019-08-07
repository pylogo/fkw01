from hashlib import md5


def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    # 加盐
    new_md5.update('木柯'.encode('utf-8'))
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 后盐
    new_md5.update('发卡网'.encode('utf-8'))
    # 加密
    return new_md5.hexdigest()
