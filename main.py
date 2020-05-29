from mirai import Mirai, Plain, MessageChain, Friend, Group, Member, GroupMessage, FriendMessage, Face, Image
from mirai.face import QQFaces
from pydantic import HttpUrl
import re
import copy
import random
import time

qq = 75960775 # 字段 qq 的值
authKey = 'AAAAAAAA' # 字段 authKey 的值
mirai_api_http_locate = 'localhost:8080/ws' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.
app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")


TABLE_FORMAT = """
"""


RECORDS_TEMPLATE = {
    "内功": {
        "current": [],
        "max": 7
    },
    "外攻": {
        "current": [],
        "max": 7
    },
    "治疗": {
        "current": [],
        "max": 4
    },
    "T": {
        "current": [],
        "max": 2
    },
    "老板": {
        "current": [],
        "max": 5
    }
}

RECORDS = {}


PROFESSION = {
    "内功": ["花间", "毒经", "田螺", "莫问", "气纯", "冰心", "明教"],
    "外攻": ["霸刀", "藏剑", "凌雪阁", "鲸鱼", "分山劲", "傲血", "剑纯", "丐帮"],
    "治疗": ["奶花", "奶歌", "奶毒", "奶秀"],
    "T": ["策T", "喵T", "和尚T", "苍云T", "铁牢", "明尊"],
    "老板": ["\S*老板"]
}


WORDS = [
    "我怀疑你们在搞黄色",
    "听。。听不懂啊",
    "放开我，我想下班！",
    "忘却难免留个疤",
    "我好饿",
    "你不对劲"
]

STATUS = True

def message_handler(member, message):
    global RECORDS
    if not RECORDS:
        RECORDS = copy.deepcopy(RECORDS_TEMPLATE)

    for p_type, p_list in PROFESSION.items():
        profession_compare = "|".join(p_list)
        records = re.findall(profession_compare, message)
        sign_up(p_type, member, records)


def sign_up(p_type, member, records):
    global RECORDS
    for record in records:
        member_info = RECORDS.get(p_type)
        if len(member_info.get("current")) >= member_info.get("max"):
            raise Exception("FULL")
        member_info["current"].append("{profession}({member})".format(profession=record, member=member.memberName))
        # member_info["current"].append("{profession}({member})".format(profession=record, member=member.nickname))

def format_table():
    global RECORDS
    table_string = ""
    for p_type, member_info in RECORDS.items():
        table_string += "{}: \n    ".format(p_type)
        table_string += "\n    ".join(member_info.get("current"))
        table_string += "\n"

    print(table_string)
    return table_string

def random_words():
    return random.choice(WORDS)


@app.receiver("GroupMessage")
async def GMHandler(app: Mirai, group: Group, member: Member, message: GroupMessage):
    print(message)
    print(message.toString())
    global RECORDS, STATUS
    if "醒醒不对劲" in message.toString():
        STATUS = True
        await app.sendGroupMessage(group, [
            Plain(text="我还想再睡会儿!")
        ])

    if not STATUS:
        return

    if "报名" in message.toString():
        try:
            message_handler(member, message.toString())
            await app.sendGroupMessage(group, [
                Plain(text=format_table())
            ])
        except Exception:
            await app.sendGroupMessage(group, [
                Plain(text="糟糕，坑满啦!")
            ])
    elif "clear" in message.toString():
        RECORDS = {}
        await app.sendGroupMessage(group, [
            Plain(text=format_table())
        ])
    elif "出来吧憨憨" in message.toString():
        time.sleep(1)
        await app.sendGroupMessage(group, [
            Plain(text="余目才是憨批！")
        ])
    elif message.toString() == "/roll":
        await app.sendGroupMessage(group, [
            Plain(text=str(random.randint(0, 100)))
        ])
    elif "At::target=75960775" in message.toString():
        if random.randint(0, 10) < 4:
            await app.sendGroupMessage(group, [
                Plain(text="喊我干啥，我又不是小爱同学"),
                Face(faceId=QQFaces['nanguo'])
            ])
        else:
            await app.sendGroupMessage(group, [
                Plain(text=random_words())
            ])
    elif "睡吧不对劲" in message.toString():
        STATUS = False
        await app.sendGroupMessage(group, [
            Plain(text="晚安~"),
            Image(type='Image', imageId='AD698F3D-FCEC-0516-C6DA-346967FF876E', url=HttpUrl(
                'http://gchat.qpic.cn/gchatpic_new/843452214/1032083209-2934067879-AD698F3DFCEC0516C6DA346967FF876E/0?term=2',
                scheme='http', host='gchat.qpic.cn', tld='cn', host_type='domain',
                path='/gchatpic_new/843452214/1032083209-2934067879-AD698F3DFCEC0516C6DA346967FF876E/0', query='term=2'))
        ])
    else:
        num = random.randint(0, 100)
        if num < 10:
            time.sleep(1)
            await app.sendGroupMessage(group, [
                Plain(text=random_words())
            ])

    if random.randint(0, 100) < 30 and "At::target" not in message.toString():
        WORDS.append(message.toString())

# @app.receiver("FriendMessage")
# async def FMHandler(app: Mirai, friend: Friend, message: FriendMessage):
#     global RECORDS
#     if "报名" in message.toString():
#         message_handler(friend, message.toString())
#         await app.sendFriendMessage(friend, [
#             Plain(text=format_table())
#         ])
#     elif "clear" in message.toString():
#         RECORDS = {}
#         await app.sendFriendMessage(friend, [
#             Plain(text=format_table())
#         ])



if __name__ == "__main__":
    app.run()