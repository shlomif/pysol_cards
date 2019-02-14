2. Edit the ``/etc/pysol_cards/pysol_cards.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://pysol_cards:PYSOL_CARDS_DBPASS@controller/pysol_cards
