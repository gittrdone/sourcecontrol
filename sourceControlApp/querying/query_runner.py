from antlr4 import *
from sourceControlApp.querying.SourceControlParser import SourceControlParser
from sourceControlApp.querying.SourceControlLexer import SourceControlLexer
import dateutil.parser
import datetime

from sourceControlApp.models import Commit, CodeAuthor, FileEntry

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

      if attr in ["commit_time"]:
        date = dateutil.parser.parse(cond.value().getText()[1:-1])
        conds.append({'commit_time__range': (datetime.datetime.combine(date, datetime.time.min),
                                             datetime.datetime.combine(date, datetime.time.max))})
      elif attr == "commit_day":
        weekday_num = {
          "sunday": 1,
          "monday": 2,
          "tuesday": 3,
          "wednesday": 4,
          "thursday": 5,
          "friday": 6,
          "saturday": 7
        }

        conds.append({"commit_time__week_day": weekday_num[cond.value().getText()[1:-1]]})
      else:
        conds.append({attr: cond.value().getText()})

  if obj_type == "users":
    db_model = CodeAuthor
  elif obj_type == "commits":
    db_model = Commit
  elif obj_type == "branches":
    db_model = Commit
  elif obj_type == "files":
    db_model = FileEntry
  else:
    return "error"

  if db_model == CodeAuthor:
    # XXX change to kwargs for different repo column names
    objs = db_model.objects.filter(git_branch=repo.git_repo.branches.all()[0])
  elif db_model == Commit:
    # TODO Fix this stuff to use branches
    objs = db_model.objects.filter(git_repo=repo.git_repo)
    pass
  elif db_model == FileEntry:
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
  
