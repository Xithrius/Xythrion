import pytest

from bot.extensions.mapping._utils.link_converter import DestinationType, validate_destination


def test_validate_destination_no_path_raises_value_error() -> None:
    with pytest.raises(ValueError):
        validate_destination("")


def test_validate_destination_random_characters_raises_value_error() -> None:
    with pytest.raises(ValueError):
        validate_destination("asdf")


def test_validate_destination_single_forward_slash_raises_value_error() -> None:
    with pytest.raises(ValueError):
        validate_destination("/")


def test_validate_destination_incomplete_url_raises_value_error() -> None:
    with pytest.raises(ValueError):
        validate_destination("https://")


def test_validate_destination_root_to_html_is_valid_xpath() -> None:
    x = validate_destination("/html")

    assert x == DestinationType.XPATH


def test_validate_destination_full_xpath() -> None:
    x = validate_destination("/html/body/div")

    assert x == DestinationType.XPATH


def test_validate_destination_very_long_xpath() -> None:
    y = (
        "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]"
        "/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/div"
        "/ytd-subscribe-button-renderer/yt-smartimation/div/__slot-el"
        "/yt-animated-action/div[1]/__slot-el/div"
        "/ytd-subscription-notification-toggle-button-renderer-next"
        "/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
    )
    x = validate_destination(y)

    assert x == DestinationType.XPATH


def test_validate_destination_example_com_is_url() -> None:
    x = validate_destination("https://example.com")

    assert x == DestinationType.URL
