import os
from flask import Flask, jsonify, render_template, session
from waitress import serve

from game.game import Game

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start_game", methods=["POST"])
def start_game():
    game = Game()
    game.initialize_game()
    session["game"] = game.serialize()

    natural_21 = game.natural_21_state()
    dealer_masked = game.get_dealer_masked()
    player_hand = game.get_player()
    dealer_hand = game.get_dealer()
    player_count = game.sum(player_hand, True)

    return jsonify(
        {
            "natural_21": natural_21,
            "dealer_masked": dealer_masked,
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_count": player_count,
        }
    )


@app.route("/api/hit", methods=["POST"])
def hit():
    game_data = session.get("game")
    if game_data:
        game = Game.deserialize(game_data)
        game.get_hit_or_stand("hit")
        session["game"] = game.serialize()

        player_hand = game.get_player()
        player_count = game.get_player_count()
        dealer_masked = game.get_dealer_masked()

        return jsonify(
            {
                "player_hand": player_hand,
                "player_count": player_count,
                "dealer_masked": dealer_masked,
            }
        )
    else:
        return jsonify({"error": "Game not started"}), 400


@app.route("/api/stand", methods=["POST"])
def stand():
    game_data = session.get("game")
    if game_data:
        game = Game.deserialize(game_data)
        game.get_hit_or_stand("stand")
        session["game"] = game.serialize()

        player_hand = game.get_player()
        player_count = game.get_player_count()
        player_state = game.get_player_state()
        dealer_hand = game.get_dealer()
        dealer_count = game.get_dealer_count()
        dealer_state = game.get_dealer_state()
        winner = game.winner

        return jsonify(
            {
                "player_hand": player_hand,
                "player_count": player_count,
                "player_state": player_state,
                "dealer_hand": dealer_hand,
                "dealer_count": dealer_count,
                "dealer_state": dealer_state,
                "winner": winner,
            }
        )
    else:
        return jsonify({"error": "Game not started"}), 400


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000, url_scheme="https")
