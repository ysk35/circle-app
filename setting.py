from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
# postgresqlのDBの設定
DATABASE = "postgres://dkfqwbueaxidfc:f37118ce7a2fcd412122ab2382ee510ebbc0284cf71d58d9a34732ff79449723@ec2-3-229-161-70.compute-1.amazonaws.com:5432/da6uc9gaenvvku"

# Engineの作成
ENGINE = create_engine(
  DATABASE,
  encoding="utf-8",
  # TrueにするとSQLが実行される度に出力される
  echo=True
)

# Sessionの作成
session = scoped_session(
  # ORM実行時の設定。自動コミットするか、自動反映するなど。
  sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE
  )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()