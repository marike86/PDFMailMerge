"""One validated merge pipeline shared by desktop, CLI and interactive mode."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import zipfile

from .data_loader import load_data, data_to_dict_list
from .pdf_processor import get_form_field_names, detect_text_placeholders, fill_form_pdf, replace_text
from .utils import parse_naming_pattern, clean_dir


class MergeError(ValueError):
    pass


@dataclass
class MergePlan:
    template: str
    mode: str
    fields: list
    columns: list
    records: list
    mapping: dict

    def values(self, index):
        record = self.records[index]
        return {name: str(record.get(self.mapping[name], "")) for name in self.fields}


@dataclass
class MergeResult:
    total: int
    files: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    cancelled: bool = False
    archive: str = ""


def inspect_inputs(template, data_path, mode="auto", mapping=None):
    if mode not in ("auto", "form", "text"):
        raise MergeError(f"Unsupported mode: {mode}")
    df = load_data(data_path)
    if df.empty:
        raise MergeError("数据文件没有记录 / Data source is empty")
    columns = [str(c).strip() for c in df.columns]
    if any(not c for c in columns) or len(set(columns)) != len(columns):
        raise MergeError("数据列名为空或重复 / Empty or duplicate columns")
    df.columns = columns
    forms = get_form_field_names(template) if mode != "text" else []
    if mode == "auto":
        mode = "form" if forms else "text"
    fields = forms if mode == "form" else detect_text_placeholders(template)
    if not fields:
        raise MergeError("模板未发现可填充字段或 {{占位符}} / No fields found")
    selected = {name: (mapping or {}).get(name, name) for name in fields}
    return MergePlan(str(Path(template).resolve()), mode, fields, columns,
                     data_to_dict_list(df), selected)


def validate_mapping(plan):
    missing = [name for name in plan.fields if plan.mapping.get(name) not in plan.columns]
    if missing:
        raise MergeError("请映射模板字段 / Missing data for fields: " + ", ".join(missing))


def check_output(output, template, data_path, clean=False):
    if not str(output).strip():
        raise MergeError("请选择输出目录 / Output directory is required")
    target = Path(output).resolve()
    if target.exists() and not target.is_dir():
        raise MergeError("输出路径不是文件夹 / Output path is not a directory")
    if clean:
        for source in (template, data_path):
            source = Path(source).resolve()
            if target == source or target in source.parents:
                raise MergeError("不能清空存放输入文件的目录 / Inputs are inside output directory")
    return target


def render_record(plan, index, output):
    validate_mapping(plan)
    operation = fill_form_pdf if plan.mode == "form" else replace_text
    operation(plan.template, plan.values(index), str(output))


def _reserve(directory, stem):
    """Exclusive reservation handles existing files and case-insensitive collisions."""
    for suffix in range(1000000):
        name = f"{stem}{'_' + str(suffix + 1) if suffix else ''}.pdf"
        path = directory / name
        try:
            with path.open("xb"):
                pass
            return path
        except FileExistsError:
            continue
    raise MergeError("Too many duplicate filenames")


def run_merge(plan, output, pattern="document_{row}", zip_enabled=False,
              cancel=None, progress=None, clean=False, data_path=""):
    validate_mapping(plan)
    if not pattern.strip():
        raise MergeError("命名规则不能为空 / Naming pattern is empty")
    import re
    unknown = set(re.findall(r"\{([^{}]+)\}", pattern)) - set(plan.columns) - {"row", "timestamp"}
    if unknown:
        raise MergeError("命名规则包含未知字段 / Unknown naming fields: " + ", ".join(sorted(unknown)))
    target = check_output(output, plan.template, data_path, clean)
    if clean and not clean_dir(str(target)):
        raise MergeError("Cannot clean output directory")
    target.mkdir(parents=True, exist_ok=True)
    result = MergeResult(len(plan.records))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for index, record in enumerate(plan.records):
        if cancel and cancel.is_set():
            result.cancelled = True
            break
        path = None
        try:
            stem = parse_naming_pattern(pattern, {**record, "row": index + 1, "timestamp": timestamp})
            if stem.lower().endswith(".pdf"):
                stem = stem[:-4] or "document"
            path = _reserve(target, stem)
            render_record(plan, index, path)
            result.files.append(str(path))
            message = path.name
        except Exception as exc:
            if path:
                path.unlink(missing_ok=True)
            message = f"第 {index + 1} 行: {exc}"
            result.errors.append(message)
        if progress:
            progress(index + 1, result.total, message)
    if zip_enabled and result.files and not result.cancelled:
        archive = target / f"PDFMailMerge_{datetime.now():%Y%m%d_%H%M%S_%f}.zip"
        try:
            with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as bundle:
                for filename in result.files:
                    bundle.write(filename, Path(filename).name)
            result.archive = str(archive)
        except Exception as exc:
            archive.unlink(missing_ok=True)
            result.errors.append(f"ZIP: {exc}")
    return result
