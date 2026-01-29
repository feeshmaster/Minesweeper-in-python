class Modes():
    def __init__(self):
        self.modes = {
            "easy": {
                "w": 9,
                "h": 9,
                "mines": 10,
                "name": "Easy"
            },
            "medium": {
                "w": 16,
                "h": 16,
                "mines": 40,
                "name": "Medium"
            },
            "hard": {
                "w": 30,
                "h": 16,
                "mines": 99,
                "name": "Hard"
            }
        }
    def modesArray(self):
        array = []
        for i in self.modes:
            array.append(i) 
        return array  