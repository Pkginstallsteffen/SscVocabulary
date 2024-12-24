import os
import logging
import random
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import language_tool_python

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MW_API_KEY = os.getenv("MW_API_KEY")  # Merriam-Webster Dictionary API Key
THESAURUS_API_KEY = os.getenv("THESAURUS_API_KEY")  # Thesaurus API Key

# Logging configuration
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Grammar Tool
grammar_tool = language_tool_python.LanguageTool("en-US")

# File paths
VOCAB_FILE = "wordlist.txt"
SYNONYM_FILE = "synonym_wordlist.txt"
ANTONYM_FILE = "antonym_wordlist.txt"

# Toggles for APIs or Local Wordlists
USE_API_FOR_VOCAB = True
USE_API_FOR_SYNONYMS = True
USE_API_FOR_ANTONYMS = True

# Global Data
user_scores = {}  # Tracks user points
active_words = []  # Tracks currently active words
user_word_usage = {}  # Tracks word usage per user
feedback_messages = []  # Stores feedback

# Initialize Scheduler
scheduler = BackgroundScheduler()

# Fetch Vocabulary
def fetch_vocabulary():
    if USE_API_FOR_VOCAB:
        vocabulary = ["eloquent", "vivacious", "serendipity", "meticulous", "ubiquitous",
"abate", "abhor", "abridge", "abscond", "acquiesce", "alleviate", 
"ambiguous", "anomaly", "apathy", "aptitude", "arbitrary", "astute", 
"atrocious", "belligerent", "beneficiary", "benevolent", "benign", 
"cajole", "capricious", "censure", "chronic", "clandestine", "coerce", 
"complacent", "concur", "conundrum", "credulous", "cursory", "demeanor", 
"detrimental", "diligent", "discrepancy", "disseminate", "dissident", 
"empathy", "enervate", "ephemeral", "equanimity", "exacerbate", "exhume", 
"facilitate", "fathom", "fervent", "flabbergasted", "fortuitous", "frivolous", 
"harbinger", "hegemony", "histrionics", "imminent", "impartial", "imperative", 
"incessant", "incorrigible", "indignant", "inevitable", "innocuous", "intrepid", 
"intricate", "juxtapose", "lethargy", "loquacious", "malleable", "mellifluous", 
"meticulous", "mitigate", "morose", "nefarious", "obfuscate", "oblivious", 
"opaque", "opportune", "paradox", "pedantic", "pernicious", "plausible", 
"precarious", "prevalent", "quaint", "quintessential", "ravenous", "recalcitrant", 
"sycophant", "serendipity", "subtle", "tantamount", "tenuous", "ubiquitous", 
"uncanny", "urbane", "vacillate", "venerate", "vociferous", "volatile", 
"warranted", "whimsical", "zealot", "zenith", "zest", 

"aberration", "abscond", "accost", "adulation", "affluent",
"aggrandize", "altruism", "ambivalent", "anachronism", "anathema",
"apathetic", "arbitrary", "ascertain", "balk", "belligerence",
"benevolence", "blandish", "brevity", "cajole", "calamity",
"censure", "coalesce", "commensurate", "complicit", "condone",
"conflagration", "congregate", "contrite", "corroborate", "cryptic",
"culpable", "defenestrate", "deference", "delineate", "denounce",
"deride", "detrimental", "diatribe", "diffident", "diligence",
"disconcerting", "discord", "discretion", "dispel", "dissipate",
"dissolve", "divulge", "emaciated", "emulate", "enervate",
"engender", "enigma", "ephemeral", "equivocal", "exacerbate",
"exemplary", "exhume", "facilitate", "feasible", "fervent",
"fickle", "flagrant", "flabbergasted", "fortuitous", "frivolous",
"garrulous", "gregarious", "harangue", "harbinger", "hegemonic",
"hubris", "idiosyncratic", "immutable", "impeccable", "imperative",
"imperturbable", "incessant", "incoherent", "indefatigable", "indignant",
"ineffable", "inept", "inexorable", "infer", "innate",
"insipid", "insolent", "interloper", "intricate", "intuitive",
"invective", "irrelevant", "laconic", "lament", "latent",
"laudable", "legitimate", "lethargic", "loquacious", "lucid",
"magnanimous", "malevolent", "malleable", "manifest", "meticulous",
"mitigate", "morose", "nefarious", "nominal", "nonchalant",
"obfuscate", "oblivious", "opaque", "opportune", "ostentatious",
"paradox", "pedantic", "perfidious", "pernicious", "plethora",
"plausible", "pragmatic", "precipitous", "precarious", "prodigal",
"prolific", "propensity", "prosaic", "rampant", "recalcitrant",
"recluse", "recant", "reciprocal", "recondite", "redolent",
"redundant", "relevant", "resilient", "reverence", "rhetoric",
"robust", "sagacious", "salient", "sarcastic", "serene",
"serendipity", "subjugate", "subtle", "superficial", "sycophant",
"taciturn", "tantamount", "tedious", "temporal", "tenuous",
"toxic", "turbulent", "ubiquitous", "uncanny", "urbane",
"vacillate", "venerate", "veracity", "vicarious", "vociferous",
"volatile", "warranted", "whimsical", "zealous", "zenith",
"absolutism", "acquaintance", "affliction", "altruistic", "antagonistic",
"apathetic", "austerity", "beneficence", "biography", "capitalism",
"civility", "clerical", "coherent", "cognitive", "compliant",
"congenial", "conscientious", "contentious", "conviction", "corrigible",
"culminate", "decadent", "deliberate", "denial", "depravity",
"devious", "diligent", "divine", "dormant", "duress",
"elusive", "emaciated", "embellish", "engage", "entail",
"erudite", "ethereal", "exceed", "exceptional", "exclusive",
"facile", "faithful", "fallacy", "frantic", "genteel",
"generic", "genuine", "gratuitous", "haughty", "hazardous",
"hypocrisy", "ignominious", "illiterate", "inaugural", "incongruous",
"inflexible", "insidious", "instigate", "insurgent", "intervene",
"invasive", "isolated", "jargon", "jeopardize", "judicious",
"keen", "latent", "laxity", "leverage", "loyal",
"malcontent", "malicious", "manipulate", "meager", "mendacious",
"mercenary", "meritorious", "methodical", "monotony", "narrative",
"nuance", "obdurate", "oppressive", "optimistic", "paragon",
"patriotic", "pedagogue", "perpetuate", "philanthropy", "plentiful",
"polemical", "populist", "precipitate", "profuse", "profound",
"propitious", "quaint", "quick-witted", "redundant", "reluctant",
"resistant", "resolute", "revile", "rigorous", "safeguard",
"self-evident", "serenity", "speculative", "spontaneous", "stagnant",
"stint", "stoic", "strenuous", "subjective", "subdued",
"subversive", "supercilious", "sustenance", "synergy", "tenacious",
"terrestrial", "trivial", "unprecedented", "unravel", "unveiled",
"vigilant", "virtue", "volition", "warranted", "zeal",
"zealous", "prodigal", "ostensible", "facile", "cogent",
"elucidate", "epiphany", "refute", "spurious", "mendicant",
"deference", "cauterize", "nonplussed", "rescind", "dispel",
"effervescent", "facade", "unfathomable", "egregious", "succinct",
"fortuitous", "abstruse", "predilection", "congenial", "exorbitant",
"plausible", "adulation", "ascetic", "solace", "succumb",
"regale", "exonerate", "ambiguity", "propagate", "malleability",
"meander", "staunch", "coercive", "consonant", "copious",
"disgruntled", "impeccable", "audacity", "abhor", "efficacious",
"tedious", "solicitous", "antipathy", "affable", "recalcitrant",
"tenable", "diffuse", "luminous", "noxious", "subterfuge",
"devious", "proscribe", "anomalous", "mundane", "overwrought",
"perturbation", "occlude", "pristine", "fallacious", "delineate",
"dubious", "serendipitous", "enervated", "impetuous", "brusque",
"apathetic", "bravado", "inclement", "subjugate", "patriarchal",
"sentient", "nefarious", "wary", "spurious", "volatile",
"emollient", "ethereal", "insolent", "nuanced", "calibrate",
"alleviate", "cynical", "quixotic", "venerable", "remunerate",
"staunch", "compel", "convoluted", "insipid", "elusive",
"dormant", "censure", "affinity", "belligerent", "sanguine",
"acquiesce", "foreshadow", "ephemeral", "veracity", "lucid",
"depreciate", "dissent", "garrulous", "nocturnal", "omnipotent",
"empathic", "grievance", "pathetic", "staunch", "prodigious",
"incumbent", "intransigent", "amalgamation", "fortuitous", "inquisitive",
"dormant", "amiable", "compelling", "serene", "lucid",
"urbane", "notorious", "vehement", "salient", "imminent",
"quandary", "candid", "perplexed", "renowned", "affluent",
"vivid", "disband", "indefatigable", "detestable", "extant",
"vindicate", "oblivion", "pervasive", "counterfeit", "discretionary",
"subjugation", "extemporaneous", "unprecedented", "compunctious", "disgorge",
"juvenile", "culpable", "accr"
                     ]
        words = []
        for word in random.sample(vocabulary, 5):
            response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MW_API_KEY}")
            data = response.json()
            definition = data[0]["shortdef"][0] if data and "shortdef" in data[0] else "No definition available."
            words.append({"word": word, "definition": definition})
        return words
    else:
        with open(VOCAB_FILE, "r") as file:
            word_list = [word.strip() for word in file.readlines()]
        return [{"word": word, "definition": "Definition not available from local wordlist."} for word in random.sample(word_list, 5)]

# Fetch Synonyms
def fetch_synonyms(word):
    if USE_API_FOR_SYNONYMS:
        response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={THESAURUS_API_KEY}")
        data = response.json()
        synonyms = data[0]["meta"]["syns"][0] if data and "meta" in data[0] else []
        return ", ".join(synonyms[:5]) if synonyms else "No synonyms available."
    else:
        with open(SYNONYM_FILE, "r") as file:
            synonym_list = [line.strip() for line in file.readlines()]
        return ", ".join(random.sample(synonym_list, 5))

# Fetch Antonyms
def fetch_antonyms(word):
    if USE_API_FOR_ANTONYMS:
        response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={THESAURUS_API_KEY}")
        data = response.json()
        antonyms = data[0]["meta"]["ants"][0] if data and "meta" in data[0] else []
        return ", ".join(antonyms[:5]) if antonyms else "No antonyms available."
    else:
        with open(ANTONYM_FILE, "r") as file:
            antonym_list = [line.strip() for line in file.readlines()]
        return ", ".join(random.sample(antonym_list, 5))

# Grammar Check
def check_grammar(text):
    matches = grammar_tool.check(text)
    return [{"message": match.message, "suggestions": match.replacements} for match in matches]

# Grammar and Vocabulary Usage Handler
async def handle_word_usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    user_id = update.effective_user.id
    used_words = [word['word'] for word in active_words if word['word'].lower() in user_input]

    if not used_words:
        await update.message.reply_text("Please use one of the active vocabulary words in your sentence.")
        return

    matches = check_grammar(user_input)
    error_count = len(matches)
    grammar_feedback = "\n".join(
        [f"❌ {m['message']}\nSuggestions: {', '.join(m['suggestions'])}" for m in matches]
    )

    for word in used_words:
        user_word_usage.setdefault(user_id, []).append(word)
        score = 30 if word not in user_word_usage[user_id] else 20
        if error_count:
            score -= error_count * 5
        user_scores[user_id] = user_scores.get(user_id, 0) + score
        message = (
            f"💎 Points earned for '{word}': {score}\n"
            f"⚙️ Grammar Feedback:\n{grammar_feedback}\n\n"
            f"Total Points: {user_scores[user_id]}"
        )
        await update.message.reply_text(message)

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Vocabulary Booster Bot! 🌟 Use /help to explore.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot\n/dailyword - Get 5 new words\n"
        "/synonym [word] - Fetch synonyms\n/antonym [word] - Fetch antonyms\n"
        "/leaderboard - View top users\n/feedback - Provide feedback"
    )

async def synonym(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = " ".join(context.args)
    synonyms = fetch_synonyms(word)
    await update.message.reply_text(f"Synonyms for {word}: {synonyms}")

async def antonym(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = " ".join(context.args)
    antonyms = fetch_antonyms(word)
    await update.message.reply_text(f"Antonyms for {word}: {antonyms}")

async def dailyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_words
    active_words = fetch_vocabulary()
    message = "\n".join([f"{word['word']}: {word['definition']}" for word in active_words])
    await update.message.reply_text(f"Today's Vocabulary:\n{message}")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaderboard = "\n".join([f"User {uid}: {score} points" for uid, score in sorted(user_scores.items(), key=lambda x: x[1], reverse=True)])
    await update.message.reply_text(f"🏆 Leaderboard:\n{leaderboard}")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback = " ".join(context.args)
    if feedback:
        feedback_messages.append(feedback)
        await update.message.reply_text("Thank you for your feedback!")
    else:
        await update.message.reply_text("Please provide feedback.")

# Broadcast Words
async def broadcast_words(application):
    global active_words
    active_words = fetch_vocabulary()
    message = "\n".join([f"{word['word']}: {word['definition']}" for word in active_words])
    for chat_id in user_scores.keys():
        await application.bot.send_message(chat_id, text=f"New Words:\n{message}")

# Main Function
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    scheduler.add_job(lambda: broadcast_words(application), IntervalTrigger(minutes=10))
    scheduler.start()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dailyword", dailyword))
    application.add_handler(CommandHandler("synonym", synonym))
    application.add_handler(CommandHandler("antonym", antonym))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_word_usage))

    application.run_polling()

if __name__ == "__main__":
    main ()