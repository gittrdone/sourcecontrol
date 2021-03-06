from antlr4 import *
from sourceControlApp.querying.SourceControlParser import SourceControlParser
from sourceControlApp.querying.SourceControlLexer import SourceControlLexer
import dateutil.parser
import datetime

from sourceControlApp.models import Commit, CodeAuthor, FileEntry, GitBranch


def get_tree(string):
    """
    Returns an ANTLR tree for the given input text
    :param string: A query, in its entirety
    :return: An ANTLR parse tree, rooted with a 'command'
    """
    text = InputStream.InputStream(string)
    lexer = SourceControlLexer(text)
    tokens = CommonTokenStream(lexer)
    parser = SourceControlParser(tokens)

    return parser.command()


def process_string(string, repo):
    """
    Processes the given query, using the given repo
    :param string: Query to run
    :param repo: Repo to run it on
    :return: Result dict containing status and items
    """
    tree = get_tree(string)
    child = tree.children[0]

    if isinstance(child, SourceControlParser.FindContext):
        ret = process_find(child, repo)
    elif isinstance(child, SourceControlParser.GetContext):
        ret = process_get(child, repo)
    elif isinstance(child, SourceControlParser.CountContext):
        ret = process_count(child, repo)
    else:
        ret = {'status': "error"}

    return ret


def filter_on_query(q, repo):
    """
    Returns objects that match a query from the repo.
    :param q: The 'query' part of a Query
    :param repo: Repo to get objects associated
    :return: A set of objects that match the filters
    """
    set_branch = False
    obj_type = q.dataType().getText()
    
    cond_list = q.condList()
    conds = []
    exclude_conds = []

    if cond_list is not None:
        for cond in cond_list.children:
            # Skip non-conditions
            if not isinstance(cond, SourceControlParser.CondContext):
                continue

            attr = cond.attrName().getText()
            comparator = cond.comparator().getText()

            if attr == 'branch_name':
                set_branch = True

            if comparator == '!=':
                conds_ = exclude_conds
                comparator = '='
            elif comparator == 'not in':
                conds_ = exclude_conds
                comparator = 'in'
            else:
                conds_ = conds

            attr += {
                '=': '',
                '>': '__gt',
                '<': '__lt',
                'in': '__in',
                'contains': '__icontains'  # Case insensitive
            }[comparator]

            if attr in ["commit_time"]:
                date = dateutil.parser.parse(cond.value().getText()[1:-1])
                conds_.append({'commit_time__range': (datetime.datetime.combine(date, datetime.time.min),
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

                conds_.append({"commit_time__week_day": weekday_num[cond.value().getText()[1:-1]]})
            else:
                cond_value = cond.value().getText()
                if cond_value[0] == '"':
                    cond_value = cond_value[1:-1]
                conds_.append({attr: cond_value})

    if obj_type == "users":
        db_model = CodeAuthor
    elif obj_type == "commits":
        db_model = Commit
    elif obj_type == "branches":
        db_model = GitBranch
    elif obj_type == "files":
        db_model = FileEntry
    else:
        return "error"

    if db_model == CodeAuthor:
        # XXX change to kwargs for different repo column names
        objs = db_model.objects.filter(git_branch=repo.git_repo.default_branch)
    elif db_model == Commit:
        # TODO Fix this stuff to use branches
        objs = db_model.objects.filter(git_repo=repo.git_repo)
    elif db_model == FileEntry:
        objs = db_model.objects.filter(git_branch=repo.git_repo.default_branch)
    elif db_model == GitBranch:
        objs = repo.git_repo.branches.all()

    for cond in conds:
        objs = objs.filter(**cond)

    for exclude_cond in exclude_conds:
        objs = objs.exclude(**exclude_cond)

    return objs
    

def process_find(find, repo):
    """
    Processes a 'find' query.
    Simply returns the found objects, if successful.
    :param find:
    :param repo:
    :return:
    """
    q = find.query()
    
    if q is None:
        return {"status": "error"}

    objects = filter_on_query(q, repo)
    return {"status": "success", "type": "find", "result": objects}


def process_get(get, repo):
    """
    A get query gets a specific piece of data from whatever
    objects are obtained.
    A list of objects is appended to the end of the results
    :param get:
    :param repo:
    :return:
    """
    q = get.query()

    if q is None:
        return {"status": "error"}

    objects = filter_on_query(q, repo)

    result = []

    gets = get.getList().children

    for obj in objects:
        current = {'object': obj}
        for get in gets:
            if not isinstance(get, SourceControlParser.AttrNameContext):
                continue
            current[get.getText()] = getattr(obj, get.getText())
        result.append(current)

    result.append(objects)
    return {"status": "success", "type": "get", "result": result}


def process_count(count, repo):
    """
    Processes a 'count' query
    The result is simply a count of the objects found
    :param count:
    :param repo:
    :return:
    """
    q = count.query()

    if q is None:
        return {"status": "error"}

    objects = filter_on_query(q, repo)
    return {"status": "success", "type": "count", "result": len(objects) }
    
