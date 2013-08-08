# This Python file uses the following encoding: utf-8

import urllib2, urllib, os, time, sys
import simplejson

#http://image.baidu.com/i?ct=201326592&cl=2&lm=-1&st=-1&tn=baiduimagejson&istype=2&rn=32&fm=index&pv=&word=%E7%BE%8E%E5%A5%B3&s=6&z=0&1363082193135&callback=my

class ImageDownload(object):
	"""docstring for ImageDownoad"""
	def __init__(self, search_name):
		super(ImageDownload, self).__init__()
		self.__api_url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&imgtype=photo&imgsz=xxlarge&rsz=8&'
		self.__search_name = search_name

	def __get_response_result_dict(self, url):
		results = {}
		for i in range(5):
			try:
				print 'search for %s' % self.__search_name
				request = urllib2.Request(url)
				response = urllib2.urlopen(request)
				results = simplejson.load(response)
			except Exception, e:
				print 'search image %s failed: %s' %(self.__search_name, e) 
				time.sleep(5)
			else:
				print 'Got response from google result %s' % str(results)
				if results: break
		try:
			results = results['responseData']['results']
		except Exception, e:
			print 'get google api response failed: %s' % e
			return None
		else:
			return results

	def __download_image(self, url, path, file_name):
		try:
			print 'downloaind image from: %s' % url
			data = urllib.urlopen(url).read()
			path = os.path.join(path, ''.join(self.__search_name))
			if not os.path.exists(path):
				os.makedirs(path)
			file_path = os.path.join(path, file_name)
			print 'writing file:%s' % file_path
			f = open(file_path, 'wb+')
			f.write(data)
			f.close()
		except Exception, e:
			print 'Download image failed: %s' % e

	def download(self, file_dir=''):
		paramDict = {'q':self.__search_name}
		url = self.__api_url + urllib.urlencode(paramDict)
		print 'URL:%s' % url
		
		results = self.__get_response_result_dict(url)
		if results is None:
			return

		if file_dir is not '':
			path = file_dir
		else:
			path = self.__module_path()

		i = 1
		for result in results:
			try:
				self.__download_image(result['url'], path, str(i) + '.' + result['url'].split('.')[-1])
				i += 1
			except Exception, e:
				pass

	def __we_are_frozen(self):
	    # All of the modules are built-in to the interpreter, e.g., by py2exe
	    return hasattr(sys, "frozen")

	def __module_path(self):
	    encoding = sys.getfilesystemencoding()
	    if self.__we_are_frozen():
	        return os.path.dirname(unicode(sys.executable, encoding))
	    return os.path.dirname(unicode(__file__, encoding))

#print results

def main():
	image_dl = ImageDownload('杭州')
	image_dl.download()

if __name__ == '__main__':
	main()