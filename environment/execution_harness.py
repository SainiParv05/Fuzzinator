"""
execution_harness.py
Fuzzinator — Target Execution Harness

Executes target binaries via subprocess.run() with a 500ms timeout.
Detects crashes by examining return codes and signals.
"""

import subprocess
import tempfile
import signal
import os
import logging


logger = logging.getLogger(__name__)


# Signals that indicate a crash (only available on Linux/Unix)
CRASH_SIGNALS = {}
if hasattr(signal, 'SIGSEGV'):
    CRASH_SIGNALS[-signal.SIGSEGV] = "SIGSEGV"
if hasattr(signal, 'SIGABRT'):
    CRASH_SIGNALS[-signal.SIGABRT] = "SIGABRT"
if hasattr(signal, 'SIGBUS'):
    CRASH_SIGNALS[-signal.SIGBUS] = "SIGBUS"
if hasattr(signal, 'SIGFPE'):
    CRASH_SIGNALS[-signal.SIGFPE] = "SIGFPE"
if hasattr(signal, 'SIGILL'):
    CRASH_SIGNALS[-signal.SIGILL] = "SIGILL"

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
        # Validate and normalize target path
        self.target_path = os.path.abspath(target_path)

        if not os.path.isfile(self.target_path):
            logger.error(f"Target binary not found: {self.target_path}")
            raise FileNotFoundError(f"Target not found: {self.target_path}")

        if not os.access(self.target_path, os.X_OK):
            logger.error(f"Target binary is not executable: {self.target_path}")
            raise PermissionError(f"Target is not executable: {self.target_path}")

        if timeout <= 0:
            logger.error(f"Invalid timeout value: {timeout}")
            raise ValueError("timeout must be positive")

        self.timeout = timeout
        logger.debug(f"ExecutionHarness initialized with target: {self.target_path}, timeout: {timeout}s")

    def run(self, input_data: bytearray) -> ExecutionResult:
        """
        Execute the target with the given input data.

        Writes input to a temp file, runs the target, and checks for crashes.

        Args:
            input_data: Bytes to feed to the target program

        Returns:
            ExecutionResult with crash/signal information
        """
        if not isinstance(input_data, (bytes, bytearray)):
            logger.error("input_data must be bytes or bytearray")
            raise ValueError("input_data must be bytes or bytearray")

        # Write input to a temporary file
        input_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".input") as f:
                f.write(bytes(input_data))
                input_path = f.name

            logger.debug(f"Executing target with input: {len(input_data)} bytes")

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
                logger.info(f"Target crashed with signal: {signal_name}")
                return ExecutionResult(
                    crashed=True,
                    signal_name=signal_name,
                    return_code=return_code,
                    timed_out=False,
                )

            # Check for ASan exit (typically exit code 1 or other non-zero)
            if return_code != 0:
                logger.info(f"Target exited with code {return_code} (likely sanitizer detection)")
                return ExecutionResult(
                    crashed=True,
                    signal_name=f"ASAN(rc={return_code})",
                    return_code=return_code,
                    timed_out=False,
                )

            # Normal clean exit
            logger.debug(f"Target exited cleanly (rc={return_code})")
            return ExecutionResult(
                crashed=False,
                signal_name="",
                return_code=return_code,
                timed_out=False,
            )

        except subprocess.TimeoutExpired:
            logger.debug(f"Target execution timed out after {self.timeout}s")
            return ExecutionResult(
                crashed=False,
                signal_name="",
                return_code=-1,
                timed_out=True,
            )

        except Exception as e:
            logger.error(f"Error executing target: {e}")
            raise

        finally:
            # Clean up temp file
            if input_path:
                try:
                    os.unlink(input_path)
                except OSError as e:
                    logger.warning(f"Failed to clean up temp file {input_path}: {e}")
