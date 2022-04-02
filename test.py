import kudu
from kudu.client import Partitioning
from datetime import datetime

# 连接到kudu主服务器
client = kudu.connect(host='kudu.master', port=7051)

# 为新表定义架构
builder = kudu.schema_builder()
builder.add_column('key').type(kudu.int64).nullable(False).primary_key()
builder.add_column('ts_val', type_=kudu.unixtime_micros, nullable=False, compression='lz4')
schema = builder.build()

# 定义分区模式
partitioning = Partitioning().add_hash_partitions(column_names=['key'], num_buckets=3)

# 创建新表
client.create_table('python-example', schema, partitioning)

# 打开表
table = client.table('python-example')

# 创建一个新会话用于操作表
session = client.new_session()

# 往表插入数据
op = table.new_insert({'key': 1, 'ts_val': datetime.utcnow()})
session.apply(op)

# 更新插入，即有则更新，无则插入
op = table.new_upsert({'key': 2, 'ts_val': "2016-01-01T00:00:00.000000"})
session.apply(op)

# 更新行
op = table.new_update({'key': 1, 'ts_val': ("2017-01-01", "%Y-%m-%d")})
session.apply(op)

# 删除数据
op = table.new_delete({'key': 2})
session.apply(op)

# 刷新写入操作，如果发生异常，则捕获异常并打印.
try:
    session.flush()
except kudu.KuduBadStatus as e:
    print(session.get_pending_errors())

# 创建一个扫描，并增加一个python-example表的断言
scanner = table.scanner()
scanner.add_predicate(table['ts_val'] == datetime(2017, 1, 1))

# 打开扫描仪并读取所有元组
# 注: 这不适用于大扫描
result = scanner.open().read_all_tuples()
