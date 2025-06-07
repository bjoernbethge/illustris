#!/usr/bin/env python3
"""
Command-line interface for Illustris Python tools.

This module provides CLI commands for building and serving documentation,
and downloading Illustris/TNG simulation data.
"""

import argparse
import subprocess
import sys
import webbrowser
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import asyncio
from typing import Optional, Dict, Any

try:
    import httpx
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please install with: uv add httpx python-dotenv")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# TNG API configuration
TNG_API_BASE = "https://www.tng-project.org/api"
DEFAULT_DATA_DIR = Path.home() / "illustris_data"

# Correct file download URLs based on TNG API documentation
def get_file_download_url(simulation: str, file_type: str, snapshot: int = None) -> str:
    """Get the correct download URL for TNG files."""
    if file_type == "snapshot" and snapshot is not None:
        return f"{TNG_API_BASE}/{simulation}/files/snapshot-{snapshot}/"
    elif file_type == "groupcat" and snapshot is not None:
        return f"{TNG_API_BASE}/{simulation}/files/groupcat-{snapshot}/"
    else:
        return f"{TNG_API_BASE}/{simulation}/files/{file_type}/"


class DocumentationServer:
    """Simple HTTP server for serving documentation."""
    
    def __init__(self, directory: Path, port: int = 8000):
        self.directory = directory
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the documentation server."""
        os.chdir(self.directory)
        handler = SimpleHTTPRequestHandler
        self.server = HTTPServer(("localhost", self.port), handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        print(f"Documentation server started at http://localhost:{self.port}")
        webbrowser.open(f"http://localhost:{self.port}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the documentation server."""
        if self.server:
            self.server.shutdown()
            print("\nDocumentation server stopped.")


async def download_file(client: httpx.AsyncClient, url: str, filepath: Path, 
                       headers: Optional[Dict[str, str]] = None) -> bool:
    """Download a file with progress indication."""
    try:
        async with client.stream("GET", url, headers=headers, follow_redirects=True) as response:
            if response.status_code != 200:
                print(f"✗ Failed to download {filepath.name}: HTTP {response.status_code}")
                return False
            
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r  Downloading {filepath.name}: {progress:.1f}%", end="", flush=True)
            
            print(f"\r✓ Downloaded {filepath.name} ({downloaded / 1024 / 1024:.1f} MB)")
            return True
            
    except Exception as e:
        print(f"\r✗ Failed to download {filepath.name}: {e}")
        return False


async def get_api_key() -> str:
    """Get TNG API key from environment or prompt user."""
    api_key = os.getenv("TNG_API_KEY")
    if not api_key:
        print("TNG API key not found in environment variables.")
        print("Please set TNG_API_KEY in your .env file or environment.")
        print("Get your API key at: https://www.tng-project.org/users/register/")
        sys.exit(1)
    return api_key


async def list_simulations():
    """List available simulations with size information."""
    api_key = await get_api_key()
    headers = {"api-key": api_key}
    
    # Simulation data with sizes from TNG specifications
    simulations = {
        "📊 TNG Project": [
            {"name": "TNG50-1", "box": "51.7 Mpc/h", "particles": "2160³", "snapshot_size": "2.7 TB", "total_volume": "~320 TB"},
            {"name": "TNG50-2", "box": "51.7 Mpc/h", "particles": "1080³", "snapshot_size": "350 GB", "total_volume": "18 TB"},
            {"name": "TNG50-3", "box": "51.7 Mpc/h", "particles": "540³", "snapshot_size": "44 GB", "total_volume": "7.5 TB"},
            {"name": "TNG50-4", "box": "51.7 Mpc/h", "particles": "270³", "snapshot_size": "5.2 GB", "total_volume": "0.6 TB"},
            {"name": "TNG100-1", "box": "75.0 Mpc/h", "particles": "1820³", "snapshot_size": "1.7 TB", "total_volume": "128 TB"},
            {"name": "TNG100-2", "box": "75.0 Mpc/h", "particles": "910³", "snapshot_size": "215 GB", "total_volume": "14 TB"},
            {"name": "TNG100-3", "box": "75.0 Mpc/h", "particles": "455³", "snapshot_size": "27 GB", "total_volume": "1.5 TB"},
            {"name": "TNG300-1", "box": "205.0 Mpc/h", "particles": "2500³", "snapshot_size": "4.1 TB", "total_volume": "235 TB"},
            {"name": "TNG300-2", "box": "205.0 Mpc/h", "particles": "1250³", "snapshot_size": "512 GB", "total_volume": "31 TB"},
            {"name": "TNG300-3", "box": "205.0 Mpc/h", "particles": "625³", "snapshot_size": "63 GB", "total_volume": "4 TB"},
        ],
        "🔬 Original Illustris": [
            {"name": "Illustris-1", "box": "106.5 Mpc/h", "particles": "1820³", "snapshot_size": "1.5 TB", "total_volume": "204 TB"},
            {"name": "Illustris-2", "box": "106.5 Mpc/h", "particles": "910³", "snapshot_size": "176 GB", "total_volume": "24 TB"},
            {"name": "Illustris-3", "box": "106.5 Mpc/h", "particles": "455³", "snapshot_size": "22 GB", "total_volume": "3 TB"},
        ]
    }
    
    print("Available simulations:\n")
    
    for category, sims in simulations.items():
        print(f"{category}:")
        for sim in sims:
            print(f"  • {sim['name']} ({sim['box']}, {sim['particles']} particles)")
            print(f"    Full snapshot: {sim['snapshot_size']}, Total data: {sim['total_volume']}")
        print()
    
    # Try to verify API connectivity
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{TNG_API_BASE}/", headers=headers, timeout=10.0)
            if response.status_code == 200:
                print("✓ TNG API is accessible")
            else:
                print(f"⚠ TNG API returned status {response.status_code}")
        except Exception as e:
            print(f"⚠ TNG API connectivity issue: {e}")
            print("  Note: Simulation list shown from cached data")


async def list_snapshots(simulation: str):
    """List snapshots for a simulation."""
    api_key = await get_api_key()
    headers = {"api-key": api_key}
    
    # Map common simulation names to correct API names
    sim_mapping = {
        "TNG50": "TNG50-1",
        "TNG100": "TNG100-1", 
        "TNG300": "TNG300-1",
        "Illustris": "Illustris-1"
    }
    
    # Use mapping if available, otherwise use as-is
    api_simulation = sim_mapping.get(simulation, simulation)
    
    async with httpx.AsyncClient() as client:
        try:
            # Try the direct simulation endpoint first
            response = await client.get(f"{TNG_API_BASE}/{api_simulation}/", headers=headers, follow_redirects=True)
            response.raise_for_status()
            
            data = response.json()
            
            # Try different possible keys
            snapshots = None
            if "snapshots" in data:
                snapshots = data["snapshots"]
            elif "results" in data:
                snapshots = data["results"]
            
            if snapshots is None:
                print(f"  No snapshots found in API response for {simulation}")
                print(f"  Available keys: {list(data.keys())}")
                return
            
            print(f"Available snapshots for {simulation} ({api_simulation}):")
            
            # If snapshots is a string (URL), we need to fetch it
            if isinstance(snapshots, str):
                # Convert HTTP to HTTPS to avoid redirect issues
                snapshots_url = snapshots.replace("http://", "https://")
                snap_response = await client.get(snapshots_url, headers=headers, follow_redirects=True)
                snap_response.raise_for_status()
                snapshots = snap_response.json()
                
            if isinstance(snapshots, list):
                for snap in snapshots[:10]:  # Show first 10
                    if isinstance(snap, dict):
                        number = snap.get('number', 'Unknown')
                        redshift = snap.get('redshift', 0.0)
                        print(f"  - Snapshot {number}: z={redshift:.2f}")
                    else:
                        # If snap is just a number
                        print(f"  - Snapshot {snap}")
                
                if len(snapshots) > 10:
                    print(f"  ... and {len(snapshots) - 10} more snapshots")
            else:
                print(f"  Unexpected snapshots format: {type(snapshots)}")
                
        except Exception as e:
            print(f"✗ Failed to fetch snapshots for {simulation}: {e}")
            print(f"  Tried API endpoint: {TNG_API_BASE}/{api_simulation}/")
            
            # Suggest correct simulation names
            print(f"  Available simulations: TNG50-1, TNG50-2, TNG50-3, TNG50-4,")
            print(f"                        TNG100-1, TNG100-2, TNG100-3,")
            print(f"                        TNG300-1, TNG300-2, TNG300-3,")
            print(f"                        Illustris-1, Illustris-2, Illustris-3")


async def download_test_data():
    """Download complete test data for TNG50-4 including multiple files for full testing."""
    print("Downloading complete test data (TNG50-4, snapshot 99)...")
    print("This includes multiple snapshot files, group catalogs, and offsets for comprehensive testing.")
    
    api_key = await get_api_key()
    headers = {"api-key": api_key}
    data_dir = Path(os.getenv("ILLUSTRIS_DATA_DIR", DEFAULT_DATA_DIR))
    
    # TNG50-4 (smallest simulation)
    simulation = "TNG50-4"
    snapshot = 99  # Final snapshot
    
    # Download all available snapshot files for TNG50-4 (up to 11 chunks)
    files_to_download = []
    
    # Snapshot files (multiple chunks) - TNG50-4 has 11 chunks per snapshot
    for chunk in range(11):
        files_to_download.append({
            "url": get_file_download_url(simulation, "snapshot", snapshot) + f"{chunk}.hdf5",
            "local_path": f"snapdir_{snapshot:03d}/snap_{snapshot:03d}.{chunk}.hdf5",
            "optional": chunk >= 3  # First 3 chunks contain most data, rest might be empty
        })
    
    # Group catalog files (multiple chunks)
    for chunk in range(1):  # TNG50-4 has 1 group catalog file
        files_to_download.append({
            "url": get_file_download_url(simulation, "groupcat", snapshot) + f"{chunk}.hdf5", 
            "local_path": f"groups_{snapshot:03d}/fof_subhalo_tab_{snapshot:03d}.{chunk}.hdf5"
        })
    
    # Try to get offsets and SubLink trees
    optional_files = [
        {
            "url": f"{TNG_API_BASE}/{simulation}/files/offsets.{snapshot}.hdf5",
            "local_path": f"postprocessing/offsets/offsets_{snapshot}.hdf5",
            "optional": True
        },
        {
            "url": f"{TNG_API_BASE}/{simulation}/files/sublink.0.hdf5",
            "local_path": f"trees/SubLink/tree_extended.0.hdf5",
            "optional": True
        }
    ]
    
    # Also create copies in the expected locations for the illustris library
    additional_copies = [
        {
            "source": f"postprocessing/offsets/offsets_{snapshot}.hdf5",
            "target": f"../postprocessing/offsets/offsets_{snapshot:03d}.hdf5"
        }
    ]
    
    base_path = data_dir / simulation / "output"
    
    async with httpx.AsyncClient(timeout=1800.0) as client:  # 30 minutes timeout
        success_count = 0
        required_files = [f for f in files_to_download if not f.get("optional", False)]
        total_files = len(required_files)
        
        # Download required files
        for file_info in files_to_download:
            url = file_info["url"]
            local_path = base_path / file_info["local_path"]
            is_optional = file_info.get("optional", False)
            
            if is_optional:
                print(f"Downloading optional {file_info['local_path']}...")
            else:
                print(f"Downloading {file_info['local_path']}...")
                
            if await download_file(client, url, local_path, headers):
                if not is_optional:
                    success_count += 1
                print(f"✓ Downloaded: {file_info['local_path']}")
            else:
                if is_optional:
                    print(f"  Note: Optional file not available: {file_info['local_path']}")
                else:
                    print(f"✗ Failed to download required file: {file_info['local_path']}")
        
        # Download optional files
        optional_success = 0
        for file_info in optional_files:
            url = file_info["url"]
            local_path = base_path / file_info["local_path"]
            
            print(f"Downloading optional {file_info['local_path']}...")
            if await download_file(client, url, local_path, headers):
                optional_success += 1
                print(f"✓ Optional file downloaded: {file_info['local_path']}")
            else:
                print(f"  Note: Optional file not available: {file_info['local_path']}")
        
        # Create additional copies for illustris library compatibility
        if optional_success > 0:
            print(f"\nCreating additional file copies for library compatibility...")
            for copy_info in additional_copies:
                source_path = base_path / copy_info["source"]
                target_path = base_path / copy_info["target"]
                
                if source_path.exists():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy2(source_path, target_path)
                    print(f"  ✓ Copied {copy_info['source']} to {copy_info['target']}")
        
        print(f"\n📊 Download Summary:")
        print(f"  Required files: {success_count}/{total_files}")
        print(f"  Optional files: {optional_success}/{len(optional_files)}")
        
        if success_count == total_files:
            print(f"\n✓ Successfully downloaded complete test data to {base_path}")
            print(f"  - Multiple snapshot files for loadSubset testing")
            print(f"  - Group catalog files for halo/subhalo analysis")
            if optional_success > 0:
                print(f"  - {optional_success} optional files for advanced testing")
                print(f"  - Additional copies created for library compatibility")
            print(f"\nUse this path in your tests: {base_path}")
            print(f"All tests should now pass with this complete dataset!")
        else:
            print(f"\n⚠️  Partial download completed")
            print(f"Some required files failed to download. Basic tests should still work.")


async def detect_available_chunks(client: httpx.AsyncClient, simulation: str, file_type: str, snapshot: int, headers: dict, max_chunks: int = 20) -> int:
    """Detect how many chunks are available for a given file type."""
    available_chunks = 0
    
    # For TNG50-4, we know the chunk counts from previous testing
    if simulation == "TNG50-4":
        if file_type == "snapshot":
            return 11  # TNG50-4 has 11 snapshot chunks
        elif file_type == "groupcat":
            return 1   # TNG50-4 has 1 group catalog chunk
    
    # For other simulations, try to detect chunks
    for chunk in range(max_chunks):
        url = get_file_download_url(simulation, file_type, snapshot) + f"{chunk}.hdf5"
        try:
            # Try GET with range header to check if file exists without downloading
            response = await client.get(url, headers={**headers, "Range": "bytes=0-0"}, timeout=10.0)
            if response.status_code in [200, 206]:  # 206 = Partial Content
                available_chunks += 1
            else:
                break
        except:
            break
    
    return available_chunks


async def download_simulation_data(simulation: str, snapshot: Optional[int] = None):
    """Download simulation data (snapshot + group catalog) with all available chunks."""
    api_key = await get_api_key()
    headers = {"api-key": api_key}
    data_dir = Path(os.getenv("ILLUSTRIS_DATA_DIR", DEFAULT_DATA_DIR))
    
    # If no snapshot specified, get the latest one
    if snapshot is None:
        print(f"Getting latest snapshot for {simulation}...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{TNG_API_BASE}/{simulation}/", headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # Get snapshots (might be a URL)
                snapshots = data.get("snapshots", [])
                if isinstance(snapshots, str):
                    # Convert HTTP to HTTPS and fetch snapshots
                    snapshots_url = snapshots.replace("http://", "https://")
                    snap_response = await client.get(snapshots_url, headers=headers, follow_redirects=True)
                    snap_response.raise_for_status()
                    snapshots = snap_response.json()
                
                if not snapshots or not isinstance(snapshots, list):
                    print(f"✗ No snapshots found for {simulation}")
                    return
                    
                snapshot = snapshots[-1]["number"]  # Latest snapshot
                print(f"Using latest snapshot: {snapshot}")
            except Exception as e:
                print(f"✗ Failed to get snapshots: {e}")
                return
    
    print(f"Downloading {simulation} snapshot {snapshot}...")
    print("Detecting available file chunks...")
    
    base_path = data_dir / simulation / "output"
    
    async with httpx.AsyncClient(timeout=1800.0) as client:  # Increased timeout
        # Detect available chunks
        snapshot_chunks = await detect_available_chunks(client, simulation, "snapshot", snapshot, headers)
        groupcat_chunks = await detect_available_chunks(client, simulation, "groupcat", snapshot, headers)
        
        print(f"Found {snapshot_chunks} snapshot chunks and {groupcat_chunks} group catalog chunks")
        
        files_to_download = []
        
        # Add all available snapshot chunks
        for chunk in range(snapshot_chunks):
            files_to_download.append({
                "url": get_file_download_url(simulation, "snapshot", snapshot) + f"{chunk}.hdf5",
                "local_path": f"snapdir_{snapshot:03d}/snap_{snapshot:03d}.{chunk}.hdf5",
                "type": "snapshot"
            })
        
        # Add all available group catalog chunks
        for chunk in range(groupcat_chunks):
            files_to_download.append({
                "url": get_file_download_url(simulation, "groupcat", snapshot) + f"{chunk}.hdf5", 
                "local_path": f"groups_{snapshot:03d}/fof_subhalo_tab_{snapshot:03d}.{chunk}.hdf5",
                "type": "groupcat"
            })
        
        # Try to get offsets and SubLink trees (optional)
        optional_files = [
            {
                "url": f"{TNG_API_BASE}/{simulation}/files/offsets.{snapshot}.hdf5",
                "local_path": f"postprocessing/offsets/offsets_{snapshot}.hdf5",
                "type": "offsets"
            },
            {
                "url": f"{TNG_API_BASE}/{simulation}/files/sublink.0.hdf5",
                "local_path": f"trees/SubLink/tree_extended.0.hdf5",
                "type": "sublink"
            }
        ]
        
        # Also create copies in the expected locations for the illustris library
        additional_copies = [
            {
                "source": f"postprocessing/offsets/offsets_{snapshot}.hdf5",
                "target": f"../postprocessing/offsets/offsets_{snapshot:03d}.hdf5"
            }
        ]
        
        success_count = 0
        total_files = len(files_to_download)
        
        # Download required files
        for file_info in files_to_download:
            url = file_info["url"]
            local_path = base_path / file_info["local_path"]
            
            print(f"Downloading {file_info['local_path']}...")
            if await download_file(client, url, local_path, headers):
                success_count += 1
                print(f"✓ Downloaded: {file_info['local_path']}")
            else:
                print(f"✗ Failed to download: {file_info['local_path']}")
        
        # Download optional files
        optional_success = 0
        for file_info in optional_files:
            url = file_info["url"]
            local_path = base_path / file_info["local_path"]
            
            print(f"Downloading optional {file_info['local_path']}...")
            if await download_file(client, url, local_path, headers):
                optional_success += 1
                print(f"✓ Optional file downloaded: {file_info['local_path']}")
            else:
                print(f"  Note: Optional file not available: {file_info['local_path']}")
        
        # Create additional copies for illustris library compatibility
        if optional_success > 0:
            print(f"\nCreating additional file copies for library compatibility...")
            for copy_info in additional_copies:
                source_path = base_path / copy_info["source"]
                target_path = base_path / copy_info["target"]
                
                if source_path.exists():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy2(source_path, target_path)
                    print(f"  ✓ Copied {copy_info['source']} to {copy_info['target']}")
        
        print(f"\n📊 Download Summary:")
        print(f"  Required files: {success_count}/{total_files}")
        print(f"  Optional files: {optional_success}/{len(optional_files)}")
        
        if success_count >= 2:  # At least one snapshot + one groupcat
            print(f"\n✓ Successfully downloaded {simulation} data to {base_path}")
            print(f"  - Snapshot: {snapshot}")
            print(f"  - Snapshot chunks: {snapshot_chunks}")
            print(f"  - Group catalog chunks: {groupcat_chunks}")
            if optional_success > 0:
                print(f"  - {optional_success} optional files for advanced analysis")
                print(f"  - Additional copies created for library compatibility")
            print(f"\nUse this path in your code: {base_path}")
        else:
            print(f"\n✗ Failed to download complete simulation data")


def build_docs():
    """Build Sphinx documentation."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("✗ docs/ directory not found. Run from project root.")
        return False
    
    print("Building documentation...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "sphinx", 
            "-b", "html", 
            str(docs_dir), 
            str(docs_dir / "_build" / "html")
        ], check=True, capture_output=True, text=True)
        
        print("✓ Documentation built successfully")
        print(f"Open: {docs_dir / '_build' / 'html' / 'index.html'}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build documentation: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def serve_docs(port: int = 8000):
    """Serve documentation with auto-reload."""
    docs_dir = Path("docs") / "_build" / "html"
    
    if not docs_dir.exists():
        print("Documentation not built. Building first...")
        if not build_docs():
            return
    
    server = DocumentationServer(docs_dir, port)
    server.start()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Illustris Python tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  illustris -docs -generate          Build documentation
  illustris -docs -serve             Serve documentation (port 8000)
  illustris -docs -serve -p 8080     Serve documentation on port 8080
  
  illustris -data -test              Download complete test data (TNG50-4, all files)
  illustris -data -load TNG50-4      Download latest snapshot for TNG50-4
  illustris -data -load TNG50-4 -snap 99  Download specific snapshot
  illustris -data -list-sims         List available simulations
  illustris -data -list-snaps TNG50  List snapshots for simulation
        """
    )
    
    # Documentation commands
    docs_group = parser.add_argument_group('documentation')
    docs_group.add_argument('-docs', action='store_true', help='Documentation commands')
    docs_group.add_argument('-generate', action='store_true', help='Build documentation')
    docs_group.add_argument('-serve', action='store_true', help='Serve documentation')
    docs_group.add_argument('-p', '--port', type=int, default=8000, help='Port for documentation server')
    
    # Data commands
    data_group = parser.add_argument_group('data')
    data_group.add_argument('-data', action='store_true', help='Data commands')
    data_group.add_argument('-test', action='store_true', help='Download complete test data (TNG50-4 with all files)')
    data_group.add_argument('-load', metavar='SIMULATION', help='Download simulation data')
    data_group.add_argument('-snap', type=int, help='Specific snapshot number (use with -load)')
    data_group.add_argument('-list-sims', action='store_true', help='List available simulations')
    data_group.add_argument('-list-snaps', metavar='SIMULATION', help='List snapshots for simulation')
    
    args = parser.parse_args()
    
    # Handle documentation commands
    if args.docs:
        if args.generate:
            build_docs()
        elif args.serve:
            serve_docs(args.port)
        else:
            print("Use -generate to build docs or -serve to serve them")
            return
    
    # Handle data commands
    elif args.data:
        if args.test:
            asyncio.run(download_test_data())
        elif args.load:
            asyncio.run(download_simulation_data(args.load, args.snap))
        elif args.list_sims:
            asyncio.run(list_simulations())
        elif args.list_snaps:
            asyncio.run(list_snapshots(args.list_snaps))
        else:
            print("Use -test, -load SIMULATION, -list-sims, or -list-snaps SIMULATION")
            return
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 