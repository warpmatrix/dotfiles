if status is-interactive
    # Commands to run in interactive sessions can go here
    if command -v fastfetch &> /dev/null
        fastfetch
    end
    if command -v tmux &> /dev/null; and not set -q TMUX
        if tmux has-session -t home
            tmux attach-session -t home
        else
            tmux new-session -s home
        end
    end
    if command -v pyenv &> /dev/null
        pyenv init - | source
    end
end
