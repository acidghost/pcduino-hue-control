import requests

class Discovery(object):
	"""docstring for Discovery"""
	@staticmethod
	def find():
		r = requests.get('https://www.meethue.com/api/nupnp')

		ips = []
		for elm in r.json():
			ips.append(elm['internalipaddress'])

		return ips
