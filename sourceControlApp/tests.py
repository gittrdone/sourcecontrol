from django.test import TestCase
from sourceControlApp.models import GitStore

# Create your tests here.
class GitStoreTest(TestCase):
    def setUp(self):
        GitStore.objects.create(gitRepositoryURL="test", numFiles=100)

    def test_dummy(self):
        dummy_object = GitStore.objects.get(numFiles=100)
        self.assertEqual(dummy_object.gitRepositoryURL, "test")
