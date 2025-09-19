class Annotation(object):

    def __init__(self, predicate, obj):
        self._predicate = predicate
        self._obj = obj

    @property
    def predicate(self):
        return self._predicate

    @predicate.setter
    def predicate(self, new_pred):
        self._predicate = new_pred

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, new_obj):
        self._obj = new_obj
