import os
from flask import jsonify, request, make_response
from werkzeug.utils import secure_filename
import cloudinary.uploader
from ..databases import TestimoniDatabase
from ..utils import generate_etag
import aiohttp
from nextcord import Webhook, Embed
from ..config import webhook_url, webhook_username
import nextcord


class TestimoniController:
    @staticmethod
    async def get_all_testimoni(limit, per_page, current_page):
        errors = {}
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                errors.setdefault("limit", []).append("MUST_NUMBER")
        if per_page:
            try:
                per_page = int(per_page)
            except ValueError:
                errors.setdefault("per_page", []).append("MUST_NUMBER")
        if current_page:
            try:
                current_page = int(current_page)
            except ValueError:
                errors.setdefault("current_page", []).append("MUST_NUMBER")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (
            testimoni_data := await TestimoniDatabase.get("all_testimoni", limit=limit)
        ):
            return jsonify({"message": "testimoni not found"}), 404
        paginated_data = [
            testimoni_data[i : i + per_page]
            for i in range(0, len(testimoni_data), per_page)
        ]
        paginated_testimoni_datas_dict = [
            [
                {
                    "testimoni": {
                        "id": f"{item.id}",
                        "rating": item.rating,
                        "description": f"{item.description}",
                        "url_testimoni": item.url_testimoni,
                        "created_at": f"{item.created_at}",
                    },
                    "user": {
                        "discord_id": f"{item.user.discord_id}",
                        "email": item.user.email,
                        "username": item.user.username,
                        "is_active": item.user.is_active,
                        "created_at": item.user.created_at,
                        "updated_at": item.user.updated_at,
                        "avatar": item.user.avatar,
                    },
                }
                for item in promotion_page
            ]
            for promotion_page in paginated_data
        ]

        total_pages = len(paginated_testimoni_datas_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_testimoni_datas_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_testimoni_datas_dict[-1]
        )

        response_data = {
            "message": "successfully retrieved all testimoni",
            "data": [
                {
                    "testimoni": {
                        "id": f"{item.id}",
                        "rating": item.rating,
                        "description": f"{item.description}",
                        "url_testimoni": item.url_testimoni,
                        "created_at": f"{item.created_at}",
                    },
                    "user": {
                        "discord_id": f"{item.user.discord_id}",
                        "id": f"{item.user.id}",
                        "username": item.user.username,
                        "is_active": item.user.is_active,
                        "created_at": item.user.created_at,
                        "updated_at": item.user.updated_at,
                        "avatar": item.user.avatar,
                    },
                }
                for item in testimoni_data
            ],
            "page": {
                "current_page": current_page,
                "current_item": paginated_items,
                "total_pages": total_pages,
                "total_items": len(testimoni_data),
                "items_per_page": per_page,
                "limit": limit,
                "next_page": (current_page + 1 if current_page < total_pages else None),
                "previous_page": current_page - 1 if current_page > 1 else None,
            },
        }
        etag = generate_etag(paginated_items)

        client_etag = request.headers.get("If-None-Match")
        if client_etag == etag:
            return make_response("", 304)

        response = make_response(response_data, 200)
        response.headers["Content-Type"] = "application/json"
        response.headers["ETag"] = etag
        return response

    @staticmethod
    async def add_testimoni(
        rating,
        description,
        proof,
        timestamp,
        provider,
        user=None,
        discord_id=None,
        username=None,
        avatar=None,
        is_active=None,
    ):
        errors = {}
        if rating is None:
            errors.setdefault("rating", []).append("IS_REQUIRED")
        else:
            try:
                rating = int(rating)
            except ValueError:
                errors.setdefault("rating", []).append("MUST_NUMBER")
            else:
                if rating < 1:
                    errors.setdefault("rating", []).append("TOO_LOW")
                if rating > 5:
                    errors.setdefault("rating", []).append("TOO_HIGH")
        if description is None or (
            isinstance(description, str) and description.strip() == ""
        ):
            errors.setdefault("description", []).append("IS_REQUIRED")
        else:
            if not isinstance(description, str):
                errors.setdefault("description", []).append("MUST_TEXT")
            if len(description) > 1000:
                errors.setdefault("description", []).append("TOO_LONG")
            if len(description) < 5:
                errors.setdefault("description", []).append("TOO_SHORT")
        if proof:
            filename = secure_filename(proof.filename)
            ext = os.path.splitext(filename)[1].lower().replace(".", "")
            if ext not in ("jpg", "jpeg", "png", "webp"):
                errors.setdefault("proof", []).append("IS_INVALID")
        if provider == "discord_bot":
            try:
                discord_id = int(discord_id)
            except ValueError:
                errors.setdefault("discord_id", []).append("MUST_NUMBER")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        created_at = int(timestamp.timestamp())
        if proof:
            result_cloudinary = cloudinary.uploader.upload(proof)
        if provider == "login":
            result_testimoni = await TestimoniDatabase.insert(
                user.discord_id,
                rating,
                description,
                result_cloudinary["secure_url"] if proof else None,
                created_at,
            )
        else:
            result_testimoni = await TestimoniDatabase.update(
                "add_testimoni_by_discord_bot",
                discord_id=discord_id,
                username=username,
                avatar=avatar,
                is_active=is_active,
                rating=rating,
                description=description,
                url_testimoni=result_cloudinary["secure_url"] if proof else None,
                created_at=created_at,
            )
        proof_url = f"[proof]({result_testimoni.url_testimoni})" if proof else None
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhook_url, session=session)
            embed = (
                Embed(
                    description=f"New Testimoni <@{result_testimoni.user.discord_id}>",
                    color=nextcord.Color.green(),
                )
                .add_field(name="message", value=description, inline=True)
                .add_field(
                    name="rating", value=result_testimoni.rating * "⭐", inline=True
                )
                .set_footer(text=f"ID: {result_testimoni.id}")
                .set_thumbnail(url=result_testimoni.user.avatar)
            )
            if proof_url:
                embed.add_field(name="proof", value=proof_url, inline=False)
            await webhook.send(
                username=webhook_username,
                embed=embed,
            )
        return (
            jsonify(
                {
                    "data": {
                        "id": f"{result_testimoni.id}",
                        "created_at": created_at,
                        "url_testimoni": result_testimoni.url_testimoni,
                        "rating": result_testimoni.rating,
                        "description": result_testimoni.description,
                    },
                    "message": "successfully add testimoni",
                }
            ),
            201,
        )
