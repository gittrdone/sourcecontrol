from antlr4 import *
from sourceControlApp.querying.SourceControlParser import SourceControlParser
from sourceControlApp.querying.SourceControlLexer import SourceControlLexer

from sourceControlApp.models import Commit, CodeAuthor

def get_tree(string):
  input = InputStream.InputStream(string)
  lexer = SourceControlLexer(input)
  tokens = CommonTokenStream(lexer)
  parser = SourceControlParser(tokens)

  return parser.command()

def process_string(str, repo):
  tree = get_tree(str)
  child = tree.children[0]

  if isinstance(child, SourceControlParser.FindContext):
    ret = process_find(child, repo)
  elif isinstance(child, SourceControlParser.GetContext):
    ret = process_get(child, repo)
  elif isinstance(child, SourceControlParser.CountContext): 
    ret = process_count(child, repo)
  else:
    ret = "error!"

  return ret

def filter_on_query(q, repo):
  obj_type = q.dataType().getText()
  
  cond_list = q.condList()
  conds = []

  if cond_list is not None:
    for cond in cond_list.children:
      # Skip non-conditions
      if not isinstance(cond, SourceControlParser.CondContext):
          continue

      attr = cond.attrName().getText()
      comparator = cond.comparator().getText()

      if attr == 'branch_name':
          set_branch = True

      attr += {
          '=': '',
          '!=': '???',
          '>': '__gt',
          '<': '__lt',
          'in': '__in',
          'contains': '__icontains' # Case insensitive
      }[comparator]

      conds.append({attr: cond.value().getText()})

  if obj_type == "users":
    db_model = CodeAuthor
  elif obj_type == "commits":
    db_model = Commit
  elif obj_type == "branches":
    db_model = Commit
  else:
    return "error"

  # XXX change to kwargs for different repo column names
  objs = db_model.objects.filter(git_branch=repo.git_repo.branches.all()[0])

  for cond in conds:
    objs = objs.filter(**cond)

  return objs
  

def process_find(find, repo):
  q = find.query()
  
  if q is None:
    return

  users = filter_on_query(q, repo)
  return users

def process_get(get, repo):
  q = get.query()

  if q is None:
    return

def process_count(count, repo):
  q = count.query()

  if q is None:
    return
  
