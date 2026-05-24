# PDF Mail Merge Tool - Portable Version

## 📦 Version Information

**Version Type**: Portable Package (开箱即用版)  
**Version Number**: 1.0.0  
**Release Date**: 2026-05-18  
**Target Users**: Non-technical users, beginners  
**Features**: Zero configuration, all dependencies included, click-to-run

---

## 🎯 Quick Start (60 Seconds)

### Step 1: Extract the Package

1. Download the ZIP file: `pdf-mail-merge-portable-v1.0.0.zip`
2. Extract to any location (e.g., Desktop, Program Files)
3. Ensure the folder name contains only English characters

### Step 2: Run the Application

**Windows**:
- Double-click `PDF邮件合并工具.exe`
- Or right-click → "Run as administrator"

**Linux/macOS**:
```bash
chmod +x PDF邮件合并工具.sh
./PDF邮件合并工具.sh
```

### Step 3: Use the Tool

```
1. Click "选择PDF模板" (Select PDF Template)
2. Click "选择数据文件" (Select Data File)
3. Click "开始生成" (Start Generation)
4. Wait for processing to complete
5. Find output in the "output" folder
```

**That's it! No installation required!**

---

## 📁 Package Contents

```
pdf-mail-merge-portable/
│
├── 📄 PDF邮件合并工具.exe    # Main executable (Windows)
├── 📄 PDF邮件合并工具.sh     # Main script (Linux/macOS)
│
├── 📁 Python/               # Bundled Python runtime
│   ├── python.exe          # Python interpreter
│   ├── Scripts/            # pip, tools
│   └── DLLs/               # Python libraries
│
├── 📁 app/                  # Application files
│   ├── src/                # Source code
│   ├── tests/              # Tests
│   ├── examples/           # Examples
│   └── docs/               # Documentation
│
├── 📁 output/               # Output directory
│
├── 📁 config/               # Configuration
│
├── 📄 使用说明.txt          # Quick guide (Chinese)
├── 📄 README.txt           # Quick guide (English)
├── 📄 LICENSE.txt          # License
└── 📄 版本信息.txt          # Version info
```

---

## ✨ Features

### Core Features

- ✅ **Dual Mode Processing**: Form filling + Text replacement
- ✅ **Multiple Data Sources**: CSV, Excel, JSON
- ✅ **Batch Generation**: Process 100+ records
- ✅ **ZIP Packaging**: Auto-compress results
- ✅ **Progress Display**: Real-time status updates

### Portable Features

- ✅ **Zero Installation**: Extract and run
- ✅ **Self-Contained**: All dependencies included
- ✅ **Cross-Platform**: Windows, Linux, macOS
- ✅ **User-Friendly**: GUI interface (optional)
- ✅ **Auto-Update**: Check for updates on startup

---

## 🖥️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 7 | Windows 10/11 |
| | macOS 10.13 | macOS 11+ |
| | Ubuntu 18.04 | Ubuntu 20.04+ |
| Memory | 4 GB | 8 GB+ |
| Disk Space | 500 MB | 1 GB SSD |
| Display | 1024x768 | 1920x1080 |

---

## 🚀 Usage Guide

### Method 1: GUI Mode (Recommended for Beginners)

1. **Launch Application**
   - Double-click `PDF邮件合并工具.exe` (Windows)
   - Or run `./PDF邮件合并工具.sh` (Linux/macOS)

2. **Select PDF Template**
   - Click "选择PDF模板" button
   - Browse to your template file
   - File type: PDF (*.pdf)

3. **Select Data File**
   - Click "选择数据文件" button
   - Choose data source:
     - CSV (*.csv)
     - Excel (*.xlsx, *.xls)
     - JSON (*.json)

4. **Configure Options**
   - Output directory (default: ./output)
   - Naming pattern (default: {row})
   - Processing mode (auto/form/text)

5. **Start Processing**
   - Click "开始生成"
   - View progress bar
   - Wait for completion

6. **Check Results**
   - Open "output" folder
   - View generated PDFs
   - (Optional) ZIP file created

---

### Method 2: Command Line Mode

For advanced users who prefer command line:

1. **Open Terminal**
   - Windows: Press `Win+R`, type `cmd`
   - Linux/macOS: Open Terminal app

2. **Navigate to Package**
   ```bash
   cd path/to/pdf-mail-merge-portable
   ```

3. **Run Commands**
   ```bash
   # Basic usage
   app\python.exe -m app.src.cli --template template.pdf --data data.csv

   # Full options
   app\python.exe -m app.src.cli --template template.pdf --data data.csv --output ./output --mode form --zip --verbose
   ```

---

### Method 3: Batch File Mode

Create batch files for repeated tasks:

1. **Create Batch File**
   ```batch
   # my_task.bat
   @echo off
   cd /d "%~dp0"
   app\python.exe -m app.src.cli --template template.pdf --data data.csv --output ./output --zip
   pause
   ```

2. **Run Batch File**
   - Double-click `my_task.bat`
   - Automatic processing

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Processing Speed | 100 records / 60s |
| Maximum Records | 10,000 |
| Maximum File Size | 50 MB |
| Memory Usage | < 500 MB |
| CPU Usage | Multi-core support |

---

## 🛠️ Troubleshooting

### Issue 1: Application Won't Start

**Symptoms**:
- Double-clicking exe does nothing
- Error message appears

**Solutions**:

1. **Check System Requirements**
   - Windows 7 or higher required
   - 64-bit system recommended

2. **Run as Administrator**
   - Right-click exe
   - Select "Run as administrator"

3. **Check Security Settings**
   - Windows: Settings → Updates → Windows Security → Virus protection
   - Allow the application to run

4. **Re-extract the Package**
   - Delete the folder
   - Re-extract from ZIP
   - Use a different location (avoid Chinese folder names)

---

### Issue 2: Template or Data File Not Found

**Symptoms**:
- "File not found" error
- Empty file selection

**Solutions**:

1. **Check File Path**
   - Avoid special characters in path
   - Avoid Chinese folder names
   - Use absolute paths

2. **Check File Extension**
   - Template must be .pdf
   - Data must be .csv/.xlsx/.json

3. **Check File Encoding**
   - CSV should be UTF-8
   - Excel should be .xlsx format

---

### Issue 3: Output Files Not Generated

**Symptoms**:
- Processing completes but no files
- "Success" message but empty folder

**Solutions**:

1. **Check Output Directory**
   - Ensure write permissions
   - Check disk space

2. **Check Template Format**
   - Form mode: PDF must have form fields
   - Text mode: PDF must have {{placeholder}}

3. **Check Data Format**
   - Ensure column names match template fields
   - Check for empty data file

---

### Issue 4: Chinese Characters Display Incorrectly

**Symptoms**:
- Chinese text shows as boxes
- Garbled characters

**Solutions**:

1. **Use Compatible Font**
   - Ensure PDF uses embedded fonts
   - Use standard Chinese fonts (SimSun, SimHei)

2. **Check Data Encoding**
   - Save CSV as UTF-8
   - Avoid special characters in data

3. **Check Terminal Encoding**
   - Windows: `chcp 65001`
   - Linux/macOS: `export LANG=en_US.UTF-8`

---

### Issue 5: Processing Too Slow

**Symptoms**:
- Processing takes more than 60s for 100 records
- Application freezes

**Solutions**:

1. **Reduce Data Volume**
   - Process in batches
   - Reduce PDF complexity

2. **Close Other Applications**
   - Free up memory and CPU

3. **Check Disk Performance**
   - Use SSD instead of HDD
   - Ensure sufficient disk space

4. **Disable Antivirus**
   - Some antivirus scan each output file
   - Temporarily disable real-time protection

---

## 🔧 Advanced Configuration

### Configuration File

Edit `config/default_settings.json`:

```json
{
  "default_output": "./output",
  "default_mode": "auto",
  "naming_pattern": "{row}",
  "zip_enabled": true,
  "verbose": false,
  "max_workers": 4,
  "language": "zh_CN"
}
```

### Custom Templates

Place your templates in `templates/` folder:
```
templates/
├── employee_card.pdf
├── certificate.pdf
└── invoice.pdf
```

### Custom Data

Place your data files in `data/` folder:
```
data/
├── employees.csv
├── awards.xlsx
└── contracts.json
```

---

## 📞 Support

### Self-Help Resources

1. **Documentation**
   - `docs/USER_GUIDE_CN.md` - Chinese user guide
   - `docs/USER_GUIDE_EN.md` - English user guide
   - `docs/TROUBLESHOOTING.md` - Troubleshooting

2. **Examples**
   - `examples/` - Sample files
   - `examples/README.md` - Example usage

3. **Version Info**
   - `版本信息.txt` - Version and changelog
   - `LICENSE.txt` - License information

### Getting Help

If self-help doesn't resolve your issue:

1. **Collect Information**
   - Error message text
   - Steps to reproduce
   - System information

2. **Submit Issue**
   - GitHub Issues: https://github.com/yourusername/pdf-mail-merge/issues
   - Include all collected information

---

## 🔒 Security & Privacy

### Security Features

- ✅ **Offline Operation**: No network required
- ✅ **Local Processing**: All data stays on your computer
- ✅ **No Telemetry**: No usage data collected
- ✅ **No Cloud Storage**: Files never uploaded

### Privacy Protection

- ✅ **No Account Required**: No registration needed
- ✅ **No Login**: No username/password
- ✅ **No Internet**: Completely offline
- ✅ **No Data Collection**: Your data is yours

---

## 📋 Version History

### v1.0.0 (2026-05-18)
- Initial release
- Core functionality: Form filling + Text replacement
- Supported formats: CSV, Excel, JSON
- Multi-platform: Windows, Linux, macOS
- Portable package with all dependencies included

---

## ✅ Verification Checklist

Use this checklist to verify successful deployment:

- [ ] Package extracted successfully
- [ ] Folder name contains only English characters
- [ ] Main executable exists and is readable
- [ ] Python runtime folder exists
- [ ] Output directory created
- [ ] Application starts without errors
- [ ] Sample files can be loaded
- [ ] Processing completes successfully
- [ ] Output files generated correctly
- [ ] ZIP file created (if enabled)

---

## 🎉 Success!

If all checks pass, your portable version is ready to use!

**Next Steps**:
1. Replace sample files with your own
2. Test with your PDF templates
3. Process your data
4. Share with colleagues

**Enjoy using PDF Mail Merge Tool!**

---

**Maintainer**: PDF Mail Merge Team  
**License**: MIT License  
**Website**: https://github.com/yourusername/pdf-mail-merge  
**Support**: https://github.com/yourusername/pdf-mail-merge/issues

---

*This portable version is designed for ease of use. For technical users who prefer more control, please use the script version.*