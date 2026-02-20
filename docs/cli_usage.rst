CLI Tool Usage
==============

The Eventyay Python SDK comes with a built-in command-line interface (CLI) for managing your account without writing code.

Setup
-----
The CLI is installed automatically when you run ``pip install .``.
To authenticate, you can set an environment variable:

.. code-block:: bash

   export EVENTYAY_API_KEY="your_token"

Basic Commands
--------------

List Organizers:

.. code-block:: bash

   eventyay organizers list

List Events:

.. code-block:: bash

   eventyay events list

Managing Organizers
-------------------

Create a new organizer:

.. code-block:: bash

   eventyay organizers create "My Org" --description "Best org ever"

Managing Events
---------------

Create an event:

.. code-block:: bash

   eventyay events create "Tech Talk" tech-talk-2026 2026-10-10T10:00:00Z 2026-10-10T11:00:00Z UTC
