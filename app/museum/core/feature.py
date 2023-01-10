class Base:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def process(self, file_path=None, file_bytes=None):
        pass

    def get_info(self):
        pass


"""
setattr은 객체의 속성값을 생성해준다.
base = Base(window_size=128)
setattr(base, window_size, 128)
self.window_size = 128 -> 다음과 같은 attribute 가 생성된다.
"""