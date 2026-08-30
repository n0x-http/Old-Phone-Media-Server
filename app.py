from flask import Flask, render_template, request, send_from_directory, abort, redirect, url_for, flash
from pathlib import Path
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "n0xxx"

MOVIES_FOLDER = Path.home() / "movies"
MOVIES_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"mp4"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_movies(search=None):
    movies = []
    for file in MOVIES_FOLDER.glob("*.mp4"):
        size_mb = round(file.stat().st_size / (1024 * 1024), 1)
        name = file.name

        if search and search.lower() not in name.lower():
            continue

        movies.append({
            "name": name,
            "size": f"{size_mb} MB",
            "path": name
        })

    movies.sort(key=lambda x: x["name"].lower())
    return movies


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    movies = get_movies(search)
    return render_template("index.html", movies=movies, search=search)


@app.route("/play/<path:filename>")
def play(filename):
    if ".." in filename or not filename.endswith(".mp4"):
        abort(404)

    file_path = MOVIES_FOLDER / filename
    if not file_path.exists():
        abort(404)

    return render_template("player.html", filename=filename)


@app.route("/video/<path:filename>")
def serve_video(filename):
    return send_from_directory(MOVIES_FOLDER, filename)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == "POST":
        if "file" not in request.files:
            msg = "Nenhum arquivo selecionado"
            if is_ajax:
                return {"success": False, "message": msg}, 400
            flash(msg, "error")
            return redirect(url_for("upload"))

        file = request.files["file"]
        custom_name = request.form.get("name", "").strip()

        if file.filename == "":
            msg = "Nenhum arquivo selecionado"
            if is_ajax:
                return {"success": False, "message": msg}, 400
            flash(msg, "error")
            return redirect(url_for("upload"))

        if file and allowed_file(file.filename):
            if custom_name:
                if not custom_name.lower().endswith(".mp4"):
                    custom_name += ".mp4"
                filename = secure_filename(custom_name)
            else:
                filename = secure_filename(file.filename)

            save_path = MOVIES_FOLDER / filename

            if save_path.exists():
                msg = "Já existe um filme com esse nome!"
                if is_ajax:
                    return {"success": False, "message": msg}, 400
                flash(msg, "error")
                return redirect(url_for("upload"))

            file.save(save_path)
            msg = f"Filme '{filename}' adicionado com sucesso!"
            if is_ajax:
                return {"success": True, "message": msg}
            flash(msg, "success")
            return redirect(url_for("index"))
        else:
            msg = "Apenas arquivos .mp4 são permitidos"
            if is_ajax:
                return {"success": False, "message": msg}, 400
            flash(msg, "error")
            return redirect(url_for("upload"))

    return render_template("upload.html")


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_movie(filename):
    if ".." in filename or not filename.endswith(".mp4"):
        abort(404)

    file_path = MOVIES_FOLDER / filename
    if file_path.exists():
        file_path.unlink()
        flash(f"Filme '{filename}' removido!", "success")
    else:
        flash("Filme não encontrado.", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    from waitress import serve
    serve(
        app,
        host="0.0.0.0",
        port=5000,
        threads=4,
        max_request_body_size=1024 * 1024 * 1024 * 10  # 10 GB
    )
