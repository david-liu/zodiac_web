from service import app, initialize_app
from zodiac_web.utils import helper

initialize_app(helper.convert_to_abspath(__file__, 'APP.INI'))

if __name__ == "__main__":
    app.run()
