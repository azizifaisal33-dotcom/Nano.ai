#!/usr/bin/env python3
import time
import random
from typing import Dict, List, Any, Optional
from core.revolver import Revolver, NeuralSharding

class ReasoningStep:
    def __init__(self):
        self.plan = ""
        self.action = ""
        self.result = ""
        self.verified = False
        self.shard_id = ""

class RecursiveAgent:
    def __init__(self, brain):
        self.brain = brain
        self.revolver: Revolver = brain.revolver
        self.state: Optional[ReasoningStep] = None
        self.max_retries = 3
        self.neural = NeuralSharding()

    def plan(self, goal: str) -> Dict[str, Any]:
        """Generate executable plan"""
        shard_id = self.neural.intent_hash(goal)
        analysis = self.neural.analyze(goal)
        
        self.state = ReasoningStep()
        self.state.shard_id = shard_id
        self.state.plan = f"GOAL: {goal}\nACTION: {analysis['action']}\nVERIFY: success markers"
        
        return {
            "plan": self.state.plan,
            "shard_id": shard_id,
            "confidence": analysis['confidence'],
            "predicted_action": analysis['action']
        }

    def execute(self) -> str:
        """Execute brain action"""
        if not self.state or not self.state.plan:
            return "❌ No plan"
        
        # Delegate to brain
        exec_cmd = f"[{self.state.shard_id}] {self.state.plan}"
        result = self.brain.think(exec_cmd)
        
        self.state.action = exec_cmd
        self.state.result = result
        return result

    def verify(self, result: str) -> bool:
        """Intelligent verification"""
        success_patterns = ["✅", "berhasil", "success", "done", "evolved"]
        fail_patterns = ["❌", "error", "failed", "corrupt"]
        
        result_lower = result.lower()
        
        # Explicit success
        if any(p in result for p in success_patterns):
            return True
        
        # Explicit failure  
        if any(p in result_lower for p in fail_patterns):
            return False
        
        # Neural confidence
        if self.state and self.state.shard_id:
            inputs = [random.random() for _ in range(32)]
            pred = max(self.neural.forward(self.state.shard_id, inputs))
            if pred > 0.6:
                return True
        
        # Heuristic: meaningful output
        return len(result.strip()) > 10 and "❌" not in result
        
    def self_correct(self) -> bool:
        """Auto-evolve on failure"""
        if not self.state or not self.state.shard_id:
            return False
        
        # Evolve agent logic
        evolution = self.revolver.evolve(
            "core/agent.py",
            f"fix reasoning failure for shard {self.state.shard_id}"
        )
        
        # Neural feedback
        inputs = [random.random() for _ in range(32)]
        success = "✅" in evolution
        self.neural.mini_backprop(self.state.shard_id, inputs, 1.0 if success else 0.0, success)
        
        time.sleep(1)  # DNA sync
        return success

    def run(self, goal: str, max_steps: int = 8) -> str:
        """Main recursive loop"""
        print(f"🎯 AGENT: {goal}")
        
        # Step 1: Plan
        plan = self.plan(goal)
        print(f"📋 PLAN: {plan['confidence']:.2f} {plan['predicted_action']}")
        
        for step in range(max_steps):
            print(f"🔄 Step {step+1}/{max_steps}")
            
            # Step 2: Execute
            result = self.execute()
            print(f"📤 {result[:80]}...")
            
            # Step 3: Verify
            if self.verify(result):
                self.revolver.feedback(self.state.shard_id, True)
                return f"✅ SUCCESS!\n{result}"
            
            # Step 4: Self-correct
            print("❌ VERIFY FAIL → SELF CORRECT")
            if not self.self_correct():
                print("⚠️ Correction failed")
            
            if step >= self.max_retries:
                self.revolver.feedback(self.state.shard_id, False)
                return f"⏹️ TIMEOUT after {step+1} steps\n{result}"
        
        return "🏁 Complete"

class Agent:
    def __init__(self, brain):
        self.brain = brain
        self.agent = RecursiveAgent(brain)
        self.running = False

    def start(self, goal: str):
        if self.running:
            return "🤖 Already running"
        self.running = True
        try:
            return self.agent.run(goal)
        finally:
            self.running = False

    def stop(self):
        self.running = False
        return "🛑 Stopped"

    def log(self):
        return "Recursive reasoning active" if self.agent.state else "Idle"
    
    def status(self):
        return self.agent.state.shard_id if self.agent.state else "ready"