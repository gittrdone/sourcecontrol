grammar SourceControl;

options {
  language=Python2;
}

command: find | get | count;

find: 'find' query;
get: 'get' getList 'from' query;
count: 'count' (getList 'from')? query;

query: dataType ('where' condList)?;

dataType: 'users' | 'branches' | 'commits' | 'files';
cond: attrName comparator value;
condList: cond (',' cond)*;
getList: attrName (',' attrName)*;
value: INT | STRING | vlist;
attrName: ATTR_NAME;
valueName: STRING;
vlist: '[' value (',' value)* ']';
comparator: '>' | '<' | '=' | '!=' | 'in' | 'not in' | 'contains';

INT: [0-9]+;
STRING: '"' [ _\-a-zA-Z0-9]+ '"';
ATTR_NAME: [_a-zA-Z0-9]+;
WS: [ \r\t\n]+ -> skip;

