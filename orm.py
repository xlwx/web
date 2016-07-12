import logging
import  asyncio, aiomysql

def log(sql,args=()):
	logging.info('SQL: %s' % sql)

async def creat_pool(loop,**kw):
	logging.info('Create database connection pool...')
	global __pool
	__pool = await aiomysql.create_pool(
		# kw.get(), if the value not exist, return the default value.
		host = kw.get('host','localhost'),
		port = kw.get('port',3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		chartset = kw.get('charset','utf8'),
		autocommit = kw.get('autocommit', True),
		maxsize = kw.get('maxsize',10),
		minsize = kw.get('minsize',1),
		loop=loop
	)


async def select(sql,arg,size=None):
	log(sql,args)
	global __pool
	with  __pool.get() as conn:
		cur = await conn.cursor(aiosql.DictCursor)
		# ? is SQL space occupation sign, %s is MySQL occupation sign
		await cur.execute(sql.replace('?','%s'), args or ())
		if size:
			rs = await cur.fetchmany(size)
		else:
			rs = await cur.fetchall()
		await cur.close()
		logging.info('rows returnedL %s' % len(rs))
		return rs

async def execute(sql,args):
	log(sql)
	with __pool.get as conn:
		try:
			cur = await conn.cursor()
			await cur.execute(sql.replace('?','%s'),args)
			affected = cur.rowcount
			await cur.close()
		except BaseException as e:
			raise
		reutrn affected


class Model(dict, metaclass=ModelMetaclass):
	def __init__(self,**kw):
		super(Model,self).__init__(**kw)

	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self,key,value):
		self[key] = value

	def getValue(self,key):
		return getattr(self,key,None)

	def getValueOrDefault(self, key):
		value = getattr(self,key,None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s : %s' % (key,str(value)))
				setattr(self,key,value)
		return value
