
from thoth.python import Source

test = Source("https://pypi.python.org/simple", True)
print(test)
# def map_url(x):
#     if x=='apple':
#         return 'mango'
#     else:
#         return x

# import attr
# @attr.s(slots=True, frozen=True)
# class C:
#     url = attr.ib(type=str, converter=map_url)
#     x = attr.ib()
#     y = attr.ib()
#     z = attr.ib(default=10)
    
#     # def __attrs_post_init__(self):
#     #     if self.url == "apple":
#     #         object.__setattr__(self, "url", "mango")
    
#     @y.default
#     def _any_name_except_a_name_of_an_attribute(self):
#         return self.x + 1

# print(C(x=4,y=5, url="apple"))