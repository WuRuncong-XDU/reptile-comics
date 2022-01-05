# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
import scrapy


# 重写父类方法
class imgsPipelines(ImagesPipeline):
    # 对item中的图片进行请求操作
    def get_media_requests(self, item, info):
        # yield手动发送请求
        yield scrapy.Request(item['img_src'])

    # 定制图片的名称
    def file_path(self, request=None, response=None, info=None, *, item):
        imageName = "/{}/{:0>3d}.jpg".format(item['title'], item['page'])
        # imageName = "{:0>3d}.jpg".format(item['page'])
        return imageName

    def item_completed(self, results, item, info):
        mes = item['title'] + str(item['page'])
        if results[0][0]:
            print('success : ' + mes)
        else:
            print('failure : ' + mes)
        return item  # 该返回值会传递给下一个即将执行的管道类
