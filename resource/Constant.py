from typing import List


class MenuAction:
    name: str = ""
    text: str = ""
    shortcut: str = ""
    icon = ""

    def __init__(self, name, text, shortcut="", icon=""):
        self.name = name
        self.text = text
        self.shortcut = shortcut
        self.icon = icon


class MenuItem:
    name: str = ""
    text: str = "未定义"
    actions: List[MenuAction]
    icon:str = ""

    def __init__(self, name, text, actions, icon=""):
        self.name = name
        self.text = text
        self.actions = actions
        self.icon = icon


class Constant:
    app = "PhotoSharp"
    menu = [
        MenuItem("file", "图片", [
            MenuAction("open", "打开", "Ctrl+O"),
            MenuAction("save", "保存", "Ctrl+S"),
            MenuAction("save_as", "另存为", "Ctrl+Alt+S"),
            MenuAction("quit", "退出", "Alt+F4"),
        ], "./resource/imageIcon.png"),
        MenuItem("edit", "编辑", [
            MenuAction("undo", "撤销", "Ctrl+Z"),
            MenuAction("redo", "恢复", "Ctrl+Y")
        ]),

        MenuItem("help", "帮助", [
            MenuAction("doc", "文档", "F4"),
            MenuAction("author", "关于作者")
        ])
    ]

