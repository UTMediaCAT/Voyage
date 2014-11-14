__author__ = 'ryan'

import os,sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import db_manager as db
import unittest

#testing db collection category
TESTING_DB = "testing"
ID = "_id"
URL = "_url"
ORIGINAL_DIC1 = {ID: 1, URL: "google.ca"}
ORIGINAL_DIC2 = {ID: 2, URL: "cnn.ca"}
ORIGINAL_DIC3 = {ID: 3, URL: "facebook.com"}
ELEMENT_TEST_DIC={"_id": 1, "list": ["I", "just", "checking"]} #since keyword database only have one document  id always 1


class testDBmanager(unittest.TestCase):

    def setUp(self):
        db.connect(TESTING_DB)

    def tearDown(self):
        db.del_all_documents()
        db.close_connection()

    def test_del_document(self):
        """
        testing delete function by deleting one document or delete all documents in the collection
        """
        self.setUp()
        db.add_document(ORIGINAL_DIC1)
        db.add_document(ORIGINAL_DIC2)
        db.add_document(ORIGINAL_DIC3)
        db.del_document(2)
        self.assertEqual(db.get_all_documents(), [ORIGINAL_DIC1, ORIGINAL_DIC3],"have document 1 2 3 in collection. After 2 is delected, should be only have 1 &3 left")
        db.del_all_documents()
        self.assertEqual(db.get_all_documents(), [], "delete all documents in the collection, so collection should be blank")
        self.tearDown()

    def test_add_document(self):
        """
        testing adding documents into collection
        """
        self.setUp()
        db.add_document(ORIGINAL_DIC3)
        db.add_document(ORIGINAL_DIC1)
        self.assertEqual(db.get_documents(ID, 1), [ORIGINAL_DIC1],"adding document 3 & 1 in the collection, should be have document 1 in collection")
        self.tearDown()

    def test_get_document(self):
        """
        testing get document function by getting one document or getting all documents in the collection
        """
        self.setUp()
        db.add_document(ORIGINAL_DIC1)
        db.add_document(ORIGINAL_DIC2)
        db.add_document(ORIGINAL_DIC3)
        self.assertEqual(db.get_documents(ID, 2), [ORIGINAL_DIC2], "asking document 2 in database, should return document 2")
        self.assertEqual(db.get_all_documents(), [ORIGINAL_DIC1, ORIGINAL_DIC2, ORIGINAL_DIC3], "asking return all document. should return a list of dictionary which are all the documents.")
        self.tearDown()


    def test_set_field_value(self):
        self.setUp()
        db.add_document(ORIGINAL_DIC1)
        db.add_document(ORIGINAL_DIC2)
        db.add_document(ORIGINAL_DIC3)
        db.set_field_value(1, URL, "testing.com")
        self.assertEqual(db.get_documents(ID, 1), [{ID: 1, URL: "testing.com"}] , "changed document URL, should be updated in database")
        self.tearDown()

    def test_edit_element(self):
        """
        testing adding/deleting/getting element fucntion in database
        """
        self.setUp()
        db.add_document(ELEMENT_TEST_DIC)
        self.assertEqual(db.get_all_elements(),["I","just","checking"],"getting keywords should get back the keyword list in the collection")
        db.add_element("testing")
        self.assertEqual(db.get_all_elements(),["I","just","checking","testing"],"add new keyword should be able to update into database")
        db.del_element("I")
        self.assertEqual(db.get_all_elements(),["just","checking","testing"], "able to delete existing keyword")
        db.del_all_elements()
        self.assertEqual(db.get_all_elements(),[], "should be erase all keywords")
        db.del_document(2)
        self.tearDown()

if __name__ == '__main__':
    unittest.main()
