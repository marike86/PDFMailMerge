import os
import pytest
from src.utils import (
    ensure_dir,
    clean_dir,
    get_file_hash,
    list_files,
    format_file_size,
    get_timestamp,
    create_zip_archive,
    extract_zip_archive,
    parse_naming_pattern,
    validate_path,
    get_progress_bar,
    print_progress,
    truncate_string,
    format_duration,
    is_pdf_file,
    get_pdf_stats,
)


class TestEnsureDir:

    def test_create_new_directory(self, tmp_path):
        new_dir = str(tmp_path / "new_dir")
        assert not os.path.exists(new_dir)
        assert ensure_dir(new_dir) is True
        assert os.path.isdir(new_dir)

    def test_existing_directory(self, tmp_path):
        assert ensure_dir(str(tmp_path)) is True

    def test_nested_directory(self, tmp_path):
        nested = str(tmp_path / "a" / "b" / "c")
        assert ensure_dir(nested) is True
        assert os.path.isdir(nested)


class TestCleanDir:

    def test_clean_existing_directory(self, tmp_path):
        test_dir = tmp_path / "to_clean"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")
        (test_dir / "subdir").mkdir()
        (test_dir / "subdir" / "inner.txt").write_text("inner")
        assert clean_dir(str(test_dir)) is True
        assert os.path.isdir(test_dir)
        assert list(os.listdir(test_dir)) == []

    def test_clean_nonexistent_directory(self, tmp_path):
        target = tmp_path / "does_not_exist"
        assert clean_dir(str(target)) is True
        assert os.path.isdir(target)

    def test_clean_empty_directory(self, tmp_path):
        test_dir = tmp_path / "empty"
        test_dir.mkdir()
        assert clean_dir(str(test_dir)) is True


class TestGetFileHash:

    def test_md5_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h = get_file_hash(str(f), "md5")
        assert len(h) == 32
        assert h == "5eb63bbbe01eeed093cb22bb8f5acdc3"

    def test_sha1_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h = get_file_hash(str(f), "sha1")
        assert len(h) == 40

    def test_sha256_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h = get_file_hash(str(f), "sha256")
        assert len(h) == 64

    def test_nonexistent_file(self):
        assert get_file_hash("nonexistent.txt") == ""

    def test_default_algorithm_is_md5(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("abc")
        h1 = get_file_hash(str(f))
        h2 = get_file_hash(str(f), "md5")
        assert h1 == h2


class TestListFiles:

    def test_list_all_files(self, tmp_path):
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.pdf").write_text("b")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "c.txt").write_text("c")
        result = list_files(str(tmp_path))
        assert len(result) == 3

    def test_list_with_extension_filter(self, tmp_path):
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.pdf").write_text("b")
        (tmp_path / "c.csv").write_text("c")
        result = list_files(str(tmp_path), ".txt")
        assert len(result) == 1
        assert result[0].endswith(".txt")

    def test_empty_directory(self, tmp_path):
        result = list_files(str(tmp_path))
        assert result == []

    def test_nonexistent_directory(self):
        result = list_files("nonexistent_dir")
        assert result == []


class TestFormatFileSize:

    @pytest.mark.parametrize("size_bytes,expected", [
        (0, "0.0 B"),
        (500, "500.0 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (1048576, "1.0 MB"),
        (1073741824, "1.0 GB"),
        (1099511627776, "1.0 TB"),
    ])
    def test_format_sizes(self, size_bytes, expected):
        assert format_file_size(size_bytes) == expected

    def test_exact_kb_boundary(self):
        assert format_file_size(1023) == "1023.0 B"
        assert format_file_size(1024) == "1.0 KB"


class TestGetTimestamp:

    def test_timestamp_format(self):
        ts = get_timestamp()
        assert len(ts) == 15
        assert ts[8] == "_"
        assert ts[:8].isdigit()
        assert ts[9:].isdigit()


class TestCreateZipArchive:

    def test_create_zip_with_subdirs(self, tmp_path):
        src = tmp_path / "source"
        src.mkdir()
        (src / "file1.txt").write_text("content1")
        sub = src / "sub"
        sub.mkdir()
        (sub / "file2.txt").write_text("content2")
        zip_path = str(tmp_path / "out" / "archive.zip")
        assert create_zip_archive(str(src), zip_path) is True
        assert os.path.exists(zip_path)
        assert os.path.getsize(zip_path) > 0

    def test_create_zip_without_subdirs(self, tmp_path):
        src = tmp_path / "source"
        src.mkdir()
        (src / "file1.txt").write_text("content1")
        sub = src / "sub"
        sub.mkdir()
        (sub / "file2.txt").write_text("content2")
        zip_path = str(tmp_path / "archive.zip")
        assert create_zip_archive(str(src), zip_path, include_subdirs=False) is True
        assert os.path.exists(zip_path)

    def test_create_zip_nonexistent_source(self, tmp_path):
        zip_path = str(tmp_path / "archive.zip")
        result = create_zip_archive("nonexistent_dir", zip_path)
        assert result is False


class TestExtractZipArchive:

    def test_extract_zip(self, tmp_path):
        src = tmp_path / "source"
        src.mkdir()
        (src / "file1.txt").write_text("hello")
        zip_path = str(tmp_path / "archive.zip")
        create_zip_archive(str(src), zip_path)
        extract_dir = str(tmp_path / "extracted")
        assert extract_zip_archive(zip_path, extract_dir) is True
        assert os.path.exists(os.path.join(extract_dir, "file1.txt"))

    def test_extract_nonexistent_zip(self, tmp_path):
        result = extract_zip_archive("nonexistent.zip", str(tmp_path / "out"))
        assert result is False


class TestParseNamingPattern:

    def test_simple_pattern(self):
        data = {"name": "张三", "row": 1}
        assert parse_naming_pattern("{name}_{row}", data) == "张三_1"

    def test_unsafe_characters_replaced(self):
        data = {"name": 'test/file\\name:with*special?"chars<>|'}
        result = parse_naming_pattern("{name}", data)
        assert "/" not in result
        assert "\\" not in result
        assert ":" not in result
        assert "*" not in result
        assert "?" not in result
        assert '"' not in result
        assert "<" not in result
        assert ">" not in result
        assert "|" not in result

    def test_default_name(self):
        assert parse_naming_pattern("", {}) == "document"
        assert parse_naming_pattern("  ", {}) == "document"

    def test_no_matching_fields(self):
        data = {"other": "value"}
        result = parse_naming_pattern("{name}", data)
        assert result == "{name}"

    def test_numeric_value(self):
        data = {"row": 42}
        result = parse_naming_pattern("doc_{row}", data)
        assert result == "doc_42"


class TestValidatePath:

    def test_empty_path(self):
        valid, msg = validate_path("")
        assert valid is False
        assert "empty" in msg

    def test_none_path(self):
        valid, msg = validate_path(None)
        assert valid is False

    def test_existing_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("x")
        valid, msg = validate_path(str(f))
        assert valid is True

    def test_nonexistent_path_must_exist(self):
        valid, msg = validate_path("nonexistent_path", must_exist=True)
        assert valid is False
        assert "does not exist" in msg

    def test_nonexistent_path_not_must_exist(self):
        valid, msg = validate_path("some/new/path", must_exist=False)
        assert valid is True

    def test_writable_directory(self, tmp_path):
        valid, msg = validate_path(str(tmp_path))
        assert valid is True

    def test_file_not_dir(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("x")
        valid, msg = validate_path(str(f))
        assert valid is True


class TestGetProgressBar:

    def test_zero_progress(self):
        bar = get_progress_bar(0, 100)
        assert "0%" in bar
        assert "0/100" in bar

    def test_half_progress(self):
        bar = get_progress_bar(50, 100)
        assert "50%" in bar
        assert "50/100" in bar

    def test_complete_progress(self):
        bar = get_progress_bar(100, 100)
        assert "100%" in bar
        assert "100/100" in bar

    def test_total_zero(self):
        bar = get_progress_bar(0, 0)
        assert "100%" in bar

    def test_custom_width(self):
        bar = get_progress_bar(5, 10, width=20)
        assert "=" * 10 in bar
        assert "-" * 10 in bar

    def test_bar_format(self):
        bar = get_progress_bar(50, 100)
        assert bar.startswith("[")
        assert "]" in bar
        assert "50%" in bar


class TestPrintProgress:

    def test_print_progress(self, capsys):
        print_progress(50, 100, prefix="Test:", suffix="done", width=30)
        captured = capsys.readouterr()
        assert "50%" in captured.out
        assert "Test:" in captured.out
        assert "done" in captured.out

    def test_print_progress_completes(self, capsys):
        print_progress(100, 100, prefix="P:", width=20)
        captured = capsys.readouterr()
        assert "100%" in captured.out


class TestTruncateString:

    def test_short_string_unchanged(self):
        assert truncate_string("hello", 10) == "hello"

    def test_exact_length_unchanged(self):
        assert truncate_string("hello", 5) == "hello"

    def test_long_string_truncated(self):
        result = truncate_string("hello world", 8)
        assert len(result) == 8
        assert result.endswith("...")

    def test_custom_suffix(self):
        result = truncate_string("hello world", 8, suffix="~~")
        assert result.endswith("~~")

    def test_very_short_max(self):
        result = truncate_string("hello", 3)
        assert len(result) == 3


class TestFormatDuration:

    def test_seconds(self):
        assert format_duration(5.5) == "5.50s"
        assert format_duration(0.01) == "0.01s"

    def test_minutes(self):
        assert format_duration(90) == "1m 30s"
        assert format_duration(120) == "2m 0s"

    def test_hours(self):
        assert format_duration(3600) == "1h 0m"
        assert format_duration(5400) == "1h 30m"
        assert format_duration(3661) == "1h 1m"


class TestIsPdfFile:

    def test_valid_pdf(self, tmp_path):
        pdf = tmp_path / "test.pdf"
        pdf.write_bytes(b"%PDF-1.4 some content")
        assert is_pdf_file(str(pdf)) is True

    def test_non_pdf(self, tmp_path):
        txt = tmp_path / "test.txt"
        txt.write_text("not a pdf")
        assert is_pdf_file(str(txt)) is False

    def test_nonexistent_file(self):
        assert is_pdf_file("nonexistent.pdf") is False

    def test_empty_file(self, tmp_path):
        pdf = tmp_path / "empty.pdf"
        pdf.write_bytes(b"")
        assert is_pdf_file(str(pdf)) is False

    def test_real_pdf(self, tmp_path, simple_pdf):
        assert is_pdf_file(simple_pdf) is True


class TestGetPdfStats:

    def test_empty_directory(self, tmp_path):
        stats = get_pdf_stats(str(tmp_path))
        assert stats["total_files"] == 0
        assert stats["total_size"] == 0
        assert stats["avg_size"] == 0
        assert stats["smallest"] is None
        assert stats["largest"] is None

    def test_with_pdf_files(self, tmp_path, simple_pdf):
        stats = get_pdf_stats(str(tmp_path))
        assert stats["total_files"] == 1
        assert stats["total_size"] > 0
        assert stats["avg_size"] > 0
        assert stats["smallest"] is not None
        assert stats["largest"] is not None

    def test_nonexistent_directory(self):
        stats = get_pdf_stats("nonexistent_dir")
        assert stats["total_files"] == 0
