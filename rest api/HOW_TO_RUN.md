
This api was written in python and tested on:
  python2.6
  python2.7


Start by creating a [virtualenv][1] in a clone of the repository


    virtualenv -p $(which python2.6) .venv
    source .venv/bin/activate

The easiest way to run the tests is with `nosetests`. You need to install it
into the virtual environment, even if it is installed system-wide.

    pip install -r requirements.txt
    nosetests

NOTE: This api was designed to run on 127.0.0.1:5000

On the command line:

    python restapi/restapi.py

That will start the application. From another terminal window:

    curl -X PUT -v -H "content-type: application/json" -d '{"word": "gotya"}' 127.0.0.1:5000/word/gotya

If the command is successful it will return with 'HTTP/1.0 204 NO CONTENT'.

If the command sends data with a space, OR if the value of 'word' is not the same as the end word,
it will result in a 'HTTP/1.0 400 BAD REQUEST'.

For example:

    curl -X PUT -v -H "content-type: application/json" -d '{"word": "gotya2"}' 127.0.0.1:5000/word/gotya
    #You will notice that the word in data is different then the end word.

[1]: http://www.virtualenv.org/en/latest/
