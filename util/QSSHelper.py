class QSSHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_qss(style):
        try:
            with open(style, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print("[QSSHelper] File Not Found")
