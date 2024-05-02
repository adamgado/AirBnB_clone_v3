#!/usr/bin/python3
"""Create a new view for State objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/', methods=['GET'])
def list_s():
    """Retrieves the list of all States"""
    states_list = [a.to_dict() for a in storage.all("State").values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def retrieve_s(s_id):
    """Retrieves a State"""
    states_list = storage.all("State").values()
    state = [a.to_dict() for a in states_list if a.id == s_id]
    if state == []:
        abort(404)
    return jsonify(state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_s(s_id):
    """Deletes a State"""
    states_list = storage.all("State").values()
    state = [a.to_dict() for a in states_list if a.id == s_id]
    if state == []:
        abort(404)
    state.remove(state[0])
    for a in states_list:
        if a.id == s_id:
            storage.delete(a)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def create_s():
    """Creates a State"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_s = State(name=request.json['name'])
    storage.new(new_s)
    storage.save()
    states.append(new_s.to_dict())
    return make_response(jsonify(states[0]), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_s(s_id):
    """Updates a State object"""
    states_list = storage.all("State").values()
    state = [a.to_dict() for a in states_list if a.id == s_id]
    if state == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state[0]['name'] = request.json['name']
    for a in states_list:
        if a.id == s_id:
            a.name = request.json['name']
    storage.save()
    return make_response(jsonify(state[0]), 200)
