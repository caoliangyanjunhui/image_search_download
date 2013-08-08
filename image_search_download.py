# This Python file uses the following encoding: utf-8
import threading, time
from google_img_api import ImageDownload

class ImagesSearchDownload(object):
	"""docstring for ClassName"""
	def __init__(self, search_list, file_dir):
		super(ImagesSearchDownload, self).__init__()
		self.__search_list = search_list
		self.__file_dir = file_dir

	def download_images(self):
		th = []
		for words in self.__search_list:
			img_dl = ImageDownload(' '.join(words))
			t = threading.Thread(target=self.__download_single_image, args=(img_dl, ))
			th.append(t)

		for t in th:
			t.start()
			time.sleep(0.1)

		for t in th:
			t.join()

	def __download_single_image(self, img_dl_obj):
		img_dl_obj.download(self.__file_dir)

def main():
	l = [['杭州', '外婆家'], ['北京', '全聚德'], ['杭州', '植物园']]
	imgs = ImagesSearchDownload(l, '.')
	imgs.download_images()

if __name__ == '__main__':
	main()