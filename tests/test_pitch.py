import unittest
from app.models import Pitch
from app import db

class UserModelTest(unittest.TestCase):

    def setUp(self):
        '''
        method to run before every test
        '''
