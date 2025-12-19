#!/usr/bin/env python3
"""
MCP Creator CLI

Command-line interface for generating MCP servers from HAR files.

Usage:
    python cli.py <har_file> [options]
    python cli.py create <har_file> --output <dir> --name <custom_name>
    python cli.py analyze <har_file>
"""

import argparse
import json
import os
import sys
from pathlib import Path

from har_parser import HARParser, parse_har_file, ServiceInfo
from mcp_generator import MCPGenerator, generate_mcp_server


def analyze_command(args: argparse.Namespace) -> int:
    """Analyze a HAR file and show discovered endpoints."""
    try:
        service_info = parse_har_file(args.har_file)
    except FileNotFoundError:
        print(f"Error: HAR file not found: {args.har_file}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in HAR file: {e}")
        return 1

    print("\n" + "=" * 60)
    print(f"HAR Analysis: {args.har_file}")
    print("=" * 60)

    print(f"\nService Name: {service_info.name}")
    print(f"Suggested MCP Name: iblai-{service_info.name}")
    print(f"Base URL: {service_info.base_url}")

    print(f"\n{'=' * 40}")
    print("Authentication Patterns Discovered")
    print("=" * 40)

    if service_info.auth_patterns:
        for auth in service_info.auth_patterns:
            print(f"  - Type: {auth.auth_type}")
            print(f"    Header: {auth.header_name}")
            print(f"    Location: {auth.location}")
            print()
    else:
        print("  No authentication patterns detected in HAR file.")
        print("  You can configure authentication via environment variables.")

    print(f"\n{'=' * 40}")
    print(f"API Endpoints ({len(service_info.endpoints)} found)")
    print("=" * 40)

    for endpoint in service_info.endpoints:
        print(f"\n  {endpoint.method} {endpoint.path}")
        print(f"  Tool name: {endpoint.tool_name}")

        if endpoint.path_params:
            print(f"  Path params: {[p.name for p in endpoint.path_params]}")

        if endpoint.query_params:
            print(f"  Query params: {[p.name for p in endpoint.query_params]}")

        if endpoint.request_body:
            print(f"  Has request body: Yes")

        if endpoint.response_example:
            print(f"  Has response example: Yes")

    print("\n" + "=" * 60)

    if args.json:
        # Output as JSON for programmatic use
        output = {
            "service_name": service_info.name,
            "mcp_name": f"iblai-{service_info.name}",
            "base_url": service_info.base_url,
            "auth_patterns": [
                {
                    "type": a.auth_type,
                    "header": a.header_name,
                    "location": a.location
                }
                for a in service_info.auth_patterns
            ],
            "endpoints": [
                {
                    "method": e.method,
                    "path": e.path,
                    "tool_name": e.tool_name,
                    "path_params": [p.name for p in e.path_params],
                    "query_params": [p.name for p in e.query_params],
                    "has_body": e.request_body is not None,
                    "has_response_example": e.response_example is not None
                }
                for e in service_info.endpoints
            ]
        }
        print("\nJSON Output:")
        print(json.dumps(output, indent=2))

    return 0


def create_command(args: argparse.Namespace) -> int:
    """Create an MCP server from a HAR file."""
    try:
        service_info = parse_har_file(args.har_file)
    except FileNotFoundError:
        print(f"Error: HAR file not found: {args.har_file}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in HAR file: {e}")
        return 1

    # Override service name if provided
    if args.name:
        # Strip iblai- prefix if provided, as it will be added automatically
        name = args.name
        if name.startswith("iblai-"):
            name = name[6:]
        service_info.name = name

    # Set output directory
    output_dir = args.output or "."
    output_dir = os.path.abspath(output_dir)

    print(f"\nGenerating MCP server...")
    print(f"  Service: {service_info.name}")
    print(f"  MCP Name: iblai-{service_info.name}")
    print(f"  Base URL: {service_info.base_url}")
    print(f"  Endpoints: {len(service_info.endpoints)}")
    print(f"  Output: {output_dir}")

    try:
        server_dir = generate_mcp_server(service_info, output_dir)
    except Exception as e:
        print(f"\nError generating MCP server: {e}")
        return 1

    print(f"\n{'=' * 60}")
    print("MCP Server Generated Successfully!")
    print("=" * 60)
    print(f"\nServer directory: {server_dir}")
    print(f"\nNext steps:")
    print(f"  1. cd {server_dir}")
    print(f"  2. Copy .env.example to .env and configure authentication")
    print(f"  3. Install dependencies: uv sync")
    print(f"  4. Run the server: uv run iblai-{service_info.name}")
    print(f"\nSee README.md for full documentation.")

    return 0


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="MCP Creator - Generate MCP servers from HAR files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a HAR file to see what endpoints were discovered
  python cli.py analyze api-calls.har

  # Generate an MCP server with auto-detected name
  python cli.py create api-calls.har

  # Generate with custom name and output directory
  python cli.py create api-calls.har --name myservice --output ./servers

  # Quick generation (same as create)
  python cli.py api-calls.har
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a HAR file and show discovered endpoints"
    )
    analyze_parser.add_argument(
        "har_file",
        help="Path to the HAR file to analyze"
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Output analysis as JSON"
    )

    # Create command
    create_parser = subparsers.add_parser(
        "create",
        help="Create an MCP server from a HAR file"
    )
    create_parser.add_argument(
        "har_file",
        help="Path to the HAR file"
    )
    create_parser.add_argument(
        "--name", "-n",
        help="Custom service name (default: auto-detected from HAR)"
    )
    create_parser.add_argument(
        "--output", "-o",
        help="Output directory (default: current directory)"
    )

    args, remaining = parser.parse_known_args()

    # Handle commands
    if args.command == "analyze":
        return analyze_command(args)
    elif args.command == "create":
        return create_command(args)
    elif remaining:
        # Direct file argument - parse as create command
        direct_parser = argparse.ArgumentParser()
        direct_parser.add_argument("har_file", help="Path to the HAR file")
        direct_parser.add_argument("--name", "-n", help="Custom service name")
        direct_parser.add_argument("--output", "-o", help="Output directory")
        direct_parser.add_argument("--analyze", "-a", action="store_true", help="Only analyze")
        direct_args = direct_parser.parse_args(remaining)

        if direct_args.analyze:
            direct_args.json = False
            return analyze_command(direct_args)
        else:
            return create_command(direct_args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
