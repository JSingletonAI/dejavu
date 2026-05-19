from typer.testing import CliRunner

from dejavu.cli import app


def test_dejavu_cli_help():
    result = CliRunner().invoke(app, ['--help'])
    assert result.exit_code == 0
    assert 'Deja Vu' in result.output
