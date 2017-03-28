from flask_restful import Resource
from flask import request, make_response
from database import Database
from cryptography.fernet import Fernet

class SignUp(Resource):
    # 회원가입
    db = Database()

    def post(self):
        connect_sns = request.form['connect_sns']
        if connect_sns == 'True' or connect_sns == 'true':
            # sns 연결 시
            uuid = request.form['uuid']

            rows = self.db.execute("SELECT * FROM account WHERE uuid='", uuid, "'")
            if rows:
                # uuid 중복 시
                return '', 409
            else:
                # 가입되어 있지 않을 때
                self.db.execute("INSERT INTO account(uuid, connected_sns) VALUES('", uuid, "', true)")
                return '', 201

        else:
            # sns 미연결 시
            uuid = request.form['uuid']
            id = request.form['id']
            password = request.form['password']

            rows = self.db.execute("SELECT * FROM account WHERE uuid='", uuid, "'")
            if rows:
                # uuid 중복 시
                return '', 409
            else:
                # uuid 미중복 시
                rows = self.db.execute("SELECT * FROM account WHERE id='", id, "'")
                if rows:
                    # id 중복 시
                    return '', 409
                else:
                    # id 미중복 시
                    if len(password) >= 8:
                        self.db.execute("INSERT INTO account(uuid, connected_sns, id, password) VALUES('",
                                        uuid, "', ", connect_sns, ", '", id, "', '", password, "')")
                        return '', 201
                    else:
                        # 비밀번호 길이가 8자리 미만
                        return '', 409


class SignIn(Resource):
    # 로그인
    pass