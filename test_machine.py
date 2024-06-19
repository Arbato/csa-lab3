import contextlib
import io
import json
import logging
import os
import tempfile

import machine
import pytest
import translator_asm


@pytest.mark.golden_test("golden/*.yml")
def test_bar(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdir:
        source_file = os.path.join(tmpdir, "source.yaasm")
        input_stream = os.path.join(tmpdir, "input.txt")
        target_file = os.path.join(tmpdir, "source.json")

        with open(source_file, "w", encoding="utf-8") as file:
            file.write(golden["source_code"])

        with open(input_stream, "w", encoding="utf-8") as file:
            file.write(golden["stdin"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator_asm.main(source_file, target_file)
            code_dict = json.load(open(target_file, encoding="utf-8"))

            input_stream = open(input_stream, encoding="utf-8").read()

            machine.main(code_dict, input_stream)


        with open(target_file, encoding="utf-8") as file:
            code = file.read()

        assert [x.strip() for x in code.strip().split("\n")] == [
            x.strip() for x in golden.out["out_code"].strip().split("\n")
        ]
        assert stdout.getvalue().strip("\n") == golden.out["stdout"].strip("\n")
        assert caplog.text.rstrip("\n") == golden.out["out_log"].rstrip("\n")
