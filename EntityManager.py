from uuid import uuid4


Id = []


class EntityManager:

    @classmethod
    def new_Id(self):
        nId = uuid4()
        Id.append(str(nId))
        return str(nId)

    @classmethod
    def remove_Id(self, rId):
        Id.remove(rId)

    @classmethod
    def lst_Ids(self):
        return Id
