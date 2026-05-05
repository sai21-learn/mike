"""Tests for CLI slash commands — /compact, /usage, /sessions, /resume, /plan, /permissions.

Uses mocking to avoid needing a real LLM provider or Ollama running.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock
from io import StringIO

from mike.core.permissions import PermissionManager


# ──────────────────────────────────────────────
# Helpers & Fixtures
# ──────────────────────────────────────────────

def _make_mike(tmp_path):
    """Build a Mike instance with mocked provider, avoiding real Ollama."""
    from mike.assistant import Mike, CONFIG_DIR
    from mike.ui.terminal import TerminalUI

    # Mock provider
    provider = MagicMock()
    provider.name = "mock"
    provider.model = "mock-model"
    provider.is_configured.return_value = True
    provider.list_models.return_value = ["mock-model"]
    provider.get_default_model.return_value = "mock-model"
    provider.get_context_length.return_value = 8192

    ui = TerminalUI()
    ui.console = MagicMock()  # Suppress all Rich output
    # Mock UI methods so we can assert on them
    ui.print_info = MagicMock()
    ui.print_warning = MagicMock()
    ui.print_success = MagicMock()
    ui.print_error = MagicMock()
    ui.print_help = MagicMock()
    ui.print_sessions = MagicMock()
    ui.print_permissions = MagicMock()
    ui.prompt_tool_permission = MagicMock(return_value="y")

    # Build Mike with patched provider init
    with patch("mike.assistant.get_provider", return_value=provider), \
         patch("mike.assistant.load_config", return_value={"provider": "mock"}), \
         patch("mike.assistant.ProjectContext") as MockPC, \
         patch("mike.assistant.get_rag_engine", return_value=None):

        MockPC.return_value.project_root = tmp_path
        MockPC.return_value.project_name = "test-project"
        MockPC.return_value.project_type = "Python"
        MockPC.return_value.git_branch = "main"
        MockPC.return_value.soul = ""
        MockPC.return_value.agents = {}
        MockPC.return_value.assistant_name = None

        mike = Mike(ui=ui, working_dir=tmp_path)

    return mike


@pytest.fixture
def mike(tmp_path):
    return _make_mike(tmp_path)


# ──────────────────────────────────────────────
# /compact
# ──────────────────────────────────────────────

class TestCompactCommand:

    def test_compact_with_few_messages(self, mike):
        """Compact on empty context prints info message."""
        result = mike._handle_command("/compact")
        mike.ui.print_info.assert_called_once()
        assert "too few" in mike.ui.print_info.call_args[0][0].lower()

    def test_compact_with_messages(self, mike):
        """Compact with messages prints before/after stats."""
        # Add enough messages to trigger compaction
        for i in range(10):
            mike.context.add_message("user", f"message {i} " * 50)
            mike.context.add_message("assistant", f"response {i} " * 50)

        result = mike._handle_command("/compact")
        mike.ui.print_success.assert_called_once()
        msg = mike.ui.print_success.call_args[0][0]
        assert "Compacted" in msg
        assert "→" in msg  # Shows before → after


# ──────────────────────────────────────────────
# /usage
# ──────────────────────────────────────────────

class TestUsageCommand:

    def test_usage_initial_zeros(self, mike):
        """Usage starts at zero tokens."""
        result = mike._handle_command("/usage")
        console_calls = [str(c) for c in mike.ui.console.print.call_args_list]
        text = " ".join(console_calls)
        assert "Session Token Usage" in text

    def test_usage_tracks_input(self, mike):
        """Session tokens track input."""
        mike.session_tokens['input'] = 1500
        mike.session_tokens['output'] = 3000
        result = mike._handle_command("/usage")
        console_calls = [str(c) for c in mike.ui.console.print.call_args_list]
        text = " ".join(console_calls)
        assert "1,500" in text
        assert "3,000" in text
        assert "4,500" in text  # total


# ──────────────────────────────────────────────
# /sessions and /resume
# ──────────────────────────────────────────────

class TestSessionCommands:

    def test_sessions_shows_table(self, mike):
        """Sessions command calls print_sessions."""
        mike.context.create_chat("Test Session 1")
        mike.context.create_chat("Test Session 2")
        result = mike._handle_command("/sessions")
        mike.ui.print_sessions.assert_called_once()
        chats = mike.ui.print_sessions.call_args[0][0]
        assert len(chats) >= 2

    def test_resume_no_args(self, mike):
        """Resume without args shows warning."""
        result = mike._handle_command("/resume")
        mike.ui.print_warning.assert_called()
        assert "Usage" in mike.ui.print_warning.call_args[0][0]

    def test_resume_valid_index(self, mike):
        """Resume with valid index switches chat."""
        chat_id = mike.context.create_chat("Resumable Session")
        mike.context.add_message("user", "hello from old session")
        mike.context.create_chat("Current")  # Switch away

        result = mike._handle_command("/resume 1")
        mike.ui.print_success.assert_called()
        assert "Resumed" in mike.ui.print_success.call_args[0][0]

    def test_resume_invalid_index(self, mike):
        """Resume with out-of-range index shows warning."""
        result = mike._handle_command("/resume 999")
        mike.ui.print_warning.assert_called()

    def test_resume_non_numeric(self, mike):
        """Resume with non-numeric arg shows warning."""
        result = mike._handle_command("/resume abc")
        mike.ui.print_warning.assert_called()


# ──────────────────────────────────────────────
# /plan
# ──────────────────────────────────────────────

class TestPlanModeCommand:

    def test_plan_toggle_on(self, mike):
        """Plan command toggles plan mode on."""
        assert mike.plan_mode is False
        mike._handle_command("/plan")
        assert mike.plan_mode is True
        mike.ui.print_info.assert_called()
        assert "PLAN MODE" in mike.ui.print_info.call_args[0][0]

    def test_plan_toggle_off(self, mike):
        """Plan command toggles plan mode off."""
        mike.plan_mode = True
        mike._handle_command("/plan")
        assert mike.plan_mode is False

    def test_plan_mode_syncs_to_agent(self, mike):
        """Plan mode state is synced to agent before runs."""
        mike.plan_mode = True
        # Mock agent.run to just return
        mike.agent.run = MagicMock(return_value="plan output")
        mike.agent.last_streamed = False
        mike.context.add_message("user", "test")
        mike._run_agent("make a plan")
        assert mike.agent.plan_mode is True


# ──────────────────────────────────────────────
# /permissions
# ──────────────────────────────────────────────

class TestPermissionsCommand:

    def test_permissions_no_args_shows_table(self, mike):
        """Permissions with no args calls print_permissions."""
        mike._handle_command("/permissions")
        mike.ui.print_permissions.assert_called_once_with(mike.permissions)

    def test_permissions_allow(self, mike):
        """Permissions allow <tool> sets override."""
        mike._handle_command("/permissions allow run_command")
        assert mike.permissions.get_setting("run_command") == "allow"
        mike.ui.print_success.assert_called()

    def test_permissions_deny(self, mike):
        """Permissions deny <tool> sets override."""
        mike._handle_command("/permissions deny write_file")
        assert mike.permissions.get_setting("write_file") == "deny"

    def test_permissions_reset(self, mike):
        """Permissions reset clears all overrides."""
        mike.permissions.set_always_allow("run_command")
        mike._handle_command("/permissions reset")
        assert mike.permissions.get_setting("run_command") == "default"


# ──────────────────────────────────────────────
# Existing commands still work
# ──────────────────────────────────────────────

class TestExistingCommands:

    def test_help(self, mike):
        """Help command works and includes new commands."""
        mike._handle_command("/help")
        # print_help was called
        mike.ui.print_help.assert_called_once()

    def test_context(self, mike):
        """Context command works."""
        mike._handle_command("/context")
        console_calls = [str(c) for c in mike.ui.console.print.call_args_list]
        text = " ".join(console_calls)
        assert "Context Usage" in text

    def test_clear(self, mike):
        """Clear command works."""
        mike.context.add_message("user", "hello")
        mike._handle_command("/clear")
        assert len(mike.context.get_messages()) == 0

    def test_unknown_command(self, mike):
        """Unknown command shows warning."""
        mike._handle_command("/foobar")
        mike.ui.print_warning.assert_called()
