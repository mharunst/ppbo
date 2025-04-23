Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> from collections import namedtuple
>>> jane = {"name": "Jane", "age": 25, "height": 1.75}
>>> jane["age"] = 26
>>> jane["age"]
26
>>> jane["weight"] = 67
>>> jane
{'name': 'Jane', 'age': 26, 'height': 1.75, 'weight': 67}
>>> # Equivalent named tuple
>>> Person = namedtuple("Person", "name age height")
>>> jane = Person("Jane", 25, 1.75)
>>> jane
Person(name='Jane', age=25, height=1.75)
>>> jane.age = 26
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    jane.age = 26
AttributeError: can't set attribute
>>> jane.weight = 67
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    jane.weight = 67
AttributeError: 'Person' object has no attribute 'weight'
