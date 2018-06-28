import logging

from oyoyo.ircevents import generated_events, protocol_events,\
                            all_events, numeric_events

# avoiding regex
def parse_raw_irc_command(element):
    """
    This function parses a raw irc command and returns a tuple
    of (prefix, command, args).
    The following is a psuedo BNF of the input text:

    <message>  ::= [':' <prefix> <SPACE> ] <command> <params> <crlf>
    <prefix>   ::= <servername> | <nick> [ '!' <user> ] [ '@' <host> ]
    <command>  ::= <letter> { <letter> } | <number> <number> <number>
    <SPACE>    ::= ' ' { ' ' }
    <params>   ::= <SPACE> [ ':' <trailing> | <middle> <params> ]

    <middle>   ::= <Any *non-empty* sequence of octets not including SPACE
                   or NUL or CR or LF, the first of which may not be ':'>
    <trailing> ::= <Any, possibly *empty*, sequence of octets not including
                     NUL or CR or LF>

    <crlf>     ::= CR LF
    """
    parts = element.strip().split(bytes(" ", "utf_8"))
    if parts[0].startswith(bytes(':', 'utf_8')):
        prefix = parts[0][1:]
        command = parts[1]
        args = parts[2:]
    else:
        prefix = None
        command = parts[0]
        args = parts[1:]

    if command.isdigit():
        try:
            command = numeric_events[command]
        except KeyError:
            logging.debug('unknown numeric event {0}'.format(command))
    command = command.lower()
    if isinstance(command, bytes): command = command.decode("utf_8")

    if args[0].startswith(bytes(':', 'utf_8')):
        args = [bytes(" ", "utf_8").join(args)[1:]]
    else:
        for idx, arg in enumerate(args):           
            if arg.startswith(bytes(':', 'utf_8')):
                args = args[:idx] + [bytes(" ", 'utf_8').join(args[idx:])[1:]]
                break

    return (prefix, command, args)


def parse_nick(name):
    """ parse a nickname and return a tuple of (nick, mode, user, host)

    <nick> [ '!' [<mode> = ] <user> ] [ '@' <host> ]
    """

    try:
        nick, rest = name.split('!')
    except ValueError:
        return (name, None, None, None)
    try:
        mode, rest = rest.split('=')
    except ValueError:
        mode, rest = None, rest
    try:
        user, host = rest.split('@')
    except ValueError:
        return (nick, mode, rest, None)

    return (nick, mode, user, host)
 
