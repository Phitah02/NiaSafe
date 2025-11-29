import pytest
from ..app import app, model, tokenizer
import unittest
from unittest.mock import patch, Mock

def test_model_loads():
    """Test that the model and tokenizer load correctly from models/"""
    assert model is not None, "Model should be loaded from models/"
    assert tokenizer is not None, "Tokenizer should be loaded from models/"

def test_predict_valid_input():
    """Test /predict endpoint with valid JSON input"""
    with app.test_client() as client:
        response = client.post('/predict', json={'text': 'This is a test message'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'text' in data
        assert 'predictions' in data
        assert isinstance(data['predictions'], dict)
        expected_keys = {'toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'}
        assert set(data['predictions'].keys()) == expected_keys
        for prob in data['predictions'].values():
            assert isinstance(prob, float)
            assert 0 <= prob <= 1

def test_predict_missing_text():
    """Test /predict endpoint with missing 'text' key"""
    with app.test_client() as client:
        response = client.post('/predict', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing text field' in data['error']

def test_predict_no_json():
    """Test /predict endpoint with no JSON body"""
    with app.test_client() as client:
        response = client.post('/predict')
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

def test_predict_non_string_text():
    """Test /predict endpoint with non-string 'text' input"""
    with app.test_client() as client:
        response = client.post('/predict', json={'text': 123})
        # Assuming the app handles non-string gracefully by returning error
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

def test_predict_empty_text():
    """Test /predict endpoint with empty string"""
    with app.test_client() as client:
        response = client.post('/predict', json={'text': ''})
        assert response.status_code == 200
        data = response.get_json()
        assert 'text' in data
        assert 'predictions' in data
        assert isinstance(data['predictions'], dict)


class TestDatabaseAndAlerts(unittest.TestCase):

    @patch('database.helpers.collection')
    def test_save_flagged_comment(self, mock_collection):
        mock_insert = Mock()
        mock_insert.inserted_id = 'test_id'
        mock_collection.insert_one.return_value = mock_insert

        from database.helpers import save_flagged_comment
        result = save_flagged_comment('test text', {'toxic': 0.5}, 'toxic')

        self.assertEqual(result, 'test_id')
        mock_collection.insert_one.assert_called_once()
        args = mock_collection.insert_one.call_args[0][0]
        self.assertEqual(args['comment_text'], 'test text')
        self.assertEqual(args['severity_scores'], {'toxic': 0.5})
        self.assertEqual(args['predicted_category'], 'toxic')
        self.assertIn('timestamp', args)
        self.assertFalse(args['alert_triggered'])

    @patch('database.helpers.collection')
    def test_get_recent_comments(self, mock_collection):
        mock_collection.find.return_value.sort.return_value.limit.return_value = [{'comment': 'test1'}, {'comment': 'test2'}]

        from database.helpers import get_recent_comments
        result = get_recent_comments(10)

        self.assertEqual(result, [{'comment': 'test1'}, {'comment': 'test2'}])
        mock_collection.find.assert_called_once()
        mock_collection.find.return_value.sort.assert_called_once_with('timestamp', -1)
        mock_collection.find.return_value.sort.return_value.limit.assert_called_once_with(10)

    @patch('database.helpers.collection')
    def test_get_comments_by_category(self, mock_collection):
        mock_collection.find.return_value = [{'category': 'toxic'}]

        from database.helpers import get_comments_by_category
        result = get_comments_by_category('toxic')

        self.assertEqual(result, [{'category': 'toxic'}])
        mock_collection.find.assert_called_once_with({'predicted_category': 'toxic'})

    @patch('backend.alerts.collection')
    @patch('backend.alerts.send_alert')
    def test_check_and_trigger_alert_triggered(self, mock_send, mock_collection):
        scores = {'threat': 0.9, 'severe_toxic': 0.8}

        from backend.alerts import check_and_trigger_alert
        result = check_and_trigger_alert('test_id', scores)

        self.assertTrue(result)
        mock_collection.update_one.assert_called_once_with({'_id': 'test_id'}, {'$set': {'alert_triggered': True}})
        mock_send.assert_called_once_with('Alert: High severity comment detected', 'multiple')

    @patch('backend.alerts.collection')
    @patch('backend.alerts.send_alert')
    def test_check_and_trigger_alert_not_triggered(self, mock_send, mock_collection):
        scores = {'threat': 0.5}

        from backend.alerts import check_and_trigger_alert
        result = check_and_trigger_alert('test_id', scores)

        self.assertFalse(result)
        mock_collection.update_one.assert_not_called()
        mock_send.assert_not_called()

    @patch('backend.app.check_and_trigger_alert')
    @patch('backend.app.save_flagged_comment')
    @patch('backend.app.predict_toxicity')
    def test_predict_route_with_alert(self, mock_predict, mock_save, mock_check):
        mock_predict.return_value = {'toxic': 0.5, 'threat': 0.9}
        mock_save.return_value = 'test_id'
        mock_check.return_value = True

        with app.test_client() as client:
            response = client.post('/predict', json={'text': 'test text'})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('alert_triggered', data)
            self.assertTrue(data['alert_triggered'])
            self.assertEqual(data['text'], 'test text')
            self.assertIn('predictions', data)