import contextlib
import io
import json
import logging
import os
import tempfile

import pytest
from translator_asm import translate
import machine


@pytest.mark.golden_test("golden/*.yml")
def test_bar(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdir:
        source_file = os.path.join(tmpdir, "source.yaasm")
        target_file = os.path.join(tmpdir, "source.json")
        input_token = [ord(i) for i in golden["stdin"].rstrip("\n")]
        input_token.append(0)

        with open(source_file, "w", encoding="utf-8") as file:
            file.write(golden["in_source"])

        with open(input_token, "w", encoding="utf-8") as file:
            file.write(golden["in_stdio"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translate(golden["source_code"], target_file)
            print("=" * 5)
            code_dict = json.load(open(target_file, encoding="utf-8"))
            machine.main(code_dict, input_token)

        with open(target_file, encoding="utf-8") as file:
            code = file.read()

        assert code == golden.out["out_code"]
        assert stdout.getvalue().rstrip("\n") == golden.out["stdout"]
        assert caplog.text.rstrip("\n") == golden.out["out_log"]
