from unittest import TestCase
from app import app, score_truncate
from flask import session
from boggle import Boggle
import json

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
    
    def test_play(self):
        with app.test_client() as client:
            resp = client.get('/play')
            html = resp.get_data(as_text = True)
            self.assertIn('<table>',html)
            self.assertIn('<h3>Score: <span id="score">0</span></h3>',html)
            self.assertEqual(resp.status_code,200)

    def test_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['t','e','s','t','s'],['t','e','s','t','s'],['t','e','s','t','s'],['t','e','s','t','s'],['t','e','s','t','s']]
            resp = client.post('/guess', json = {'guess':'foo'})
            json = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('not-on-board',json)
    
    def test_score_keeper(self):
        with app.test_client() as client:
            resp = client.post('/game/data',json={"score":'test'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('test',session['games'])
    def test_score_truncate(self):
        self.assertEqual([7,6,5], score_truncate([1,2,3,4,5,6,7],3))
        self.assertEqual([3,2,1], score_truncate([1,2,3],5))


