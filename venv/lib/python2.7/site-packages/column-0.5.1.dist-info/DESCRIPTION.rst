column is a thin wrapper on top of ansible API, to serve
as an entry point for other code when ansible is needed. As ansible
internal API is not officially exposed and thus changes are very likely,
this wrapper should be used instead of touching ansible directly,
so that any further ansible API change will only incur change in this module.

It exposes two classes:
column.APIRunner and column.SubprocessRunner

Both of them implement API described in column.Runner.
Each runner expose two public methods:
run_playbook() and run_module().


