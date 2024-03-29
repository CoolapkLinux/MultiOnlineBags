## 简介

以MongoDB数据库存储背包数据，在多个minecraft BDS服务端（即官方基岩版服务端）之间同步玩家的背包、穿戴、主手物品、末影箱等数据，从而无缝衔接游戏体验。可跨服务器同步。

在BDS 1.17.2和1.17.10上测试通过。

这个插件依赖于：

- MongoDB服务端
- Python3.7（未测试在其他版本上的可行性）
- liteloader BDS （yzu999 fork）
- BDSpyrunner
- pymongo python模块

MultiOnlineBags以GPLv3许可证开源，这意味着**你需要自行承担丢失数据的风险**。它的所有衍生版本亦应按照GPLv3开源。

## 部署

<font color=Red>注意！以下内容仅对1.17.10适用，请在左上角branch调成你的MC版本！</font>

### Windows7/10/11

现在假定你已经将minecraft BDS安装到了硬盘的某一位置。

1. 在 [Index of /ftp/python/](https://www.python.org/ftp/python/) 下载以3.7开头的python-3.7.x-amd64.exe，安装，注意安装的时候**一定一定一定**要勾选添加PATH。
2. 在 [Community Download | MongoDB](https://www.mongodb.com/try/download/community) 下载mongodb，选择Cloud>MongoDB Community Server，version选最新稳定版，Platform选windows，Package选msi，下载安装。（网页可能显示不全）
3. 在 https://github.com/LiteLDev/LiteLoaderBDS/releases/ 页面下载liteloader1.1.0版。下载后把解压出的所有文件放入BDS根目录，运行SymDB2.exe文件。
4. 在[Release 适配1.17.10 · yzu999/BDSpyrunner (github.com)](https://github.com/yzu999/BDSpyrunner/releases/tag/1.6.0) 下载dll文件，放入plugins文件夹，运行BDS主程序，如果出现BDSpyrunner说明配置成功。
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

如果您需要使用物理跨服，请参考[配置文件选项_MonogDB 中文网](https://mongodb.net.cn/manual/reference/configuration-options/)写配置文件，写bindIp要涵盖你配置插件的服务器ip，port要用映射到公网的端口，然后在上面address配置成数据库所在服务器ip:port。

Windows上mongodb二进制文件和默认配置文件装在`C:\Program Files\MongoDB\Server\<版本号>\bin`，在此目录下输入`.\mongodb --config <配置文件目录>`开启mongodb。

## 使用

在玩家进入和退出的时候会自动同步其背包，进入时默认加载1号背包。

输入/bags打开背包菜单，可存入当前背包、取用背包，但取用之前必须确保自己没有物品（包括穿戴主手末影箱）

## 问题排查与避免

- 玩家进入后，BDS卡死，退出后过一段时间滚出大堆错误：MongoDB server没启动，或者ip/端口配置出错
- 每个玩家进入时都会提示是第一次进入：刚装插件后第一次进提示是正常现象，每次进入都提示，请发issue
- 输入命令的时候会出现未知指令的提示，属正常现象，不影响使用（上游的锅，已提issue）
- 其他问题，包括README看不懂，操作卡在哪一步之类，发issue就行。
- 如果输入/bags没反应，可能是服务器没开作弊（修改BDS根目录的server.properties，allow-cheats=true）
- 部署都正确的情况下，打开BDS报错，显示import xxx转来转去到了一个不存在的目录（甚至不存在的盘符）。你可能使用了某种开服包，作者在把python库打包成dll文件后，这个dll会干扰python的path。可以尝试删除BDS根目录以python37开头的dll文件，再进入报错就用部署第6点的方法缺啥装啥，但是这样其他一些插件可能挂掉。
- 在测试过程中，突然关闭服务器未见背包丢失情况，但关服前还是让所有玩家先自行退出为妙。~~可以直接kick @a~~  再强调一遍，**你需要自行承担数据丢失的风险。**

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

