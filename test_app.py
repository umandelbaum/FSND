import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import Hero, Team
from app import app

ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
CONTRIB_TOKEN = os.environ.get('CONTRIB_TOKEN')
ADMIN_JWT = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ADMIN_TOKEN
}
CONTRIB_JWT = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + CONTRIB_TOKEN
}
PUBLIC_JWT = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BAD_TOKEN'
}


class HeroDBTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client

    def tearDown(self):
        pass

    '''TESTS OF PUBLIC ENDPOINTS'''

    '''Test the public /heroes route'''
    def test_retrieve_heroes(self):
        res = self.client().get('/heroes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''Test a failure of the public /heroes route'''
    def test_404_for_failed_retrieve_heroes(self):
        res = self.client().get('/heroes?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''Test the public /heroes/{id} route'''
    def test_retrieve_hero_by_id(self):
        res = self.client().get('/heroes/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''Test a failure of the public /heroes{id} route'''
    def test_404_for_failed_retrieve_hero_by_id(self):
        res = self.client().get('/heroes/32767')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''Test the public /teams route'''
    def test_retrieve_teams(self):
        res = self.client().get('/teams')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''Test a failure of the public /teams route'''
    def test_404_for_failed_retrieve_teams(self):
        res = self.client().get('/teams?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''Test the public /teams/{id} route'''
    def test_retrieve_team_by_id(self):
        res = self.client().get('/teams/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''Test a failure of the public /teams{id} route'''
    def test_404_for_failed_retrieve_team_by_id(self):
        res = self.client().get('/teams/32767')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''UNAUTHORIZED PUBLIC ACCESS TESTS'''

    '''Test an attempt to POST to heros from the public'''
    def test_401_for_failed_public_post_to_heroes(self):
        new_hero = {
                   "name": "The Founder",
                   "secret_identity": "Rafael Rivera",
                   "hometown": "Las Vegas",
                   "power_level": "7"
                    }
        res = self.client().post('/heroes',
                                 headers=PUBLIC_JWT,
                                 json=new_hero
                                 )
        self.assertEqual(res.status_code, 401)

    '''Test an attempt to PATCH a hero from the public'''
    def test_401_for_failed_public_patch_to_hero_by_id(self):
        update = {"power_level": "2"}
        res = self.client().patch('/heroes/1',
                                  headers=PUBLIC_JWT,
                                  json=update
                                  )
        self.assertEqual(res.status_code, 401)

    '''Test an attempt to POST to teams from the public'''
    def test_401_for_failed_public_post_to_teams(self):
        new_team = {
                   "name": "Vegas Buds",
                   "location": "Las Vegas"
                    }
        res = self.client().post('/teams',
                                 headers=PUBLIC_JWT,
                                 json=new_team
                                 )
        self.assertEqual(res.status_code, 401)

    '''Test an attempt to PATCH a team from the public'''
    def test_401_for_failed_public_patch_to_team_by_id(self):
        update = {"name": "Vegas Not Friends"}
        res = self.client().patch('/teams/1',
                                  headers=PUBLIC_JWT,
                                  json=update
                                  )
        self.assertEqual(res.status_code, 401)

    '''CONTRIBUTOR ROLE TESTS'''

    '''Test an attempt to POST to heros from a contributor'''
    def test_post_new_hero(self):
        new_hero = {
                   "name": "The Founder",
                   "secret_identity": "Rafael Rivera",
                   "hometown": "Las Vegas",
                   "power_level": "7"
                    }
        res = self.client().post('/heroes',
                                 headers=CONTRIB_JWT,
                                 json=new_hero
                                 )
        data = json.loads(res.data)
        get_hero = Hero.query.filter(Hero.name == 'The Founder').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(new_hero['name'], get_hero.name)
        self.assertEqual(new_hero['secret_identity'], get_hero.secret_identity)
        self.assertEqual(new_hero['hometown'], get_hero.hometown)
        self.assertEqual(int(new_hero['power_level']), get_hero.power_level)

    '''Test an attempt to PATCH a hero from a contributor'''
    def test_patch_to_hero_by_id(self):
        update = {"power_level": "2"}
        res = self.client().patch('/heroes/1',
                                  headers=CONTRIB_JWT,
                                  json=update
                                  )
        data = json.loads(res.data)

        get_hero = Hero.query.filter(Hero.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(update['power_level']), get_hero.power_level)

    '''Test an attempt to POST to teams from a contributor'''
    def test_post_new_teams(self):
        new_team = {
                   "name": "Vegas Buds",
                   "location": "Las Vegas"
                    }
        res = self.client().post('/teams',
                                 headers=CONTRIB_JWT,
                                 json=new_team
                                 )
        data = json.loads(res.data)
        get_team = Team.query.filter(Team.name == 'Vegas Buds').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(new_team['name'], get_team.name)
        self.assertEqual(new_team['location'], get_team.location)

    '''Test an attempt to PATCH a team from a contributor'''
    def test_patch_team_by_id(self):
        update = {"name": "West Coast Avengers"}
        res = self.client().patch('/teams/1',
                                  headers=CONTRIB_JWT,
                                  json=update
                                  )
        data = json.loads(res.data)
        get_team = Team.query.filter(Team.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(update['name'], get_team.name)

    '''Test adding a hero to a team'''
    def test_add_hero_to_team(self):
        new_team = {"team_id": "1"}
        res = self.client().post('/heroes/1',
                                 headers=CONTRIB_JWT,
                                 json=new_team
                                 )
        data = json.loads(res.data)

        get_hero = Hero.query.filter(Hero.id == 1).one_or_none().format()
        get_team = Team.query.filter(Team.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(get_team.name in get_hero['team_memberships'])

    '''ADMIN ROLE TESTS'''

    '''Test an attempt to delete a hero from an admin'''
    def test_delete_hero(self):
        res = self.client().delete('/heroes/2', headers=ADMIN_JWT)
        data = json.loads(res.data)

        hero = Hero.query.filter(Hero.id == 2).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertIsNone(hero)

    '''Test 404 for attempt to delete hero not in database'''
    def test_404_for_failed_delete_hero(self):
        res = self.client().delete('/heroes/100', headers=ADMIN_JWT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''Test an attempt to delete a team from an admin'''
    def test_delete_team(self):
        res = self.client().delete('/teams/2', headers=ADMIN_JWT)
        data = json.loads(res.data)

        team = Team.query.filter(Team.id == 2).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertIsNone(team)

    '''Test 404 for attempt to delete team not in database'''
    def test_404_for_failed_delete_team(self):
        res = self.client().delete('/teams/100', headers=ADMIN_JWT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
