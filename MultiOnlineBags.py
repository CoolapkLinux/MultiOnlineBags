import mc
import json
import pymongo
import os

# 从文件中获取JSON
def fileConvert(file):
    with open( file, 'r' ) as f:
        content = f.read()
    return content
class playerClass(): 
    # 注意Data是json格式，oganesson和alexhhh都是伞兵
    def __init__(self, player):
        # 初始化玩家对应的数据库
        address = "localhost:27017/"
        client = pymongo.MongoClient("mongodb://" + address)
        db = client['bagsDB']
        self.col = db[player.xuid]
        self.player = player
        self.totalBagNum = 2 #为将来玩家背包数不同铺路
        self.getNonFreeBags()
        self.getFreeBags()
    def delAllItem(self):
        # 删除游戏中数据，通过调用写入实现
        Data = fileConvert("defaultBag.json")
        self.player.setAllItem(Data)
    def getDbItem(self, bagNum):
        # 从数据库中获取背包
        Data = self.col.find_one({"_id": bagNum})
        del Data["_id"]
        DataJson = json.dumps(Data)
        self.Data = DataJson
    def setDbItem(self, bagNum):
        # 将背包放入数据库
        DataDict = json.loads(self.Data)
        DataDict["_id"] = bagNum
        #Data = json.dumps(DataDict)
        self.col.insert_one(DataDict)
    def delDbItem(self, bagNum):
        self.col.delete_one( { "_id": bagNum })        
    def getNonFreeBags(self):
        # 获取非空背包位置,这里的空和非空是对于MongoDB数据库而言
        self.nonFreeBagNumList = []
        for data in self.col.find({},{"_id": 1 }):
            self.nonFreeBagNumList.append(data["_id"])
        self.nonFreeBagNumList.sort()
    def getFreeBags(self):
        # 获取空背包位置
        self.allBagNumList = (1,self.totalBagNum)
        self.freeBagNumList = [numx for numx in self.allBagNumList if numx not in self.nonFreeBagNumList]
        self.freeBagNumList.sort()
    def newForm(self, mode):
        # 调用form类，为玩家显示窗体
        self.form = form(mode, self.player, self)
        self.form.push()
    def get(self, arg):
        # 执行get操作
        if json.loads(str(self.player.getAllItem())) == json.loads(str(fileConvert("defaultBag.json"))):
            self.getDbItem(self.nonFreeBagNumList[arg])
            self.player.setAllItem(self.Data) # self.data就是json格式
            self.delDbItem(self.nonFreeBagNumList[arg])
            mc.logout("name:"+str(self.player.name)+" xuid:"+str(self.player.xuid)+" 的背包获取完毕\n")
            code = 0
        else:
            code = 114514
        return code
    def save(self, arg):
        #执行save操作
        self.Data = self.player.getAllItem()
        if self.freeBagNumList != []:
            self.setDbItem(self.freeBagNumList[arg])
            self.delAllItem()
        mc.logout("name:"+str(self.player.name)+" xuid:"+str(self.player.xuid)+" 的背包保存完毕\n")
    def getBagList(self, bagNumList):
        bagList = "["
        for bagNum in bagNumList:
            bagList = bagList + json.dumps({'text':str(bagNum)}) + ","
        bagList = bagList[:-1] + "]"
        return bagList

class form():
    def __init__(self, mode, player, playerObject):
        # 将外参转变为内......参（字面意思
        self.mode = mode
        self.playerObject = playerObject
        self.player = player
    def push(self):
        self.playerObject.getNonFreeBags()
        self.playerObject.getFreeBags()
        if self.mode == "main":
            self.listId = self.player.sendSimpleForm('MultiOnlineBags', '请选择:', '[{"text":"保存当前背包"},{"text":"获取背包"},{"text":"取消"}]')
        elif self.mode == "get":
            bagList = self.playerObject.getBagList(self.playerObject.nonFreeBagNumList)
            if self.playerObject.nonFreeBagNumList == []:
                self.listId = self.player.sendSimpleForm('MultiOnlineBags', '当前没有可以取用的背包|･ω･｀)', '[{"text":"返回"}]')
            else:
                self.listId = self.player.sendSimpleForm('MultiOnlineBags', '请选择取用的背包\n当前可用背包:', str(bagList))
        elif self.mode == "save":
            bagList = self.playerObject.getBagList(self.playerObject.freeBagNumList)
            if self.playerObject.freeBagNumList == []:
                self.listId = self.player.sendSimpleForm('MultiOnlineBags', '数据库中你的背包已经存满w(ﾟДﾟ)w', '[{"text":"返回"}]')
            else:
                self.listId = self.player.sendSimpleForm('MultiOnlineBags', '请选择存储的背包\n当前可用背包:', str(bagList))
        elif self.mode == "get_pass":
            self.listId = self.player.sendSimpleForm('MultiOnlineBags', '取出成功 (ﾉ*･ω･)ﾉ', '[{"text":"返回主菜单"},{"text":"完成"}]')
        elif self.mode == "save_pass":
            self.listId = self.player.sendSimpleForm('MultiOnlineBags', '存入成功 =￣ω￣=', '[{"text":"返回主菜单"},{"text":"完成"}]')
        elif self.mode == "get_not_empty":
            self.listId = self.player.sendSimpleForm('MultiOnlineBags', '您当前身上存在物品，无法取出，请清除身上物品后重试', '[{"text":"完成"}]')
        elif self.mode == "incorrect":
            self.player.sendTextPacket("[MOB]您输入的命令有误，我们提供了/bags，/bags save与/bags get以更改您的背包")
        global listDict
        listDict[int(self.listId)] = self
    def execute(self, arg):
        if self.mode == "main":
            if arg == 0:
                self.playerObject.newForm("save")
            if arg == 1:
                self.playerObject.newForm("get")
        elif self.mode == "get":
            code = self.playerObject.get(arg)
            if code == 0:
                self.playerObject.newForm("get_pass")
            elif code == 114514:
                self.playerObject.newForm("get_not_empty")
        elif self.mode == "save":
            self.playerObject.save(arg)
            self.playerObject.newForm("save_pass")
        elif self.mode == "save_pass":  
            if arg == 0:
                self.playerObject.newForm("main")
        elif self.mode == "get_pass":
            if arg == 0:
                self.playerObject.newForm("main")

def command(arg):
    player = arg['player']
    cmd = arg['cmd'].split()
    global playerObject
    if cmd[0] == "/bags":
        if len(cmd) == 1:
            playerObject[player].newForm("main")
        elif cmd[1] == 'get':
            playerObject[player].newForm("get")
        elif cmd[1] == 'save':
            playerObject[player].newForm("save")
        else:
            playerObject[player].newForm("incorrect")

def replyForm(arg):
    if arg['selected'] != 'null':
        global playerObject
        formid = arg['formid']
        playerObject[arg['player']].form.execute(int(arg['selected']))

def join(player):
    global playerObject
    playerObject[player] = playerClass(player) #将playerClass实例化，从而调用属性和方法
    if playerObject[player].nonFreeBagNumList == []:
        player.sendTextPacket("[MOB]你是第一次登录服务器耶！\n如果不是，请向腐竹反馈")
    else:
        playerObject[player].get(0)

def left(player):
    global playerObject
    playerObject[player].getNonFreeBags()
    playerObject[player].getFreeBags()
    playerObject[player].save(0)
    del playerObject[player]

listDict = {}
playerObject = {}
#defaultTotalBagNum = 2

# 注册指令
mc.setCommandDescription('bags','背包同步')

# 进入监听器
mc.setListener('onPlayerJoin', join)

# 退出监听器
mc.setListener('onPlayerLeft', left)

# 命令监听器
mc.setListener('onInputCommand', command)

# 表单监视器
mc.setListener('onSelectForm', replyForm)
