"""Tests for the file_access module."""

import pytest
from file_access import enable_file_access, is_file_type_allowed, get_file_extension


class TestGetFileExtension:
    def test_returns_lowercase_extension(self):
        assert get_file_extension("report.TXT") == ".txt"

    def test_returns_extension_with_dot(self):
        assert get_file_extension("data.csv") == ".csv"

    def test_no_extension_returns_empty_string(self):
        assert get_file_extension("noextension") == ""

    def test_hidden_file_with_no_extension(self):
        assert get_file_extension(".hiddenfile") == ""

    def test_multiple_dots_returns_last_extension(self):
        assert get_file_extension("archive.tar.gz") == ".gz"


class TestIsFileTypeAllowed:
    def test_allowed_text_extension(self):
        assert is_file_type_allowed("notes.txt") is True

    def test_allowed_data_extension(self):
        assert is_file_type_allowed("config.json") is True

    def test_disallowed_extension(self):
        assert is_file_type_allowed("script.py") is False

    def test_no_extension_not_allowed(self):
        assert is_file_type_allowed("Makefile") is False

    def test_allowed_types_filter(self):
        # .csv is text but not data
        assert is_file_type_allowed("data.csv", allowed_types=["text"]) is True
        assert is_file_type_allowed("data.csv", allowed_types=["data"]) is False

    def test_empty_allowed_types_disallows_all(self):
        assert is_file_type_allowed("notes.txt", allowed_types=[]) is False

    def test_unknown_category_in_allowed_types(self):
        assert is_file_type_allowed("notes.txt", allowed_types=["nonexistent"]) is False


class TestEnableFileAccess:
    def test_grants_access_for_allowed_file(self):
        result = enable_file_access("alice", "report.pdf")
        assert result["access_granted"] is True
        assert result["user"] == "alice"
        assert result["filename"] == "report.pdf"

    def test_denies_access_for_disallowed_file(self):
        result = enable_file_access("alice", "script.exe")
        assert result["access_granted"] is False
        assert ".exe" in result["reason"]

    def test_denies_access_for_empty_user(self):
        result = enable_file_access("", "report.pdf")
        assert result["access_granted"] is False
        assert "Invalid user" in result["reason"]

    def test_denies_access_for_blank_user(self):
        result = enable_file_access("   ", "report.pdf")
        assert result["access_granted"] is False

    def test_denies_access_for_empty_filename(self):
        result = enable_file_access("alice", "")
        assert result["access_granted"] is False
        assert "Invalid filename" in result["reason"]

    def test_grants_access_with_type_filter(self):
        result = enable_file_access("bob", "data.json", allowed_types=["data"])
        assert result["access_granted"] is True

    def test_denies_access_with_restrictive_type_filter(self):
        result = enable_file_access("bob", "notes.txt", allowed_types=["data"])
        assert result["access_granted"] is False

    def test_case_insensitive_extension(self):
        result = enable_file_access("carol", "photo.PNG")
        assert result["access_granted"] is True
