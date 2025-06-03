import argparse
from .sidekick import sidekick_core
from .context.context_memory import set_context_field



def main():
    parser = argparse.ArgumentParser(description="Run Sidekick AI assistant")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Process notes via CLI")
    run_p.add_argument("--notes", required=True, help="Notes to process")

    proj_p = sub.add_parser("set-project", help="Set the active Jira project")
    proj_p.add_argument("key", help="Project key")

    assign_p = sub.add_parser("set-assignee", help="Set the default assignee")
    assign_p.add_argument("assignee", help="Username or email")

    serve_p = sub.add_parser("serve", help="Run HTTP API server")

    args = parser.parse_args()

    if args.command == "run":
        sidekick_core(args.notes)
    elif args.command == "set-project":
        set_context_field("active_project_key", args.key)
        print(f"Active project set to {args.key}")
    elif args.command == "set-assignee":
        set_context_field("default_assignee", args.assignee)
        print(f"Default assignee set to {args.assignee}")
    elif args.command == "serve":
        from .server import app
        app.run(debug=True)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
