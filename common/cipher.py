# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# import argparse
# import base64
#
# from Crypto.Cipher import AES
#
#
# # 128bits block size
# BLOCK_SIZE = 16
# PADDING = '\0'
# pad_it = lambda s: s+(16 - len(s)%16)*PADDING
#
#
# #使用aes算法，进行加密解密操作
# #为跟java实现同样的编码，注意PADDING符号自定义，支持AES/CBC/NoPadding的方式！！！！！！
# def aes_encrypt(message, key, iv):
#     generator = AES.new(key, AES.MODE_CBC, iv)
#     crypt = generator.encrypt(pad_it(message))
#     cryptedStr = base64.b64encode(crypt)
#     return cryptedStr.decode("utf-8")
#
# def aes_decrypt(cryptedStr, key, iv):
#     padding = bytes(PADDING, 'utf-8') # 转换成字节流
#     generator = AES.new(key, AES.MODE_CBC, iv)
#     cryptedStr = base64.b64decode(cryptedStr)
#     recovery = generator.decrypt(cryptedStr)
#     decryptedStr = recovery.rstrip(padding)
#     return decryptedStr.decode("utf-8")
#     #b'LgD+;?~\x98\xc9tsSM7]\xdb'
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="encrypt program")
#     group = parser.add_mutually_exclusive_group()
#     group.add_argument("-e", "--encrypt",
#                        action="store_true",
#                        help="encrypt the string")
#     group.add_argument("-d", "--decrypt",
#                        action="store_true",
#                        help="decrypt the string")
#     parser.add_argument("-k", "--key",
#                         help="the key , contact the admin to get the key")
#     parser.add_argument("-i", "--iv",
#                         help="the iv , contact the admin to get the iv")
#     parser.add_argument("-s", "--string",
#                         help="the string you want to decrypt or encrypt")
#     args = parser.parse_args()
#     if args.encrypt:
#         print(aes_encrypt(args.string, args.key, args.iv))
#     elif args.decrypt:
#         print(aes_decrypt(args.string, args.key, args.iv))
#
#     else:
#         print("illegal usage ,please see the help")
