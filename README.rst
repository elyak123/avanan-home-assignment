Avanan's Home Assignment
========================

Builing a Data Loss Prevention Tool

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

This is the exercise solution for Avanan's `Home Assignment <https://gist.github.com/chesstrian/eafa36a05dad589f487d0900881efc9e>`_.

The Data Loss Prevention Tool will detect any regular expressions saved by the user in the Django Admin and will delete such messages in the Slack channel that has been added by an administrator user of a workspace.


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

SetUp
-----

Setting Up environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to run the system you will to create a ``.envs`` directory at the root of the project to assign some environment variables for the django and mysql containers:

==================================  =========   =================   ===============================================================================
Variable                            Container   Location            Observations
----------------------------------  ---------   -----------------   -------------------------------------------------------------------------------
DJANGO_AWS_ACCESS_KEY_ID            Django      ``.envs/.django``   Access id from AWS user must have read and write permissions for SQS
DJANGO_AWS_SECRET_ACCESS_KEY        Django      ``.envs/.django``   AWS secret key
DJANGO_AWS_SQS_MAIN_QUEUE           Django      ``.envs/.django``   The name of the SQS queue that will be created on startup
DJANGO_DEFAULT_SUPERUSER_EMAIL      Django      ``.envs/.django``   Django's superuser email that will be created on startup
DJANGO_DEFAULT_SUPERUSER_USERNAME   Django      ``.envs/.django``   Django's superuser username that will be created on startup
DJANGO_DEFAULT_SUPERUSER_PASSWORD   Django      ``.envs/.django``   Django's superuser password
DJANGO_SECRET_KEY                   Django      ``.envs/.django``   Django's security secret key
DJANGO_SETTINGS_MODULE              Django      ``.envs/.django``   ``config.settings.production`` value recommended
SLACK_APP_TOKEN                     Django      ``.envs/.django``   Slack's app token; scopes and permissions will be described in the next section
SLACK_BOT_TOKEN                     Django      ``.envs/.django``   Slack's bot token
SLACK_USER_TOKEN                    Django      ``.envs/.django``   Slack's user token
USE_DOCKER                          Django      ``.envs/.django``    ``yes`` recommended
IPYTHONDIR                          Django      ``.envs/.django``    ``/app/.ipython`` recommended
MYSQL_PORT                          MySQL       ``.envs/.mysql``     ``3306`` recommended
MYSQL_ROOT_HOST                     MySQL       ``.envs/.mysql``     ``mysql`` value recomended
MYSQL_DATABASE                      MySQL       ``.envs/.mysql``     ``avanan`` value recomended
MYSQL_USER                          MySQL       ``.envs/.mysql``     MySQL's user
MYSQL_PASSWORD                      MySQL       ``.envs/.mysql``     MySQL's user's password
MYSQL_ALLOW_EMPTY_PASSWORD          MySQL       ``.envs/.mysql``    ``true`` recommended
==================================  =========   =================   ===============================================================================

Slack API configuration
^^^^^^^^^^^^^^^^^^^^^^^


1. First, to create a bot for our app we have to go to the Slack application panel in the `Slack API section <https://api.slack.com/apps>`_. Look for the "create new app" button.

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/1create_app.PNG
   :width: 600pt
   :align: center

2. Now, Click on "create an app from scratch"

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/2scratch_img.PNG
   :width: 300pt
   :align: center

3. Provide a name for your app, select the workspace where you need to create a bot

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/3name_workspace.PNG
   :width: 300pt
   :align: center

4. After this you will see the page to configure the app.

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/4settings.PNG
   :width: 400pt
   :align: center

Set the parameters to give access to your bot in your workspace.

5. Next, navigate to the "OAuth & Permissions" tab in the Features on the left panel.

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/5OAuth.PNG
   :width: 100pt
   :align: center

6. Under "Bot Token Scopes" section add the following scopes:

* app_mentions:read
* channels:history
* chat:write
* files:read
* groups:history
* im:history
* links:read
* mpim:history
* remote_files:write

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/6BotScopes.png
   :width: 400pt
   :align: center

7. Under "User Token Scopes" section add the following scopes:
* channels:history
* files:read
* groups:history
* chat:write
* im:read
* links:read
*  mpim:history

.. image:: https://pruebaelyak.s3.us-west-2.amazonaws.com/slack-config-img/7UserScopes.png
   :width: 400pt
   :align: center

8. Navigate to the event subscriptions menu and enable the Event API, toogle the button so that marks "on" and place the full url (domain included) for the event subscription
9. The url will be ``$YOUR_DOMAIN/slack/events/``
10. Having the service running, place the url, Slack will try to access the url and if it receives a ``200`` http code, the subscription will be authorized. Click Save changes.
11. Remember to instal the app with a user that has administrative permissions in the workplace.
12. The bot must be added to the workspace that will be monitoring.


DNS Configuration
^^^^^^^^^^^^^^^^^

Because we're using http events (instead of sockets method) we need a publicly accesible domain. If do have a it you can skip this section. If that is not possible you could create a ``ngrok`` to create an account and setup go to its documentation_.

.. _documentation: https://ngrok.com/docs#getting-started-expose


In another terminal you to run it do::

    $ ngrok http 8000

That will proxy the ``8000`` port to 80 or 443

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

Assuming that docker and docker compose are already installed and available in your ``PATH``, once the environment variables in its place, you could run::

    $ docker-compose up -f production.yml

