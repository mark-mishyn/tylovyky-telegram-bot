import os

from sqlalchemy import or_
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from database import Session
from database.models import User


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
        actors = session.query(User).all()
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
            session.query(User)
            .filter(
                or_(
                    User.first_name.contains(keyword),
                    User.last_name.contains(keyword),
                    User.date_of_birth.contains(keyword),
                    User.phone.contains(keyword),
                    User.email.contains(keyword),
                    User.social_media_link.contains(keyword),
                    User.sizes.contains(keyword),
                    User.hair_colour.contains(keyword),
                    User.eyes_colour.contains(keyword),
                    User.type.contains(keyword),
                    User.actors_skills.contains(keyword),
                    User.language.contains(keyword),
                    User.driver_license.contains(keyword),
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

    def _format_actor_info(self, actor: User) -> str:
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
