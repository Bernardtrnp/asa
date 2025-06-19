from flask import jsonify, request, make_response
from ..databases import TestimoniDatabase
from ..utils import generate_etag


class StoreProfileController:
    @staticmethod
    async def store_profile():
        if not (testimoni_data := await TestimoniDatabase.get("all_testimoni")):
            return jsonify({"message": "testimoni not found"}), 404
        total_rating = sum([testimoni.rating for testimoni in testimoni_data])
        rata_rata = total_rating / len(testimoni_data)
        current_data = {
            "rata_rata": round(rata_rata, ndigits=2),
            "total_rating": total_rating,
            "total_testimoni": len(testimoni_data),
        }
        etag = generate_etag(current_data)
        client_etag = request.headers.get("If-None-Match")
        if client_etag == etag:
            return make_response("", 304)

        response_data = {
            "data": current_data,
            "message": "success get current user",
        }

        response = make_response(jsonify(response_data), 200)
        response.headers["Content-Type"] = "application/json"
        response.headers["ETag"] = etag
        return response
