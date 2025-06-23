from flask_classful import FlaskView, route


class TestView(FlaskView):
    @route("/", methods=["GET"])
    def test(self):
        return "test"
