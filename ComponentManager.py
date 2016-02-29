Component = {}


class ComponentManager:

    @classmethod
    def new_Component(self, componentname):
        if componentname not in Component:
            Component[componentname] = {}

    @classmethod
    def dict_of(self, componentname):
        return Component[componentname]

    @classmethod
    def add_Component(self, Id, componentname, component):
        if componentname not in Component:
            ComponentManager.new_Component(componentname)
        Component[componentname][Id] = component

    @classmethod
    def add_Components(self, Id, componentdict):
        for key, value in componentdict:
            ComponentManager.add_Component(Id, key, value)

    @classmethod
    def remove_Component(self, componentname, Id):
        if Id in Component[componentname]:
            del Component[componentname][Id]

    @classmethod
    def remove_Components(self, componentnamelist, Id):
        for key in componentnamelist:
            ComponentManager.remove_Component(key, Id)

    @classmethod
    def cleanup(self, Id):
        for key in Component:
            ComponentManager.remove_Component(key, Id)

    @classmethod
    def get_Component(self, componentname, Id):
        return Component[componentname][Id]

    @classmethod
    def get_Components(self, componentname, Idlist):
        components = {}
        for Id in Idlist:
            component = ComponentManager.get_Component(componentname, Id)
            components[Id] = component
        return components
