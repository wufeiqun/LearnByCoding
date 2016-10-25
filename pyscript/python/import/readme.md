#### import 使用说明

* `from aa import * (不推荐使用)`

```
$cat aa.py

#__all__ =["aa"]

def _aa():
    print "_aa"

def aa():
    print "aa"

def bb():
    print "bb"

如果aa.py中定义了__all__变量,那么from aa import *的时候只会引用已经定义的模块名字,如果没定义__all__的话,_aa不会引用,其他的都引用
```

