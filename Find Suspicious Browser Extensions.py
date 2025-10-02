import webbrowser
import platform
import subprocess
import json

class BrowserExtensionManager:
    def __init__(self):
        self.browser = self.detect_browser()
        self.extensions = []
        self.suspicious_extensions = []
        
    def detect_browser(self):
        """Detect default browser"""
        system = platform.system()
        if system == "Windows":
            return "chrome"
        elif system == "Darwin":
            return "chrome" if platform.mac_ver()[0] else "safari"
        else:
            return "firefox"
    
    def open_extension_manager(self):
        """Open browser's extension manager"""
        if self.browser == "chrome":
            webbrowser.open("chrome://extensions/")
        elif self.browser == "firefox":
            webbrowser.open("about:addons")
        elif self.browser == "safari":
            webbrowser.open("safari://settings/extensions")
    
    def list_installed_extensions(self):
        """List all installed extensions"""
        if self.browser == "chrome":
            self._list_chrome_extensions()
        elif self.browser == "firefox":
            self._list_firefox_extensions()
        elif self.browser == "safari":
            self._list_safari_extensions()
    
    def _list_chrome_extensions(self):
        """List Chrome extensions"""
        try:
            output = subprocess.check_output(["chrome-cli", "extensions"])
            self.extensions = output.decode().splitlines()
        except FileNotFoundError:
            print("chrome-cli not installed")
    
    def _list_firefox_extensions(self):
        """List Firefox extensions"""
        try:
            output = subprocess.check_output(["jpm", "list"])
            self.extensions = output.decode().splitlines()
        except FileNotFoundError:
            print("jpm not installed")
    
    def _list_safari_extensions(self):
        """List Safari extensions"""
        try:
            output = subprocess.check_output(["defaults", "read", 
                "~/Library/Preferences/com.apple.Safari.plist", "Extensions"])
            self.extensions = json.loads(output.decode()).keys()
        except subprocess.CalledProcessError:
            print("Safari extensions not accessible")
    
    def analyze_extensions(self):
        """Analyze extensions for suspicious behavior"""
        for ext in self.extensions:
            if self._is_suspicious(ext):
                self.suspicious_extensions.append(ext)
    
    def _is_suspicious(self, extension):
        """Check if extension is suspicious"""
        suspicious_keywords = [
            "password", "vpn", "adblocker", "search", "privacy",
            "download", "optimizer", "cleaner", "saver"
        ]
        
        return any(keyword in extension.lower() for keyword in suspicious_keywords)
    
    def remove_extensions(self):
        """Remove suspicious extensions"""
        for ext in self.suspicious_extensions:
            if self.browser == "chrome":
                self._remove_chrome_extension(ext)
            elif self.browser == "firefox":
                self._remove_firefox_extension(ext)
            elif self.browser == "safari":
                self._remove_safari_extension(ext)
    
    def _remove_chrome_extension(self, extension):
        """Remove Chrome extension"""
        try:
            subprocess.run(["chrome-cli", "uninstall", extension])
            print(f"Removed {extension}")
        except FileNotFoundError:
            print("chrome-cli not installed")
    
    def _remove_firefox_extension(self, extension):
        """Remove Firefox extension"""
        try:
            subprocess.run(["jpm", "uninstall", extension])
            print(f"Removed {extension}")
        except FileNotFoundError:
            print("jpm not installed")
    
    def _remove_safari_extension(self, extension):
        """Remove Safari extension"""
        try:
            subprocess.run(["defaults", "delete", 
                "~/Library/Preferences/com.apple.Safari.plist", 
                f"Extensions/{extension}"])
            print(f"Removed {extension}")
        except subprocess.CalledProcessError:
            print("Failed to remove Safari extension")

def main():
    manager = BrowserExtensionManager()
    manager.list_installed_extensions()
    manager.analyze_extensions()
    
    if manager.suspicious_extensions:
        print("Suspicious extensions found:")
        for ext in manager.suspicious_extensions:
            print(f"- {ext}")
        
        remove = input("Remove suspicious extensions? (y/n): ")
        if remove.lower() == "y":
            manager.remove_extensions()
            print("Restart browser for changes to take effect")
    else:
        print("No suspicious extensions found")

if __name__ == "__main__":
    main()