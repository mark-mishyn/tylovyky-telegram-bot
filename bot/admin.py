from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext
from database import Session
from database.models import Actor
from typing import List
import os
from sqlalchemy import or_


class Admin:
    def __init__(self):
        self.admin_ids = [int(id) for id in os.getenv("ADMIN_ID").split(",")]

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.admin_ids

    def handle(self, update: Update, context: CallbackContext):
        if self.is_admin(update.effective_user.id):
            keyboard = [
                [InlineKeyboardButton("Show all profiles", callback_data="show_all")],
                [InlineKeyboardButton("Search profiles", callback_data="search")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Choose an option:",
                reply_markup=reply_markup,
            )

    def handle_message(self, update: Update, context: CallbackContext):
        if self.is_admin(update.effective_user.id):
            if context.user_data.get("search"):
                self.search(update, context, update.message.text)
                context.user_data["search"] = False

    def show_all(self, update: Update, context: CallbackContext):
        session = Session()
        actors = session.query(Actor).all()
        for actor in actors:
            message = self._format_actor_info(actor)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            for i in range(1, 4):
                photo_id = getattr(actor, f"photo_{i}")
                if photo_id:
                    context.bot.send_photo(
                        chat_id=update.effective_chat.id, photo=photo_id
                    )

    def search(self, update: Update, context: CallbackContext, keyword: str):
        session = Session()
        actors = (
            session.query(Actor)
            .filter(
                or_(
                    Actor.first_name.contains(keyword),
                    Actor.last_name.contains(keyword),
                    Actor.date_of_birth.contains(keyword),
                    Actor.phone.contains(keyword),
                    Actor.email.contains(keyword),
                    Actor.social_media_link.contains(keyword),
                    Actor.sizes.contains(keyword),
                    Actor.hair_colour.contains(keyword),
                    Actor.eyes_colour.contains(keyword),
                    Actor.type.contains(keyword),
                    Actor.actors_skills.contains(keyword),
                    Actor.language.contains(keyword),
                    Actor.driver_license.contains(keyword),
                )
            )
            .all()
        )
        for actor in actors:
            message = self._format_actor_info(actor)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            for i in range(1, 4):
                photo_id = getattr(actor, f"photo_{i}")
                if photo_id:
                    context.bot.send_photo(
                        chat_id=update.effective_chat.id, photo=photo_id
                    )

    def _format_actor_info(self, actor: Actor) -> str:
        info = [
            f"🆔ID: {actor.id}",
            f"👤First name: {actor.first_name}",
            f"👤Last name: {actor.last_name}",
            f"🎁Date of birth: {actor.date_of_birth}",
            f"☎️Phone: {actor.phone}",
            f"📧Email: {actor.email}",
            f"📹Social media link: {actor.social_media_link}",
            f"👕Sizes: {actor.sizes}",
            f"👩‍🦰Hair colour: {actor.hair_colour}",
            f"👁Eyes colour: {actor.eyes_colour}",
            f"💄Type: {actor.type}",
            f"👩🏻‍🎓Actors skills: {actor.actors_skills}",
            f"🇺🇦Language: {actor.language}",
            f"🪪Driver license: {actor.driver_license}",
        ]
        return "\n".join(info)
