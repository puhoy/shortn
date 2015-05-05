__author__ = 'meatpuppet'

from .. import redis_store


# TODO: NOT USED, delete later


"""based on: http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html"""
class RedisLoopedList(object):
    def __init__(self, name, namespace='LoopedList', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis_store
        self.key = '%s:%s' %(namespace, name)
        self.top = 0
        self.size = 10000

        #create a new, empty list
        for x in range(0, self.size):
            self.__db.lpush(self.key, x, {'url': '',
                                          'clicks': 0,
                                          'creation_time': None,
                                          'last_click_time': None})

    def put(self, item):
        """Put item into the queue."""
        # check if item is in the list
        index = self._is_in_list(self.key, item)
        if index:
            return index

        # def linsert(self, name, where, refvalue, value):
        # Insert ``value`` in list ``name`` either immediately before or after [``where``] ``refvalue``
        self.__db.lset(self.key, self.top, item)
        self.top %= self.top
        self.top += 1
        return self.top - 1

    def get(self, index):

        return self.__db.lindex(self.key, index)

    def _is_in_list(self, list, value):
        for x in range(0, self.size):
            if self.__db.lindex(list, x).get('url', None) == value:
                return x
        return False
