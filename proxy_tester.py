import requests
from requests.packages.urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
from colorama import init, Fore, Back, Style
import urllib3, sys
init(convert=True)

site=input(" < Enter Site towards you want to test your proxies,(for example: https://www.kith.com): ")

indexProxy = 0 
def getProxy():
	global indexProxy
	try:
		x=open("proxies.txt", 'r')
		lines=x.readlines()
		if(indexProxy == len(lines)):
			print(" <<< Checked all proxies, leaving...")
			sys.exit(1)
		else :
			proxy = lines[indexProxy]
			indexProxy += 1
		return proxy 


	except Exception as e:
		raise e


def proxies(s):
	getProxy()

	prox = getProxy()
	prox = prox.replace("\n","")
	proxies = {
		'http': 'http://'+str(prox),
		'https': 'http://'+str(prox),
	}
	proxies=proxies
	s.proxies = proxies

header={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
class connAdapter(HTTPAdapter):
    def init_poolmanager(pat, connections, maxsize, block=False):
        pat.poolmanager = PoolManager(num_pools=connections,
        maxsize=maxsize,
        block=block)

class tester():
	def __init__(pat,):
		pat.user_agent=header
		pat.site=site
		pat.proxies=proxies

	def check_proxies(pat):

		pat.s=requests.session()
		pat.s.mount('https://', connAdapter())
		while True:
			proxies(pat.s)
			proxy_ip=(pat.s.proxies)['https']
			try:
				req=pat.s.get(pat.site, headers=pat.user_agent, timeout=10, proxies=pat.s.proxies)
				if req.status_code==429 or req.status_code==403 or req.status_code==401:
					print(Fore.YELLOW+" < PROXY %s WORKS, BUT IP IS RATE LIMITED / ACCESS IS FORBIDDEN / AUTHENTICATION IS REQUIRED" %proxy_ip)
				elif req.status_code==403 and req.headers.get("Server", "").startswith("cloudflare") and "/cdn-cgi/l/chk_captcha" in req.text:
					print(Fore.WHITE+" < PROXY %s WORKS, BUT THE SITE NEEDS A CLOUDFLARE-CAPTCHA." %proxy_ip)
				elif req.status_code==503 or req.status_code==502:
					print(Fore.WHITE+" < PROXY %s WORKS, BUT A SITE ERROR OCCURRED." %proxy_ip)
				elif (req.status_code==503 or req.status_code==429) and req.headers.get("Server", "").startswith("cloudflare") and "jschl_vc" in req.text:
					print(Fore.WHITE+" < PROXY %s WORKS, BUT THE SITE IS CLOUDFLARE PROTECTED." %proxy_ip)
				elif req.status_code in (200,302,201):
					print(Fore.GREEN+" < SUCCESSFULLY CONNECTED TO {} with Proxy {}, Proxy Works.".format(pat.site,proxy_ip))
			except ConnectionError:
				print(Fore.RED+"< [ERROR] Unable to connect to Proxy %s " % proxy_ip)
			except TimeoutError:
				print(Fore.YELLOW+"< [INFO] Connection timed out with Proxy %s " % proxy_ip)
			except requests.exceptions.InvalidURL as e:
				print(Fore.RED+"< [INFO] Invalid proxy format entered.")
			except requests.exceptions.ReadTimeout as rT:
				print(Fore.YELLOW+"< [INFO] Connection timed out with Proxy %s " % proxy_ip)
			except ProxyError: 
				print(Fore.RED+" < ERROR : PROXY ERROR aka proxy dead")
			except Exception as e:
				print(Fore.RED+"< ERROR : {}".format(str(e)))

t=tester()
t.check_proxies()

