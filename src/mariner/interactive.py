import sys

from cliff import interactive


class MarinerInteractive(interactive.InteractiveApp):

    def __init__(self, parent_app, command_manager, stdin, stdout):
        self.parent_app = parent_app
        if not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
            self.prompt = '(%s) ' % parent_app.NAME
        else:
            # batch/pipe mode
            self.prompt = ''
        self.command_manager = command_manager
        import cmd2
        cmd2.Cmd.__init__(
            self,
            'tab',
            stdin=stdin,
            stdout=stdout,
            persistent_history_file='/tmp/mariner'
        )
