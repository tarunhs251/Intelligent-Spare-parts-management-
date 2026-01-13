# Installation Guide
## Troubleshooting Common Installation Issues

### Issue: setuptools.build_meta Error

If you encounter the error: `Cannot import 'setuptools.build_meta'`

**Solution:**

1. **First, upgrade pip, setuptools, and wheel:**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Then install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Alternative Installation Method

If the above doesn't work, install dependencies in stages:

```bash
# Step 1: Install build tools
pip install --upgrade pip setuptools wheel

# Step 2: Install core dependencies
pip install pandas==2.1.4 numpy==1.24.3 scikit-learn==1.3.2

# Step 3: Install ML libraries
pip install lightgbm==4.1.0 xgboost==2.0.3

# Step 4: Install statistical libraries
pip install statsmodels==0.14.1 scipy==1.11.4

# Step 5: Install visualization
pip install matplotlib==3.8.2 seaborn==0.13.0 plotly==5.18.0

# Step 6: Install Streamlit
pip install streamlit==1.29.0

# Step 7: Install testing and utilities
pip install pytest==7.4.3 pytest-cov==4.1.0 pyyaml==6.0.1 joblib==1.3.2

# Step 8: Optional - pmdarima (for auto-ARIMA)
pip install pmdarima==2.0.4
```

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt
```

### Minimum Requirements (Without Pinned Versions)

If version conflicts occur, try installing without pinned versions:

```bash
pip install --upgrade pip setuptools wheel

pip install pandas numpy scikit-learn
pip install lightgbm xgboost
pip install statsmodels scipy
pip install matplotlib seaborn plotly
pip install streamlit
pip install pytest pytest-cov pyyaml joblib
pip install pmdarima  # Optional
```

### Common Issues and Solutions

#### Issue 1: pip is outdated
```bash
python -m pip install --upgrade pip
```

#### Issue 2: setuptools missing
```bash
pip install --upgrade setuptools
```

#### Issue 3: wheel missing
```bash
pip install --upgrade wheel
```

#### Issue 4: Compilation errors (Windows)
- Install Visual C++ Build Tools
- Or use pre-compiled wheels:
  ```bash
  pip install --only-binary :all: lightgbm xgboost
  ```

#### Issue 5: Memory errors during installation
- Install packages one at a time
- Close other applications
- Use `--no-cache-dir` flag:
  ```bash
  pip install --no-cache-dir -r requirements.txt
  ```

### Verification

After installation, verify all packages:

```bash
python -c "import pandas, numpy, sklearn, lightgbm, xgboost, streamlit, plotly; print('All packages installed successfully!')"
```

### System-Specific Notes

**Windows:**
- May need Visual C++ Build Tools for some packages
- Use pre-compiled wheels when possible

**Linux:**
- May need: `sudo apt-get install python3-dev build-essential`

**Mac:**
- May need: `xcode-select --install`

### Getting Help

If issues persist:
1. Check Python version: `python --version` (should be 3.10+)
2. Check pip version: `pip --version`
3. Check setuptools: `pip show setuptools`
4. Review error messages carefully
5. Try installing packages individually to identify problematic ones

