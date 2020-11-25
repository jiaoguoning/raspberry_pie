import importlib

pkg = __name__.rpartition('.')[0]
mname = '.'.join((pkg, '_pafprocess')).lstrip('.')
print(mname)
_pafprocess = importlib.import_module(mname)
_swig_property = property

def process_paf(p1, h1, f1):
    return _pafprocess.process_paf(p1, h1, f1)

process_paf = _pafprocess.process_paf

def get_num_humans():
    return _pafprocess.get_num_humans()
get_num_humans = _pafprocess.get_num_humans

def get_part_cid(human_id, part_id):
    return _pafprocess.get_part_cid(human_id, part_id)
get_part_cid = _pafprocess.get_part_cid

def get_score(human_id):
    return _pafprocess.get_score(human_id)
get_score = _pafprocess.get_score

def get_part_x(cid):
    return _pafprocess.get_part_x(cid)
get_part_x = _pafprocess.get_part_x

def get_part_y(cid):
    return _pafprocess.get_part_y(cid)
get_part_y = _pafprocess.get_part_y

def get_part_score(cid):
    return _pafprocess.get_part_score(cid)
get_part_score = _pafprocess.get_part_score