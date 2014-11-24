grammar SourceControl;

options {
  language=Python2;
}

command: find | get | count;

find: 'find' SPACE query;
get: 'get' SPACE getList SPACE 'from' SPACE query;
count: 'count' SPACE (getList SPACE 'from' SPACE)? query;

query: dataType (SPACE 'where' SPACE condList)?;

dataType: 'users' | 'branches' | 'commits' | 'files';
cond: attrName SPACE? comparator SPACE? value;
condList: cond (',' SPACE? cond)*;
getList: valueName (',' SPACE? valueName)*;
value: INT | STRING | vlist;
attrName: ATTR_NAME;
valueName: STRING;
vlist: '[' value (',' SPACE? value)* ']';
comparator: '>' | '<' | '=' | '!=' | 'in' | 'not in' | 'contains';

INT: [0-9]+;
STRING: '"' [ _a-zA-Z0-9]+ '"';
ATTR_NAME: [_a-zA-Z0-9]+;
SPACE: ' '+;
