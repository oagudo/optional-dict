# optional-dict

Recursive default dictionary definition allowing to traverse it based on optional (potential missing) keys. Useful for traversing JSON with missing keys

print opt_d["key_2"]["missing_key"]["..."]["..."].get("key_2_1_1", "default_value")
> default_value
