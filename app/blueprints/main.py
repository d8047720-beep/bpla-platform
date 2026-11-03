from flask import Blueprint, render_template, abort, jsonify
from app import models

main = Blueprint("main", __name__)

@main.route("/")
def index():
    drones = models.all_drones()
    return render_template("index.html", drones=drones)

@main.route("/drones")
def drones():
    return render_template("drones.html", drones=models.all_drones())

@main.route("/drones/<slug>")
def drone_detail(slug):
    drone = models.get_drone(slug)
    if not drone:
        abort(404)
    return render_template("drone_detail.html", drone=drone, drones=models.all_drones())

@main.route("/map")
def map_view():
    return render_template("map.html", drones=models.all_drones())

@main.route("/compare")
def compare():
    return render_template("compare.html", drones=models.all_drones())

@main.route("/health")
def health():
    return {"status": "ok", "drones": len(models.all_drones())}


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
