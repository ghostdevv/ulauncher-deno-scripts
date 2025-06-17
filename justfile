EXTENSION_DIR := "$HOME/.local/share/ulauncher/extensions/ulauncher-deno-scripts"

dev:
    mkdir -p "{{ EXTENSION_DIR }}"
    pnpm dlx chokidar-cli \
        '**/**.{py,json,png}' \
        --command "rm -rf {{ EXTENSION_DIR }} \
                   && mkdir -p {{ EXTENSION_DIR }} \
                   && cp -r ./* {{ EXTENSION_DIR }} \
                   && pkill -9 ulauncher";

format:
    black main.py src/**
