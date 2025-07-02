import unittest
import json
from backend.app import app, db, FeatureFlag

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # Create a sample feature flag for testing
        with app.app_context():
            sample_feature = FeatureFlag(name='sample_feature', description='Sample Feature', is_active=True)
            db.session.add(sample_feature)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_features(self):
        response = self.app.get('/features')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'sample_feature')

    def test_get_feature_by_name(self):
        response = self.app.get('/features/sample_feature')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'sample_feature')

    def test_create_feature(self):
        new_feature = {
            'name': 'new_feature',
            'description': 'New Feature Description',
            'is_active': False
        }
        response = self.app.post('/features', json=new_feature)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'new_feature')

    def test_update_feature(self):
        updated_feature = {
            'description': 'Updated Description',
            'is_active': True
        }
        response = self.app.put('/features/sample_feature', json=updated_feature)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['description'], 'Updated Description')
        self.assertTrue(data['is_active'])

    def test_delete_feature(self):
        response = self.app.delete('/features/sample_feature')
        self.assertEqual(response.status_code, 200)

        # Check if the feature is actually deleted
        response = self.app.get('/features/sample_feature')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
