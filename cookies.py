import hashlib,random, time

def bakeCookie():
	randy = str(random.random() + time.time() )
	hashy = hashlib.sha256(randy).hexdigest()
	token = hashy[:128]
	return(token)