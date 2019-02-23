import unittest

from _AddPostPage_Test import TestAddPostPage
from _EditMyProfilePage_Test import TestEditMyProfilePage
from _LoginPage_Test import TestLoginPage
from _NotLoggedIn_Test import TestNotLoggedIn
from _RegisterPage_Test import TestRegisterPage
from _RemovePostPage_Test import TestRemovePostPage
from _SearchUsersPage_AND_FeedPage_Test import TestSearchUsersPageAndFeedPage
from _ViewMyPostsPage_Test import TestViewMyPostsPage
from _ViewMyProfilePage_Test import TestViewMyProfilePage

# get all tests
test_addPostPage = unittest.TestLoader().loadTestsFromTestCase(TestAddPostPage)
test_editMyProfilePage = unittest.TestLoader().loadTestsFromTestCase(TestEditMyProfilePage)
test_loginPage = unittest.TestLoader().loadTestsFromTestCase(TestLoginPage)
test_notLoggedIn = unittest.TestLoader().loadTestsFromTestCase(TestNotLoggedIn)
test_registerPage = unittest.TestLoader().loadTestsFromTestCase(TestRegisterPage)
test_removePostPage = unittest.TestLoader().loadTestsFromTestCase(TestRemovePostPage)
test_searchUsersPage_AND_feedPage = unittest.TestLoader().loadTestsFromTestCase(TestSearchUsersPageAndFeedPage)
test_viewMyPostsPage = unittest.TestLoader().loadTestsFromTestCase(TestViewMyPostsPage)
test_viewMyProfilePage = unittest.TestLoader().loadTestsFromTestCase(TestViewMyProfilePage)

# create a test suite
test_suite_mikeBook = unittest.TestSuite([
    test_addPostPage,
    test_editMyProfilePage,
    test_loginPage,
    test_notLoggedIn,
    test_registerPage,
    test_removePostPage,
    test_searchUsersPage_AND_feedPage,
    test_viewMyPostsPage,
    test_viewMyProfilePage])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite_mikeBook)


