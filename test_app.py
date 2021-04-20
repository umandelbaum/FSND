import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import Hero, Team, db, app


class HeroDBTestCase(unittest.TestCase):

    def setUp(self):
        ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
        CONTRIB_TOKEN = os.environ.get('CONTRIB_TOKEN')
        ADMIN_JWT = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token ' + ADMIN_TOKEN
        }
        CONTRIB_JWT = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token ' + CONTRIB_JWT
        }
        PUBLIC_JWT = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token fail'
        }

    def tearDown(self):
        pass







 def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        all_categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            str(category.id): category.type 
            for category in all_categories
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertDictEqual(data['categories'], formatted_categories)
    
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        all_categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            str(category.id): category.type 
            for category in all_categories
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertDictEqual(data['categories'], formatted_categories)
        self.assertLessEqual(len(data['questions']),10)
        self.assertIsNone(data['current_category'])
        self.assertGreater(data['total_questions'], 0)
    
    def test_404_for_failed_retrieve_questions(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertIsNone(question)
    
    def test_422_for_failed_delete_question(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_questions(self):
        searchTerm = {'searchTerm': 'title'}
        res = self.client().post('/questions', json=searchTerm)
        data = json.loads(res.data)


        matches = Question.query.filter(Question.question.ilike('%title%')).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']),10)
        self.assertIsNone(data['current_category'])
        self.assertEqual(data['total_questions'], len(matches))
    
    def test_404_for_bad_page_on_search_questions(self):
        searchTerm = {'searchTerm': 'title'}
        res = self.client().post('/questions?page=5000', json=searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        new_question = {
            'question': 'Hello',
            'answer': 'Hi ya',
            'category': '1',
            'difficulty': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        get_question = Question.query.filter(Question.answer == 'Hi ya')\
            .one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(new_question['question'], get_question.question)
        self.assertEqual(new_question['answer'], get_question.answer)
        self.assertEqual(int(new_question['category']), get_question.category)
        self.assertEqual(new_question['difficulty'], get_question.difficulty)
    
    def test_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        selected_category = Category.query.filter(Category.id == 1)\
            .one_or_none()
        
        selected_questions = Question.query.filter(
            Question.category == '1').all()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], selected_category.type)
        self.assertEqual(data['total_questions'],len(selected_questions))
    
    def test_404_for_bad_page_on_questions_by_category(self):
        res = self.client().get('/categories/1/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_quizzes_with_no_previous_questions(self):
        quiz_input ={
            'quiz_category': {'id': 0},
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=quiz_input)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
    
    def test_quizzes_full_previous_questions(self):
        quiz_input ={
            'quiz_category': {'id': 6},
            'previous_questions': [10, 11]
        }

        res = self.client().post('/quizzes', json=quiz_input)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()