#!/usr/bin/env python3

import base64
import os

import pytest


@pytest.fixture(scope="session")
def valid_credentials_path(tmpdir_factory):

    # This fixture will return a path to a valid configuration file
    # that contain valid credentials to interact with the Play Store.

    if os.environ.get("GITHUB_ACTIONS", "false").lower() == "true":
        # Automatic CI testing.
        test_credentials = base64.b64decode(os.environ["CREDENTIALS"]).decode("ascii")
    else:
        # Local testing. Make sure to use a valid json file with the credentials.
        credentials_location = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.path.pardir,
            "private_credentials.json",
        )
        if not os.path.isfile(credentials_location):
            # Use the default credentials file if no private credentials are present.
            credentials_location = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.path.pardir,
                "credentials.json",
            )

        with open(
            credentials_location,
            "r",
        ) as file:
            test_credentials = file.read()

    tmp_credentials_file = tmpdir_factory.mktemp("credentials").join("credentials.json")

    with open(str(tmp_credentials_file), "w") as file:
        file.write(test_credentials)

    return str(tmp_credentials_file)


@pytest.fixture(scope="session")
def wrong_credentials_path(tmpdir_factory):

    # This fixture will return a path to a configuration file
    # which contains wrong credentials.

    tmp_credentials_file = tmpdir_factory.mktemp("credentials").join("credentials.json")

    with open(str(tmp_credentials_file), "w") as file:
        file.write(
            '[{"USERNAME":"bad.username","PASSWORD":"invalid_password",'
            '"ANDROID_ID":"android","LANG_CODE":"en_US","LANG":"us"}]'
        )

    return str(tmp_credentials_file)


@pytest.fixture(scope="session")
def incomplete_configuration_path(tmpdir_factory):

    # This fixture will return a path to a configuration file
    # which does not contain all the required fields.

    tmp_credentials_file = tmpdir_factory.mktemp("credentials").join("credentials.json")

    with open(str(tmp_credentials_file), "w") as file:
        file.write('[{"ANDROID_ID":"android","LANG_CODE":"en_US","LANG":"us"}]')

    return str(tmp_credentials_file)


@pytest.fixture(scope="session")
def corrupted_configuration_path(tmpdir_factory):

    # This fixture will return a path to a corrupted configuration file.

    tmp_credentials_file = tmpdir_factory.mktemp("credentials").join("credentials.json")

    with open(str(tmp_credentials_file), "w") as file:
        file.write('[{"ANDROID_ID": invalid json')

    return str(tmp_credentials_file)


@pytest.fixture(scope="session")
def download_folder_path(tmpdir_factory):

    # This fixture will return a path to a folder where to download the applications.

    tmp_download_directory = tmpdir_factory.mktemp("download")

    return str(tmp_download_directory)
