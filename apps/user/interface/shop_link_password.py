# 加密
def encrypt_pk(user_pk):
    num = (int(user_pk) + 1024) * 1024
    return num


# 解密
def deciphering_pk(encrypt_pk):
    num = (int(encrypt_pk) / 1024) - 1024
    return num
