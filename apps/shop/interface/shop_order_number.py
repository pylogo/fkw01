# 生成商品订单号
import random


def shop_order():
    res = ''.join(random.sample(
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n',
         'm',
         'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd',
         'c', 'b', 'a'], 30))
    return res
