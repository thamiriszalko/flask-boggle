from unittest import TestCase
from app import app


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_start(self):
        with self.client as client:
            resp = client.get('/start')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form method="POST" action="">', html)
            self.assertIn('<div id="max-score">', html)
            self.assertIn('<div id="message"></div>', html)
            self.assertIn('<div id="score"></div>', html)

    def test_check_if_word_is_ok(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["A", "B", "C", "D", "E"],
                    ["B", "E", "E", "R", "D"],
                    ["I", "N", "H", "I", "T"],
                    ["G", "A", "O", "K", "Y"],
                    ["F", "A", "B", "E", "O"]
                ]
            response = client.post('/check-word', json={'word': 'bee'})
            self.assertEqual(response.json['result'], 'ok')

    def test_check_if_word_is_not_on_board(self):
        with app.test_client() as client:
            with self.client as sess:
                sess['board'] = [
                    ["A", "B", "C", "D", "E"],
                    ["B", "E", "E", "R", "D"],
                    ["I", "N", "H", "I", "T"],
                    ["G", "A", "O", "K", "Y"],
                    ["F", "A", "B", "E", "O"]
                ]
            response = client.post('/check-word', json={'word': 'cute'})
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_if_check_word_return_correct_values(self):
        with self.client as client:
            response = client.post('/check-word', json={'word': 'in'})
            actual = response.json
            expected = {
                "result": "ok",
                "word": "in",
            }
            self.assertEqual(expected, actual)

    def test_handle_score(self):
        with self.client as client:
            response = client.post(
                '/handle-score',
                json={'result': 'ok', 'word': 'bee'}
            )
            actual = response.json
            expected = {
                'score': 3,
                'word': 'bee',
                'guessed_words': ['bee'],
            }
            self.assertEqual(expected, actual)

    def test_handle_score_score(self):
        with self.client as client:
            response = client.post(
                '/handle-score',
                json={'result': 'not-word', 'word': 'hhh'}
            )
            actual = response.json
            expected = {
                'score': 0,
                'word': 'hhh',
                'guessed_words': [],
            }
            self.assertEqual(expected, actual)
