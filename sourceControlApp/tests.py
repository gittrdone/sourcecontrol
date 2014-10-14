from django.test import TestCase
from sourceControlApp.models import GitStore

import repo_mgmt

# Create your tests here.
class GitStoreTest(TestCase):
    def setUp(self):
        GitStore.objects.create(gitRepositoryURL="test", numFiles=100)

    def test_dummy(self):
        dummy_object = GitStore.objects.get(numFiles=100)
        self.assertEqual(dummy_object.gitRepositoryURL, "test")

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

    def test_isvalidurl(self):
        # Fix this test
        url = "https://google.com/code"

        self.assertFalse(repo_mgmt.is_valid_repo(url))