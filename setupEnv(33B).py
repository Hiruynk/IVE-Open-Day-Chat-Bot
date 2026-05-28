import os
import subprocess
import sys
import platform
import shutil

def run_command(command_list):
    try:
        subprocess.run(command_list, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Execution failed / 執行指令失敗: {' '.join(command_list)}")
        print(f"Error message / 錯誤訊息: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error occured / 發生未預期的錯誤: {e}")
        return False

def get_os_instructions():
    os_name = platform.system()
    
    if os_name == "Windows":
        return (
            "1. 📥 Download Windows installer (.exe) from official site:\n"
            "   👉 https://ollama.com/download/windows\n"
            "   前往官方網站下載 Windows 安裝檔 (.exe)。\n"
            "2. 🖱️ Double-click to install. Make sure the 'Llama' icon appears in the system tray.\n"
            "   雙擊執行安裝，安裝完成後，請確保螢幕右下角工作列出現了「小羊駝」圖示。\n"
            "3. 🔄 Close current terminal (CMD/PowerShell) and open a new one to run this script again.\n"
            "   關閉當前的終端機 (CMD/PowerShell)，重新打開一個新的再執行本腳本。"
        )
    elif os_name == "Darwin":
        return (
            "1. 📥 Download Mac installer (.zip) from official site:\n"
            "   👉 https://ollama.com/download/mac\n"
            "   前往官方網站下載 Mac 安裝檔 (.zip)。\n"
            "2. 📦 Extract files and drag Ollama into your 'Applications' folder.\n"
            "   解壓縮並將 Ollama 拖曳至「應用程式 (Applications)」資料夾。\n"
            "3. 🖱️ Launch Ollama and confirm the 'Llama' icon appears in the top menu bar.\n"
            "   啟動 Ollama 應用程式，並在頂部狀態列確認「小羊駝」圖示已出現。"
        )
    elif os_name == "Linux":
        return (
            "1. 🐧 Linux supports one-command installation. Run this command in terminal:\n"
            "   👉 curl -fsSL https://ollama.com/install.sh | sh\n"
            "   Linux 系統支援一鍵安裝。請複製以上指令並在終端機執行。\n"
            "2. ⚙️ After installation, Ollama service will run automatically in the background.\n"
            "   安裝完成後，Ollama 服務通常會自動在背景運行。"
        )
    else:
        return (
            "📥 Please visit the official site to download for your OS: https://ollama.com/download\n"
            "   請前往官方網站下載適合您系統的版本。"
        )

def main():
    print("==================================================")
    print("🚀 IVE HKIIT Open Day Chatbot - Auto Environment Setup Script")
    print("🚀 IVE HKIIT 開放日智能助手 - 全自動環境配置腳本")
    print("==================================================")
    
    packages = [
        "requests",
        "beautifulsoup4",
        "streamlit",
        "ollama",
        "opencc-python-reimplemented"
    ]
    
    print("\n📦 Phase 1: Installing core Python packages...")
    print("📦 階段 1: 開始安裝 Python 核心套件...")
    pip_cmd = [sys.executable, "-m", "pip", "install"] + packages
    if run_command(pip_cmd):
        print("✅ All Python packages installed successfully!")
        print("✅ 所有 Python 套件安裝成功！")
    else:
        print("🚨 Package installation failed. Please check your internet connection.")
        print("🚨 部分套件安裝失敗，請檢查網路連線。")
        sys.exit(1)

    print("\n🦙 Phase 2: Checking system environment & Ollama model...")
    print("🦙 階段 2: 檢查系統環境與 Ollama 大模型...")
    
    if shutil.which("ollama") is None:
        print("\n❌ System command 'ollama' not found! It seems Ollama is not installed yet.")
        print("❌ 系統偵測不到 'ollama' 指令！您似乎尚未安裝 Ollama 引擎。")
        print("==================================================")
        print(f"🛠️ Setup Guide / 專屬安裝指南 (Detected OS / 偵測到您的系統為: {platform.system()})")
        print("--------------------------------------------------")
        print(get_os_instructions())
        print("==================================================")
        print("\n💡 Please install Ollama according to the steps above, then re-run this script (python setupEnv.py).")
        print("💡 請按照上述步驟安裝 Ollama 後，重新執行此腳本 (python setupEnv.py)。")
        sys.exit(1)
        
    print("✅ Ollama engine detected!")
    print("✅ 偵測到 Ollama 引擎已安裝！")
    print("⏳ Connecting to local Ollama service and pulling 'nemotron3:33b' (Very large file, please wait)...")
    print("⏳ 正在連線本地 Ollama 服務並下載 nemotron3:33b 模型 (檔案非常巨大，請耐心等候)...")
    
    # ✨ 這裡已將指令無縫切換至 nemotron3:33b
    ollama_cmd = ["ollama", "pull", "nemotron3:33b"]
    
    if run_command(ollama_cmd):
        print("✅ Nemotron3 33B model is downloaded and ready!")
        print("✅ Nemotron3 33B 大模型已成功下載並準備就緒！")
    else:
        print("\n❌ Model download failed, or Ollama service is not running!")
        print("❌ 無法下載模型，或 Ollama 服務尚未啟動！")
        print("💡 Make sure Ollama app is running in the background (Check for the Llama icon).")
        print("💡 請確認 Ollama 應用程式正在後台運行（找找看有沒有小羊駝圖示）。")
        sys.exit(1)

    print("\n==================================================")
    print("🎉 Congratulations! All environment configurations are fully completed!")
    print("🎉 恭喜！所有環境配置已滿血完成！")
    print("💡 Now you can start the Chatbot by typing the following command:")
    print("💡 現在您只需在終端機輸入以下指令即可啟動 Chatbot:")
    print("   streamlit run chatBot.py")
    print("==================================================")

if __name__ == "__main__":
    main()