#!/usr/bin/env python3
"""
42 Project Privacy Tool - Standalone Version

A self-contained tool to find and make your 42 School projects private.
Embeds all necessary HTTP functionality without external dependencies.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Optional


class SimpleHTTPClient:
    """Simple HTTP client to replace requests library."""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': '42-Privacy-Tool/1.0'
        }
    
    def get(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Perform GET request."""
        if params:
            url += '?' + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e}")
    
    def patch(self, url: str, data: Dict) -> bool:
        """Perform PATCH request."""
        json_data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(
            url, 
            data=json_data, 
            headers={**self.headers, 'Content-Type': 'application/json'},
            method='PATCH'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except urllib.error.URLError:
            return False


def is_42_project(repo_name: str) -> bool:
    """Check if repository name looks like a 42 project."""
    name = repo_name.lower()
    
    # Contains '42'
    if '42' in name:
        return True
    
    # Comprehensive 42 project patterns with common variations
    project_patterns = [
        # Core projects - libft
        'libft', 'lib-ft', 'lib_ft', 'mylibft', 'my-libft', 'my_libft',
        
        # Core projects - printf
        'printf', 'ft_printf', 'ft-printf', 'ftprintf', 'my_printf', 'my-printf',
        
        # Core projects - get_next_line
        'get_next_line', 'get-next-line', 'getnextline', 'gnl', 'get_next_line_42',
        'ft_get_next_line', 'ft-get-next-line',
        
        # Core projects - born2beroot
        'born2beroot', 'born-2-be-root', 'born_2_be_root', 'born-to-be-root',
        'born_to_be_root', 'b2br', 'born2root', 'borntoberoot',
        
        # Core projects - pipex
        'pipex', 'pipe-x', 'pipe_x', 'ft_pipex', 'ft-pipex',
        
        # Core projects - so_long
        'so_long', 'so-long', 'solong', 'so_long_game', 'game-so-long',
        'ft_so_long', 'ft-so-long',
        
        # Core projects - fdf
        'fdf', 'fil-de-fer', 'fil_de_fer', 'wireframe', 'ft_fdf', 'ft-fdf',
        'fdf_wireframe', 'fdf-wireframe',
        
        # Core projects - minitalk
        'minitalk', 'mini-talk', 'mini_talk', 'ft_minitalk', 'ft-minitalk',
        
        # Core projects - push_swap
        'push_swap', 'push-swap', 'pushswap', 'push_swap_algorithm',
        'sorting-algorithm', 'ft_push_swap', 'ft-push-swap',
        
        # Core projects - minishell
        'minishell', 'mini-shell', 'mini_shell', 'ft_minishell', 'ft-minishell',
        'shell', 'my-shell', 'simple-shell', 'bash-clone',
        
        # Core projects - philosophers
        'philosophers', 'philo', 'philosopher', 'dining-philosophers',
        'ft_philosophers', 'ft-philosophers', 'dining_philosophers',
        
        # Core projects - netpractice
        'netpractice', 'net-practice', 'net_practice', 'network-practice',
        'networking', 'ft_netpractice',
        
        # Core projects - cub3d
        'cub3d', 'cub-3d', 'cub_3d', 'cube3d', 'raycaster', 'raycast',
        'ft_cub3d', 'ft-cub3d', '3d-game', 'cub3d-game',
        
        # Core projects - cpp modules
        'cpp', 'cpp-modules', 'cpp_modules', 'c++', 'cplusplus',
        'cpp00', 'cpp01', 'cpp02', 'cpp03', 'cpp04', 'cpp05', 'cpp06', 'cpp07', 'cpp08', 'cpp09',
        'cpp-00', 'cpp-01', 'cpp-02', 'cpp-03', 'cpp-04', 'cpp-05', 'cpp-06', 'cpp-07', 'cpp-08', 'cpp-09',
        'cpp_00', 'cpp_01', 'cpp_02', 'cpp_03', 'cpp_04', 'cpp_05', 'cpp_06', 'cpp_07', 'cpp_08', 'cpp_09',
        
        # Core projects - inception
        'inception', 'docker-inception', 'ft_inception', 'ft-inception',
        'docker-compose-project', 'inception-docker',
        
        # Core projects - ft_containers
        'ft_containers', 'ft-containers', 'containers', 'stl-containers',
        'cpp-containers', 'ft_stl', 'ft-stl',
        
        # Core projects - webserv
        'webserv', 'web-serv', 'web_serv', 'webserver', 'web-server',
        'http-server', 'ft_webserv', 'ft-webserv', 'httpd',
        
        # Core projects - ft_transcendence
        'ft_transcendence', 'ft-transcendence', 'transcendence', 'pong-game',
        'web-pong', 'final-project', 'transcendence-game',
        
        # Piscine projects
        'piscine', 'piscine-c', 'c-piscine', 'swimming-pool', 'ecole42-piscine',
        'rush00', 'rush01', 'rush02', 'rush03', 'rush04',
        'rush-00', 'rush-01', 'rush-02', 'rush-03', 'rush-04',
        'rush_00', 'rush_01', 'rush_02', 'rush_03', 'rush_04',
        'bsq', 'biggest-square', 'biggest_square',
        'shell00', 'shell01', 'shell-00', 'shell-01', 'shell_00', 'shell_01',
        
        # Piscine C modules
        'c00', 'c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c11', 'c12', 'c13',
        'c-00', 'c-01', 'c-02', 'c-03', 'c-04', 'c-05', 'c-06', 'c-07', 'c-08', 'c-09', 'c-10', 'c-11', 'c-12', 'c-13',
        'c_00', 'c_01', 'c_02', 'c_03', 'c_04', 'c_05', 'c_06', 'c_07', 'c_08', 'c_09', 'c_10', 'c_11', 'c_12', 'c_13',
        
        # Exam projects
        'exam', 'exam-rank-02', 'exam-rank-03', 'exam-rank-04', 'exam-rank-05', 'exam-rank-06',
        'examrank02', 'examrank03', 'examrank04', 'examrank05', 'examrank06',
        'exam_rank_02', 'exam_rank_03', 'exam_rank_04', 'exam_rank_05', 'exam_rank_06',
        'exam-02', 'exam-03', 'exam-04', 'exam-05', 'exam-06',
        'exam_02', 'exam_03', 'exam_04', 'exam_05', 'exam_06',
        
        # Specialization projects - Data Science
        'ft_linear_regression', 'ft-linear-regression', 'linear-regression', 'linear_regression',
        'machine-learning', 'ml-regression', 'dslr', 'data-science-logistic-regression',
        'logistic-regression', 'logistic_regression', 'multilayer_perceptron', 'multilayer-perceptron',
        'neural-network', 'perceptron', 'mlp', 'kmeans', 'k-means', 'clustering',
        'ft_kmeans', 'ft-kmeans', 'ready_set_boole', 'ready-set-boole', 'boolean-evaluation',
        'matrix', 'ft_matrix', 'ft-matrix', 'linear-algebra', 'computorv1', 'computor-v1',
        'computor_v1', 'polynomial-solver',
        
        # Specialization projects - Cybersecurity
        'darkly', 'web-security', 'cybersecurity', 'rainfall', 'reverse-engineering',
        'binary-exploitation', 'override', 'system-security', 'privilege-escalation',
        'ft_malcom', 'ft-malcom', 'network-scanner', 'port-scanner',
        'ft_onion', 'ft-onion', 'tor-service', 'onion-service',
        'woody_woodpacker', 'woody-woodpacker', 'binary-packer', 'elf-packer',
        'ft_ping', 'ft-ping', 'ping-implementation', 'network-ping',
        'ft_traceroute', 'ft-traceroute', 'traceroute-implementation',
        'ft_nmap', 'ft-nmap', 'network-mapper', 'matt_daemon', 'matt-daemon',
        'daemon-process', 'system-daemon', 'taskmaster', 'task-master', 'process-manager',
        
        # Specialization projects - System Administration
        'ft_services', 'ft-services', 'kubernetes-services', 'k8s-services',
        'cloud_1', 'cloud-1', 'cloud-infrastructure', 'aws-cloud',
        
        # Specialization projects - iOS
        'swifty_proteins', 'swifty-proteins', 'protein-viewer', 'ios-proteins',
        'swifty_companion', 'swifty-companion', 'ios-companion', '42-api-ios',
        
        # Specialization projects - Graphics
        'scop', 'opengl-viewer', '3d-viewer', 'obj-viewer', 'humangl', 'human-gl',
        'opengl-human', '3d-human', 'particle_system', 'particle-system',
        'opengl-particles', 'mod1', 'raytracer', 'ray-tracer', 'miniRT', 'minirt',
        'rt', 'ray_tracer', 'ray_tracing',
        
        # Common prefixes that indicate 42 projects
        'ft_', 'ft-', 'ecole42-', 'school42-', '42-', '42_'
    ]
    
    # Check for exact matches and partial matches
    for pattern in project_patterns:
        if pattern in name or name.startswith(pattern):
            return True
    
    # Check for patterns that end with common 42 suffixes
    suffixes = ['-42', '_42', '-ecole42', '-school42', '42']
    for suffix in suffixes:
        if name.endswith(suffix):
            return True
    
    return False


def fetch_repos(client: SimpleHTTPClient) -> List[Dict]:
    """Fetch all repositories owned by user."""
    repos = []
    page = 1
    
    while True:
        url = "https://api.github.com/user/repos"
        params = {'page': page, 'per_page': 100, 'type': 'owner'}
        
        page_repos = client.get(url, params)
        
        if not page_repos:
            break
            
        repos.extend(page_repos)
        page += 1
    
    return repos


def change_visibility(client: SimpleHTTPClient, repo_full_name: str, private: bool) -> bool:
    """Change repository visibility."""
    url = f"https://api.github.com/repos/{repo_full_name}"
    data = {'private': private}
    return client.patch(url, data)


def main():
    """Main function."""
    print("42 Project Visibility Tool v1.0")
    print("=" * 40)
    print("Self-contained executable - no dependencies required!")
    print()
    
    # Get token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print()
        print("Setup instructions:")
        print("   1. Go to: https://github.com/settings/tokens")
        print("   2. Generate a token with 'repo' scope")
        print("   3. Set environment variable:")
        print("      Linux/Mac: export GITHUB_TOKEN=your_token_here")
        print("      Windows:   set GITHUB_TOKEN=your_token_here")
        print()
        input("Press Enter to exit...")
        sys.exit(1)
    
    try:
        # Initialize HTTP client
        client = SimpleHTTPClient(token)
        
        # Fetch repos
        print("Fetching repositories...")
        all_repos = fetch_repos(client)
        
        # Find 42 projects
        projects_42 = []
        for repo in all_repos:
            if is_42_project(repo['name']):
                projects_42.append(repo)
        
        if not projects_42:
            print("No 42 projects found in your repositories")
            print("Searched for common project names and '42' in repository names")
            input("Press Enter to exit...")
            return
        
        print(f"\nFound {len(projects_42)} 42 projects:")
        print("-" * 60)
        
        # Show all projects with numbers
        print()
        for i, repo in enumerate(projects_42, 1):
            status = "private" if repo['private'] else "public"
            print(f"{i:2}. {repo['name']:<25} {status}")
        
        public_count = sum(1 for repo in projects_42 if not repo['private'])
        private_count = len(projects_42) - public_count
        
        print(f"\nSummary: {public_count} public, {private_count} private")
        
        # Choose action
        print("\nWhat would you like to do?")
        print("   1. Make repositories private")
        print("   2. Make repositories public")
        print("   3. Exit")
        
        while True:
            action_choice = input("\nChoose action (1/2/3): ").strip()
            if action_choice in ['1', '2', '3']:
                break
            print("Invalid choice. Enter 1, 2, or 3")
        
        if action_choice == '3':
            print("Goodbye!")
            input("Press Enter to exit...")
            return
        
        target_private = action_choice == '1'
        action_word = "private" if target_private else "public"
        action_emoji = "(private)" if target_private else "(public)"
        
        # Filter available repositories
        if target_private:
            available_repos = [repo for repo in projects_42 if not repo['private']]
            filter_word = "public"
        else:
            available_repos = [repo for repo in projects_42 if repo['private']]
            filter_word = "private"
        
        if not available_repos:
            print(f"\nNo {filter_word} 42 projects found to make {action_word}!")
            input("Press Enter to exit...")
            return
        
        print(f"\nSelect repositories to make {action_word}:")
        print(f"   Available {filter_word} repositories:")
        print()
        
        for i, repo in enumerate(available_repos, 1):
            current_status = "private" if repo['private'] else "public"
            print(f"   {i:2}. {repo['name']:<25} {current_status}")
        
        print(f"\n   Enter numbers separated by spaces (e.g., '1 3 5')")
        print(f"   Enter 'all' to select all {filter_word} repositories")
        print(f"   Press Enter to skip")
        
        # Selection process
        selected_repos = []
        
        while True:
            # Show current selection
            if selected_repos:
                selected_names = [repo['name'] for repo in selected_repos]
                print(f"\nCurrently selected: {', '.join(selected_names)}")
            
            choice = input(f"\nSelect repositories (1-{len(available_repos)}, 'all', or Enter to continue): ").strip().lower()
            
            if choice == '':
                break
            elif choice == 'all':
                selected_repos = available_repos.copy()
                print(f"Selected all {len(selected_repos)} {filter_word} repositories")
                break
            else:
                try:
                    # Parse numbers
                    numbers = [int(x.strip()) for x in choice.split()]
                    selected_repos = []
                    
                    for num in numbers:
                        if 1 <= num <= len(available_repos):
                            repo = available_repos[num - 1]
                            if repo not in selected_repos:
                                selected_repos.append(repo)
                        else:
                            print(f"Invalid number: {num} (valid range: 1-{len(available_repos)})")
                    
                    if selected_repos:
                        selected_names = [repo['name'] for repo in selected_repos]
                        print(f"Selected: {', '.join(selected_names)}")
                    else:
                        print("No valid repositories selected")
                        
                except ValueError:
                    print("Invalid input. Enter numbers separated by spaces, 'all', or press Enter")
        
        if not selected_repos:
            print("No repositories selected. Exiting.")
            input("Press Enter to exit...")
            return
        
        # Confirm and process
        print(f"\n{action_emoji} Will make these {len(selected_repos)} repositories {action_word}:")
        for repo in selected_repos:
            print(f"   • {repo['name']}")
        
        confirm = input(f"\nProceed with making {len(selected_repos)} repositories {action_word}? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            print(f"\n{action_emoji} Making {len(selected_repos)} repositories {action_word}...")
            print("⏳ This may take a few moments...")
            print()
            
            success_count = 0
            for i, repo in enumerate(selected_repos, 1):
                print(f"   [{i}/{len(selected_repos)}] Processing {repo['name']}...", end=" ")
                if change_visibility(client, repo['full_name'], target_private):
                    print("Done")
                    success_count += 1
                else:
                    print("Failed")
            
            print(f"\nCompleted! {success_count}/{len(selected_repos)} repositories made {action_word}")
            
            if success_count < len(selected_repos):
                failed_count = len(selected_repos) - success_count
                print(f"Warning: {failed_count} repositories failed (check permissions)")
        else:
            print("Operation cancelled - no changes made")
        
        print()
        input("Press Enter to exit...")
    
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("   • Check your internet connection")
        print("   • Verify your GitHub token is valid")
        print("   • Ensure the token has 'repo' scope permissions")
        print()
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()