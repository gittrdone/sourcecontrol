from django.test import TestCase
from sourceControlApp.models import GitRepo

import repo_mgmt


# Tests the GitRepo model
class GitRepoTest(TestCase):
    def setUp(self):
        GitRepo.objects.create(git_repository_url="test", status=100)

    def test_dummy(self):
        dummy_object = GitRepo.objects.get(status=100)
        self.assertEqual(dummy_object.git_repository_url, "test")


class RepoMgmtTest(TestCase):
    def test_canonicalizeurl(self):
        url1 = "https://github.com/gittrdone/sourcecontrol/"
        url2 = "https://github.com/gittrdone/sourcecontrol.git/"
        url3 = "https://github.com/gittrdone/sourcecontrol.git"
        url4 = "http://github.com/gittrdone/sourcecontrol.git"

        canonicalized_url = "http://github.com/gittrdone/sourcecontrol"

        self.assertEqual(canonicalized_url, repo_mgmt.canonicalize_repo_url(url1))
        self.assertEqual(canonicalized_url, repo_mgmt.canonicalize_repo_url(url2))
        self.assertEqual(canonicalized_url, repo_mgmt.canonicalize_repo_url(url3))
        self.assertEqual(canonicalized_url, repo_mgmt.canonicalize_repo_url(url4))

    # def test_isvalidurl(self):
    #     # XXX We should use mocks for this test
    #     url = "https://google.com/code"
    #
    #     self.assertFalse(repo_mgmt.is_valid_repo(url))
    #
    #     self.assertTrue(repo_mgmt.is_valid_repo("http://github.com/gittrdone/sourcecontrol"))

    def test_getrepodatafailoninvalidurl(self):
        self.assertEqual(-1, repo_mgmt.get_repo_data_from_url("bad data!", "Test", "Test", "Test"))

    # def test_getrepodata(self):
    #     # XXX We should be using mocks!!
    #     repo = repo_mgmt.get_repo_data_from_url("http://github.com/gittrdone/sourcecontrol.git", "Repo", "Desc", None)
    #     self.assertEqual("Repo", repo.name)
    #     self.assertEqual("Desc", repo.repo_description)
    #     self.assertEqual("http://github.com/gittrdone/sourcecontrol", repo.git_repo.git_repository_url)
    #
    #     new_repo = repo_mgmt.get_repo_data_from_url("http://github.com/gittrdone/sourcecontrol", "Repo", "Desc", None)
    #     self.assertNotEqual(repo, new_repo)
    #     self.assertEqual(repo.git_repo, new_repo.git_repo)
