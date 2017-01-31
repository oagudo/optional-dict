from collections import defaultdict
import copy

class OptDict(defaultdict):
    """ Recursive default dictionary definition allowing to traverse it based 
        on optional (potential missing) keys. Useful for traversing JSON with 
        potential missing keys
    """
    
    def __missing__(self, key):
        return self.default_factory()

    @classmethod
    def from_dict(cls, dictionary):
        """Creates an OptDict from a dict"""

        empty = lambda: cls(empty) # Recursive empty defaultdict definition
        opt_dict_factory = lambda dict_val: cls(empty, dict_val)

        def to_opt_dict(d):
            for k, v in d.iteritems():
                if isinstance(v, dict):
                    new_dict = to_opt_dict(v)
                    d[k] = new_dict
                elif isinstance(v, list):
                    new_list = map(lambda x: to_opt_dict(x) if isinstance(x, dict) else x, v)
                    d[k] = new_list
            return opt_dict_factory(d)
                
        return to_opt_dict(copy.deepcopy(dictionary))

# USAGE:

d = { "key_1" : "val_1", "key_2" : {"key_2_1" : {"key_2_1_1" : "val_2"}}, "key_3" : [1, 2, 3] }
opt_d = OptDict.from_dict(d)

print opt_d.get("key_1", "default_value")
# > val_1
print opt_d.get("missing_key", "default_value")
# > default_value

print opt_d["key_2"]["key_2_1"]["key_2_1_1"]
# > val_2
print opt_d["key_2"]["missing_key"]["missing_key"]["missing_key"]["missing_key"]["missing_key"].get("key_2_1_1", "default_value")
# > default_value

for i in opt_d.get("key_3", []):
    print i
# > 1
# > 2
# > 3
for i in opt_d.get("missing_key", []):
    print i # Nothing is printed