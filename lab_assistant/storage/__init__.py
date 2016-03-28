from copy import deepcopy
import pickle
import uuid

from lab_assistant import conf, utils


__all__ = [
    'get_storage',
    'store',
    'retrieve',
]


def get_storage(path=None, **opts):
    if not path:
        path = conf.storage['path']
        _opts = deepcopy(conf.storage['options'])
        _opts.update(opts)
        opts = _opts

    if path in get_storage._cache:
        return get_storage._cache[path]

    Storage = utils.import_path(path)
    get_storage._cache[path] = Storage(**opts)
    return get_storage._cache[path]
get_storage._cache = {}


def store(result, storage=None):
    storage = storage or get_storage()
    key = str(uuid.uuid4)
    return storage.set(key, pickle.dumps(result))


def retrieve(key, storage=None):
    storage = storage or get_storage()
    result = storage.get(key)
    if result:
        return pickle.loads(result)