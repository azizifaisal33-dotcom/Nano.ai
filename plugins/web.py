import os
import re
import json
import time
import subprocess
from urllib.parse import urlparse, quote
from typing import Dict, List, Optional

class WebAgent:
    def __init__(self):
        self.termux_api = self._check_termux_api()
        self.history = []

    def _check_termux_api(self) -> bool:
        """Check if Termux:API available"""
        try:
            subprocess.run(["pkg_install"], shell=True, check=True, capture_output=True)
            return True
        except:
            return False

    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Google search via Termux"""
        results = []
        try:
            if self.termux_api:
                # Termux:API way (fastest)
                cmd = f'termux-open-url "https://www.google.com/search?q={quote(query)}"'
                os.system(cmd)
                results.append({"url": f"https://google.com/search?q={quote(query)}", "title": "OPENING GOOGLE..."})
            else:
                # Fallback curl
                cmd = f'curl -s "https://www.google.com/search?q={quote(query)}" | head -500'
                output = subprocess.getoutput(cmd)
                results.append({"snippet": output[:300], "method": "curl"})
        except:
            results.append({"error": "Search failed"})
        return results

    def get_page(self, url: str) -> Optional[str]:
        """Fetch webpage content"""
        try:
            if self.termux_api:
                cmd = f'termux-open "{url}"'
                os.system(cmd)
                return f"📱 OPENING: {url}"
            
            # Lynx fallback (install: pkg install lynx)
            cmd = f'lynx -dump -nolist "{url}" | head -20'
            content = subprocess.getoutput(cmd)
            return content.strip() if content else f"📄 {url}"
        except Exception as e:
            return f"❌ {e}"

    def scrape_title(self, html: str) -> str:
        """Extract title from HTML"""
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
        return match.group(1).strip() if match else "No title"

    def youtube(self, query: str) -> str:
        """Open YouTube search"""
        url = f"https://m.youtube.com/results?search_query={quote(query)}"
        if self.termux_api:
            os.system(f'termux-open "{url}"')
            return f"🎥 YouTube: {query}"
        return url

    def github(self, query: str) -> str:
        """GitHub search"""
        url = f"https://github.com/search?q={quote(query)}"
        os.system(f'termux-open "{url}"')
        return f"🐙 GitHub: {query}"

    def process(self, command: str) -> str:
        """Main web command processor"""
        cmd = command.lower().strip()
        
        if "cari" in cmd or "search" in cmd or "google" in cmd:
            query = cmd.split("cari ", 1)[-1].split("search ", 1)[-1]
            results = self.search(query)
            self.history.append({"type": "search", "query": query})
            return f"🔍 {query}\n" + json.dumps(results[0], indent=2)

        if "buka" in cmd or "open" in cmd:
            url = cmd.split("buka ", 1)[-1].split("open ", 1)[-1]
            if not url.startswith(('http', 'www')):
                url = 'https://' + url
            result = self.get_page(url)
            self.history.append({"type": "open", "url": url})
            return result

        if "youtube" in cmd:
            query = cmd.replace("youtube", "").strip()
            result = self.youtube(query)
            self.history.append({"type": "youtube", "query": query})
            return result

        if "github" in cmd:
            query = cmd.replace("github", "").strip()
            result = self.github(query)
            return result

        return "Web: cari 'query' | buka 'url' | youtube 'topik'"

# Global instance
web = WebAgent()