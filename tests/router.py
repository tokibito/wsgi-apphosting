#coding:utf-8
from unittest import TestCase

from apphosting.router import DomainRouter, UserDomainRouter

DOMAIN = 'example.com'

__all__ = ('RouterTestCase',)

class RouterTestCase(TestCase):
    def test_domain_router(self):
        router = DomainRouter(DOMAIN)
        app_name = router.get_route({'HTTP_HOST': 'simpleapp.example.com'})
        self.assertEqual(app_name, 'simpleapp')
        app_name2 = router.get_route({'HTTP_HOST': 'simpleapp2.example.com:8080'})
        self.assertEqual(app_name2, 'simpleapp2')

    def test_user_domain_router(self):
        router = UserDomainRouter(DOMAIN)
        app_name = router.get_route({'HTTP_HOST': 'simpleapp.user1.example.com'})
        self.assertEqual(app_name, 'user1.simpleapp')
        app_name2 = router.get_route({'HTTP_HOST': 'simpleapp2.user2.example.com:8080'})
        self.assertEqual(app_name2, 'user2.simpleapp2')
