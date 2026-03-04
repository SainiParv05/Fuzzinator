"""
execution_harness.py
Fuzzinator — Target Execution Harness

Executes target binaries via subprocess.run() with a 50ms timeout.
Detects crashes by examining return codes and signals.
"""

import subprocess
import tempfile
import signal
import os


# Signals that indicate a crash
CRASH_SIGNALS = {
    -signal.SIGSEGV: "SIGSEGV",
    -signal.SIGABRT: "SIGABRT",
    -signal.SIGBUS:  "SIGBUS",
    -signal.SIGFPE:  "SIGFPE",
    -signal.SIGILL:  "SIGILL",
}

# Timeout in seconds (500ms instead of 50ms to allow ASan to print crash dump)
EXECUTION_TIMEOUT = 0.5


class ExecutionResult:
    """Result of executing a target program."""

    def __init__(self, crashed: bool, signal_name: str, return_code: int,
                 timed_out: bool):
        self.crashed = crashed
        self.signal_name = signal_name
        self.return_code = return_code
        self.timed_out = timed_out

    def __repr__(self):
        if self.crashed:
            return f"ExecutionResult(CRASH: {self.signal_name})"
        elif self.timed_out:
            return "ExecutionResult(TIMEOUT)"
        else:
            return f"ExecutionResult(OK, rc={self.return_code})"


class ExecutionHarness:
    """Runs target binaries and detects crashes."""

    def __init__(self, target_path: str, timeout: float = EXECUTION_TIMEOUT):
        self.target_path = os.path.abspath(target_path)
        self.timeout = timeout

        if not os.path.isfile(self.target_path):
            raise FileNotFoundError(f"Target not found: {self.target_path}")

    def run(self, input_data: bytearray) -> ExecutionResult:
        """
        Execute the target with the given input data.

        Writes input to a temp file, runs the target, and checks for crashes.

        Args:
            input_data: Bytes to feed to the target program

        Returns:
            ExecutionResult with crash/signal information
        """
        # Write input to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".input") as f:
            f.write(bytes(input_data))
            input_path = f.name

        try:
            result = subprocess.run(
                [self.target_path, input_path],
                timeout=self.timeout,
                capture_output=True,
                env={**os.environ, "ASAN_OPTIONS": "abort_on_error=1:detect_leaks=0"},
            )

            return_code = result.returncode

            # Check for crash signals (negative return code)
            if return_code < 0:
                sig = return_code
                signal_name = CRASH_SIGNALS.get(sig, f"SIG({-sig})")
                return ExecutionResult(
                    crashed=True,
                    signal_name=signal_name,
                    return_code=return_code,
                    timed_out=False,
                )

            # Check for ASan exists (typically exit code 1 or other non-zero)
            if return_code != 0:
                return ExecutionResult(
                    crashed=True,
                    signal_name=f"ASAN(rc={return_code})",
                    return_code=return_code,
                    timed_out=False,
                )

            # Normal clean exit
            return ExecutionResult(
                crashed=False,
                signal_name="",
                return_code=return_code,
                timed_out=False,
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                crashed=False,
                signal_name="",
                return_code=-1,
                timed_out=True,
            )

        finally:
            # Clean up temp file
            try:
                os.unlink(input_path)
            except OSError:
                pass
