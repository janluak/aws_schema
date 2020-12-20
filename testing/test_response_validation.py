from os.path import dirname, realpath
from os import chdir, getcwd
from pytest import fixture


@fixture
def response_validation_env():
    actual_cwd = getcwd()
    chdir(dirname(realpath(__file__)))
    yield
    chdir(actual_cwd)


def test_passing_string_response(response_validation_env, caplog):
    from aws_schema.response_validation import (
        ResponseDataValidator,
    )

    response_schema_file = (
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource.json"
    )
    response_data = {
        "statusCode": 200,
        "body": "single_allowed_answer",
        "headers": {"Content-Type": "text/plain"},
    }
    ResponseDataValidator(
        file=response_schema_file,
        response_data=response_data,
        httpMethod="POST",
        api_name="test_response_resource",
    )
    assert len(caplog.messages) == 0


def test_passing_object_response(response_validation_env, caplog):
    from aws_schema.response_validation import (
        ResponseDataValidator,
    )

    response_schema_file = (
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource.json"
    )
    response_data = {
        "statusCode": 200,
        "body": {"key1": 1, "key2": 2},
        "headers": {"Content-Type": "text/plain"},
    }
    ResponseDataValidator(
        file=response_schema_file,
        response_data=response_data,
        httpMethod="POST",
        api_name="test_response_resource",
    )
    assert len(caplog.messages) == 0


def test_wrong_string_response(response_validation_env, caplog):
    from aws_schema.response_validation import (
        ResponseDataValidator,
    )

    response_schema_file = (
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource.json"
    )
    response_data = {
        "statusCode": 200,
        "body": "false_answer",
        "headers": {"Content-Type": "text/plain"},
    }
    ResponseDataValidator(
        file=response_schema_file,
        response_data=response_data,
        httpMethod="POST",
        api_name="test_response_resource",
    )

    assert len(caplog.messages) == 1
    assert "invalid response" in caplog.text


def test_unspecified_status_code_response(response_validation_env, caplog):
    from aws_schema.response_validation import (
        ResponseDataValidator,
    )

    response_schema_file = (
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource.json"
    )
    response_data = {
        "statusCode": 418,
        "body": "I'm a teapot",
        "headers": {"Content-Type": "text/plain"},
    }
    ResponseDataValidator(
        file=response_schema_file,
        response_data=response_data,
        httpMethod="POST",
        api_name="test_response_resource",
    )

    assert len(caplog.messages) == 1
    assert "no specified response schema available for statusCode 418" in caplog.text
