import subprocess
import sys
from datetime import date

def test_full_scenario_add_and_report():
    input_data = f"1\n100\nЕда\n{date.today().isoformat()}\nОбед\n0\n"
    
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=input_data,
        capture_output=True,
        text=True,
        cwd=".",
        env={"PYTHONPATH": "."}
    )
    
    assert result.returncode == 0
    assert "Расход добавлен." in result.stdout  # без эмодзи