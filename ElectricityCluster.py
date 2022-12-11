import json


class ElectricityCluster:
    def __init__(self):
        self.collection = []

    def add_electricity(self, elect):
        self.collection.append(elect)

    def get_cluster(self):
        return self.collection

    def get_JSON(self):
        write_collection = []
        for elem in self.collection:
            write_collection.append([elem.get_x(), 
                                     elem.get_y(), 
                                     elem.get_clockwise()])
        return json.dumps(write_collection)
