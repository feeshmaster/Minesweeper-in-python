class Modes():
    def __init__(self):
        self.modes = {
            "easy": {
                "w": 5,
                "h": 5,
                "mines": 4,
                "name": "Easy"
            },
            "medium": {
                "w": 7,
                "h": 7,
                "mines": 8,
                "name": "Medium"
            }
        }
    def modesArray(self):
        array = []
        for i in self.modes:
            array.append(i) 
        return array  