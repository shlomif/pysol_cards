Prerequisites
-------------

Before you install and configure the cards service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``pysol_cards`` database:

     .. code-block:: none

        CREATE DATABASE pysol_cards;

   * Grant proper access to the ``pysol_cards`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON pysol_cards.* TO 'pysol_cards'@'localhost' \
          IDENTIFIED BY 'PYSOL_CARDS_DBPASS';
        GRANT ALL PRIVILEGES ON pysol_cards.* TO 'pysol_cards'@'%' \
          IDENTIFIED BY 'PYSOL_CARDS_DBPASS';

     Replace ``PYSOL_CARDS_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``pysol_cards`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt pysol_cards

   * Add the ``admin`` role to the ``pysol_cards`` user:

     .. code-block:: console

        $ openstack role add --project service --user pysol_cards admin

   * Create the pysol_cards service entities:

     .. code-block:: console

        $ openstack service create --name pysol_cards --description "cards" cards

#. Create the cards service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        cards public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        cards internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        cards admin http://controller:XXXX/vY/%\(tenant_id\)s
