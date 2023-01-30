import sqlparse as sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where
from sqlparse.tokens import Keyword, DML

sql = "select id,name_,age from dual where aa = #{aa};select id,'18;19',age from actor;"
# 1.分割SQL
stmts = sqlparse.split(sql)
for stmt in stmts:
    # 2.format格式化
    print(sqlparse.format(stmt, reindent=True, keyword_case="upper"))
    # 3.解析SQL
    stmt_parsed = sqlparse.parse(stmt)
    print(stmt_parsed[0].tokens)
    for parse in stmt_parsed:
        for token_parse in parse.tokens:
            print(token_parse)
            if isinstance(token_parse, IdentifierList):
                for identifier in token_parse.get_identifiers():
                    identifier.get_name()
            elif isinstance(token_parse, Identifier):
                token_parse.get_name()
            # It's a bug to check for Keyword here, but in the example
            # above some tables names are identified as keywords...
            elif token_parse.ttype is Keyword:
                token_parse.value