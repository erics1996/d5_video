import os
import datetime

import uuid


# 修改文件名称
def change_filename(filename):  # 需要将filename转换为安全的文件爱你名称（filename）有时间前缀字符串拼接的名称
    file_info = os.path.splitext(filename)  # 分割成后缀加前缀
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + file_info[-1]
    return filename
