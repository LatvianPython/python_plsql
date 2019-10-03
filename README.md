# python_plsql

# Description

Right now it's use is only academic, however potential applications would be to make testing PL/SQL easier by providing a simple way to call them from an easy to use language 

# How to use this right now?

What you need is just the client.py file, the cx_Oracle package (refer to it's documentation on how to install it) and an Oracle database you can point this script to.


# Example(s)

Hopefully if all goes well you will be able to call most of the PL/SQL code from Python
```Python
>>>plsql.simple_function(p_int=5)
10
```

Refer to tests for what is being supported right now, it is not a lot, but enough for a proof of concept (Creating an easy way to call PL/SQL from Python)
