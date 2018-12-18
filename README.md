# OCDS Kingfisher Scrape - No Framework!



This is a Hacky McHack Face version so James could have something to push test data to process.

It's basically a copy of the old Kingfisher, with all Postgres and store stuff deleted.

Instead, if you look in ocds kingfisher/base.py you will see a new function push_to_server - this pushes data to a remote server.

Which remote server is currently hard coded in ocdskingfisher/config.py

If you want to run a source, run it using the same CLI command as the old code.

Hacky McHack Face!

Seriously, don't use this for real as it currently stands.
