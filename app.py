from flask import Flask, render_template, request, redirect, url_for, session
from game_logic import LifeSimulator, SocioEconomicClass, Nationality, Religion
from datetime import timedelta
import json
import os
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=1)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.template_filter('format_number')
def format_number(value):
    return "{:,}".format(int(value))

def get_game():
    if 'game' not in session:
        logger.debug("No game in session, creating new LifeSimulator")
        return LifeSimulator()
    
    try:
        game_data = session['game']
        if isinstance(game_data, str):
            game_data = json.loads(game_data)
        game = LifeSimulator.from_dict(game_data)
        logger.debug("Loaded game from session")
        return game
    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        logger.error(f"Error loading game from session: {e}")
        return LifeSimulator()

def save_game(game):
    try:
        session['game'] = game.to_dict()
        session.modified = True
        logger.debug("Game state saved to session")
    except Exception as e:
        logger.error(f"Error saving game to session: {e}")

@app.route('/')
def index():
    game = get_game()
    if not game.player:
        logger.debug("No player found, redirecting to character creation")
        return redirect(url_for('character_creation'))
    return render_template('index.html', game=game, SocioEconomicClass=SocioEconomicClass)

# ... (rest of app.py remains the same up to /character route)

@app.route('/character', methods=['GET', 'POST'])
def character_creation():
    game = get_game()
    
    if request.method == 'POST':
        logger.debug("Received POST request for character creation")
        socio_class = request.form.get('socio_class', 'MIDDLE')
        nationality = request.form.get('nationality', 'AMERICAN')
        religion = request.form.get('religion', 'NONE')
        first_name = request.form.get('first_name', 'Alex')
        last_name = request.form.get('last_name', 'Smith')
        gender = request.form.get('gender', 'Non-Binary')

        logger.debug(f"Form data: first_name={first_name}, last_name={last_name}, gender={gender}, socio_class={socio_class}, nationality={nationality}, religion={religion}")

        try:
            socio_class = SocioEconomicClass[socio_class]
            nationality = Nationality[nationality]
            religion = Religion[religion]
        except KeyError as e:
            logger.warning(f"Invalid enum value: {e}, using defaults")
            socio_class = SocioEconomicClass.MIDDLE
            nationality = Nationality.AMERICAN
            religion = Religion.NONE
        
        # Clear session to ensure fresh state
        session.clear()
        logger.debug("Session cleared before creating new character")

        game.create_character(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            socio_class=socio_class,
            nationality=nationality,
            religion=religion
        )
        logger.debug("Character created, saving game")
        save_game(game)
        if game.player:
            logger.debug(f"Player created: {game.player.full_name()}, redirecting to index")
            return redirect(url_for('index'))
        else:
            logger.error("Player creation failed, staying on character page")
            return render_template(
                'character.html',
                socio_classes=[c.name for c in SocioEconomicClass],
                nationalities=[n.name for n in Nationality],
                religions=[r.name for r in Religion],
                error="Failed to create character. Please try again."
            )
    
    logger.debug("Rendering character creation page")
    return render_template(
        'character.html',
        socio_classes=[c.name for c in SocioEconomicClass],
        nationalities=[n.name for n in Nationality],
        religions=[r.name for r in Religion]
    )

# ... (rest of app.py remains the same)

@app.route('/advance', methods=['POST'])
def advance_year():
    game = get_game()
    action = request.form.get('action', '')
    
    if action == 'pause':
        game.paused = not game.paused
        logger.debug(f"Game paused: {game.paused}")
    elif action == 'speed':
        game.game_speed = int(request.form.get('speed', 1))
        logger.debug(f"Game speed set to: {game.game_speed}")
    elif action == 'advance':
        if not game.paused:
            game.update()
            logger.debug("Advanced one year")
    elif action == 'choice':
        choice_index = int(request.form.get('choice', 0))
        game.handle_choice(choice_index)
        logger.debug(f"Handled choice: {choice_index}")
    
    save_game(game)
    return redirect(url_for('index'))

# ... (rest of app.py unchanged up to handle_event)

@app.route('/event', methods=['GET', 'POST'])
def handle_event():
    game = get_game()
    if request.method == 'POST':
        if 'new_name' in request.form:  # Handle next gen name input
            game.current_event['new_name'] = request.form['new_name']
            logger.debug(f"Next gen name set to: {request.form['new_name']}")
            game.handle_choice(0)
        else:
            choice_index = int(request.form.get('choice', 0))
            logger.debug(f"Event choice made: {choice_index}, action: {game.current_event['choices'][choice_index]['action']}")
            game.handle_choice(choice_index)
        save_game(game)
        return redirect(url_for('index'))
    currency_code, currency_symbol = game.get_currency()
    return render_template('event.html', event=game.current_event, currency_symbol=currency_symbol, currency_code=currency_code)

# ... (rest of app.py unchanged)

@app.route('/death', methods=['GET', 'POST'])
def death_screen():
    game = get_game()
    if request.method == 'POST':
        action = request.form.get('action')
        choice_index = next((i for i, choice in enumerate(game.current_event['choices']) if choice['action'] == action), 0)
        game.handle_choice(choice_index)
        logger.debug(f"Death choice made: {action}")
        save_game(game)
        return redirect(url_for('index'))
    
    return render_template('death.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)
