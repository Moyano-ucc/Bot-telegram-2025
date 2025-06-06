from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import json
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

PROGRESO_FILE = "progreso_usuarios.json"

def cargar_progreso():
    if os.path.exists(PROGRESO_FILE):
        with open(PROGRESO_FILE, "r") as f:
            return json.load(f)
    return {}
async def my_job():
    print("tarea")

def guardar_progreso(progreso):
    with open(PROGRESO_FILE, "w") as f:
        json.dump(progreso, f, indent=2)

def obtener_usuarios_con_progreso():
    progreso = cargar_progreso()
    return [user_id for user_id, datos in progreso.items() if "respuestas" in datos and datos["respuestas"]]

TOKEN = "7776335738:AAHPfygxVC7vfCjP9AU-uspZ6cgsNvbFu4w"

LECCIONES_MODULOS = {
    "modulo1": {
        "leccion1": {

            "pregunta": "¡Bienvenido al Módulo 1 de tu curso de inglés básico! En este primer módulo, aprenderás algunas de las palabras más esenciales para comenzar a comunicarte: los saludos y las despedidas. Estas expresiones son fundamentales en cualquier idioma, ya que te permiten iniciar y cerrar una conversación de manera cortés y natural.\n\n📺 Mira este video: https://youtu.be/2o46gKeQTwc?si=ecn5WQbJUtmrCXII\n\n ¿Qué significa 'Hello'?",
            "opciones": {
                "A": "Hola",
                "B": "Gracias",
                "C": "Adiós"
            },
            "respuesta": "A"
        },
        "leccion2": {
            "pregunta": "📺 Mira este video: https://youtu.be/2o46gKeQTwc?si=ecn5WQbJUtmrCXII\n\n¿Qué significa 'Goodbye'?",
            "opciones": {
                "A": "Hola",
                "B": "Gracias",
                "C": "Adiós"
            },
            "respuesta": "C"
        }
    },
    "modulo2": {

        "leccion1": {


            "pregunta": " En este Módulo 2 aprenderás uno de los conceptos más importantes del inglés: el verbo “to be”, esto mediante del presente simple. Aprenderás a como aplicarlo y a completar frases simples para lograr un mayor entendimiento del tema. \n\n Mira este video: https://www.youtube.com/watch?v=KRyK79yP0oA\n\n¿Que es el verbo to be?",
            "opciones":{
                "A":"Una accion",
                "B":"Ser o Estar",
                "C":"Un pronombre"
            },
            "respuesta": "B"
        },
        "leccion2": {
            "pregunta":"Mira este video: https://www.youtube.com/watch?v=KRyK79yP0oA\n\n¿Cuales se usan en el presente simple?",
            "opciones":{
                "A":"Am, Are, Is",
                "B":"You, They, We",
                "C":"Am, It, Was"
            },
            "respuesta":"A"
        },
        "leccion3": {
            "pregunta":"Mira este video: https://www.youtube.com/watch?v=KRyK79yP0oA\n\nCompleta la frase\nYou_____a school student",
            "opciones":{
                "A":"Is",
                "B":"am",
                "C":"Are"
            },
            "respuesta":"C"
        }
    },
    "modulo3": {

        "leccion1": {

            "pregunta":" ¡Bienvenido al Módulo 3! En esta unidad aprenderás vocabulario relacionado con lugares de la ciudad. Saber cómo nombrar estos sitios en inglés es muy útil para moverte, pedir indicaciones o simplemente describir tu entorno. Este módulo te ayudará a relacionar imágenes y palabras, mejorando tu comprensión auditiva y visual. Al finalizar, podrás identificar varios lugares en inglés y decir para qué se usan. \n\n Mira este video: https://www.youtube.com/watch?v=o3ghpdHWMwI\n\nMenciona 3 lugares que se muestran en el video.",
            "opciones":{
                "A":"Supermarket, Library, Shoping Mall",
                "B":"Police Office, School, Restaurant",
                "C":"Park, Airport, Post Office"
            },
            "respuesta":"A"
        },
        "leccion2": {
            "pregunta":"Mira este video: https://www.youtube.com/watch?v=o3ghpdHWMwI\n\nTrue or False: ¿Se puede jugar en un park?",
            "opciones":{
                "A":"True",
                "B":"False"
            },
            "respuesta":"A"
        }
    },
    "modulo4": {

        "leccion1": {

            "pregunta": "¡Llegamos al Módulo 4! En esta unidad aprenderás cómo hablar sobre rutinas diarias en inglés, usando el presente simple (present simple). Este tiempo verbal es ideal para describir acciones que haces todos los días, como levantarte, ir a la escuela o cenar con tu familia. Con este módulo podrás contar tu día a día en inglés, usando expresiones claras y frecuentes. Presta atención a las estructuras que se repiten, ya que te ayudarán a formar oraciones de manera más natural. '\n\n Mira este video: https://www.youtube.com/watch?v=6j3r452hbUA\n\n¿Qué usamos para describir rutinas?",
            "opciones": {
                "A": "Present continuous",
                "B": "Present simple",
                "C": "past simple"
            },
            "respuesta": "B"
        },
        "leccion2":{
            "pregunta": "Mira este video: https://www.youtube.com/watch?v=6j3r452hbUA\n\n¿Para qué usamos get to?",
            "opciones":{
                "A":"Levantarse",
                "B":"Despertar",
                "C":"Llegar a un lugar",
                "D":"Salir de un lugar"
            },
            "respuesta":"C"
        },
        "leccion3":{
            "pregunta":"Mira este video: https://www.youtube.com/watch?v=6j3r452hbUA\n\nCompleta la oración:\nI always ____ when i get home",
            "opciones":{
                "A":"Take a shower",
                "B":"Have breakfast",
                "C":"Get up"
            },
            "respuesta":"A"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy Naomy 📚\nEstoy aquí para ayudarte a aprender inglés de forma divertida.\n\n"
        "Usa /leccion para ver los módulos y sus lecciones.\n"
        "Usa /help para más comandos.\n\n"
        "📈 *¿Quieres ver tu avance?* Usa /progreso en cualquier momento.",
        parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = ("📚 *Comandos disponibles:*\n\n"
             "/start - Inicia Naomy\n"
             "/leccion - Muestra los módulos y lecciones\n"
             "/progreso - Muestra tu avance actual\n"
             "/help - Muestra esta ayuda")
    await update.message.reply_text(texto, parse_mode="Markdown")

async def leccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones = [[
        InlineKeyboardButton(f"Módulo {i+1}",
                             callback_data=f"modulo_modulo{i+1}")
    ] for i in range(len(LECCIONES_MODULOS))]
    await update.message.reply_text("Selecciona un módulo:",
                                    reply_markup=InlineKeyboardMarkup(botones))

async def progreso_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    progreso = cargar_progreso()

    if user_id not in progreso or "respuestas" not in progreso[user_id]:
        await update.message.reply_text(
            "📭 No tienes progreso aún. Usa /leccion para empezar.")
        return

    modulo_actual = progreso[user_id].get("modulo_actual", "Desconocido")
    respuestas = progreso[user_id]["respuestas"]
    texto = f"📊 *Tu progreso en el {modulo_actual}:*\n\n"

    for leccion_id, datos in respuestas.items():
        estado = "✅ Correcto" if datos[
            "acertada"] else f"❌ Incorrecto (era {datos['correcta']})"
        texto += f"🔹 *{leccion_id}*: Marcaste {datos['respuesta_usuario']} → {estado}\n"

    puntaje = progreso[user_id].get("puntaje", 0)
    total = len(respuestas)
    texto += f"\n🏆 Puntaje final: {puntaje}/{total}"
    await update.message.reply_text(texto, parse_mode="Markdown")

async def mostrar_lecciones_modulo(query, modulo_id):
    lecciones = LECCIONES_MODULOS.get(modulo_id, {})
    botones = [[
        InlineKeyboardButton(f"Lección {i+1}",
                             callback_data=f"leccion_{modulo_id}_leccion{i+1}")
    ] for i in range(len(lecciones))]
    await query.message.reply_text("Selecciona una lección:",
                                   reply_markup=InlineKeyboardMarkup(botones))

async def mostrar_pregunta_modulo(query, modulo_id, leccion_id):
    leccion = LECCIONES_MODULOS[modulo_id][leccion_id]
    botones = [[
        InlineKeyboardButton(f"{key}) {val}",
                             callback_data=f"resp_{leccion_id}_{key}")
    ] for key, val in leccion["opciones"].items()]
    await query.message.reply_text(leccion["pregunta"],
                                   reply_markup=InlineKeyboardMarkup(botones))

async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    progreso = cargar_progreso()
    data = query.data.split("_")
    tipo = data[0]

    if tipo == "modulo":
        modulo_id = data[1]
        context.user_data["modulo_actual"] = modulo_id
        context.user_data["puntaje"] = 0

        progreso[user_id] = {
            "modulo_actual": modulo_id,
            "leccion_actual": None,
            "puntaje": 0,
            "respuestas": {}
        }
        guardar_progreso(progreso)

        await mostrar_lecciones_modulo(query, modulo_id)

    elif tipo == "leccion":
        modulo_id = data[1]
        leccion_id = data[2]
        context.user_data["leccion_actual"] = leccion_id

        if user_id not in progreso:
            progreso[user_id] = {"respuestas": {}}
        progreso[user_id]["leccion_actual"] = leccion_id
        guardar_progreso(progreso)

        await mostrar_pregunta_modulo(query, modulo_id, leccion_id)

    elif tipo == "resp":
        modulo_id = context.user_data.get("modulo_actual")
        leccion_id = data[1]
        respuesta = data[2]

        correcta = LECCIONES_MODULOS[modulo_id][leccion_id]["respuesta"]

        if user_id not in progreso:
            progreso[user_id] = {"respuestas": {}}

        # Verifica si ya respondió esta lección
        ya_respondida = leccion_id in progreso[user_id].get("respuestas", {})

        if not ya_respondida:
            # Solo suma puntaje si no ha respondido antes
            if respuesta == correcta:
                context.user_data["puntaje"] = context.user_data.get("puntaje", 0) + 1
                texto = "✅ ¡Correcto! 🎉"
            else:
                texto = f"❌ Incorrecto. La respuesta correcta era '{correcta}'"

            progreso[user_id]["puntaje"] = context.user_data["puntaje"]
            progreso[user_id].setdefault("respuestas", {})
            progreso[user_id]["respuestas"][leccion_id] = {
                "respuesta_usuario": respuesta,
                "correcta": correcta,
                "acertada": respuesta == correcta
            }
        else:
            # Si ya respondió, solo muestra el resultado anterior
            datos_previos = progreso[user_id]["respuestas"][leccion_id]
            if datos_previos["acertada"]:
                texto = "✅ Ya respondiste correctamente esta lección."
            else:
                texto = f"❌ Ya respondiste incorrectamente. La respuesta correcta era '{correcta}'"

        lecciones = list(LECCIONES_MODULOS[modulo_id].keys())
        actual_idx = lecciones.index(leccion_id)
        siguiente_idx = actual_idx + 1

        if siguiente_idx < len(lecciones):
            siguiente_leccion = lecciones[siguiente_idx]
            progreso[user_id]["leccion_actual"] = siguiente_leccion
            guardar_progreso(progreso)

            await query.edit_message_text(
                f"{texto}\n\n⏭️ Siguiente lección en 2 segundos...")
            await asyncio.sleep(2)
            await mostrar_pregunta_modulo(query, modulo_id, siguiente_leccion)
        else:
            guardar_progreso(progreso)
            puntaje = context.user_data["puntaje"]
            total = len(lecciones)
            mensaje_final = f"🎉 ¡Has terminado el módulo!\n🏆 Puntaje final: {puntaje}/{total}"
            await query.edit_message_text(f"{texto}\n\n{mensaje_final}")

async def enviar_recordatorio(context: ContextTypes.DEFAULT_TYPE):
    usuarios = obtener_usuarios_con_progreso()
    for user_id in usuarios:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="⏰ ¡No olvides repasar! Vuelve a practicar una lección hoy con Naomy. Usa /leccion para continuar."
            )
        except Exception as e:
            print(f"Error enviando recordatorio a {user_id}: {e}")

async def post_init(application):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_recordatorio, "cron", hour=15, minute=20, args=[application])
   # scheduler.add_job(enviar_recordatorio, IntervalTrigger(seconds=10), args=[application])

    scheduler.start()

app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("leccion", leccion))
app.add_handler(CommandHandler("progreso", progreso_command))
app.add_handler(CallbackQueryHandler(manejar_callback))
app.run_polling()