from src import create_app
import os

app = create_app()


@app.route("/", methods=['GET'])
def helth_check():
    return {"message": "Football API is running", "status": "healthy"}


if __name__ == "__main__":
    app.run(
        debug=app.config.get("DEBUG", False),
        host=os.getenv("HOST", "0.0.0.0"),
        port=os.getenv("PORT", 5000)
    )
