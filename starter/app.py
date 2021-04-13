import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Hero, Team
from auth import AuthError, requires_auth

ITEMS_PER_PAGE = 10


def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    '''All Routes'''

    '''
    Public 'get' route for heroes
    Returns paginated list of heroes and number of total heroes
    Returns 404 if no heroes are in the database at the given page
    '''
    @app.route('/heroes', methods=['GET'])
    def retrieve_heroes():
        all_heroes = Hero.query.order_by(Hero.id).all()
        current_heroes = paginate_items(request, all_heroes)
        if len(current_heroes) == 0:
            abort(404)
        return jsonify({
          'success': True,
          'heroes': current_heroes,
          'total_heroes': len(all_heroes)
        }), 200

    '''
    Public 'get' route for a particular hero
    Returns a particular hero's information
    Returns 404 if no hero exists with the given id
    '''
    @app.route('/heroes/<int:hero_id>', methods=['GET'])
    def retrieve_hero(hero_id):
        hero = Hero.query.filter(Hero.id == hero_id).one_or_none()
        if hero is None:
            abort(404)
        return jsonify({
            'success': True,
            'hero': hero.format()
        }), 200

    '''
    Post route to add a hero
    Returns the hero's information with id
    ''''
    @app.route('/heroes', methods=['POST'])
    @requires_auth('post:info')
    def create_hero(jwt):
        body = request.get_json()
        try:
            new_name = body['name']
            new_identity = body['secret_identity']
            new_home = body['hometown']
            new_power = int(body['power_level'])
            new_hero = Hero(name=new_name,
                            secret_identity=new_identity,
                            hometown=new_home,
                            power_level=new_power)
            new_hero.insert()
            return jsonify({
                'success': True,
                'hero': new_hero.format()
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    '''
    Patch route to update hero information
    Returns the updated hero's information
    '''
    @app.route('/heroes/<int:hero_id>', methods=['PATCH'])
    @requires_auth('patch:info')
    def update_hero(jwt, hero_id):
        body = request.get_json()
        to_update = Hero.query.filter(Hero.id == hero_id).one_or_none()
        if to_update is None:
            abort(404)
        try:
            if 'name' in body:
                to_update.name = body['name']
            if 'secret_identity' in body:
                to_update.secret_identity = body['secret_identity']
            if 'hometown' in body:
                to_update.hometown = body['hometown']
            if 'power_level' in body:
                to_update.power_level = int(bpdy['power_level'])
            to_update.update()
            return jsonify({
                'success': True,
                'hero': to_update.format()
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    '''
    Delete route for a hero
    Returns status code of 200 and hero ID if hero was deleted
    '''
    @app.route('/heroes/<int:hero_id>', methods=['DELETE'])
    @requires_auth('delete:info')
    def delete_hero(jwt, hero_id):
        to_delete = Hero.query.filter(Hero.id == hero_id).one_or_none()
        if to_delete is None:
            abort(404)
        to_delete.delete()
        return jsonify({
            'success': True,
            'delete': hero_id
        }), 200

    '''
    Route to add hero to team
    Returns updated hero info with added membership
    '''
    @app.route('/heroes/<int:hero_id>', methods=['POST'])
    @requires_auth('post:info')
    def add_membership(jwt, hero_id):
        body = request.get_json()
        to_update = Hero.query.filter(Hero.id == hero_id).one_or_none()
        if to_update is None:
            abort(404)
        team_id = int(body['team_id'])
        new_team = Team.query.filter(Team.id == new_team).one_or_none()
        if new_team is None:
            abort(404)
        to_update.teams.append(new_team)
        to_update.update()
        return jsonify({
            'success': True,
            'hero': to_update.format()
        }), 200

    '''
    Public 'get' route for teams
    Returns paginated list of teams and number of total teams
    Returns 404 if no teams are in the database at the given page
    '''
    @app.route('/teams', methods=['GET'])
    def retrieve_teams():
        all_teams = Team.query.order_by(Team.id).all()
        current_teams = paginate_items(request, all_teams)
        if len(current_teams) == 0:
            abort(404)
        return jsonify({
          'success': True,
          'teams': current_heroes,
          'total_teams': len(all_teams)
        }), 200

    '''
    Public 'get' route for a particular team
    Returns a particular team's information
    Returns 404 if no team exists with the given id
    '''
    @app.route('/teams/<int:team_id>', methods=['GET'])
    def retrieve_team(team_id):
        team = Team.query.filter(Team.id == team_id).one_or_none()
        if team is None:
            abort(404)
        return jsonify({
            'success': True,
            'team': team.format()
        }), 200
    '''
    Post route to add a team
    Returns the team's information with id
    ''''
    @app.route('/teams', methods=['POST'])
    @requires_auth('post:info')
    def create_team(jwt):
        body = request.get_json()
        try:
            new_name = body['name']
            new_home = body['location']
            new_team = Team(name=new_name,
                            location=new_home)
            new_team.insert()
            return jsonify({
                'success': True,
                'team': new_team.format()
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    Patch route to update team information
    Returns the updated team's information
    '''
    @app.route('/teams/<int:team_id>', methods=['PATCH'])
    @requires_auth('patch:info')
    def update_team(jwt, team_id):
        body = request.get_json()
        to_update = Team.query.filter(Team.id == team_id).one_or_none()
        if to_update is None:
            abort(404)
        try:
            if 'name' in body:
                to_update.name = body['name']
            if 'location' in body:
                to_update.location = body['location']
            to_update.update()
            return jsonify({
                'success': True,
                'team': to_update.format()
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    '''
    Delete route for a team
    Returns status code of 200 and team ID if team was deleted
    '''
    @app.route('/teams/<int:team_id>', methods=['DELETE'])
    @requires_auth('delete:info')
    def delete_team(jwt, team_id):
        to_delete = Team.query.filter(Team.id == team_id).one_or_none()
        if to_delete is None:
            abort(404)
        to_delete.delete()
        return jsonify({
            'success': True,
            'delete': team_id
        }), 200


return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
