from flask import render_template, request
import logging
from logging.handlers import RotatingFileHandler
import json


def init_error(app):

    if app.debug is not True:
        app.logger.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler = RotatingFileHandler('error.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

    @app.errorhandler(404)
    def not_found(error):
        # return "<h1>404</h1>"
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):

        '''
        method = request.method,
                path = request.path,
                ip = request.remote_addr,
                agent_platform = request.user_agent.platform,
                agent_browser = request.user_agent.browser,
                agent_browser_version = request.user_agent.version,
                agent = request.user_agent.string,
                user=user
        '''

        app.logger.error(error)

        # return "<h1>500</h1>"
        return render_template('500.html'), 500

    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)

