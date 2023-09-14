# from hashlib import md5
import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView
# from sqlalchemy.exc import IntegrityError
import schema
from models import Ad, Session

my_app = flask.Flask('Ads service')


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


@my_app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"status": "Error", "description": er.message})
    response.status_code = er.status_code
    return response


def get_ad(session, ad_id):
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, f"Ad #{ad_id} not found.")
    return ad


class AdView(MethodView):
    def get(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            return jsonify(
                {
                    "id": ad.id,
                    "header": ad.header,
                    "text": ad.text,
                    "creation_time": ad.creation_time.isoformat(),
                }
            )

    def post(self):
        validated_json = validate(schema.CreateAd, request.json)
        with Session() as session:
            ad = Ad(**validated_json)
            session.add(ad)
            session.commit()
            return jsonify({"id": ad.id})

    def patch(self, ad_id):
        validated_json = validate(schema.UpdateAd, request.json)
        with Session() as session:
            ad = get_ad(session, ad_id)
            for field, value in validated_json.items():
                setattr(ad, field, value)
            session.add(ad)
            session.commit()
            return jsonify({"id": ad.id})

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return jsonify({"status": "success"})


ad_view = AdView.as_view("ads")
my_app.add_url_rule(
    "/ad/<int:ad_id>", view_func=ad_view, methods=["GET", "PATCH", "DELETE"]
)
my_app.add_url_rule("/ad/", view_func=ad_view, methods=["POST"])

if __name__ == "__main__":
    my_app.run()
