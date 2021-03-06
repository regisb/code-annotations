"""
Helpers for code_annotations scripts.
"""
import os
import sys

import click


def fail(msg):
    """
    Log the message and exit.

    Args:
        msg: Message to log
    """
    click.secho(msg, fg="red")
    sys.exit(1)


class VerboseEcho(object):
    """
    Helper to handle verbosity-dependent logging.
    """

    verbosity = 1

    def __call__(self, output, **kwargs):
        """
        Echo the given output regardless of verbosity level.

        This is just a convenience method to avoid lots of `self.echo.echo()`.

        Args:
            output: Text to output
            kwargs: Any additional keyword args to pass to click.echo
        """
        self.echo(output, **kwargs)

    def set_verbosity(self, verbosity):
        """
        Override the default verbosity level.

        Args:
            verbosity: The verbosity level to set to
            kwargs: Any additional keyword args to pass to click.echo
        """
        self.verbosity = verbosity
        self.echo_v("Verbosity level set to {}".format(verbosity))

    def echo(self, output, verbosity_level=0, **kwargs):
        """
        Echo the given output, if over the verbosity threshold.

        Args:
            output: Text to output
            verbosity_level: Only output if our verbosity level is >= this.
            kwargs: Any additional keyword args to pass to click.echo
        """
        if verbosity_level <= self.verbosity:
            click.secho(output, **kwargs)

    def echo_v(self, output, **kwargs):
        """
        Echo the given output if verbosity level is >= 1.

        Args:
            output: Text to output
            kwargs: Any additional keyword args to pass to click.echo
        """
        self.echo(output, 1, **kwargs)

    def echo_vv(self, output, **kwargs):
        """
        Echo the given output if verbosity level is >= 2.

        Args:
            output: Text to output
            kwargs: Any additional keyword args to pass to click.echo
        """
        self.echo(output, 2, **kwargs)

    def echo_vvv(self, output, **kwargs):
        """
        Echo the given output if verbosity level is >= 3.

        Args:
            output: Text to output
            kwargs: Any additional keyword args to pass to click.echo
        """
        self.echo(output, 3, **kwargs)


def clean_abs_path(filename_to_clean, parent_path):
    """
    Safely strips the parent path from the given filename, leaving only the relative path.

    Args:
        filename_to_clean: Input filename
        parent_path: Path to remove from the input

    Returns:
        Updated path
    """
    # If we are operating on only one file we don't know what to strip off here,
    # just return the whole thing.
    if filename_to_clean == parent_path:
        return os.path.basename(filename_to_clean)
    return os.path.relpath(filename_to_clean, parent_path)


def get_annotation_regex(annotation_regexes):
    """
    Return the full regex to search inside comments for configured annotations.

    Args:
        annotation_regexes: List of re.escaped annotation tokens to search for.

    Returns:
        Regex ready for searching comments for annotations.
    """
    # pylint: disable=pointless-string-statement
    r"""
    This format string/regex finds our annotation token and choices / comments inside a comment:

    [\s\S]*? - Strip out any characters between the start of the comment and the annotation
    ({})     - {} is a Python format string that will be replaced with a regex escaped and
               then or-joined to make a list of the annotation tokens we're looking for
               Ex: (\.\.\ pii\:\:|\.\.\ pii\_types\:\:)
    (.*)     - and capture all characters until the end of the line

    Returns a 2-tuple of found annotation token and annotation comment

    TODO: Make multi line annotation comments work again.
    """
    annotation_regex = r'[\s\S]*?({})(.*)'
    return annotation_regex.format('|'.join(annotation_regexes))
