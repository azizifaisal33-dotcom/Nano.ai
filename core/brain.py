
        # =========================
        # 5. COMMAND AI LAYER
        # =========================
        commands = self.cmd_ai.generate(text)
        if commands and len(commands) > 0 and commands[0] != text:
            safe_cmds = [safe_command(cmd) for cmd in commands if safe_command(cmd)]
            if safe_cmds:
                result = f"💻 Saran command: {' | '.join(safe_cmds[:3])}"
                self.remember(text, result, "command")
                return result

        # =========================
        # 6. GENERATOR LAYER (FALLBACK)
        # =========================
        fallback = self.generator.reply(text)
        self.remember(text, fallback, "generator")
        return fallback

    # =========================
    # ADDITIONAL METHODS
    # =========================
    def status(self):
        return f"🧠 Session: {self.session_id}\n📊 Memory: {len(memory.search(''))} records"

    def clear_memory(self):
        memory.clear()
        return "🧹 Memory dibersihkan"