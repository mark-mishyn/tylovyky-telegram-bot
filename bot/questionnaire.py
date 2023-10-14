from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from database import Session
from database.models import User


class Questionnaire:
    def __init__(self):
        self.questions = {
            "en": [
                "First name",
                "Last name",
                "Date of birth",
                "Phone",
                "Email",
                "Social media link",
                "Sizes",
                "Hair colour",
                "Eyes colour",
                "Type",
                "Actors skills",
                "Language",
                "Driver license",
            ],
            "uk": [
                "Ім'я",
                "Прізвище",
                "Дата народження",
                "Телефон",
                "Електронна пошта",
                "Посилання на соціальні медіа",
                "Розміри",
                "Колір волосся",
                "Колір очей",
                "Тип",
                "Акторські навички",
                "Мова",
                "Права водія",
            ],
        }
        self.bot_responses = {
            "en": {
                "ask_photo": "Please send photo {0}.",
                "invalid_date": "Invalid date format. Enter the date in YYYY/MM/DD format.",
                "thank_you": "Thank you for completing the questionnaire!",
                "already_started": "You've already started the questionnaire. Please complete it or use the /restart command to start over.",
            },
            "uk": {
                "ask_photo": "Будь ласка, надішліть фото {0}.",
                "invalid_date": "Неправильний формат дати. Введіть дату в форматі РРРР/ММ/ДД.",
                "thank_you": "Дякую за заповнення анкети!",
                "already_started": "Ви вже розпочали заповнення анкети. Будь ласка, завершіть її або використайте команду /restart, щоб розпочати знову.",
            },
        }

        self.attributes = [
            "first_name",
            "last_name",
            "date_of_birth",
            "phone",
            "email",
            "social_media_link",
            "sizes",
            "hair_colour",
            "eyes_colour",
            "type",
            "actors_skills",
            "language",
            "driver_license",
        ]
        self.current_question = 0
        self.received_photos = 0
        self.language = "en"  # Default language

    def start(self, update: Update, context: CallbackContext):
        # Ask user for language
        keyboard = [
            [
                InlineKeyboardButton("English", callback_data="en"),
                InlineKeyboardButton("Українська", callback_data="uk"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Please choose your language:", reply_markup=reply_markup
        )

    def set_language(self, language: str):
        # Set the questionnaire language
        if language in self.questions:
            self.language = language
        else:
            raise ValueError(f"Unsupported language: {language}")

    def handle_callback_query(self, update: Update, context: CallbackContext):
        # Handle language selection callback
        query = update.callback_query
        language = query.data
        if language in ["en", "uk"]:
            self.set_language(language)
            query.answer()
            query.edit_message_text(
                text=f"You've selected {language}. The questionnaire will now be conducted in {language}."
            )
            # Start the questionnaire
            self.ask_question(update, context)

    def ask_question(self, update: Update, context: CallbackContext):
        # Ask a question to the user
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.questions[self.language][self.current_question],
        )

    def handle_message(self, update: Update, context: CallbackContext):
        # Handling the response to the questionnaire question
        self.save_answer(update, context)
        self.current_question += 1
        if self.current_question < len(self.questions[self.language]):
            self.ask_question(update, context)
        else:
            self.ask_for_photo(update, context)

    def handle_photo(self, update: Update, context: CallbackContext):
        # Handling photo
        if update.message.photo is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Please send a photo."
            )
            return

        photo = update.message.photo[-1]
        session = Session()
        actor = session.query(User).filter_by(id=update.effective_user.id).first()
        setattr(actor, f"photo_{self.received_photos+1}", photo.file_id)
        session.commit()

        self.received_photos += 1
        if self.received_photos < 3:
            self.ask_for_photo(update, context)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Thank you for completing the questionnaire!",
            )

    def ask_for_photo(self, update: Update, context: CallbackContext):
        # Ask the user to send a photo
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Please send photo {self.received_photos+1}.",
        )

    def save_answer(self, update: Update, context: CallbackContext):
        # Save user response
        session = Session()
        actor = session.query(User).get(update.effective_user.id)
        attribute_name = self.attributes[self.current_question]
        # If the actor exists, update its data
        if actor:
            if attribute_name == "date_of_birth":
                try:
                    date_of_birth = datetime.strptime(
                        update.message.text, "%Y/%m/%d"
                    ).date()
                except ValueError:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Invalid date format. Enter the date in YYYY/MM/DD format.",
                    )
                    return
                setattr(actor, attribute_name, date_of_birth)
            else:
                setattr(actor, attribute_name, update.message.text)
            session.merge(actor)
        else:
            # If the actor does not exist, create a new entry
            actor = User(id=update.effective_user.id)
            if attribute_name == "date_of_birth":
                try:
                    date_of_birth = datetime.strptime(
                        update.message.text, "%Y/%m/%d"
                    ).date()
                except ValueError:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Invalid date format. Enter the date in YYYY/MM/DD format.",
                    )
                    return
                setattr(actor, attribute_name, date_of_birth)
            else:
                setattr(actor, attribute_name, update.message.text)
            session.add(actor)
        session.commit()
        session.close()
