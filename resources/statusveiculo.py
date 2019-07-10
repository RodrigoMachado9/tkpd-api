from flask_restful import Resource, reqparse
from models.status_veiculo import StatusModel
from flask_jwt_extended import jwt_required
import sqlite3


class Status(Resource):

    def get(self):

        #todo;  retornando uma lista de objetos.
        return {'Status_veiculo':[status.json() for status in StatusModel.query.all()]}

class StatusVeiculo(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('carregado')
    atributos.add_argument('pesocarga')
    atributos.add_argument('veiculo_id', type=int, required=True, help="Every status_veiculo needs to be linked veiculo.")

    def get(self, status_id):
        status = StatusModel.find_status(status_id)
        if status:
            return status.json()
        return {'message': 'status_veiculo not found.'}, 404

    @jwt_required
    def post(self, status_id):
        if StatusModel.find_status(status_id):
            return {"message": "Type status_veiculo id '{}' already exists.".format(status_id)}, 400 #Bad Request

        dados = StatusVeiculo.atributos.parse_args()
        status = StatusModel(**dados)

        try:
            status.save_status()
        except:
            #todo; cnh  =  unique.
            return {"message": "An error ocurred trying to create status_veiculo."}, 500 #Internal Server Error
        return status.json(), 201

    @jwt_required
    def delete(self, status_id):
        status = StatusModel.find_status(status_id)
        if status:
            status.delete_status()
            return {'message': 'Type status_veiculo deleted.'}
        return {'message': 'Type status_veiculo not found.'}, 404