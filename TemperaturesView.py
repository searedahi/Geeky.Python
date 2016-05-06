""" All the temperature webserver functions. """
from flask.ext.classy import FlaskView

class TemperaturesView(FlaskView):
    """all api temperature functionality"""

    # we'll make a list to hold some quotes for our app
    quotes = ["A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
              "If there is a way to do it better... find it. ~ Thomas Edison",
              "No one knows what he can do till he tries. ~ Publilius Syrus"]

    def index(self):
        """ root of the view. """
        return "<br>".join(self.quotes)

    def get(self, recordid):
        """ get of the view. """
        target_id = recordid
        return self.quotes[1] + target_id
