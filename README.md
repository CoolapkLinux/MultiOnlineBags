## 简介

以MongoDB数据库存储背包数据，在多个minecraft BDS服务端（即官方基岩版服务端）之间同步玩家的背包、穿戴、主手物品、末影箱等数据，从而无缝衔接游戏体验。可跨服务器同步。

在BDS 1.17.2上测试通过。由于BDSpyrunner上游原因，暂未支持BDS 1.17.10。

这个插件依赖于：

- MongoDB服务端
- Python3.7（未测试在其他版本上的可行性）
- liteloader BDS（<1.0.3）
- BDSpyrunner
- pymongo python模块

MultiOnlineBags以GPLv3许可证开源，这意味着**你需要自行承担丢失数据的风险**。它的所有衍生版本亦应按照GPLv3开源。

## 部署

### Windows7/10/11

现在假定你已经将minecraft BDS安装到了硬盘的某一位置。

1. 在 [Index of /ftp/python/](https://www.python.org/ftp/python/) 下载以3.7开头的python-3.7.x-amd64.exe，安装，注意安装的时候**一定一定一定**要勾选添加PATH。
2. 在 [Community Download | MongoDB](https://www.mongodb.com/try/download/community) 下载mongodb，选择Cloud>MongoDB Community Server，version选最新稳定版，Platform选windows，Package选msi，下载安装。（网页可能显示不全）
3. 在 https://github.com/LiteLDev/LiteLoaderBDS/releases/ 页面下载lightloader，注意暂不能使用1.0.3及更高版本，因为没适配。下载后把解压出的所有文件放入BDS根目录，运行RoDB.exe文件。
4. 在 [Actions · twoone-3/BDSpyrunner (github.com)](https://github.com/twoone-3/BDSpyrunner/actions) 页面找“x.x.x更新”开头的workflow，下载其中artifacts里的dll文件。将dll文件放入BDS根目录中的plugins文件夹。
5. 运行BDS主程序，如果出现BDSpyrunner说明配置成功。
6. 下载release里的压缩包，将其中的MultiOnlineBags.py放入plugins/py文件夹，defaultBag.json放入BDS根目录。
7. 打开powershell（或者命令提示符），执行pip install pymongo --target=plugins/py文件夹的路径
8. 在硬盘某一位置建立一个文件夹。（该目录和上级目录最好都是英文）
9. 在mongodb的bin目录（默认在C:\Program Files\MongoDB\Server\\[版本号]\bin）shift右键，用powershell（命令提示符也行）执行.\mongod --dbpath 刚才的文件夹目录，并保持这个终端窗口不要关闭。
10. 打开BDS，看到 loading MultiOnlineBags 应该就可以使用了。

## 配置

在MultiOnlineBags.py上直接修改：

```python
class playerClass(): 
    def __init__(self, player):
        address = "localhost:27017/" #写成你的MongoDB数据库ip:端口
        client = pymongo.MongoClient("mongodb://" + address)
        db = client['bagsDB']
        self.col = db[player.xuid]
        self.player = player
        self.totalBagNum = 2 #每个玩家拥有的背包个数
        self.getNonFreeBags()
        self.getFreeBags()
```

## 使用

在玩家进入和退出的时候会自动同步其背包，进入时默认加载1号背包。

输入/bags打开背包菜单，可存入当前背包、取用背包，但取用之前必须确保自己没有物品（包括穿戴主手末影箱）

## 问题排查与避免

- 玩家进入后，BDS卡死，退出后过一段时间滚出大堆错误：MongoDB server没启动，或者ip/端口配置出错
- 每个玩家进入时都会提示是第一次进入：刚装插件后第一次进提示是正常现象，每次进入都提示，请发issue
- 弹出对话框提示XXX dll出错：可能是按照BDSpyrunner的wiki装了最新版的BDXcore而不是liteloader，wiki害人呐
- 输入命令的时候会出现未知指令的提示，属正常现象，不影响使用（上游的锅，已提issue）
- 其他问题，包括README看不懂，操作卡在哪一步之类，发issue就行。

在测试过程中，突然关闭服务器未见背包丢失情况，但关服前还是让所有玩家先自行退出为妙。~~可以直接kick @a~~  再强调一遍，**你需要自行承担数据丢失的风险。**

如需关闭数据库的终端窗口，请先关闭BDS服务端！！！

上插件之前最好也做一次备份，避免背包数据丢失。

## TODO(gugugu)

- [ ] 在BDS on Linux上尝试部署
- [ ] 使用c++重写一个版本
- [ ] 支持 *真正的* 指令注册
- [ ] 支持玩家背包数不同，甚至可以与货币插件对接
- [ ] 随着配置项变多了，肯定还是要写配置文件（

## 鸣谢

感谢oganesson不懈（麻了/懂了）地修改代码（大部分代码是他写的）(๑•̀ㅂ•́)و✧

感谢我自己为插件引入了许多bug，增大了debug的工作量 Σ( ° △ °|||)︴

感谢俺妹（lighthua）维护了一个优秀的服务器，给我们写插件带来了动力ヽ(✿ﾟ▽ﾟ)ノ

（加QQ群1101450234，欢迎来玩）

