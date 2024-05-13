import json


class Mp3Data:
    def __init__(self):
        self.title = ""
        self.url = ""
        self.duration = ""
        self.published = ""

    def __repr__(self):
        return f"Mp3Data(title={self.title}, url={self.url}, duration={self.duration}, published={self.published})"


class Author:
    def __init__(self):
        self.author_name = ""
        self.data_list = []

    def add_mp3_data(self, mp3_data):
        self.data_list.append(mp3_data)

    def __repr__(self):
        return f"Author(name={self.author_name}, data_list={self.data_list})"


class DataAll:
    def __init__(self):
        self.data_date = ""
        self.authors = []

    def add_author(self, author):
        self.authors.append(author)

    def __repr__(self):
        return f"DataAll(date={self.data_date}, authors={self.authors})"


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Mp3Data):
            return {
                'title': obj.title,
                'url': obj.url,
                'duration': obj.duration,
                'published': obj.published
            }
        elif isinstance(obj, Author):
            return {
                'name': obj.author_name,
                'dataList': [self.default(item) for item in obj.data_list]  # 使用self.default
            }
        elif isinstance(obj, DataAll):
            return {
                'dataDate': obj.data_date,
                'authors': [self.default(author) for author in obj.authors]
            }
        # 对于不支持的类型，让基类来处理
        return super().default(obj)  # 使用super().default更简洁


# # 示例用法
# data_all = DataAll()
# author = Author()
# author.author_name = "Some Author"
# mp3_data = Mp3Data()
# mp3_data.title = "Example Title"
# mp3_data.url = "http://example.com/mp3"
# mp3_data.duration = "3:20"
# mp3_data.published = "2023-01-01"
# author.add_mp3_data(mp3_data)
# data_all.data_date = "2023-01-01"
# data_all.add_author(author)
#
# json_str = json.dumps(data_all, cls=CustomEncoder, indent=4)  # 使用indent增加可读性
# print(json_str)