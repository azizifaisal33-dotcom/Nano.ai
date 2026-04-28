
#!/usr/bin/env python3
import time
import json
import random
from typing import Dict, List, Any, Optional
from core.revolver import Revolver, NeuralSharding

class ReasoningState:
    def __init__(self):
        self.plan = ""
        self.actions = []
        self.verifications = []
        self.shard_id = ""
        self.attempts = 0
        self.max_attempts = 3

class RecursiveAgent:
    def __init__(self, brain):
        self.brain = brain
        self.revolver: Revolver = brain.revolver
        self.running = False
        self.state: Optional[ReasoningState] = None
        self.neural = NeuralSharding()

    def plan(self, goal: str) -> Dict[str, Any]:
        """Generate structured plan"""
        try:
            # Neural intent sharding
            shard_analysis = self.neural.get_recommendation(goal)
            self.state.shard_id = shard_analysis['shard_id']
            
            steps = [
                f"1. Analyze: {goal}",
                f"2. Execute: {shard_analysis['action_type']} via brain",
                f"3. Verify: Check success markers",
                f"4. Evolve: If failed, trigger DNA update"
            ]
            
            self.state.plan = "\n".join(steps)
            return {
                "plan": self.state.plan,
                "shard_id": self.state.shard_id,
                "confidence": shard_analysis['confidence']
            }
        except Exception as e:
            return {"error": str(e), "confidence": 0.0}

    def execute(self) -> str:
        """Execute single reasoning step"""
        try:
            if not self.state.plan:
                return "❌ No plan generated"
                
            # Delegate to brain with shard context
            step_input = f"[{self.state.shard_id}] {self.state.plan.split('\\n')[self.state.attempts % 4]}"
            result = self.brain.think(step_input)
            
            self.state.actions.append({
                "attempt": self.state.attempts,
                "input": step_input,
                "result": result,
                "timestamp": time.time()
            })
            
            return result
        except Exception as e:
            return f"💥 Execute Error: {e}"

    def verify(self, result: str) -> bool:
        """Intelligent verification with multiple checks"""
        try:
            success_markers = ["✅", "berhasil", "selesai", "success", "done"]
            failure_markers = ["❌", "error", "gagal", "failed", "corruption"]
            
            result_lower = result.lower()
            
            # Success check
            if any(marker in result for marker in success_markers):
                return True
                
            # Failure check  
            if any(marker in result_lower for marker in failure_markers):
                return False
            
            # Neural confidence check
            if self.state.shard_id:
                inputs = [random.random() for _ in range(16)]
                pred = max(self.neural.forward_pass(self.state.shard_id, inputs))
                if pred > 0.6:
                    return True
            
            # Default: partial success
            return "plan" in result or len(result) > 20
            
        except:
            return False

    def self_evolve(self) -> bool:
        """Trigger DNA evolution when verification fails"""
        try:
            if not self.state.shard_id:
                return False
                
            # Analyze failure pattern
            failure_pattern = f"agent_failed_{self.state.goal[:20]}"
            evolution_target = "core/agent.py"
            
            # Trigger revolver evolution
            evolution_result = self.revolver.evolve(
                evolution_target, 
                f"fix agent reasoning failure pattern: {failure_pattern}"
            )
            
            # Feedback to neural shard
            self.revolver.feedback(self.state.shard_id, "✅" in evolution_result)
            
            time.sleep(1)  # Allow DNA sync
            return "✅" in evolution_result
            
        except Exception as e:
            print(f"❌ Self-Evolve Error: {e}")
            return False

    def start(self, goal: str) -> str:
        if self.running:
            return "🤖 Agent sudah berjalan"
            
        self.running = True
        self.state = ReasoningState()
        self.state.goal = goal
        
        print(f"🎯 Goal: {goal}")
        plan_result = self.plan(goal)
        print(f"📋 Plan: {json.dumps(plan_result, indent=2)}")
        
        max_iterations = 10
        for iteration in range(max_iterations):
            print(f"\n🔄 Iteration {iteration + 1}/{max_iterations}")
            
            # Execute step
            exec_result = self.execute()
            print(f"📤 Execute: {exec_result[:100]}...")
            
            # Verify
            if self.verify(exec_result):
                self.revolver.feedback(self.state.shard_id, True)
                self.running = False
                return f"🎉 SUCCESS in {self.state.attempts + 1} attempts!\n{exec_result}"
            
            # Self-evolution on failure
            self.state.attempts += 1
            print("❌ Verification failed - Triggering DNA evolution...")
            
            if self.self_evolve():
                print("🧬 DNA evolved - Retrying...")
                time.sleep(2)
                continue
            else:
                print("⚠️ Evolution failed - Next attempt")
            
            if self.state.attempts >= self.state.max_attempts:
                self.revolver.feedback(self.state.shard_id, False)
                self.running = False
                return f"⏹️ Goal timeout after {iteration + 1} iterations\nLast: {exec_result}"
        
        self.running = False
        return "🏁 Recursive reasoning complete"

    def stop(self):
        self.running = False
        if self.state:
            self.revolver.feedback(self.state.shard_id, False)
        return "🛑 Agent stopped"

    def status(self) -> str:
        if not self.state:
            return "Idle"
        return f"Shard: {self.state.shard_id} | Attempts: {self.state.attempts} | Actions: {len(self.state.actions)}"

class Agent:
    def __init__(self, brain):
        self.brain = brain
        self.agent = RecursiveAgent(brain)
        self.running = False

    def start(self, goal: str):
        return self.agent.start(goal)

    def stop(self):
        return self.agent.stop()

    def log(self):
        if not self.agent.state or not self.agent.state.actions:
            return "tidak ada log"
        return "\n".join([
            f"{a['attempt']}: {a['result'][:50]}..." 
            for a in self.agent.state.actions[-5:]
        ])