# -*- coding: utf-8 -*-


# 错误码设计规则
# =0 正常， > 0 不正常，  4前缀为客户端错误， 5前缀为服务端错误， 错误码分段<前缀><服务模块代码2位><具体错误代码2位>
# 01 数据库模块  02 微信后台交互模块

# 正常
CODE_OK = 0

# 客户端传参校验错误
CODE_INVALID_PARAMS = 40000

# 数据库相关模块
CODE_DB_TABLE_NOT_EXIST = 50101

# 微信登录相关错误
CODE_WX_LOGIN_FAILED = 50201

# 第三方接口调用相关错误

# 一般问题
CODE_COMMON = 2000

# 内部服务错误
CODE_SERVER_ERROR = 5002


CODE_TOKEN_EXPIRE = 9006
CODE_TOKEN_DISABLED = 9022
