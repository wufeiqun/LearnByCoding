# 很多情况下我们会去使用临时文件, 比如之前写过一个备份恢复mysql的脚本, 每一个表先备份到一个临时目录中
# 之前做过一个修改远程服务器的hosts文件的, 使用的也是一个临时的目录
# 这个时候我们使用python内置模块tempfile再合适不过了
import tempfile
# 临时文件

with tempfile.TemporaryFile() as f:
    f.write(b"AAA")
    # Seek back to beginning and read the data
    f.seek(0)
    f.read()
# Now the temprory file is destroyed

f = tempfile.TemporaryFile()
f.write(b"AAA")
f.seek(0)
data = f.read()
print(data)
f.close()
# Now the temprory file is destroyed

# 临时目录
with tempfile.TemporaryDirectory() as dirname:
    print(type(dirname)) #str
    print(dirname) # /tmp/path

# 临时目录销毁

tmpdir = tempfile.TemporaryDirectory()
# 使用临时目录
dirname = tmpdir.name
# 显式销毁, 如果不显式销毁, 程序执行完也会自动销毁的
tmpdir.cleanup()


